# Relaxed Result F1 – metrika pre text-to-SQL.
# Riadky výsledku porovnáva ako množiny hodnôt, takže nezáleží na tom,
# aké stĺpce a v akom poradí dotaz vrátil. Predikovaný riadok sa zhoduje
# s očakávaným, ak jeden obsahuje všetky hodnoty druhého.
# Pre každú otázku sa počíta F1 (precision/recall nad riadkami), výsledok je priemer.

import csv
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "Task_2" / "data"))
from evaluate_retrieval_predictions import load_database  # noqa: E402

LABELS = ROOT / "Task_2" / "data" / "restaurants_dataset.csv"
PRED_DIR = ROOT / "Task_2" / "predictions"
PROMPTS = ["ICIO", "RTF", "CoT"]


def norm(v):
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip().lower()


def greedy_matches(pred, gold):
    # Párovanie riadkov: predikovaný riadok P a očakávaný G sa zhodujú, ak P ⊆ G alebo G ⊆ P.
    from collections import Counter, defaultdict
    from itertools import combinations
    gold_sets = [frozenset(map(norm, g)) for g in gold]
    left = Counter(gold_sets)
    index = defaultdict(set)
    for gs in left:
        for v in gs:
            index[v].add(gs)
    hits = 0
    for p in pred:
        ps = frozenset(map(norm, p))
        found = None
        # G ⊆ P (aj zhoda): skúšame podmnožiny P od najväčšej
        for k in range(len(ps), 0, -1):
            for sub in combinations(ps, k):
                if left[frozenset(sub)] > 0:
                    found = frozenset(sub)
                    break
            if found:
                break
        # P ⊆ G
        if found is None and ps:
            rare = min(ps, key=lambda v: len(index[v]))
            for gs in index[rare]:
                if left[gs] > 0 and ps <= gs:
                    found = gs
                    break
        if found is not None:
            left[found] -= 1
            hits += 1
    return hits


def f1(pred, gold):
    if not pred and not gold:
        return 1.0
    if not pred or not gold:
        return 0.0
    hits = greedy_matches(pred, gold)
    if hits == 0:
        return 0.0
    p, r = hits / len(pred), hits / len(gold)
    return 2 * p * r / (p + r)


def main():
    csv.field_size_limit(1_000_000_000)
    with LABELS.open(encoding="utf-8", newline="") as f:
        gold = [json.loads(r["result"]) for r in csv.DictReader(f)]

    conn = load_database()
    out_rows = []
    summary = {}
    for prompt in PROMPTS:
        with (PRED_DIR / f"{prompt}.csv").open(encoding="utf-8", newline="") as f:
            preds = list(csv.DictReader(f))
        scores = []
        for g, row in zip(gold, preds):
            try:
                pred = conn.execute(row["predicted_sql"]).fetchall()
            except sqlite3.Error:
                pred = None
            s = 0.0 if pred is None else f1(pred, g)
            scores.append(s)
            out_rows.append([prompt, row["question"], round(s, 4)])
        summary[prompt] = sum(scores) / len(scores)
        print(f"{prompt}: Relaxed Result F1 = {summary[prompt]:.4f}")

    with (Path(__file__).parent / "relaxed_f1_scores.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["prompt", "question", "relaxed_f1"])
        w.writerows(out_rows)


if __name__ == "__main__":
    main()
