"""Conflict checker node (agentic, gpt-6-luna) - consistency and blacklist (OS7, OS9).

Finds requirements that contradict each other, or that are nonsensical / out of
scope, and resolves them:

  * conflicts: one requirement is kept (and possibly revised so that it
    reconciles both sides), the others are moved to the blacklist with an
    explanation;
  * invalid requirements: moved to the blacklist with the reason.

To decide which side wins, the LLM sees each source document's type and date
(later decisions supersede the early draft specification; agreed beats
proposed; hard technical constraints beat wishes).

Deterministic support around the LLM:
  * hints: pairs flagged as possible conflicts by the merger, plus pairs of
    similar but non-duplicate requirements (where conflicts typically hide);
  * validation: unknown IDs, a requirement both kept and discarded, or a
    requirement discarded twice are ignored;
  * check-and-retry loop: every conflict flagged by the merger must be
    addressed; unaddressed ones are sent back to the LLM once more.

Usable as a LangGraph node (`check_conflicts`) or standalone:
    python conflict_checker.py Task_1/data/corpus [--merged output/merged.json] [--out output/resolved.json]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from config import CONFLICT_MODEL, get_llm
from merger import suspected_pairs
from schemas import (
    BlacklistEntry,
    ConflictRecord,
    LLMConflictResult,
    MergedRequirement,
    SourceDocument,
)

MAX_RETRY_ROUNDS = 1
RELATED_PAIR_THRESHOLD = 0.3
MAX_RELATED_PAIRS = 150
DESCRIPTION_PREVIEW = 300

SYSTEM_PROMPT = """You are a senior requirements engineer responsible for the \
consistency of a requirements specification. The requirements were extracted from \
several elicitation documents (an early draft specification, emails, interviews, \
meeting minutes, a survey, reference documentation of the existing system) and \
already deduplicated.

Task 1 - conflicts. Find requirements that cannot all be satisfied as written:
- contradiction: one requires what another forbids or rejects;
- inconsistent-parameter: different values for the same thing (timing, limits, formats, \
retention periods, scope);
- incompatible-alternatives: mutually exclusive solutions to the same need.
Requirements that are merely related, complementary, or at different levels of detail \
are NOT conflicts. Requirements that can both be satisfied (e.g. two login methods that \
can coexist, or real-time for some reports and historical data for others) are not \
conflicts unless a source says only one is allowed - in that case, or when one \
requirement can be revised to cover both sides, prefer reconciling: keep one, write a \
revised statement and description, and discard the other(s) as superseded.

Resolve every conflict by choosing which requirement to keep, using the sources:
1. A later explicit decision (meeting minutes, agreed status) supersedes earlier \
proposals, especially the early draft specification.
2. 'agreed' beats 'proposed'; a requirement backed by more stakeholders or sources \
generally beats a single request.
3. Hard technical constraints (from the system administrator or technical subcommittee) \
beat wishes that violate them.
Explain the rationale with reference to the documents.

Task 2 - invalid requirements. Identify requirements that are nonsensical, outside the \
scope of the system being specified, or not system requirements at all (project tasks, \
process steps, remarks). Be conservative: when a requirement is plausible, keep it.

Rules: use only the given IDs; each ID may be discarded at most once; never discard and \
keep the same ID; return empty lists if there is nothing to report."""


def _doc_table(documents: list[SourceDocument]) -> str:
    return "\n".join(f"{d.doc_id} | {d.doc_type} | {d.date or 'unknown date'} | {d.title}" for d in documents)


def _requirement_listing(merged: list[MergedRequirement]) -> str:
    lines = []
    for m in merged:
        desc = m.description if len(m.description) <= DESCRIPTION_PREVIEW else m.description[:DESCRIPTION_PREVIEW] + "..."
        line = f"{m.merge_id} [{m.area}] {m.name} (sources: {', '.join(m.source_doc_ids)})\n  {m.statement}\n  {desc}"
        if m.candidate_statuses:
            line += "\n  status: " + "; ".join(m.candidate_statuses)
        lines.append(line)
    return "\n".join(lines)


def flagged_pairs(merged: list[MergedRequirement]) -> list[tuple[str, str, str]]:
    """Conflicts flagged by the merger, translated from candidate IDs (C###) to requirement IDs (M###)."""
    owner = {c: m.merge_id for m in merged for c in m.source_candidate_ids}
    pairs = []
    for m in merged:
        for note in m.conflict_notes:
            others = {owner[c] for c in re.findall(r"C\d{3,}", note) if c in owner} - {m.merge_id}
            for other in sorted(others):
                pair = tuple(sorted((m.merge_id, other)))
                if pair not in [(a, b) for a, b, _ in pairs]:
                    pairs.append((pair[0], pair[1], note))
    return pairs


def _ask(merged: list[MergedRequirement], documents: list[SourceDocument], flagged: list[tuple[str, str, str]],
         related: list[tuple[str, str, float]], feedback: str | None, focus: str | None = None) -> LLMConflictResult:
    flagged_text = "\n".join(f"- {a} / {b}: {note}" for a, b, note in flagged) or "(none)"
    related_text = "\n".join(f"- {a} / {b}" for a, b, _ in related) or "(none)"
    user = (
        f"Source documents (ID | type | date | title):\n{_doc_table(documents)}\n\n"
        f"Requirements:\n{_requirement_listing(merged)}\n\n"
        f"Possible conflicts flagged during merging (check each):\n{flagged_text}\n\n"
        f"Similar but distinct requirements (conflicts often hide here):\n{related_text}"
    )
    if feedback:
        user += f"\n\nReviewer feedback from a previous pass - take it into account:\n{feedback}"
    if focus:
        user += f"\n\nIMPORTANT: {focus}"
    llm = get_llm(CONFLICT_MODEL).with_structured_output(LLMConflictResult)
    return llm.invoke([("system", SYSTEM_PROMPT), ("user", user)])


def resolve_conflicts(merged: list[MergedRequirement], documents: list[SourceDocument],
                      feedback: str | None = None) -> tuple[list[MergedRequirement], list[BlacklistEntry], list[ConflictRecord]]:
    by_id = {m.merge_id: m for m in merged}
    flagged = flagged_pairs(merged)
    related = suspected_pairs(merged, threshold=RELATED_PAIR_THRESHOLD, limit=MAX_RELATED_PAIRS)

    removed: dict[str, BlacklistEntry] = {}
    kept_ids: set[str] = set()
    records: list[ConflictRecord] = []
    addressed: set[frozenset] = set()

    def apply(result: LLMConflictResult) -> None:
        for c in result.conflicts:
            ids = [i for i in dict.fromkeys(x.strip().upper() for x in c.requirement_ids) if i in by_id]
            keep = c.keep_id.strip().upper()
            if keep not in by_id or keep in removed:
                continue
            discards = [d for d in dict.fromkeys(x.strip().upper() for x in c.discard_ids)
                        if d in by_id and d != keep and d not in removed and d not in kept_ids]
            involved = list(dict.fromkeys([keep] + ids + discards))
            if len(involved) < 2:
                continue
            if c.discard_ids and not discards and not c.revised_statement.strip():
                continue  # every requested removal was invalid, so nothing would be resolved
            kept_ids.add(keep)
            target = by_id[keep]
            revised = bool(c.revised_statement.strip())
            if revised:
                target.statement = c.revised_statement.strip()
                if c.revised_description.strip():
                    target.description = c.revised_description.strip()
            # The kept requirement inherits the tracing of the requirements it superseded (OS4).
            for d in discards:
                loser = by_id[d]
                target.source_doc_ids = sorted(set(target.source_doc_ids) | set(loser.source_doc_ids)) if revised else target.source_doc_ids
                removed[d] = BlacklistEntry(
                    source_id=d, name=loser.name, statement=loser.statement, source_doc_ids=loser.source_doc_ids,
                    category="conflict", explanation=f"{c.description} Resolution: {c.rationale}",
                    conflicts_with=[f"{keep} {target.name}"],
                )
            note = f"Conflict with {', '.join(i for i in involved if i != keep)} ({c.conflict_type}): {c.description} " \
                   f"Resolution: {c.rationale}"
            target.resolution_notes.append(note)
            records.append(ConflictRecord(requirement_ids=involved, conflict_type=c.conflict_type,
                                          description=c.description, kept=keep, discarded=discards,
                                          revised=revised, rationale=c.rationale))
            for i, a in enumerate(involved):
                for b in involved[i + 1:]:
                    addressed.add(frozenset((a, b)))
        for inv in result.invalid:
            rid = inv.requirement_id.strip().upper()
            if rid in by_id and rid not in removed and rid not in kept_ids:
                m = by_id[rid]
                removed[rid] = BlacklistEntry(source_id=rid, name=m.name, statement=m.statement,
                                              source_doc_ids=m.source_doc_ids, category=inv.reason,
                                              explanation=inv.explanation)

    print(f"Conflict check with {CONFLICT_MODEL}: {len(merged)} requirements, {len(flagged)} flagged pairs, "
          f"{len(related)} related pairs ...", flush=True)
    apply(_ask(merged, documents, flagged, related, feedback))

    # Deterministic check: was every flagged pair either resolved or explicitly judged? Retry once.
    for _ in range(MAX_RETRY_ROUNDS):
        open_pairs = [(a, b, n) for a, b, n in flagged
                      if frozenset((a, b)) not in addressed and a not in removed and b not in removed]
        if not open_pairs:
            break
        print(f"  {len(open_pairs)} flagged pairs not addressed - asking again", flush=True)
        remaining = [m for m in merged if m.merge_id not in removed]
        focus = ("Decide explicitly for each of these flagged pairs whether it is a real conflict; "
                 "report it under 'conflicts' only if it is: " + ", ".join(f"{a}/{b}" for a, b, _ in open_pairs))
        apply(_ask(remaining, documents, open_pairs, [], feedback, focus))
        # Pairs the LLM saw twice and did not report are judged compatible.
        addressed.update(frozenset((a, b)) for a, b, _ in open_pairs)

    for m in merged:  # conflict notes are now either resolved or judged not to be conflicts
        if m.merge_id not in removed:
            m.conflict_notes = []
    final = [m for m in merged if m.merge_id not in removed]
    return final, list(removed.values()), records


def check_conflicts(state: dict) -> dict:
    """LangGraph node: reads `merged_requirements`, `documents`, optional `conflict_feedback`."""
    final, blacklist, records = resolve_conflicts(
        state["merged_requirements"], state["documents"], state.get("conflict_feedback"),
    )
    return {"resolved_requirements": final, "conflict_blacklist": blacklist, "conflict_records": records}


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Detect and resolve conflicting requirements.")
    parser.add_argument("input_dir", help="Corpus directory (for document types and dates)")
    parser.add_argument("--merged", default="output/merged.json", help="Output of merger.py")
    parser.add_argument("--out", default="output/resolved.json")
    args = parser.parse_args()

    docs, _ = load_corpus(args.input_dir)
    data = json.loads(Path(args.merged).read_text(encoding="utf-8"))
    reqs = [MergedRequirement.model_validate(x) for x in data["merged_requirements"]]

    final_reqs, black, recs = resolve_conflicts(reqs, docs)

    print(f"\n{len(reqs)} requirements -> {len(final_reqs)} kept, {len(black)} blacklisted, {len(recs)} conflicts resolved")
    for r in recs:
        action = "revised + " if r.revised else ""
        print(f"\n  [{r.conflict_type}] {' / '.join(r.requirement_ids)} -> keep {r.kept} ({action}discard {', '.join(r.discarded) or 'none'})")
        print(f"    {r.description}")
        print(f"    Why: {r.rationale}")
    invalid = [b for b in black if b.category != "conflict"]
    if invalid:
        print("\nRemoved as invalid:")
        for b in invalid:
            print(f"  {b.source_id} [{b.category}] {b.name} - {b.explanation}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "model": CONFLICT_MODEL,
        "areas": data["areas"],
        "glossary": data["glossary"],
        "requirements": [x.model_dump() for x in final_reqs],
        "conflict_blacklist": [x.model_dump() for x in black],
        "discarded_candidates": data["discarded_candidates"],
        "conflicts": [x.model_dump() for x in recs],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
