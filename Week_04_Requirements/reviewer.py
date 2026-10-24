"""Reviewer and reviser nodes - the feedback loop of the network (ANS3).

    validator (code) --> reviewer (gpt-6-luna) --[actions]--> reviser (gpt-5.6-luna) --+
        ^                        |                                                      |
        |                        +--[approved or max rounds]--> renderer               |
        +-------------------------------------------------------------------------------+

* The validator checks the requirement set against the output specification and
  reports errors and warnings (validator.py).
* The reviewer reads that report plus the whole requirement list. For every
  error it orders a fix; for every warning it either orders a fix or dismisses it
  with a reason; it also looks for problems the code cannot see (duplicates with
  different wording, unclear statements, implausible priorities). Its output is a
  list of concrete actions: merge, rewrite, change_priority, remove.
* Errors the reviewer did not address are turned into rewrite actions by code,
  so a validator error can never be silently ignored.
* The reviser applies only those actions; tracing data of merged requirements is
  combined in code (OS4). Removed requirements go to the blacklist (OS9).
* The loop ends when the validator finds no errors and the reviewer orders no
  more actions, or after MAX_REVIEW_ROUNDS.

Usable as LangGraph nodes (`review_requirements`, `revise_requirements`,
`route_after_review`) or standalone (runs the whole loop):
    python reviewer.py Task_1/data/corpus
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from config import MAX_CONCURRENCY, MAX_REVIEW_ROUNDS, REVIEWER_MODEL, REVISER_MODEL, get_llm, raise_if_interrupted
from prioritizer import PRIORITY_ORDER, PRIORITY_SCALE
from schemas import (
    BlacklistEntry,
    GlossaryTerm,
    LLMReview,
    LLMReviewAction,
    LLMRevision,
    MergedRequirement,
    ReviewRound,
    ValidationReport,
)

MAX_ACTIONS_PER_ROUND = 40
MAX_IDS_PER_MERGE = 4       # a merge of more requirements is almost certainly a mistake
MAX_IDS_PER_ACTION = 5      # rewrite/remove/change_priority on more IDs = blanket action, rejected
AUTO_FIX_CHECKS = {"short-description", "missing-name", "missing-statement", "duplicate-name", "duplicate-statement"}

REVIEW_PROMPT = """You are the quality reviewer of a software requirements specification \
produced by an automated pipeline. The specification must satisfy:
- unique IDs and no semantically duplicate requirements;
- tracing to source documents (handled in code - you do not need to check it);
- each requirement has a short descriptive name (3-8 words), one statement 'The system \
shall ...', and a paragraph-long description (3-6 sentences);
- a MoSCoW priority ({priorities}) that fits the evidence;
- consistent language and vocabulary (use the glossary), no contradictions;
- only genuine requirements for the system.

You receive the validator's issues (numbered I1, I2, ...), full details of the \
requirements named in them, and the list of ALL requirements. To keep it short, that \
list shows only name and statement - every requirement DOES have a description; \
description length and form are checked by the validator, so judge descriptions only \
where details are shown.
1. For every ERROR, order an action that fixes it.
2. For every WARNING, either order an action or dismiss it with a reason (e.g. two \
similar names that are in fact different reports).
3. Look for further problems the validator cannot detect: duplicates worded \
differently, unclear or vague statements, statements that mix several requirements, \
clearly implausible priorities, items that are not system requirements.
Actions: 'merge' (2-4 IDs describing the same need), 'rewrite' (exactly ONE ID; say \
exactly what to change), 'change_priority' (one ID; give new_priority and the reason), \
'remove' (one ID; give the reason; it will be listed in the blacklist). Use \
new_priority 'none' except for change_priority. Never order one action for many \
requirements at once.
The sources are elicitation material: do not demand details they do not contain \
(e.g. numeric targets nobody stated). A genuine stakeholder need that is somewhat \
general is acceptable - at most rewrite it to be clear, never remove it for lacking \
detail. Remove only items that are not about the system at all.
In later rounds you also see what earlier rounds already decided and changed: do not \
reopen those points; raise only significant new problems. Order at most {max_actions} \
actions, most important first. If the specification is in good shape, return no \
actions - that ends the review."""

REVISE_PROMPT = """You are a requirements engineer applying a reviewer's instruction to \
a requirements specification. Apply the instruction precisely and change nothing else.
- For a merge: write one requirement that covers all given requirements without losing \
any detail.
- Base details only on the given texts and evidence quotes; do not invent.
- name: 3-8 words. statement: one sentence starting 'The system shall'. description: \
one paragraph of 3-6 sentences explaining what is needed, who needs it and why, and \
the key parameters.
- Use the preferred glossary terms.
- Write only the requirement itself: never add placeholders such as 'pending evidence' \
or 'to be defined', and never write about the review, the instruction or this task. If \
the instruction asks for a detail the evidence does not contain, leave that detail out.

Glossary:
{glossary}"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _issue_key(check: str, message: str) -> str:
    """Stable key for a warning (IDs change between rounds, names and messages do not)."""
    return f"{check}|{message}"


def _glossary_text(glossary: list[GlossaryTerm]) -> str:
    return "\n".join(f"- {g.term}" + (f" (avoid: {', '.join(g.avoid)})" if g.avoid else "") for g in glossary)


def _ids_in(text: str) -> list[str]:
    return re.findall(r"REQ-\d+", text)


def _requirement_block(m: MergedRequirement, with_evidence: bool = False) -> str:
    block = (f"{m.req_id} [{m.area}] [{m.priority}] {m.name}\n  Statement: {m.statement}\n"
             f"  Description: {m.description}")
    if with_evidence:
        quotes = [f'  - ({e.doc_id}) "{e.quote}"' for e in m.evidence[:6]]
        block += "\n  Evidence:\n" + "\n".join(quotes)
    return block


# ---------------------------------------------------------------------------
# Reviewer node
# ---------------------------------------------------------------------------
def review(final: list[MergedRequirement], report: ValidationReport, dismissed_keys: set[str],
           round_no: int, history: list[ReviewRound] | None = None
           ) -> tuple[LLMReview, list[LLMReviewAction], set[str]]:
    """Return the LLM review, the complete action list (incl. automatic ones) and newly dismissed keys."""
    by_id = {m.req_id: m for m in final}
    open_issues = [i for i in report.issues if i.severity != "info"
                   and not (i.severity == "warning" and _issue_key(i.check, i.message) in dismissed_keys)]
    numbered = {f"I{n}": i for n, i in enumerate(open_issues, start=1)}
    issue_text = "\n".join(f"{iid} [{i.severity}] {i.check} - {i.target}: {i.message}"
                           for iid, i in numbered.items()) or "(none)"
    affected = sorted({rid for i in open_issues for rid in _ids_in(i.target) if rid in by_id})
    details = "\n".join(_requirement_block(by_id[rid]) for rid in affected) or "(none)"
    listing = "\n".join(f"{m.req_id} [{m.area}] [{m.priority}] {m.name}: {m.statement}" for m in final)
    history_text = "\n".join(
        f"Round {h.round}: {h.summary}\n" + "\n".join(f"  - {a[:200]}" for a in h.actions)
        for h in history or []) or "(this is the first round)"

    llm = get_llm(REVIEWER_MODEL).with_structured_output(LLMReview)
    print(f"Review round {round_no} with {REVIEWER_MODEL}: {report.stats['errors']} errors, "
          f"{len(open_issues) - report.stats['errors']} open warnings ...", flush=True)
    result: LLMReview = llm.invoke([
        ("system", REVIEW_PROMPT.format(priorities=", ".join(PRIORITY_ORDER), max_actions=MAX_ACTIONS_PER_ROUND)),
        ("user", f"Earlier review rounds (already decided and applied):\n{history_text}\n\n"
                 f"Validator issues:\n{issue_text}\n\nDetails of the requirements named in the issues:\n{details}"
                 f"\n\nAll requirements (name and statement only):\n{listing}"),
    ])

    # Keep only well-formed actions on existing IDs, each ID touched at most once per round.
    actions: list[LLMReviewAction] = []
    touched: set[str] = set()
    rejected = 0
    for a in result.actions[:MAX_ACTIONS_PER_ROUND]:
        ids = [i for i in dict.fromkeys(x.strip().upper() for x in a.requirement_ids) if i in by_id and i not in touched]
        if not ids or (a.action == "change_priority" and a.new_priority not in PRIORITY_SCALE):
            continue
        if a.action == "merge":
            if not 2 <= len(ids) <= MAX_IDS_PER_MERGE:
                rejected += 1
                continue
            touched.update(ids)
            actions.append(LLMReviewAction(action="merge", requirement_ids=ids, new_priority="none",
                                           instruction=a.instruction))
            continue
        if len(ids) > MAX_IDS_PER_ACTION:   # blanket action over many requirements: never apply
            rejected += 1
            continue
        for rid in ids:                     # rewrite / change_priority / remove work on one ID each
            touched.add(rid)
            actions.append(LLMReviewAction(action=a.action, requirement_ids=[rid], new_priority=a.new_priority,
                                           instruction=a.instruction))
    if rejected:
        print(f"  rejected {rejected} malformed reviewer actions (too many IDs)", flush=True)

    # Deterministic safety net: every fixable error gets an action, even if the reviewer missed it.
    for i in open_issues:
        if i.severity != "error" or i.check not in AUTO_FIX_CHECKS:
            continue
        for rid in _ids_in(i.target)[-1:] if i.check.startswith("duplicate") else _ids_in(i.target):
            if rid in by_id and rid not in touched:
                touched.add(rid)
                instruction = {"short-description": "Expand the description into one paragraph of 3-6 sentences "
                                                    "explaining what is needed, who needs it and why, and the key "
                                                    "parameters, using the evidence."}.get(
                    i.check, f"Fix this problem: {i.message}. Make the requirement distinct and complete.")
                actions.append(LLMReviewAction(action="rewrite", requirement_ids=[rid], new_priority="none",
                                               instruction=instruction))

    new_dismissed = {_issue_key(numbered[d.issue_id.strip().upper()].check, numbered[d.issue_id.strip().upper()].message)
                     for d in result.dismissed if d.issue_id.strip().upper() in numbered
                     and numbered[d.issue_id.strip().upper()].severity == "warning"}
    return result, actions, new_dismissed


def review_requirements(state: dict) -> dict:
    """LangGraph node: reviews `final_requirements` using `validation`; increments `review_round`."""
    round_no = state.get("review_round", 0) + 1
    dismissed = set(state.get("dismissed_warnings") or [])
    report: ValidationReport = state["validation"]
    history = list(state.get("review_history") or [])
    result, actions, new_dismissed = review(state["final_requirements"], report, dismissed, round_no, history)
    history.append(ReviewRound(
        round=round_no, errors=report.stats["errors"], warnings=report.stats["warnings"], summary=result.summary,
        actions=[f"{a.action} {', '.join(a.requirement_ids)}: {a.instruction}" for a in actions],
        dismissed=len(new_dismissed)))
    print(f"  reviewer: {len(actions)} actions, {len(new_dismissed)} warnings dismissed", flush=True)
    return {"review_round": round_no, "review_actions": actions, "review_history": history,
            "dismissed_warnings": sorted(dismissed | new_dismissed)}


def route_after_review(state: dict) -> str:
    """Conditional edge: loop back to the reviser, or finish."""
    if state.get("review_actions") and state.get("review_round", 0) < MAX_REVIEW_ROUNDS:
        return "revise"
    if state.get("review_actions"):
        print(f"  max review rounds ({MAX_REVIEW_ROUNDS}) reached - {len(state['review_actions'])} actions left open",
              flush=True)
    return "finish"


# ---------------------------------------------------------------------------
# Reviser node
# ---------------------------------------------------------------------------
def _highest_priority(members: list[MergedRequirement]) -> MergedRequirement:
    order = {p: i for i, p in enumerate(PRIORITY_ORDER)}
    return min(members, key=lambda m: order.get(m.priority or "", len(order)))


def revise(final: list[MergedRequirement], actions: list[LLMReviewAction], glossary: list[GlossaryTerm]
           ) -> tuple[list[MergedRequirement], list[BlacklistEntry]]:
    by_id = {m.req_id: m for m in final}
    removed: set[str] = set()   # merge_ids that disappear
    blacklist: list[BlacklistEntry] = []

    # Deterministic actions first.
    for a in actions:
        if a.action == "change_priority":
            m = by_id[a.requirement_ids[0]]
            m.priority = a.new_priority
            m.priority_rationale = f"Changed by review: {a.instruction}"
        elif a.action == "remove":
            for rid in a.requirement_ids:
                m = by_id[rid]
                removed.add(m.merge_id)
                blacklist.append(BlacklistEntry(source_id=m.merge_id, name=m.name, statement=m.statement,
                                                source_doc_ids=m.source_doc_ids, category="removed in review",
                                                explanation=a.instruction,
                                                source_candidate_ids=m.source_candidate_ids))

    # LLM actions (rewrite, merge) in parallel.
    llm_actions = [a for a in actions if a.action in ("rewrite", "merge")]
    if llm_actions:
        llm = get_llm(REVISER_MODEL).with_structured_output(LLMRevision)
        system = REVISE_PROMPT.format(glossary=_glossary_text(glossary))
        inputs = [[("system", system), ("user", f"Action: {a.action}\nInstruction: {a.instruction}\n\n"
                   + "\n\n".join(_requirement_block(by_id[rid], with_evidence=True) for rid in a.requirement_ids))]
                  for a in llm_actions]
        print(f"Revising with {REVISER_MODEL}: {len(llm_actions)} actions ...", flush=True)
        results = raise_if_interrupted(llm.batch(inputs, config={"max_concurrency": MAX_CONCURRENCY}, return_exceptions=True))
        for a, r in zip(llm_actions, results):
            if isinstance(r, Exception) or r is None:
                print(f"  {a.action} {', '.join(a.requirement_ids)} failed: {type(r).__name__}", flush=True)
                continue  # the next validation/review round will see the problem again
            members = [by_id[rid] for rid in a.requirement_ids]
            original_names = [m.name for m in members]
            target = members[0]
            target.name, target.statement = r.name.strip(), r.statement.strip()
            target.description, target.req_type = r.description.strip(), r.req_type
            if a.action == "merge":
                # Tracing and evidence are combined in code (OS4); the highest priority wins.
                top = _highest_priority(members)
                target.priority, target.priority_rationale = top.priority, top.priority_rationale
                for other in members[1:]:
                    removed.add(other.merge_id)
                    for field in ("source_candidate_ids", "stakeholders", "priority_signals",
                                  "candidate_statuses", "resolution_notes"):
                        setattr(target, field, list(dict.fromkeys(getattr(target, field) + getattr(other, field))))
                    target.source_doc_ids = sorted(set(target.source_doc_ids) | set(other.source_doc_ids))
                    target.evidence = target.evidence + other.evidence
                target.resolution_notes.append(f"Merged in review from: {', '.join(original_names)}.")

    return [m for m in final if m.merge_id not in removed], blacklist


def revise_requirements(state: dict) -> dict:
    """LangGraph node: applies `review_actions`; the result goes back to the validator."""
    reqs, blacklist = revise(state["final_requirements"], state["review_actions"], state["glossary"])
    return {"resolved_requirements": reqs,
            "reviewer_blacklist": list(state.get("reviewer_blacklist") or []) + blacklist}


# ---------------------------------------------------------------------------
# Standalone: run the whole loop (validator -> reviewer -> reviser -> ...)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from loader import load_corpus
    from schemas import (BlacklistEntry as BE, CandidateRequirement, DiscardedCandidate, IgnoredStatement)
    from validator import print_report, validate_requirements

    parser = argparse.ArgumentParser(description="Run the validate -> review -> revise feedback loop.")
    parser.add_argument("input_dir")
    parser.add_argument("--prioritized", default="output/prioritized.json")
    parser.add_argument("--merged", default="output/merged.json")
    parser.add_argument("--candidates", default="output/candidates.json")
    parser.add_argument("--out", default="output/reviewed.json")
    args = parser.parse_args()

    docs, chunks = load_corpus(args.input_dir)
    data = json.loads(Path(args.prioritized).read_text(encoding="utf-8"))
    merged_data = json.loads(Path(args.merged).read_text(encoding="utf-8"))
    cand_data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    state = {
        "documents": docs,
        "areas": data["areas"],
        "glossary": [GlossaryTerm.model_validate(g) for g in data["glossary"]],
        "candidates": [CandidateRequirement.model_validate(c) for c in cand_data["candidates"]],
        "ignored_statements": [IgnoredStatement.model_validate(i) for i in cand_data["ignored"]],
        "merged_requirements": [MergedRequirement.model_validate(x) for x in merged_data["merged_requirements"]],
        "discarded_candidates": [DiscardedCandidate.model_validate(x) for x in data["discarded_candidates"]],
        "conflict_blacklist": [BE.model_validate(x) for x in data["conflict_blacklist"]],
        "resolved_requirements": [MergedRequirement.model_validate(x) for x in data["requirements"]],
    }
    while True:
        state.update(validate_requirements(state))
        print_report(state["validation"]) if state.get("review_round", 0) == 0 else print(
            f"Validation: {state['validation'].stats['errors']} errors, {state['validation'].stats['warnings']} warnings, "
            f"{state['validation'].stats['requirements']} requirements")
        print()
        state.update(review_requirements(state))
        if route_after_review(state) == "finish":
            break
        state.update(revise_requirements(state))

    print("\nFeedback loop history:")
    for h in state["review_history"]:
        print(f"  round {h.round}: {h.errors} errors, {h.warnings} warnings -> {len(h.actions)} actions, "
              f"{h.dismissed} warnings dismissed")
        print(f"    {h.summary}")
    final_report: ValidationReport = state["validation"]
    print(f"\nFinal: {final_report.stats['requirements']} requirements, {final_report.stats['errors']} errors, "
          f"{len(state.get('reviewer_blacklist') or [])} removed in review")

    data["requirements"] = [x.model_dump() for x in state["final_requirements"]]
    data["validation"] = final_report.model_dump()
    data["reviewer_blacklist"] = [x.model_dump() for x in state.get("reviewer_blacklist") or []]
    data["review_history"] = [x.model_dump() for x in state["review_history"]]
    data["review_models"] = {"reviewer": REVIEWER_MODEL, "reviser": REVISER_MODEL}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
