"""Prioritiser node (agentic, gpt-5.6-luna) - assigns a MoSCoW priority (OS6).

The priority scale is defined once here (PRIORITY_SCALE) and used both in the
prompt and in the final document, so the document explains exactly the scale
the LLM applied.

Deterministic support around the LLM:
  * evidence is computed in code for each requirement (number of source
    documents and stakeholders, agreed decisions, verbatim priority signals,
    survey backing) and given to the LLM, so its judgement is grounded;
  * coverage check: every requirement must receive a priority; missing ones
    are asked for again, and as a last resort a transparent rule assigns one
    (marked as such in the rationale).

Usable as a LangGraph node (`prioritize_requirements`) or standalone:
    python prioritizer.py Task_1/data/corpus [--resolved output/resolved.json] [--out output/prioritized.json]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from config import MAX_CONCURRENCY, PRIORITISER_MODEL, get_llm, raise_if_interrupted
from schemas import LLMPriorityResult, MergedRequirement, SourceDocument

PRIORITY_SCALE = {
    "Must": "Essential for the system to be acceptable. Explicitly marked as critical or mandatory, "
            "agreed as a decision by the working group, required by law, audit or policy, or a hard "
            "technical constraint. Without it the system fails its purpose.",
    "Should": "Important and expected, typically requested by several stakeholders or sources, but the "
              "system is still usable without it for a time, or a workaround exists.",
    "Could": "Desirable improvement with limited impact, typically raised by a single stakeholder or as an "
             "example; implemented if time and budget allow.",
    "Won't": "Acknowledged but explicitly deferred or of very low value for this release; recorded so it "
             "is not forgotten.",
}
PRIORITY_ORDER = list(PRIORITY_SCALE)
MAX_RETRY_ROUNDS = 1
# Calibration: if more than MAX_MUST_SHARE of all requirements are Must, a second
# LLM call compares all Musts together and keeps about TARGET_MUST_SHARE.
MAX_MUST_SHARE = 0.35
TARGET_MUST_SHARE = 0.30

SYSTEM_PROMPT = """You are a senior requirements engineer assigning MoSCoW priorities \
to requirements of a reporting system for a library consortium.

Priority scale:
{scale}

Use the evidence given for each requirement:
- verbatim priority signals ('CRITICAL', 'must', 'nice to have', survey percentages);
- decisions: each agreement is listed with the type of document it comes from. Only an \
agreement recorded in meeting minutes is a formal decision and strong evidence for Must. \
Agreement in an email thread, interview or survey means stakeholder SUPPORT - it counts \
as breadth, not as a decision, and alone does not justify Must;
- breadth: the number of independent source documents and stakeholders;
- source type: the early draft specification lists many example reports - an example \
mentioned only there, with no other support, is usually Could; needs confirmed by the \
survey, interviews or meetings rank higher;
- legal, audit, privacy, security, accessibility and hard technical constraints are \
usually Must.
- Won't: use it for needs that a source explicitly defers, rejects for this release or \
calls low priority, and for marginal ideas with no real support.
Be discriminating: typically only about a quarter to a third of requirements are Must. \
Assign a priority to EVERY requirement ID you receive, with a one-sentence justification \
that cites the evidence."""

CALIBRATION_PROMPT = """You are a senior requirements engineer calibrating MoSCoW \
priorities across a whole specification. The requirements below were each marked 'Must' \
by reviewers working on separate functional areas, so together there are too many: \
{n_must} of {n_total} requirements ({share:.0%}).

Priority scale:
{scale}

Keep as Must only the about {target} most essential requirements: legal, audit, privacy \
and security obligations, hard technical constraints, formal decisions from meeting \
minutes, and core capabilities without which the reporting system fails its purpose. \
Downgrade the others to Should. Return an assignment for EVERY requirement ID below \
(priority 'Must' or 'Should') with a one-sentence justification that cites the evidence."""

USER_TEMPLATE = """Functional area: {area}

Source documents (ID | type | date):
{docs}

Requirements with evidence:
{items}{feedback}"""


def _scale_text() -> str:
    return "\n".join(f"- {name}: {text}" for name, text in PRIORITY_SCALE.items())


def _evidence(m: MergedRequirement, doc_types: dict[str, str]) -> dict:
    """Evidence summary computed in code (no LLM)."""
    cand_doc = {e.candidate_id: e.doc_id for e in m.evidence}
    agreed = []
    for status in m.candidate_statuses:
        if ": agreed" not in status:
            continue
        cid = status.split(":", 1)[0].strip()
        agreed.append(f"[{doc_types.get(cand_doc.get(cid, ''), 'unknown')}] {status}")
    return {
        "id": m.merge_id,
        "name": m.name,
        "statement": m.statement,
        "type": m.req_type,
        "source_documents": len(m.source_doc_ids),
        "source_types": sorted(Counter(doc_types.get(d, "other") for d in m.source_doc_ids).items()),
        "stakeholders": len(m.stakeholders),
        "agreed_decisions": agreed,
        "priority_signals": m.priority_signals,
    }


def rule_based_priority(m: MergedRequirement) -> tuple[str, str]:
    """Transparent fallback used only if the LLM fails to assign a priority."""
    signals = " ".join(m.priority_signals).lower()
    agreed = any(": agreed" in s for s in m.candidate_statuses)
    if re.search(r"critical|must|mandatory|required|essential|law|audit", signals) or agreed or m.req_type == "constraint":
        return "Must", "Assigned by rule: explicit mandatory wording, an agreed decision, or a constraint."
    if len(m.source_doc_ids) >= 3:
        return "Should", "Assigned by rule: supported by three or more source documents."
    return "Could", "Assigned by rule: limited support in the sources."


def prioritize(requirements: list[MergedRequirement], documents: list[SourceDocument],
               feedback: str | None = None) -> list[MergedRequirement]:
    doc_types = {d.doc_id: d.doc_type for d in documents}
    doc_table = "\n".join(f"{d.doc_id} | {d.doc_type} | {d.date or 'unknown'}" for d in documents)
    by_id = {m.merge_id: m for m in requirements}
    llm = get_llm(PRIORITISER_MODEL).with_structured_output(LLMPriorityResult)
    system = SYSTEM_PROMPT.format(scale=_scale_text())
    feedback_text = f"\n\nReviewer feedback from a previous pass - take it into account:\n{feedback}" if feedback else ""

    # With reviewer feedback everything is re-assessed; otherwise only unprioritised ones.
    pending = list(requirements) if feedback else [m for m in requirements if m.priority is None]
    for round_no in range(MAX_RETRY_ROUNDS + 1):
        if not pending:
            break
        by_area: dict[str, list[MergedRequirement]] = defaultdict(list)
        for m in pending:
            by_area[m.area].append(m)
        jobs = list(by_area.items())
        label = "Prioritising" if round_no == 0 else "  retry for missing priorities:"
        print(f"{label} {len(pending)} requirements in {len(jobs)} groups with {PRIORITISER_MODEL} ...", flush=True)
        inputs = [[("system", system), ("user", USER_TEMPLATE.format(
            area=area, docs=doc_table,
            items=json.dumps([_evidence(m, doc_types) for m in items], ensure_ascii=False, indent=1),
            feedback=feedback_text))] for area, items in jobs]
        results = raise_if_interrupted(llm.batch(inputs, config={"max_concurrency": MAX_CONCURRENCY}, return_exceptions=True))

        for (area, items), result in zip(jobs, results):
            if isinstance(result, Exception) or result is None:
                print(f"  group '{area}' failed: {type(result).__name__}", flush=True)
                continue
            allowed = {m.merge_id for m in items}
            for a in result.assignments:
                rid = a.requirement_id.strip().upper()
                if rid in allowed:  # ignore IDs from other groups or invented ones
                    by_id[rid].priority = a.priority
                    by_id[rid].priority_rationale = a.justification.strip()
        # Coverage check (deterministic): retry only requirements still without a priority.
        pending = [m for m in pending if m.priority is None]

    for m in pending:  # last resort, never leave a requirement without priority
        m.priority, m.priority_rationale = rule_based_priority(m)
    if pending:
        print(f"  {len(pending)} priorities assigned by rule", flush=True)
    calibrate_musts(requirements, doc_types)
    return requirements


def calibrate_musts(requirements: list[MergedRequirement], doc_types: dict[str, str]) -> None:
    """Check (code) the overall Must share; if too high, re-rank all Musts together (LLM)."""
    musts = [m for m in requirements if m.priority == "Must"]
    total = len(requirements)
    share = len(musts) / total if total else 0
    if share <= MAX_MUST_SHARE:
        return
    target = round(TARGET_MUST_SHARE * total)
    print(f"Calibrating: {len(musts)} Must ({share:.0%}) > {MAX_MUST_SHARE:.0%}, "
          f"re-ranking with {PRIORITISER_MODEL} to about {target} ...", flush=True)
    items = []
    for m in musts:
        ev = _evidence(m, doc_types)
        ev["area"] = m.area
        ev["previous_justification"] = m.priority_rationale
        items.append(ev)
    llm = get_llm(PRIORITISER_MODEL).with_structured_output(LLMPriorityResult)
    try:
        result: LLMPriorityResult = llm.invoke([
            ("system", CALIBRATION_PROMPT.format(n_must=len(musts), n_total=total, share=share,
                                                 scale=_scale_text(), target=target)),
            ("user", "Requirements currently marked Must:\n" + json.dumps(items, ensure_ascii=False, indent=1)),
        ])
    except Exception as exc:  # priorities stay valid, only less calibrated
        print(f"  calibration failed, kept area priorities: {type(exc).__name__}", flush=True)
        return
    by_id = {m.merge_id: m for m in musts}
    downgraded = 0
    for a in result.assignments:
        m = by_id.get(a.requirement_id.strip().upper())
        if m and a.priority in ("Should", "Could"):
            m.priority = a.priority
            m.priority_rationale = a.justification.strip()
            downgraded += 1
    new_share = sum(m.priority == "Must" for m in requirements) / total
    print(f"  downgraded {downgraded}; Must share now {new_share:.0%}", flush=True)


def prioritize_requirements(state: dict) -> dict:
    """LangGraph node: reads `resolved_requirements`, `documents`, optional `priority_feedback`."""
    reqs = prioritize(state["resolved_requirements"], state["documents"], state.get("priority_feedback"))
    return {"resolved_requirements": reqs}


def print_summary(requirements: list[MergedRequirement]) -> None:
    counts = Counter(m.priority for m in requirements)
    total = len(requirements)
    print(f"\n{total} requirements prioritised:")
    for p in PRIORITY_ORDER:
        print(f"  {p:<7}{counts.get(p, 0):>5}  ({100 * counts.get(p, 0) / total:.0f}%)")
    print(f"\n{'Must':>5}{'Should':>7}{'Could':>6}{'Wont':>5}  area")
    areas = list(dict.fromkeys(m.area for m in requirements))
    for area in areas:
        c = Counter(m.priority for m in requirements if m.area == area)
        wont = c["Won't"]
        print(f"{c['Must']:>5}{c['Should']:>7}{c['Could']:>6}{wont:>5}  {area}")
    print("\nExamples of Must:")
    for m in [m for m in requirements if m.priority == "Must"][:6]:
        print(f"  {m.merge_id} {m.name} - {m.priority_rationale}")
    wont = [m for m in requirements if m.priority == "Won't"]
    if wont:
        print("\nWon't:")
        for m in wont:
            print(f"  {m.merge_id} {m.name} - {m.priority_rationale}")
    by_rule = sum(m.priority_rationale.startswith("Assigned by rule") for m in requirements)
    if by_rule:
        print(f"\nAssigned by fallback rule: {by_rule}")


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Assign MoSCoW priorities to resolved requirements.")
    parser.add_argument("input_dir", help="Corpus directory (for document types)")
    parser.add_argument("--resolved", default="output/resolved.json", help="Output of conflict_checker.py")
    parser.add_argument("--out", default="output/prioritized.json")
    args = parser.parse_args()

    docs, _ = load_corpus(args.input_dir)
    data = json.loads(Path(args.resolved).read_text(encoding="utf-8"))
    reqs = [MergedRequirement.model_validate(x) for x in data["requirements"]]

    reqs = prioritize(reqs, docs)
    print_summary(reqs)

    data["requirements"] = [x.model_dump() for x in reqs]
    data["priority_model"] = PRIORITISER_MODEL
    data["priority_scale"] = PRIORITY_SCALE
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
