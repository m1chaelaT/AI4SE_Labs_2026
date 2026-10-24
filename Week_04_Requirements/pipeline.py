"""Agentic network for software requirements refinement (LangGraph, ANS5).

Graph:

    START -> load -> extract -> merge -> check_conflicts -> prioritize -> validate -> review
                                                                             ^          |
                                                                             |   (actions left and
                                                                             |    round < max)
                                                                          revise <------+
                                                                                        |
                                                                    (approved or max rounds)
                                                                                        v
                                                                                     render -> END

  Node             Kind            Model            Spec
  load             deterministic   -                ANS2, OS4 (document IDs)
  extract          LLM             gpt-5-mini       OS8, OS9 (ignored statements)
  merge            LLM + code      gpt-5.6-luna     OS3, OS5, OS7 (glossary), OS8
  check_conflicts  LLM + code      gpt-6-luna       OS7, OS9
  prioritize       LLM + code      gpt-5.6-luna     OS6
  validate         deterministic   -                ANS2, OS2, all checks
  review           LLM + code      gpt-6-luna       ANS3 (feedback loop)
  revise           LLM + code      gpt-5.6-luna     ANS3
  render           deterministic   -                ANS2, OS1

Usage:
    python pipeline.py <input_dir> [--out output/requirements.md] [--graph]

Only the input directory is given; all files in it (recursively) are processed.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from conflict_checker import check_conflicts
from extractor import extract_requirements
from loader import load_documents
from merger import merge_requirements
from prioritizer import prioritize_requirements
from renderer import render_document
from reviewer import review_requirements, revise_requirements, route_after_review
from validator import validate_requirements


class PipelineState(TypedDict, total=False):
    # input / output
    input_dir: str
    output_path: str
    document_path: str
    # loader
    documents: list
    chunks: list
    # extractor
    candidates: list
    ignored_statements: list
    extraction_errors: list
    extraction_feedback: str
    # merger
    merged_requirements: list
    discarded_candidates: list
    areas: list
    glossary: list
    merge_feedback: str
    # conflict checker
    resolved_requirements: list
    conflict_blacklist: list
    conflict_records: list
    conflict_feedback: str
    # prioritiser
    priority_feedback: str
    # validator
    final_requirements: list
    validation: Any
    # reviewer / reviser (feedback loop)
    review_round: int
    review_actions: list
    review_history: list
    dismissed_warnings: list
    reviewer_blacklist: list


def _logged(name: str, fn):
    """Wrap a node so that the console shows where the pipeline is and how long each step took."""
    def node(state: PipelineState) -> dict:
        print(f"\n=== {name} ===", flush=True)
        start = time.time()
        update = fn(state)
        print(f"--- {name} done in {time.time() - start:.1f}s", flush=True)
        return update
    return node


def build_graph():
    graph = StateGraph(PipelineState)
    graph.add_node("load", _logged("load", load_documents))
    graph.add_node("extract", _logged("extract", extract_requirements))
    graph.add_node("merge", _logged("merge", merge_requirements))
    graph.add_node("check_conflicts", _logged("check_conflicts", check_conflicts))
    graph.add_node("prioritize", _logged("prioritize", prioritize_requirements))
    graph.add_node("validate", _logged("validate", validate_requirements))
    graph.add_node("review", _logged("review", review_requirements))
    graph.add_node("revise", _logged("revise", revise_requirements))
    graph.add_node("render", _logged("render", render_document))

    graph.add_edge(START, "load")
    graph.add_edge("load", "extract")
    graph.add_edge("extract", "merge")
    graph.add_edge("merge", "check_conflicts")
    graph.add_edge("check_conflicts", "prioritize")
    graph.add_edge("prioritize", "validate")
    graph.add_edge("validate", "review")
    # Feedback loop (ANS3): the reviewer checks the validated output and either sends
    # concrete actions to the reviser - whose result is validated and reviewed again -
    # or approves and lets the document be rendered.
    graph.add_conditional_edges("review", route_after_review, {"revise": "revise", "finish": "render"})
    graph.add_edge("revise", "validate")
    graph.add_edge("render", END)
    return graph.compile()


def _dump(value):
    """JSON-serialise pydantic models inside the state."""
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if isinstance(value, list):
        return [_dump(v) for v in value]
    if isinstance(value, dict):
        return {k: _dump(v) for k, v in value.items()}
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description="Refine a corpus of documents into a requirements specification.")
    parser.add_argument("input_dir", help="Directory with the input documents (searched recursively)")
    parser.add_argument("--out", default="output/requirements.md", help="Path of the generated document")
    parser.add_argument("--graph", action="store_true", help="Only print the graph as a Mermaid diagram and exit")
    args = parser.parse_args()

    app = build_graph()
    mermaid = app.get_graph().draw_mermaid()
    out_dir = Path(args.out).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "pipeline_graph.mmd").write_text(mermaid, encoding="utf-8")
    if args.graph:
        print(mermaid)
        return

    start = time.time()
    final = app.invoke({"input_dir": args.input_dir, "output_path": args.out},
                       config={"recursion_limit": 100})

    # Save the full final state for inspection and for the report.
    keep = ["documents", "candidates", "ignored_statements", "extraction_errors", "areas", "glossary",
            "discarded_candidates", "conflict_blacklist", "conflict_records", "final_requirements",
            "validation", "review_history", "review_actions", "reviewer_blacklist"]
    state_path = out_dir / "pipeline_result.json"
    state_path.write_text(json.dumps({k: _dump(final.get(k)) for k in keep}, indent=2, ensure_ascii=False),
                          encoding="utf-8")

    v = final["validation"]
    print("\n=== Summary ===")
    print(f"Documents: {len(final['documents'])}, candidates: {len(final['candidates'])}, "
          f"final requirements: {len(final['final_requirements'])}")
    print("Priorities: " + ", ".join(f"{k.split('_', 1)[1]}: {n}" for k, n in v.stats.items() if k.startswith("priority_")))
    print(f"Validation: {'passed' if v.passed else 'FAILED'} ({v.stats['errors']} errors, {v.stats['warnings']} warnings)")
    print(f"Review rounds: {final.get('review_round', 0)}, open review actions: {len(final.get('review_actions') or [])}")
    if final.get("extraction_errors"):
        print(f"WARNING: {len(final['extraction_errors'])} chunks failed extraction - see {state_path}")
    print(f"Document: {final['document_path']}")
    print(f"Full result: {state_path}; graph: {out_dir / 'pipeline_graph.mmd'}")
    print(f"Total time: {(time.time() - start) / 60:.1f} min")


if __name__ == "__main__":
    main()
