"""Merger node (agentic, gpt-5.6-luna) - removes semantic duplicates (OS3).

Several hundred candidates are too many for one reliable LLM call, so the node
works in stages:

  1. Taxonomy (LLM):   map the many free-text categories from the extractor to a
                       small set of canonical areas, and agree on a glossary of
                       preferred terms (OS7 - consistent vocabulary).
  2. Area merge (LLM): per area (split into groups of at most MERGE_GROUP_SIZE),
                       merge candidates expressing the same need and write a name,
                       statement and paragraph-long description (OS5). Candidates
                       that are not real requirements are discarded with a reason
                       (OS9). Contradicting candidates are NOT merged, but flagged
                       for the conflict checker.
  3. Coverage repair (code + LLM): every candidate must end up in exactly one
                       merged requirement or in the discarded list (OS8). Missing
                       ones are sent back to the LLM; if still missing, each one
                       becomes its own requirement, so nothing is lost.
  4. Global dedup (LLM): one pass over the names/statements of all merged
                       requirements catches duplicates that landed in different
                       areas or groups.

Source documents, stakeholders, priority signals and evidence quotes are always
computed in code from the candidates, never taken from the LLM (OS4).

Usable as a LangGraph node (`merge_requirements`) or standalone:
    python merger.py Task_1/data/corpus [--candidates output/candidates.json] [--out output/merged.json]
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from config import MAX_CONCURRENCY, MERGE_GROUP_SIZE, MERGER_MODEL, get_llm, raise_if_interrupted
from extractor import quote_in_source
from schemas import (
    CandidateRequirement,
    DiscardedCandidate,
    DocumentChunk,
    Evidence,
    GlossaryTerm,
    LLMAreaMergeResult,
    LLMDedupResult,
    LLMTaxonomy,
    MergedRequirement,
)

MAX_REPAIR_ROUNDS = 2
MAX_DEDUP_PASSES = 3          # global duplicate pass repeats until nothing more is merged
SIMILARITY_THRESHOLD = 0.4    # word-overlap score for the suspected-pair pre-filter
MAX_SUSPECTED_PAIRS = 200
FALLBACK_AREA = "General"

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
TAXONOMY_PROMPT = """You are a senior requirements engineer organising candidate \
requirements extracted from many elicitation documents for one software system.

You receive the free-text categories the extractor used, each with the number of \
candidates and a few example requirement names. Tasks:
1. Define between 8 and 20 canonical functional areas (e.g. 'Circulation reports', \
'Query tool', 'Security and access control', 'Performance'). Areas must not overlap; \
prefer areas with at most ~60 candidates (use the counts) by splitting large topics.
2. Map EVERY input category, copied exactly, to exactly one area.
3. Write a glossary of 10-25 preferred terms that all requirements must use \
consistently (e.g. 'staff user' instead of 'librarian'/'employee'; 'branch' vs \
'library system'), listing synonyms to avoid."""

AREA_MERGE_PROMPT = """You are a senior requirements engineer. You receive candidate \
requirements from ONE functional area, extracted independently from different source \
documents, so many of them describe the same need. Produce a clean, deduplicated list.

Rules:
1. Merge candidates that express the same need, even if worded differently or at a \
different level of detail. When a general and a detailed version of the same need \
exist, merge them and keep all details.
2. Do NOT merge needs that are related but distinct (e.g. two different reports, or a \
report and the tool that schedules it). Keep them as separate requirements.
3. Do NOT merge candidates that contradict each other (e.g. different values for the \
same parameter, or one asks for X and another rejects X). Keep them separate and \
describe the contradiction in 'conflict_note' of each; a later step resolves it.
4. Every candidate ID in the input must appear in exactly one requirement's \
'source_candidate_ids' OR in 'discarded'. Discard only candidates that are not a \
requirement for the system, nonsensical, off-topic or too vague to be useful, and \
explain why. Do not discard a candidate just because it is a duplicate - merge it.
5. 'name': short and descriptive (3-8 words). 'statement': one sentence 'The system \
shall ...'. 'description': one paragraph of 3-6 sentences explaining what is needed, \
who needs it and why, and the key parameters, combining details from all merged \
candidates. Do not invent details.
6. Use the glossary's preferred terms consistently.
7. 'priority_signals': copy the verbatim signals of the merged candidates (no duplicates)."""

DEDUP_PROMPT = """You are a senior requirements engineer doing a final duplicate check \
on a requirements list. Requirements were merged per functional area, so the same \
need may still appear twice in different areas or groups.

Return groups of requirement IDs that describe the SAME need (or where one is fully \
contained in another), with a merged name, statement ('The system shall ...') and a \
one-paragraph description combining their details. Be thorough: requirements with \
almost the same name (e.g. 'Claims Returned Report' and 'Claims-Returned Reporting'), \
or a feature and a step of that same feature described as a separate requirement, are \
duplicates. A list of suspected pairs is given to help you; judge every pair. Rules:
- Only group true duplicates. Related but distinct needs stay separate.
- Never group requirements that contradict each other.
- Each ID may appear in at most one group. Requirements without a duplicate are simply \
not mentioned. If there are no duplicates, return an empty list.
- Use the glossary's preferred terms."""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _glossary_text(glossary: list[GlossaryTerm]) -> str:
    if not glossary:
        return "(none)"
    return "\n".join(
        f"- {g.term}: {g.definition}" + (f" (avoid: {', '.join(g.avoid)})" if g.avoid else "")
        for g in glossary
    )


def _feedback_text(feedback: str | None) -> str:
    return f"\n\nReviewer feedback from a previous pass - take it into account:\n{feedback}" if feedback else ""


def _candidate_view(c: CandidateRequirement) -> dict:
    """Compact representation of a candidate for the LLM (keeps the prompt small)."""
    view = {"id": c.candidate_id, "doc": c.doc_id, "name": c.name, "statement": c.statement,
            "type": c.req_type}
    if c.details:
        view["details"] = c.details
    if c.priority_signals:
        view["priority_signals"] = c.priority_signals
    if c.status != "proposed":
        view["status"] = f"{c.status}: {c.status_note}"
    return view


def _split(items: list, size: int) -> list[list]:
    """Split into roughly equal groups of at most `size` items."""
    if len(items) <= size:
        return [items]
    n_groups = -(-len(items) // size)
    step = -(-len(items) // n_groups)
    return [items[i:i + step] for i in range(0, len(items), step)]


def _unique(values) -> list:
    return list(dict.fromkeys(v for v in values if v))


def reverify_quotes(candidates: list[CandidateRequirement], chunks: list[DocumentChunk]) -> None:
    """Re-check quotes with the current checker (results saved by older versions may differ)."""
    texts = {c.chunk_id: c.text for c in chunks}
    for c in candidates:
        if c.chunk_id in texts:
            c.quote_verified = quote_in_source(c.quote, texts[c.chunk_id])


# ---------------------------------------------------------------------------
# Stage 1: taxonomy and glossary
# ---------------------------------------------------------------------------
def build_taxonomy(candidates: list[CandidateRequirement], feedback: str | None) -> tuple[dict[str, str], list[str], list[GlossaryTerm]]:
    by_category: dict[str, list[CandidateRequirement]] = defaultdict(list)
    for c in candidates:
        by_category[c.category.strip() or FALLBACK_AREA].append(c)
    listing = "\n".join(
        f"- {cat} ({len(items)}): " + "; ".join(i.name for i in items[:3])
        for cat, items in sorted(by_category.items(), key=lambda kv: -len(kv[1]))
    )
    llm = get_llm(MERGER_MODEL).with_structured_output(LLMTaxonomy)
    print(f"Taxonomy with {MERGER_MODEL}: {len(by_category)} raw categories ...", flush=True)
    result: LLMTaxonomy = llm.invoke([
        ("system", TAXONOMY_PROMPT),
        ("user", f"Categories (name (count): example names):\n{listing}{_feedback_text(feedback)}"),
    ])

    areas = _unique(a.name.strip() for a in result.areas)
    area_lookup = {a.lower(): a for a in areas}
    mapping: dict[str, str] = {}
    for m in result.mapping:
        area = area_lookup.get(m.area.strip().lower())
        if area:
            mapping[m.raw_category.strip().lower()] = area
    # Deterministic fallback for categories the LLM forgot or mapped to an unknown area.
    unmapped = [cat for cat in by_category if cat.lower() not in mapping]
    if unmapped:
        print(f"  {len(unmapped)} categories unmapped -> '{FALLBACK_AREA}'", flush=True)
        for cat in unmapped:
            mapping[cat.lower()] = FALLBACK_AREA
        if FALLBACK_AREA not in areas:
            areas.append(FALLBACK_AREA)
    glossary = [GlossaryTerm(**g.model_dump()) for g in result.glossary]
    return mapping, areas, glossary


# ---------------------------------------------------------------------------
# Stage 2 + 3: merge per area, with coverage repair
# ---------------------------------------------------------------------------
def _run_area_merges(jobs: list[tuple[str, list[CandidateRequirement]]], glossary_text: str,
                     feedback: str | None) -> list[tuple[str, list[CandidateRequirement], LLMAreaMergeResult | Exception]]:
    llm = get_llm(MERGER_MODEL).with_structured_output(LLMAreaMergeResult)
    inputs = []
    for area, group in jobs:
        payload = json.dumps([_candidate_view(c) for c in group], ensure_ascii=False, indent=1)
        inputs.append([
            ("system", AREA_MERGE_PROMPT),
            ("user", f"Functional area: {area}\n\nGlossary:\n{glossary_text}{_feedback_text(feedback)}\n\n"
                     f"Candidates ({len(group)}):\n{payload}"),
        ])
    results = raise_if_interrupted(llm.batch(inputs, config={"max_concurrency": MAX_CONCURRENCY}, return_exceptions=True))
    for i, result in enumerate(results):
        if isinstance(result, Exception) or result is None:
            print(f"  retrying merge of '{jobs[i][0]}' ({type(result).__name__})", flush=True)
            try:
                results[i] = llm.invoke(inputs[i])
            except Exception as exc:
                results[i] = exc
    return [(area, group, result) for (area, group), result in zip(jobs, results)]


def _build_merged(area: str, name: str, statement: str, description: str, req_type: str,
                  members: list[CandidateRequirement], extra_signals: list[str], conflict_notes: list[str]) -> MergedRequirement:
    """Create a merged requirement; all tracing data comes from the member candidates."""
    return MergedRequirement(
        merge_id="",
        area=area, name=name.strip(), statement=statement.strip(), description=description.strip(),
        req_type=req_type,
        source_candidate_ids=[c.candidate_id for c in members],
        source_doc_ids=sorted(_unique(c.doc_id for c in members)),
        stakeholders=_unique(s.strip() for c in members for s in c.stakeholders),
        priority_signals=_unique([s.strip() for c in members for s in c.priority_signals] + [s.strip() for s in extra_signals]),
        candidate_statuses=[f"{c.candidate_id}: {c.status}" + (f" - {c.status_note}" if c.status_note else "")
                            for c in members if c.status != "proposed"],
        conflict_notes=_unique(n.strip() for n in conflict_notes),
        evidence=[Evidence(candidate_id=c.candidate_id, doc_id=c.doc_id, quote=c.quote, quote_verified=c.quote_verified)
                  for c in members],
    )


def merge_areas(candidates: list[CandidateRequirement], mapping: dict[str, str], areas: list[str],
                glossary: list[GlossaryTerm], feedback: str | None) -> tuple[list[MergedRequirement], list[DiscardedCandidate]]:
    by_id = {c.candidate_id: c for c in candidates}
    by_area: dict[str, list[CandidateRequirement]] = defaultdict(list)
    for c in candidates:
        by_area[mapping.get((c.category.strip() or FALLBACK_AREA).lower(), FALLBACK_AREA)].append(c)

    jobs = []
    for area in areas:
        group = sorted(by_area.get(area, []), key=lambda c: c.name.lower())  # similar names end up together
        for part in _split(group, MERGE_GROUP_SIZE):
            if part:
                jobs.append((area, part))
    print(f"Merging with {MERGER_MODEL}: {len(candidates)} candidates in {len(jobs)} groups ...", flush=True)

    glossary_text = _glossary_text(glossary)
    merged: list[MergedRequirement] = []
    discarded: list[DiscardedCandidate] = []
    assigned: set[str] = set()

    for round_no in range(MAX_REPAIR_ROUNDS + 1):
        for area, group, result in _run_area_merges(jobs, glossary_text, feedback):
            allowed = {c.candidate_id for c in group}
            if isinstance(result, Exception) or result is None:
                print(f"  merge of '{area}' failed: {type(result).__name__}: {str(result)[:150]}", flush=True)
                continue
            for req in result.requirements:
                # Keep only IDs that belong to this group and are not assigned yet.
                ids = [i for i in _unique(x.strip().upper() for x in req.source_candidate_ids)
                       if i in allowed and i not in assigned]
                if not ids:
                    continue  # nothing real behind it - the LLM invented it or it was already used
                assigned.update(ids)
                merged.append(_build_merged(area, req.name, req.statement, req.description, req.req_type,
                                            [by_id[i] for i in ids], req.priority_signals,
                                            [req.conflict_note] if req.conflict_note else []))
            for d in result.discarded:
                cid = d.candidate_id.strip().upper()
                if cid in allowed and cid not in assigned:
                    assigned.add(cid)
                    c = by_id[cid]
                    discarded.append(DiscardedCandidate(candidate_id=cid, doc_id=c.doc_id, name=c.name,
                                                        statement=c.statement, reason=d.reason,
                                                        explanation=d.explanation))

        # Coverage check (deterministic): which candidates are still unaccounted for?
        missing_by_area: dict[str, list[CandidateRequirement]] = defaultdict(list)
        for area, group in jobs:
            for c in group:
                if c.candidate_id not in assigned:
                    missing_by_area[area].append(c)
        n_missing = sum(len(v) for v in missing_by_area.values())
        if not n_missing:
            break
        if round_no == MAX_REPAIR_ROUNDS:
            # Last resort: never lose a candidate - keep each one as its own requirement.
            print(f"  {n_missing} candidates still unassigned -> kept as separate requirements", flush=True)
            for area, items in missing_by_area.items():
                for c in items:
                    assigned.add(c.candidate_id)
                    merged.append(_build_merged(area, c.name, c.statement, c.details or c.statement,
                                                c.req_type, [c], [], []))
            break
        print(f"  coverage repair round {round_no + 1}: {n_missing} candidates were not accounted for", flush=True)
        jobs = [(area, part) for area, items in missing_by_area.items() for part in _split(items, MERGE_GROUP_SIZE)]

    return merged, discarded


# ---------------------------------------------------------------------------
# Stage 4: global duplicate pass
# ---------------------------------------------------------------------------
def _number(merged: list[MergedRequirement]) -> None:
    for i, m in enumerate(merged, start=1):
        m.merge_id = f"M{i:03d}"


_STOPWORDS = set(
    "the system shall a an and or of to for in on by with be is are from that this as at each all any can "
    "should must will their its it into per via allow allows provide provides support supports staff user users "
    "report reports reporting".split()
)


def _tokens(text: str) -> set[str]:
    """Content words with a crude stemming, for the deterministic similarity pre-filter."""
    result = set()
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if len(word) < 3 or word in _STOPWORDS:
            continue
        for suffix in ("ing", "ed", "es", "s"):
            if word.endswith(suffix) and len(word) - len(suffix) >= 4:
                word = word[: -len(suffix)]
                break
        result.add(word)
    return result


def suspected_pairs(merged: list[MergedRequirement], threshold: float = SIMILARITY_THRESHOLD,
                    limit: int = MAX_SUSPECTED_PAIRS) -> list[tuple[str, str, float]]:
    """Deterministic pre-filter: pairs with high word overlap (Jaccard) in name or statement.

    The LLM judges every pair itself; this list only directs its attention, because
    a single pass over hundreds of requirements tends to miss obvious duplicates.
    """
    names = {m.merge_id: _tokens(m.name) for m in merged}
    full = {m.merge_id: _tokens(f"{m.name} {m.statement}") for m in merged}

    def jaccard(a: set, b: set) -> float:
        return len(a & b) / len(a | b) if a and b else 0.0

    pairs = []
    for i, a in enumerate(merged):
        for b in merged[i + 1:]:
            score = max(jaccard(names[a.merge_id], names[b.merge_id]), jaccard(full[a.merge_id], full[b.merge_id]))
            if score >= threshold:
                pairs.append((a.merge_id, b.merge_id, score))
    pairs.sort(key=lambda p: -p[2])
    return pairs[:limit]


def global_dedup(merged: list[MergedRequirement], areas: list[str], glossary: list[GlossaryTerm],
                 feedback: str | None) -> list[MergedRequirement]:
    """Repeat the duplicate pass until it finds nothing more (at most MAX_DEDUP_PASSES)."""
    for pass_no in range(1, MAX_DEDUP_PASSES + 1):
        merged, n_merged = _dedup_pass(merged, glossary, feedback, pass_no)
        if n_merged == 0:
            break
    return merged


def _dedup_pass(merged: list[MergedRequirement], glossary: list[GlossaryTerm], feedback: str | None,
                pass_no: int) -> tuple[list[MergedRequirement], int]:
    _number(merged)
    listing = "\n".join(f"{m.merge_id} [{m.area}] {m.name}: {m.statement}" for m in merged)
    pairs = suspected_pairs(merged)
    pair_text = "\n".join(f"- {a} / {b}" for a, b, _ in pairs) or "(none)"
    llm = get_llm(MERGER_MODEL).with_structured_output(LLMDedupResult)
    print(f"Global duplicate check {pass_no} with {MERGER_MODEL}: {len(merged)} requirements, "
          f"{len(pairs)} suspected pairs ...", flush=True)
    try:
        result: LLMDedupResult = llm.invoke([
            ("system", DEDUP_PROMPT),
            ("user", f"Glossary:\n{_glossary_text(glossary)}{_feedback_text(feedback)}\n\n"
                     f"Requirements:\n{listing}\n\n"
                     f"Suspected duplicate pairs found by word overlap (judge each one; also look for "
                     f"duplicates not listed here):\n{pair_text}"),
        ])
    except Exception as exc:  # the list is still valid without this pass
        print(f"  global dedup failed, skipped: {type(exc).__name__}: {str(exc)[:150]}", flush=True)
        return merged, 0

    by_id = {m.merge_id: m for m in merged}
    used: set[str] = set()
    replacements: dict[str, MergedRequirement] = {}  # first member ID -> merged requirement
    for g in result.groups:
        ids = [i for i in _unique(x.strip().upper() for x in g.ids) if i in by_id and i not in used]
        if len(ids) < 2:
            continue
        used.update(ids)
        members = [by_id[i] for i in ids]
        area_counts = Counter(m.area for m in members)
        combined = MergedRequirement(
            merge_id=ids[0],
            area=area_counts.most_common(1)[0][0],
            name=g.name.strip(), statement=g.statement.strip(), description=g.description.strip(),
            req_type=g.req_type,
            source_candidate_ids=_unique(c for m in members for c in m.source_candidate_ids),
            source_doc_ids=sorted(_unique(d for m in members for d in m.source_doc_ids)),
            stakeholders=_unique(s for m in members for s in m.stakeholders),
            priority_signals=_unique(s for m in members for s in m.priority_signals),
            candidate_statuses=_unique(s for m in members for s in m.candidate_statuses),
            conflict_notes=_unique(n for m in members for n in m.conflict_notes),
            evidence=[e for m in members for e in m.evidence],
        )
        replacements[ids[0]] = combined
    print(f"  merged {len(used)} requirements into {len(replacements)}", flush=True)

    result_list = []
    for m in merged:
        if m.merge_id in replacements:
            result_list.append(replacements[m.merge_id])
        elif m.merge_id not in used:
            result_list.append(m)
    return result_list, len(used)


# ---------------------------------------------------------------------------
# Node
# ---------------------------------------------------------------------------
def merge_candidates(candidates: list[CandidateRequirement], chunks: list[DocumentChunk] | None = None,
                     feedback: str | None = None) -> tuple[list[MergedRequirement], list[DiscardedCandidate], list[str], list[GlossaryTerm]]:
    if chunks:
        reverify_quotes(candidates, chunks)
    mapping, areas, glossary = build_taxonomy(candidates, feedback)
    merged, discarded = merge_areas(candidates, mapping, areas, glossary, feedback)
    merged = global_dedup(merged, areas, glossary, feedback)

    # Stable order: by area (taxonomy order), then name; then final temporary IDs.
    area_order = {a: i for i, a in enumerate(areas)}
    merged.sort(key=lambda m: (area_order.get(m.area, len(areas)), m.name.lower()))
    _number(merged)
    return merged, discarded, areas, glossary


def merge_requirements(state: dict) -> dict:
    """LangGraph node: reads `candidates`, `chunks` and optional `merge_feedback`."""
    merged, discarded, areas, glossary = merge_candidates(
        state["candidates"], state.get("chunks"), state.get("merge_feedback"),
    )
    return {"merged_requirements": merged, "discarded_candidates": discarded,
            "areas": areas, "glossary": glossary}


def print_summary(candidates, merged, discarded, areas) -> None:
    covered = {c for m in merged for c in m.source_candidate_ids} | {d.candidate_id for d in discarded}
    lost = [c.candidate_id for c in candidates if c.candidate_id not in covered]
    print(f"\n{len(candidates)} candidates -> {len(merged)} merged requirements, {len(discarded)} discarded")
    print(f"Candidates not accounted for: {len(lost)}" + (f" ({', '.join(lost[:10])})" if lost else ""))
    print(f"With possible conflicts flagged: {sum(bool(m.conflict_notes) for m in merged)}")
    print(f"\n{'reqs':>5}  area")
    for area in areas:
        n = sum(m.area == area for m in merged)
        if n:
            print(f"{n:>5}  {area}")
    docs_used = Counter(d for m in merged for d in m.source_doc_ids)
    print("\nRequirements per source document: " + ", ".join(f"{d}:{n}" for d, n in sorted(docs_used.items())))
    if discarded:
        print("\nDiscarded:")
        for d in discarded:
            print(f"  {d.candidate_id} ({d.doc_id}) [{d.reason}] {d.name} - {d.explanation}")


if __name__ == "__main__":
    from loader import load_corpus

    parser = argparse.ArgumentParser(description="Merge extracted candidate requirements.")
    parser.add_argument("input_dir", help="Corpus directory (used to re-check quotes against the source)")
    parser.add_argument("--candidates", default="output/candidates.json", help="Output of extractor.py")
    parser.add_argument("--out", default="output/merged.json")
    parser.add_argument("--dedup-only", action="store_true",
                        help="Only re-run the global duplicate check on an existing --out file")
    args = parser.parse_args()

    data = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
    cands = [CandidateRequirement.model_validate(c) for c in data["candidates"]]
    _, all_chunks = load_corpus(args.input_dir)

    if args.dedup_only:
        prev = json.loads(Path(args.out).read_text(encoding="utf-8"))
        area_list = prev["areas"]
        gloss = [GlossaryTerm.model_validate(g) for g in prev["glossary"]]
        disc = [DiscardedCandidate.model_validate(x) for x in prev["discarded_candidates"]]
        m = global_dedup([MergedRequirement.model_validate(x) for x in prev["merged_requirements"]],
                         area_list, gloss, None)
        order = {a: i for i, a in enumerate(area_list)}
        m.sort(key=lambda r: (order.get(r.area, len(area_list)), r.name.lower()))
        _number(m)
    else:
        m, disc, area_list, gloss = merge_candidates(cands, all_chunks)
    print_summary(cands, m, disc, area_list)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "model": MERGER_MODEL,
        "areas": area_list,
        "glossary": [g.model_dump() for g in gloss],
        "merged_requirements": [x.model_dump() for x in m],
        "discarded_candidates": [x.model_dump() for x in disc],
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWritten to {out}")
