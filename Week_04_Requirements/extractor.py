"""Extractor node (agentic, gpt-5-mini).

For every document chunk produced by the loader, asks the LLM to list all
candidate requirements (OS8 - completeness) together with a verbatim supporting
quote, and to list statements it deliberately ignored, with a reason (feeds the
blacklist, OS9). Source IDs are attached in code, not by the LLM (OS4), and each
quote is checked against the source text to flag hallucinations.

Usable as a LangGraph node (`extract_requirements`) or standalone:
    python extractor.py Task_1/data/corpus [--out output/candidates.json] [--limit N]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from config import EXTRACTOR_MODEL, MAX_CONCURRENCY, get_llm, raise_if_interrupted
from schemas import (
    CandidateRequirement,
    DocumentChunk,
    ExtractionError,
    IgnoredStatement,
    LLMExtractionResult,
    SourceDocument,
)

SYSTEM_PROMPT = """You are a senior requirements engineer. You read one source document \
(or one part of a long document) collected during requirements elicitation for a \
software system, and you extract every candidate software requirement it contains.

Rules:
1. Completeness: extract EVERY need, request, feature, report, constraint or quality \
expectation that someone states, proposes, supports or agrees on - including ones \
mentioned briefly in emails, interview answers, meeting discussions or survey comments. \
When in doubt, extract it; duplicates are removed later. Concerns about performance, \
data volume, scale, security or privacy (e.g. 'batch updates need to be efficient') are \
non-functional requirements, not remarks to ignore.
2. Granularity: one requirement = one distinct capability or quality. Split lists of \
different capabilities into separate requirements, but keep the parameters of the same \
capability (e.g. the fields of one report) together in its 'details'.
3. Wording: write 'statement' as one clear sentence 'The system shall ...'. Use neutral, \
consistent vocabulary (e.g. 'staff user', 'patron', 'item', 'branch', 'report'). Do not \
invent anything that is not supported by the text.
4. Types: functional = a capability; non-functional = a quality such as performance, \
usability, security, accessibility, reliability; constraint = a fixed technical or \
organisational limit (e.g. a required database, file format or standard).
5. Status: if the text shows a decision, mark 'agreed'; if someone objects or people \
disagree, mark 'disputed'; if it is explicitly turned down or declared out of scope, mark \
'rejected'. Explain who and why in 'status_note'. Otherwise use 'proposed'.
6. Priority: copy any verbatim wording that signals importance or urgency into \
'priority_signals' (e.g. 'CRITICAL', 'must', 'nice to have', survey percentages).
7. Evidence: 'quote' must be copied verbatim from the text (max ~300 characters).
8. Ignore, and list under 'ignored' with a reason: personal or off-topic chatter (hobbies, \
pets, films, cosmetics, small talk), plain questions or facts with no need behind them, \
and descriptions of what the CURRENT system already does. For reference documentation \
of the existing system, extract only explicitly stated gaps, limitations or constraints \
that imply something the new system must do or respect.
9. If the text contains no requirements, return an empty 'requirements' list."""

USER_TEMPLATE = """Document ID: {doc_id}
Document type: {doc_type}
Title: {title}
Date: {date}
Part: {index} of {total}{overlap_note}
{feedback}
--- BEGIN TEXT ---
{text}
--- END TEXT ---"""


def _normalise(text: str) -> str:
    text = text.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"[\"'`*>|]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def quote_in_source(quote: str, source: str) -> bool:
    """True if the quote (or a substantial part of it) appears in the source text."""
    q, s = _normalise(quote), _normalise(source)
    if not q:
        return False
    if q in s:
        return True
    # LLMs often stitch a list heading to one of its items, or join sentences
    # with "...": accept if every meaningful fragment appears in the source.
    parts = re.split(r"\n|\.\.\.|\u2026|\s-\s|(?<=[.;:?!])\s", quote)
    parts = [_normalise(p).strip(" -:.") for p in parts]
    parts = [p for p in parts if len(p) >= 8]
    return bool(parts) and all(p in s for p in parts)


def _build_messages(chunk: DocumentChunk, doc: SourceDocument, feedback: str | None) -> list[tuple[str, str]]:
    overlap_note = ""
    if chunk.total > 1:
        overlap_note = " (consecutive parts overlap slightly; extract everything in this part)"
    feedback_block = ""
    if feedback:
        feedback_block = f"\nReviewer feedback from a previous pass - pay special attention to it:\n{feedback}\n"
    user = USER_TEMPLATE.format(
        doc_id=doc.doc_id, doc_type=doc.doc_type, title=doc.title, date=doc.date or "unknown",
        index=chunk.index, total=chunk.total, overlap_note=overlap_note,
        feedback=feedback_block, text=chunk.text,
    )
    return [("system", SYSTEM_PROMPT), ("user", user)]


def extract_from_chunks(
    documents: list[SourceDocument],
    chunks: list[DocumentChunk],
    feedback: str | None = None,
) -> tuple[list[CandidateRequirement], list[IgnoredStatement], list[ExtractionError]]:
    """Run the extractor LLM over all chunks in parallel and post-process deterministically."""
    docs_by_id = {d.doc_id: d for d in documents}
    llm = get_llm(EXTRACTOR_MODEL).with_structured_output(LLMExtractionResult)

    inputs = [_build_messages(c, docs_by_id[c.doc_id], feedback) for c in chunks]
    print(f"Extracting with {EXTRACTOR_MODEL}: {len(chunks)} chunks, {MAX_CONCURRENCY} in parallel ...", flush=True)
    results = raise_if_interrupted(llm.batch(inputs, config={"max_concurrency": MAX_CONCURRENCY}, return_exceptions=True))

    # Retry failed chunks once, one at a time.
    for i, result in enumerate(results):
        if isinstance(result, Exception) or result is None:
            print(f"  retrying {chunks[i].chunk_id} ({type(result).__name__})", flush=True)
            try:
                results[i] = llm.invoke(inputs[i])
            except Exception as exc:  # recorded below
                results[i] = exc

    candidates: list[CandidateRequirement] = []
    ignored: list[IgnoredStatement] = []
    errors: list[ExtractionError] = []
    for chunk, result in zip(chunks, results):
        if isinstance(result, Exception) or result is None:
            errors.append(ExtractionError(chunk_id=chunk.chunk_id, error=f"{type(result).__name__}: {result}"[:500]))
            continue
        for req in result.requirements:
            candidates.append(CandidateRequirement(
                **req.model_dump(),
                candidate_id=f"C{len(candidates) + 1:03d}",
                doc_id=chunk.doc_id,
                chunk_id=chunk.chunk_id,
                quote_verified=quote_in_source(req.quote, chunk.text),
            ))
        for item in result.ignored:
            ignored.append(IgnoredStatement(**item.model_dump(), doc_id=chunk.doc_id, chunk_id=chunk.chunk_id))
    return candidates, ignored, errors


def extract_requirements(state: dict) -> dict:
    """LangGraph node: reads `documents`, `chunks` and optional `extraction_feedback`."""
    candidates, ignored, errors = extract_from_chunks(
        state["documents"], state["chunks"], state.get("extraction_feedback"),
    )
    return {"candidates": candidates, "ignored_statements": ignored, "extraction_errors": errors}


def print_summary(documents, candidates, ignored, errors) -> None:
    print(f"\n{len(candidates)} candidate requirements, {len(ignored)} ignored statements, {len(errors)} failed chunks")
    unverified = [c for c in candidates if not c.quote_verified]
    print(f"Quotes not found verbatim in source: {len(unverified)}")
    print(f"\n{'doc':<5}{'reqs':>5}{'ignored':>9}  path")
    for d in documents:
        n_req = sum(c.doc_id == d.doc_id for c in candidates)
        n_ign = sum(i.doc_id == d.doc_id for i in ignored)
        flag = "   <-- no requirements" if n_req == 0 else ""
        print(f"{d.doc_id:<5}{n_req:>5}{n_ign:>9}  {d.path}{flag}")
    for e in errors:
        print(f"FAILED {e.chunk_id}: {e.error}")


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Run the requirement extractor on a corpus directory.")
    parser.add_argument("input_dir", help="Directory with the input documents")
    parser.add_argument("--out", default="output/candidates.json", help="Where to write the JSON result")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N chunks (for quick tests)")
    args = parser.parse_args()

    docs, all_chunks = load_corpus(args.input_dir)
    selected = all_chunks[: args.limit] if args.limit else all_chunks
    selected_docs = [d for d in docs if any(c.doc_id == d.doc_id for c in selected)]

    cands, ign, errs = extract_from_chunks(docs, selected)
    print_summary(selected_docs, cands, ign, errs)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "model": EXTRACTOR_MODEL,
        "candidates": [c.model_dump() for c in cands],
        "ignored": [i.model_dump() for i in ign],
        "errors": [e.model_dump() for e in errs],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
    sys.exit(1 if errs else 0)
