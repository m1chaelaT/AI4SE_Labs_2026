"""Match an input task against the vector store and return the n most relevant chunks.

The store from Task 3 holds L2-normalised embeddings, so cosine similarity
is a single matrix-vector product. Before ranking, chunks that cannot help
are masked out (by default the empty stub methods). Top-n selection uses
``np.argpartition`` and only the selected candidates are fully sorted.

Usage:
    python retrieve.py "Return the number of line items." [--n 5] [--store DIR]
    python retrieve.py --eval [--n 5] [--store DIR]   # all tasks in missing_code.json

Other scripts can ``from retrieve import Retriever, task_to_query``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
SOLUTIONS = SCRIPT_DIR.parent
sys.path.insert(0, str(SOLUTIONS / "Task_3"))
from embed_chunks import VectorStore, split_identifiers  # noqa: E402

DEFAULT_STORE = SOLUTIONS / "Task_3" / "vector_store" / "minilm"
DEFAULT_TASKS = SOLUTIONS.parent / "Assignments" / "missing_code.json"


@dataclass
class Match:
    rank: int
    score: float
    chunk: dict

    @property
    def id(self) -> str:
        return self.chunk["id"]


def task_to_query(task: dict) -> str:
    """Build query text for one entry of missing_code.json.

    It mirrors the representation used for chunks in Task 3 (kind, location,
    split identifiers, docstring), so query and chunks live in the same
    'language' before they are embedded.
    """
    doc = task.get("docstring", "").strip().strip('"').strip()
    where = f"{task['class']}.{task['method']}"
    return "\n".join([
        f"method {where} in {task['file']}",
        split_identifiers(f"{task['file']} {task['class']} {task['method']}"),
        doc,
    ])


class Retriever:
    def __init__(self, store: VectorStore):
        self.store = store
        self.matrix = store.embeddings                     # (n_chunks, dim), unit rows
        self._is_stub = np.array([bool(c.get("is_stub")) for c in store.chunks])
        self._kind = np.array([c["kind"] for c in store.chunks])

    @classmethod
    def load(cls, store_dir: Path = DEFAULT_STORE) -> "Retriever":
        return cls(VectorStore.load(store_dir))

    # ------------------------------------------------------------------ core matching
    def top_n(
        self,
        query_vec: np.ndarray,
        n: int = 5,
        *,
        skip_stubs: bool = True,
        kinds: Optional[Iterable[str]] = None,
        exclude_ids: Sequence[str] = (),
        min_score: Optional[float] = None,
    ) -> List[Match]:
        """Return the ``n`` chunks most similar to ``query_vec``.

        skip_stubs   drop methods whose body is only ``pass`` (no useful code)
        kinds        keep only these chunk kinds, e.g. {"method", "class"}
        exclude_ids  chunk ids to leave out
        min_score    drop matches below this cosine similarity
        """
        q = np.asarray(query_vec, dtype=np.float32)
        q = q / (np.linalg.norm(q) or 1.0)
        scores = self.matrix @ q                            # cosine similarity

        mask = np.ones(len(scores), dtype=bool)
        if skip_stubs:
            mask &= ~self._is_stub
        if kinds is not None:
            mask &= np.isin(self._kind, list(kinds))
        if exclude_ids:
            ex = set(exclude_ids)
            mask &= np.array([c["id"] not in ex for c in self.store.chunks])
        scores = np.where(mask, scores, -np.inf)

        k = min(n, int(mask.sum()))
        if k <= 0:
            return []
        idx = np.argpartition(-scores, k - 1)[:k]           # O(N) selection
        idx = idx[np.argsort(-scores[idx])]                 # sort only the k winners
        out = [Match(r + 1, float(scores[i]), self.store.chunks[i]) for r, i in enumerate(idx)]
        if min_score is not None:
            out = [m for m in out if m.score >= min_score]
        return out

    def search(self, text: str, n: int = 5, **kw) -> List[Match]:
        """Embed ``text`` with the store's own model and return top-n matches."""
        return self.top_n(self.store.embed_query(text), n, **kw)


# ---------------------------------------------------------------------- evaluation

def evaluate(retriever: Retriever, tasks: List[dict], n: int) -> List[dict]:
    """For each task: does top-n contain code from the target class / a test of the method?"""
    rows = []
    for t in tasks:
        matches = retriever.search(task_to_query(t), n)
        same_class = [m for m in matches
                      if m.chunk["file"] == t["file"] and m.chunk.get("cls") == t["class"]
                      or (m.chunk["kind"] == "class" and m.chunk["name"] == t["class"])]
        tests = [m for m in matches if m.chunk["kind"] == "test"
                 and t["method"].strip("_").lower() in m.chunk["name"].lower()]
        rows.append({
            "task": f"{t['class']}.{t['method']}",
            "class_hit": bool(same_class),
            "test_hit": bool(tests),
            "kinds": [m.chunk["kind"] for m in matches],
            "matches": [(round(m.score, 3), m.id) for m in matches],
        })
    return rows


def print_matches(matches: List[Match]) -> None:
    for m in matches:
        print(f"  {m.rank}. {m.score:.3f}  [{m.chunk['kind']}]  {m.id}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("query", nargs="?", help="free-text task description")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--store", type=Path, default=DEFAULT_STORE)
    ap.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    ap.add_argument("--eval", action="store_true", help="run on every task in missing_code.json")
    ap.add_argument("--keep-stubs", action="store_true", help="do not filter out empty stubs")
    ap.add_argument("--out", type=Path, default=None, help="write --eval results as JSON")
    args = ap.parse_args()

    retriever = Retriever.load(args.store)
    print(f"Store: {retriever.store.meta['model']} ({len(retriever.store.chunks)} chunks)\n")

    if args.eval:
        tasks = json.loads(args.tasks.read_text(encoding="utf-8"))
        rows = evaluate(retriever, tasks, args.n)
        for r in rows:
            print(f"{r['task']}: class_hit={r['class_hit']} test_hit={r['test_hit']}")
            for score, cid in r["matches"]:
                print(f"    {score:.3f}  {cid}")
        print(f"\nTop-{args.n} contains target-class code: {sum(r['class_hit'] for r in rows)}/{len(rows)}")
        print(f"Top-{args.n} contains a test of the method: {sum(r['test_hit'] for r in rows)}/{len(rows)}")
        out = args.out or SCRIPT_DIR / f"eval_{retriever.store.meta['backend']}.json"
        out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
        print(f"Saved {out}")
    elif args.query:
        print_matches(retriever.search(args.query, args.n, skip_stubs=not args.keep_stubs))
    else:
        ap.error("give a query or --eval")


if __name__ == "__main__":
    main()
