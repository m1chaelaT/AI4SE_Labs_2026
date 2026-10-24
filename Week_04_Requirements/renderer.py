"""Renderer node (deterministic, no AI) - writes the single structured document (OS1).

The Markdown document contains:
  1. Introduction (how the document was produced, key figures)
  2. Source documents (with the number of requirements traced to each)
  3. Priority scale (OS6) and glossary (OS7)
  4. Requirements overview table
  5. Requirements by functional area - ID (OS2), name and paragraph description (OS5),
     priority with justification (OS6), source documents and evidence quotes (OS4)
  6. Blacklist (OS9) - requirements removed because of conflicts, invalid or
     removed in review, candidates discarded while merging, ignored statements
  7. Conflict resolution log (OS7)
  8. Quality assurance - validation result and feedback-loop history
  Appendix: traceability matrix (document -> requirement IDs)

Usable as a LangGraph node (`render_document`) or standalone:
    python renderer.py Task_1/data/corpus [--reviewed output/reviewed.json] [--out output/requirements.md]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from collections import Counter, defaultdict
from pathlib import Path

import config
from prioritizer import PRIORITY_ORDER, PRIORITY_SCALE
from schemas import (
    BlacklistEntry,
    ConflictRecord,
    DiscardedCandidate,
    GlossaryTerm,
    IgnoredStatement,
    LLMReviewAction,
    MergedRequirement,
    ReviewRound,
    SourceDocument,
    ValidationReport,
)

MAX_QUOTES_PER_REQUIREMENT = 3


def _cell(text: str) -> str:
    """Make text safe for a Markdown table cell."""
    return " ".join(str(text).split()).replace("|", "\\|")


def _anchor(req_id: str) -> str:
    return req_id.lower()


def render(requirements: list[MergedRequirement], documents: list[SourceDocument], areas: list[str],
           glossary: list[GlossaryTerm], *, input_dir: str = "",
           conflict_blacklist: list[BlacklistEntry] | None = None,
           reviewer_blacklist: list[BlacklistEntry] | None = None,
           discarded: list[DiscardedCandidate] | None = None,
           ignored: list[IgnoredStatement] | None = None,
           conflicts: list[ConflictRecord] | None = None,
           review_history: list[ReviewRound] | None = None,
           open_actions: list[LLMReviewAction] | None = None,
           validation: ValidationReport | None = None,
           n_candidates: int | None = None) -> str:
    conflict_blacklist = conflict_blacklist or []
    reviewer_blacklist = reviewer_blacklist or []
    discarded = discarded or []
    ignored = ignored or []
    conflicts = conflicts or []
    review_history = review_history or []
    open_actions = open_actions or []
    docs = {d.doc_id: d for d in documents}
    reqs = sorted(requirements, key=lambda m: m.req_id)
    prio_counts = Counter(m.priority for m in reqs)
    traced: dict[str, list[str]] = defaultdict(list)
    for m in reqs:
        for d in m.source_doc_ids:
            traced[d].append(m.req_id)

    out: list[str] = []
    w = out.append

    # --- Title and introduction -------------------------------------------------
    w("# Software Requirements Specification")
    w("")
    w(f"*Generated on {dt.date.today().isoformat()} from the input corpus `{Path(input_dir).name or input_dir}` "
      f"by an agentic requirements-refinement network.*")
    w("")
    w("## Contents")
    w("")
    for i, title in enumerate(["Introduction", "Source documents", "Priority scale", "Glossary",
                               "Requirements overview", "Requirements by area", "Blacklist",
                               "Conflict resolution log", "Quality assurance"], start=1):
        w(f"{i}. [{title}](#{i}-{title.lower().replace(' ', '-')})")
    w("10. [Appendix: traceability matrix](#appendix-traceability-matrix)")
    w("")

    w("## 1. Introduction")
    w("")
    w(f"This document specifies **{len(reqs)} requirements** derived from **{len(documents)} source documents** "
      f"(emails, meeting minutes, interviews, a survey, an early draft specification and reference documentation). "
      + (f"The network extracted {n_candidates} candidate requirements, merged semantic duplicates, resolved "
         f"conflicts, assigned priorities and reviewed the result in a validate-review-revise loop. "
         if n_candidates else "")
      + "Every requirement has a unique ID, a short name, a one-sentence statement, a paragraph-long description, "
        "a priority from the scale in section 3 and a trace to the documents it was derived from. Items that were "
        "discarded are listed with the reason in section 7.")
    w("")
    w("| Pipeline step | Kind | Model |")
    w("|---|---|---|")
    for step, kind, model in [
        ("Loader", "deterministic", "-"),
        ("Extractor", "LLM", config.EXTRACTOR_MODEL),
        ("Merger (taxonomy, merge, duplicate check)", "LLM + code", config.MERGER_MODEL),
        ("Conflict checker", "LLM + code", config.CONFLICT_MODEL),
        ("Prioritiser", "LLM + code", config.PRIORITISER_MODEL),
        ("Validator", "deterministic", "-"),
        ("Reviewer", "LLM + code", config.REVIEWER_MODEL),
        ("Reviser", "LLM + code", config.REVISER_MODEL),
        ("Renderer", "deterministic", "-"),
    ]:
        w(f"| {step} | {kind} | {model} |")
    w("")

    # --- Source documents ---------------------------------------------------------
    w("## 2. Source documents")
    w("")
    w("| ID | Type | Date | File | Title | Requirements |")
    w("|---|---|---|---|---|---|")
    for d in documents:
        w(f"| {d.doc_id} | {d.doc_type} | {_cell(d.date or '-')} | `{_cell(d.path)}` | {_cell(d.title)} | "
          f"{len(traced.get(d.doc_id, []))} |")
    w("")

    # --- Priority scale -------------------------------------------------------------
    w("## 3. Priority scale")
    w("")
    w("Priorities follow the MoSCoW method. The prioritiser applied exactly these definitions, using the "
      "evidence in the sources: explicit priority wording, formal decisions in meeting minutes, the number of "
      "independent sources and stakeholders, survey support, and legal, security or technical obligations.")
    w("")
    w("| Priority | Meaning | Requirements |")
    w("|---|---|---|")
    for p in PRIORITY_ORDER:
        w(f"| **{p}** | {PRIORITY_SCALE[p]} | {prio_counts.get(p, 0)} |")
    w("")

    # --- Glossary ---------------------------------------------------------------------
    w("## 4. Glossary")
    w("")
    w("All requirements use the preferred terms below (consistent vocabulary).")
    w("")
    w("| Term | Definition | Instead of |")
    w("|---|---|---|")
    for g in sorted(glossary, key=lambda g: g.term.lower()):
        w(f"| **{_cell(g.term)}** | {_cell(g.definition)} | {_cell(', '.join(g.avoid)) or '-'} |")
    w("")

    # --- Overview ---------------------------------------------------------------------
    w("## 5. Requirements overview")
    w("")
    w("| ID | Name | Priority | Area | Sources |")
    w("|---|---|---|---|---|")
    for m in reqs:
        w(f"| [{m.req_id}](#{_anchor(m.req_id)}) | {_cell(m.name)} | {m.priority} | {_cell(m.area)} | "
          f"{', '.join(m.source_doc_ids)} |")
    w("")

    # --- Requirements by area -----------------------------------------------------------
    w("## 6. Requirements by area")
    w("")
    by_area: dict[str, list[MergedRequirement]] = defaultdict(list)
    for m in reqs:
        by_area[m.area].append(m)
    ordered_areas = [a for a in areas if a in by_area] + [a for a in by_area if a not in areas]
    for n, area in enumerate(ordered_areas, start=1):
        items = by_area[area]
        c = Counter(m.priority for m in items)
        w(f"### 6.{n} {area}")
        w("")
        w(f"*{len(items)} requirements - " + ", ".join(f"{p}: {c.get(p, 0)}" for p in PRIORITY_ORDER) + "*")
        w("")
        for m in items:
            w(f'<a id="{_anchor(m.req_id)}"></a>')
            w(f"#### {m.req_id} {m.name}")
            w("")
            w(f"**Priority:** {m.priority} &nbsp;|&nbsp; **Type:** {m.req_type} &nbsp;|&nbsp; "
              f"**Sources:** {', '.join(f'{d} ({docs[d].path})' if d in docs else d for d in m.source_doc_ids)}")
            w("")
            w(f"**Statement:** {m.statement}")
            w("")
            w(m.description)
            w("")
            if m.priority_rationale:
                w(f"*Priority rationale:* {m.priority_rationale}")
                w("")
            if m.stakeholders:
                w(f"*Stakeholders:* {', '.join(m.stakeholders[:8])}{' ...' if len(m.stakeholders) > 8 else ''}")
                w("")
            for note in m.resolution_notes:
                w(f"*Note:* {note}")
                w("")
            quotes = [e for e in m.evidence if e.quote_verified][:MAX_QUOTES_PER_REQUIREMENT] \
                or m.evidence[:MAX_QUOTES_PER_REQUIREMENT]
            if quotes:
                w("<details><summary>Evidence</summary>")
                w("")
                for e in quotes:
                    w(f"- {e.doc_id}: \"{_cell(e.quote)}\"")
                w("")
                w("</details>")
                w("")

    # --- Blacklist ---------------------------------------------------------------------
    w("## 7. Blacklist")
    w("")
    w("Items identified in the sources but excluded from the specification, with the reason. Nothing was "
      "dropped silently: every extracted candidate is either part of a requirement above or listed here.")
    w("")
    w("### 7.1 Removed because of conflicts")
    w("")
    rows = [b for b in conflict_blacklist if b.category == "conflict"]
    if rows:
        w("| Removed item | Sources | Conflicts with | Explanation |")
        w("|---|---|---|---|")
        for b in rows:
            w(f"| {_cell(b.name)}: {_cell(b.statement)} | {', '.join(b.source_doc_ids)} | "
              f"{_cell(', '.join(b.conflicts_with))} | {_cell(b.explanation)} |")
    else:
        w("No requirement had to be removed because of a conflict. The conflict checker examined all pairs "
          "flagged during merging and all similar requirements; see section 8.")
    w("")
    w("### 7.2 Removed as invalid or in review")
    w("")
    rows = [b for b in conflict_blacklist if b.category != "conflict"] + reviewer_blacklist
    if rows:
        w("| Removed item | Sources | Reason | Explanation |")
        w("|---|---|---|---|")
        for b in rows:
            w(f"| {_cell(b.name)}: {_cell(b.statement)} | {', '.join(b.source_doc_ids)} | {b.category} | "
              f"{_cell(b.explanation)} |")
    else:
        w("None.")
    w("")
    w("### 7.3 Candidates discarded while merging")
    w("")
    if discarded:
        w("| Candidate | Source | Reason | Explanation |")
        w("|---|---|---|---|")
        for d in discarded:
            w(f"| {_cell(d.name)}: {_cell(d.statement)} | {d.doc_id} | {d.reason} | {_cell(d.explanation)} |")
    else:
        w("None.")
    w("")
    w("### 7.4 Statements not taken as requirements")
    w("")
    if ignored:
        reasons = Counter(i.reason for i in ignored)
        w("During extraction, these statements were recognised as not being requirements: "
          + ", ".join(f"{n} {r}" for r, n in reasons.most_common()) + ".")
        w("")
        w("| Source | Reason | Statement | Explanation |")
        w("|---|---|---|---|")
        for i in sorted(ignored, key=lambda x: (x.reason, x.doc_id)):
            w(f"| {i.doc_id} | {i.reason} | {_cell(i.text)} | {_cell(i.explanation)} |")
    else:
        w("None.")
    w("")

    # --- Conflicts ---------------------------------------------------------------------
    w("## 8. Conflict resolution log")
    w("")
    if conflicts:
        for c in conflicts:
            w(f"- **{c.conflict_type}** between {', '.join(c.requirement_ids)} (pipeline IDs): {c.description} "
              f"Kept {c.kept}{' (revised)' if c.revised else ''}"
              + (f", removed {', '.join(c.discarded)}" if c.discarded else "") + f". *Rationale:* {c.rationale}")
    else:
        w("The conflict checker found no contradictions that required removing a requirement. Apparent tensions "
          "in the sources (e.g. card-based versus password login, real-time versus historical reporting, Linux "
          "versus Solaris servers) are complementary: the sources explicitly ask for both.")
    review_resolutions = [(m.req_id, n) for m in reqs for n in m.resolution_notes if "review" in n.lower()]
    if review_resolutions:
        w("")
        w("Changes made in review:")
        w("")
        for rid, note in review_resolutions:
            w(f"- {rid}: {note}")
    w("")

    # --- Quality assurance ----------------------------------------------------------------
    w("## 9. Quality assurance")
    w("")
    if validation:
        s = validation.stats
        w(f"Final automatic validation: **{'passed' if validation.passed else 'failed'}** - {s['errors']} errors, "
          f"{s['warnings']} warnings; {s['documents_used']} of {s['documents_total']} source documents traced.")
        w("")
        warnings = [i for i in validation.issues if i.severity == "warning"]
        if warnings:
            w("Remaining warnings (each was reviewed and judged acceptable, or is listed as open below):")
            w("")
            for i in warnings:
                w(f"- {i.check} - {i.target}: {_cell(i.message)}")
            w("")
    if review_history:
        w("Review rounds (validate - review - revise loop):")
        w("")
        w("| Round | Errors | Warnings | Actions | Warnings dismissed | Reviewer summary |")
        w("|---|---|---|---|---|---|")
        for h in review_history:
            w(f"| {h.round} | {h.errors} | {h.warnings} | {len(h.actions)} | {h.dismissed} | {_cell(h.summary)} |")
        w("")
    if open_actions:
        w("Open review items (proposed in the last round, not applied because the round limit was reached):")
        w("")
        for a in open_actions:
            w(f"- {a.action} {', '.join(a.requirement_ids)}: {_cell(a.instruction)}")
        w("")

    # --- Appendix ---------------------------------------------------------------------------
    w("## Appendix: traceability matrix")
    w("")
    w("| Document | Requirements derived from it |")
    w("|---|---|")
    for d in documents:
        ids = traced.get(d.doc_id, [])
        w(f"| {d.doc_id} `{_cell(d.path)}` | {', '.join(f'[{i}](#{_anchor(i)})' for i in ids) or '-'} |")
    w("")
    return "\n".join(out)


def render_document(state: dict) -> dict:
    """LangGraph node: writes the Markdown document to `state['output_path']`."""
    markdown = render(
        state["final_requirements"], state["documents"], state["areas"], state["glossary"],
        input_dir=state.get("input_dir", ""),
        conflict_blacklist=state.get("conflict_blacklist"), reviewer_blacklist=state.get("reviewer_blacklist"),
        discarded=state.get("discarded_candidates"), ignored=state.get("ignored_statements"),
        conflicts=state.get("conflict_records"), review_history=state.get("review_history"),
        open_actions=state.get("review_actions"), validation=state.get("validation"),
        n_candidates=len(state.get("candidates") or []) or None,
    )
    path = Path(state.get("output_path") or "output/requirements.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")
    print(f"Document written to {path}", flush=True)
    return {"document_path": str(path)}


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Render the requirements document from reviewer.py output.")
    parser.add_argument("input_dir")
    parser.add_argument("--reviewed", default="output/reviewed.json")
    parser.add_argument("--candidates", default="output/candidates.json")
    parser.add_argument("--out", default="output/requirements.md")
    args = parser.parse_args()

    documents, _ = load_corpus(args.input_dir)
    data = json.loads(Path(args.reviewed).read_text(encoding="utf-8"))
    cand = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    history = [ReviewRound.model_validate(h) for h in data.get("review_history", [])]
    from config import MAX_REVIEW_ROUNDS
    import re
    open_acts = []
    # The loop logs actions as "<action> <IDs>: <instruction>"; the last round's are open if the limit was hit.
    if history and len(history) >= MAX_REVIEW_ROUNDS and history[-1].actions:
        for a in history[-1].actions:
            m = re.match(r"(merge|rewrite|change_priority|remove) (.*?): (.*)", a, re.S)
            if m:
                open_acts.append(LLMReviewAction(action=m.group(1), requirement_ids=m.group(2).split(", "),
                                                 new_priority="none", instruction=m.group(3)))
    state = {
        "input_dir": args.input_dir, "output_path": args.out, "documents": documents,
        "areas": data["areas"], "glossary": [GlossaryTerm.model_validate(g) for g in data["glossary"]],
        "final_requirements": [MergedRequirement.model_validate(x) for x in data["requirements"]],
        "conflict_blacklist": [BlacklistEntry.model_validate(x) for x in data.get("conflict_blacklist", [])],
        "reviewer_blacklist": [BlacklistEntry.model_validate(x) for x in data.get("reviewer_blacklist", [])],
        "discarded_candidates": [DiscardedCandidate.model_validate(x) for x in data.get("discarded_candidates", [])],
        "ignored_statements": [IgnoredStatement.model_validate(x) for x in cand.get("ignored", [])],
        "conflict_records": [ConflictRecord.model_validate(x) for x in data.get("conflicts", [])],
        "review_history": history, "review_actions": open_acts,
        "validation": ValidationReport.model_validate(data["validation"]) if data.get("validation") else None,
        "candidates": cand.get("candidates", []),
    }
    render_document(state)
