"""Validator node (deterministic, no AI - ANS2).

Assigns the final unique requirement IDs (OS2) and checks the requirement set
against the output specification. Every problem found is recorded as an issue
with a severity and the node responsible for fixing it; the reviewer uses this
report to decide whether to loop back (ANS3).

Checks:
  OS2  unique IDs; no two requirements with the same name or statement
  OS3  possible remaining duplicates (high word overlap)
  OS4  every requirement traces to at least one existing source document,
       backed by evidence; quotes that could not be verified are reported
  OS5  name present and short; statement and paragraph-long description present
  OS6  priority present and from the defined scale
  OS7  glossary terms used consistently; no unresolved conflict notes left
  OS8  every candidate requirement is accounted for (kept, merged or
       blacklisted); every input document contributes or is explained
  OS9  blacklisted items carry an explanation

Usable as a LangGraph node (`validate_requirements`) or standalone:
    python validator.py Task_1/data/corpus
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

from merger import suspected_pairs
from prioritizer import PRIORITY_ORDER, PRIORITY_SCALE
from schemas import (
    BlacklistEntry,
    CandidateRequirement,
    DiscardedCandidate,
    GlossaryTerm,
    IgnoredStatement,
    MergedRequirement,
    SourceDocument,
    ValidationIssue,
    ValidationReport,
)

ID_PREFIX = "REQ"
MAX_NAME_WORDS = 10
MIN_DESCRIPTION_CHARS = 150
MIN_DESCRIPTION_SENTENCES = 2
DUPLICATE_WARNING_THRESHOLD = 0.6


def assign_ids(requirements: list[MergedRequirement], areas: list[str]) -> list[MergedRequirement]:
    """Order by area, then priority, then name, and assign REQ-001, REQ-002, ... (OS2)."""
    area_order = {a: i for i, a in enumerate(areas)}
    prio_order = {p: i for i, p in enumerate(PRIORITY_ORDER)}
    ordered = sorted(requirements, key=lambda m: (area_order.get(m.area, len(areas)),
                                                   prio_order.get(m.priority or "", len(PRIORITY_ORDER)),
                                                   m.name.lower()))
    width = max(3, len(str(len(ordered))))
    for i, m in enumerate(ordered, start=1):
        m.req_id = f"{ID_PREFIX}-{i:0{width}d}"
    return ordered


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _checkable_avoid_terms(glossary: list[GlossaryTerm]) -> dict[str, str]:
    """Avoid-terms that can be checked mechanically.

    Skipped: conditional entries ('location, when meaning a branch') - only a reader
    can judge the context - and words that are part of a preferred term ('library'
    in 'library system'), which are ambiguous on their own.
    """
    preferred_words = {w for g in glossary for w in _norm(g.term).split()}
    result = {}
    for g in glossary:
        for raw in g.avoid:
            if "," in raw or re.search(r"\b(when|unless)\b", raw):
                continue
            term = _norm(raw)
            if term and not set(term.split()) <= preferred_words:
                result[term] = g.term
    return result


def validate(requirements: list[MergedRequirement], documents: list[SourceDocument], areas: list[str],
             glossary: list[GlossaryTerm], candidates: list[CandidateRequirement] | None = None,
             merged_before_conflicts: list[MergedRequirement] | None = None,
             discarded: list[DiscardedCandidate] | None = None,
             blacklist: list[BlacklistEntry] | None = None,
             ignored: list[IgnoredStatement] | None = None) -> tuple[list[MergedRequirement], ValidationReport]:
    discarded = discarded or []
    blacklist = blacklist or []
    ignored = ignored or []
    issues: list[ValidationIssue] = []

    def issue(severity, check, target, message, responsible):
        issues.append(ValidationIssue(severity=severity, check=check, target=target,
                                      message=message, responsible=responsible))

    final = assign_ids(requirements, areas)
    doc_ids = {d.doc_id for d in documents}

    # --- OS2: unique IDs, names and statements -------------------------------
    for rid, n in Counter(m.req_id for m in final).items():
        if n > 1:
            issue("error", "duplicate-id", rid, f"ID used {n} times", "none")
    for field in ("name", "statement"):
        groups: dict[str, list[str]] = {}
        for m in final:
            groups.setdefault(_norm(getattr(m, field)), []).append(m.req_id)
        for ids in groups.values():
            if len(ids) > 1:
                issue("error", f"duplicate-{field}", ", ".join(ids),
                      f"Requirements share the same {field}; merge them or make them distinct", "merger")

    # --- OS3: possible remaining duplicates (for the reviewer to judge) ------
    by_merge = {m.merge_id: m for m in final}
    for a, b, score in suspected_pairs(final, threshold=DUPLICATE_WARNING_THRESHOLD, limit=100):
        ma, mb = by_merge[a], by_merge[b]
        issue("warning", "possible-duplicate", f"{ma.req_id}, {mb.req_id}",
              f"'{ma.name}' and '{mb.name}' are very similar (overlap {score:.2f})", "merger")

    # --- OS4, OS5, OS6, OS7 per requirement ----------------------------------
    avoid_terms = _checkable_avoid_terms(glossary)
    preferred = sorted({_norm(g.term) for g in glossary}, key=len, reverse=True)
    for m in final:
        rid = m.req_id
        if not m.name.strip():
            issue("error", "missing-name", rid, "Requirement has no name", "merger")
        elif len(m.name.split()) > MAX_NAME_WORDS:
            issue("warning", "long-name", rid, f"Name has {len(m.name.split())} words (max {MAX_NAME_WORDS})", "merger")
        if not m.statement.strip():
            issue("error", "missing-statement", rid, "Requirement has no statement", "merger")
        elif not m.statement.lower().startswith("the system shall"):
            issue("warning", "statement-form", rid, "Statement does not start with 'The system shall'", "merger")
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", m.description.strip()) if len(s) > 3]
        if len(m.description) < MIN_DESCRIPTION_CHARS or len(sentences) < MIN_DESCRIPTION_SENTENCES:
            issue("error", "short-description", rid,
                  f"Description is not a paragraph ({len(m.description)} chars, {len(sentences)} sentences)", "merger")
        if m.priority not in PRIORITY_SCALE:
            issue("error", "missing-priority", rid, f"Priority '{m.priority}' is not on the scale", "prioritizer")
        elif not m.priority_rationale.strip():
            issue("warning", "missing-priority-rationale", rid, "Priority has no justification", "prioritizer")
        if not m.source_doc_ids:
            issue("error", "no-trace", rid, "Requirement has no source document", "merger")
        unknown = [d for d in m.source_doc_ids if d not in doc_ids]
        if unknown:
            issue("error", "unknown-source", rid, f"Unknown source documents: {', '.join(unknown)}", "merger")
        if not m.evidence:
            issue("error", "no-evidence", rid, "Requirement has no supporting quote", "merger")
        elif not any(e.quote_verified for e in m.evidence):
            issue("warning", "unverified-evidence", rid,
                  "None of the supporting quotes was found verbatim in the sources", "extractor")
        text = f" {_norm(m.name)} {_norm(m.statement)} "
        for term in preferred:  # correct uses of glossary terms must not trigger the check
            text = re.sub(rf" {re.escape(term)}(?:s|es)? ", " ", text)
        for term, preferred_term in avoid_terms.items():
            if re.search(rf" {re.escape(term)}(?:s|es)? ", text):
                issue("warning", "vocabulary", rid, f"Uses '{term}' instead of the glossary term '{preferred_term}'", "merger")
        if m.conflict_notes:
            issue("warning", "unresolved-conflict", rid, "Conflict notes left unresolved", "conflict_checker")

    # --- OS8: candidate coverage ----------------------------------------------
    if candidates is not None:
        accounted = {c for m in final for c in m.source_candidate_ids} | {d.candidate_id for d in discarded}
        if merged_before_conflicts is not None:
            blacklisted_ids = {b.source_id for b in blacklist}
            accounted |= {c for m in merged_before_conflicts if m.merge_id in blacklisted_ids
                          for c in m.source_candidate_ids}
        accounted |= {c for b in blacklist for c in b.source_candidate_ids}
        lost = [c.candidate_id for c in candidates if c.candidate_id not in accounted]
        if lost:
            issue("error", "lost-candidates", "document",
                  f"{len(lost)} extracted candidates are neither in a requirement nor blacklisted: "
                  f"{', '.join(lost[:15])}{' ...' if len(lost) > 15 else ''}", "merger")

    # --- OS8: document coverage -----------------------------------------------
    used = Counter(d for m in final for d in m.source_doc_ids)
    for d in documents:
        if used[d.doc_id]:
            continue
        n_cands = sum(c.doc_id == d.doc_id for c in candidates or [])
        n_excluded = sum(x.doc_id == d.doc_id for x in discarded) + sum(d.doc_id in b.source_doc_ids for b in blacklist)
        n_ignored = sum(i.doc_id == d.doc_id for i in ignored)
        if n_cands == 0:
            issue("error", "document-not-used", d.doc_id,
                  f"No requirement was extracted from '{d.path}' ({n_ignored} statements ignored)", "extractor")
        elif n_excluded:
            issue("info", "document-only-blacklisted", d.doc_id,
                  f"All requirements from '{d.path}' were blacklisted (see blacklist)", "none")
        else:
            issue("error", "document-not-used", d.doc_id,
                  f"{n_cands} candidates from '{d.path}' do not appear in any requirement", "merger")

    # --- OS9: blacklist explanations ------------------------------------------
    for b in blacklist:
        if not b.explanation.strip():
            issue("error", "blacklist-unexplained", b.source_id, "Blacklisted item has no explanation", "conflict_checker")
    for d in discarded:
        if not d.explanation.strip():
            issue("error", "blacklist-unexplained", d.candidate_id, "Discarded candidate has no explanation", "merger")

    severity_counts = Counter(i.severity for i in issues)
    stats = {
        "requirements": len(final),
        **{f"priority_{p}": sum(m.priority == p for m in final) for p in PRIORITY_ORDER},
        "documents_used": sum(1 for d in documents if used[d.doc_id]),
        "documents_total": len(documents),
        "blacklisted": len(blacklist) + len(discarded),
        "errors": severity_counts["error"],
        "warnings": severity_counts["warning"],
    }
    order = {"error": 0, "warning": 1, "info": 2}
    issues.sort(key=lambda i: (order[i.severity], i.check, i.target))
    return final, ValidationReport(passed=severity_counts["error"] == 0, issues=issues, stats=stats)


def validate_requirements(state: dict) -> dict:
    """LangGraph node: validates `resolved_requirements` and returns `final_requirements` + `validation`."""
    final, report = validate(
        state["resolved_requirements"], state["documents"], state["areas"], state["glossary"],
        candidates=state.get("candidates"), merged_before_conflicts=state.get("merged_requirements"),
        discarded=state.get("discarded_candidates"),
        blacklist=(state.get("conflict_blacklist") or []) + (state.get("reviewer_blacklist") or []),
        ignored=state.get("ignored_statements"),
    )
    return {"final_requirements": final, "validation": report}


def print_report(report: ValidationReport) -> None:
    s = report.stats
    print(f"Validation {'PASSED' if report.passed else 'FAILED'}: {s['errors']} errors, {s['warnings']} warnings")
    print(f"{s['requirements']} requirements (" + ", ".join(f"{p}: {s['priority_' + p]}" for p in PRIORITY_ORDER)
          + f"), {s['documents_used']}/{s['documents_total']} documents used, {s['blacklisted']} blacklisted")
    by_check = Counter((i.severity, i.check, i.responsible) for i in report.issues)
    if by_check:
        print(f"\n{'severity':<9}{'count':>6}  {'check':<28}responsible")
        for (sev, check, resp), n in sorted(by_check.items(), key=lambda kv: ({'error': 0, 'warning': 1, 'info': 2}[kv[0][0]], kv[0][1])):
            print(f"{sev:<9}{n:>6}  {check:<28}{resp}")
        print("\nDetails (first 3 per check):")
        shown = Counter()
        for i in report.issues:
            if shown[i.check] < 3:
                shown[i.check] += 1
                print(f"  [{i.severity}] {i.check} {i.target}: {i.message}")


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Assign final IDs and validate the requirement set.")
    parser.add_argument("input_dir", help="Corpus directory")
    parser.add_argument("--prioritized", default="output/prioritized.json", help="Output of prioritizer.py")
    parser.add_argument("--merged", default="output/merged.json", help="Output of merger.py (for coverage)")
    parser.add_argument("--candidates", default="output/candidates.json", help="Output of extractor.py (for coverage)")
    parser.add_argument("--out", default="output/validated.json")
    args = parser.parse_args()

    docs, _ = load_corpus(args.input_dir)
    data = json.loads(Path(args.prioritized).read_text(encoding="utf-8"))
    merged_data = json.loads(Path(args.merged).read_text(encoding="utf-8"))
    cand_data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))

    final_reqs, rep = validate(
        [MergedRequirement.model_validate(x) for x in data["requirements"]], docs, data["areas"],
        [GlossaryTerm.model_validate(g) for g in data["glossary"]],
        candidates=[CandidateRequirement.model_validate(c) for c in cand_data["candidates"]],
        merged_before_conflicts=[MergedRequirement.model_validate(x) for x in merged_data["merged_requirements"]],
        discarded=[DiscardedCandidate.model_validate(x) for x in data["discarded_candidates"]],
        blacklist=[BlacklistEntry.model_validate(x) for x in data["conflict_blacklist"]],
        ignored=[IgnoredStatement.model_validate(x) for x in cand_data["ignored"]],
    )
    print_report(rep)

    data["requirements"] = [x.model_dump() for x in final_reqs]
    data["validation"] = rep.model_dump()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
