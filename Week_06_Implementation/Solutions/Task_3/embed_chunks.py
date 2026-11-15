"""Turn repository chunks into embeddings and store chunk-embedding pairs.

Two local backends are available, neither needs an API key:

* ``minilm`` - the sentence-transformers model ``all-MiniLM-L6-v2``
  (384-dimensional). Downloaded once, then runs offline on the CPU.
  Requires ``pip install sentence-transformers``.
* ``lsa``    - latent semantic analysis: TF-IDF over identifier-aware
  tokens, reduced by SVD to 256 dimensions. Pure numpy, no download.

The script reads ``chunks.jsonl`` from Task 2, builds an embedding text
for every chunk, embeds it and writes a vector store directory:

    vector_store/<backend>/
        embeddings.npy   float32 matrix (n_chunks x dim), L2-normalised
        chunks.jsonl     the chunks, in the same row order as the matrix
        meta.json        backend, model name, dimension, counts
        lsa_model.npz    (lsa only) vocabulary, idf and SVD projection

Usage:
    python embed_chunks.py [--backend minilm|lsa] [--chunks PATH] [--out DIR]

Other scripts can ``from embed_chunks import VectorStore`` and call
``VectorStore.load(dir)`` and ``store.embed_query(text)``.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_CHUNKS = SCRIPT_DIR.parent / "Task_2" / "chunks.jsonl"
DEFAULT_OUT = SCRIPT_DIR / "vector_store"

MINILM_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LSA_DIM = 256


# --------------------------------------------------------------------------- text representation

_CAMEL = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")
_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+")


def split_identifiers(text: str) -> str:
    """'can_afford InventoryLedger' -> 'can afford inventory ledger'."""
    words = []
    for tok in _WORD.findall(text):
        for part in tok.split("_"):
            if part:
                words.extend(_CAMEL.sub(" ", part).split())
    return " ".join(w.lower() for w in words)


def embedding_text(chunk: dict) -> str:
    """Text that represents a chunk for embedding.

    Natural-language description first (kind, location, split identifiers,
    docstring), then the code itself. Queries in Task 5 are natural
    language plus identifiers, so both halves can match.
    """
    where = f"{chunk['cls']}.{chunk['name']}" if chunk.get("cls") else chunk["name"]
    head = [
        f"{chunk['kind']} {where} in {chunk['file']}",
        split_identifiers(f"{chunk['file']} {chunk.get('cls') or ''} {chunk['name']}"),
    ]
    if chunk.get("signature"):
        head.append(chunk["signature"])
    if chunk.get("docstring"):
        head.append(chunk["docstring"])
    return "\n".join(head) + "\n" + chunk["code"]


def load_chunks(path: Path) -> List[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def l2_normalise(m: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(m, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (m / norms).astype(np.float32)


# --------------------------------------------------------------------------- backends

class MiniLMEmbedder:
    name = "minilm"

    def __init__(self, model_name: str = MINILM_MODEL):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise SystemExit(
                "sentence-transformers is not installed. Run\n"
                "    pip install sentence-transformers\n"
                "or use the dependency-free backend: --backend lsa"
            ) from exc
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, device="cpu")

    def fit(self, texts: List[str]) -> None:
        pass                                    # pre-trained, nothing to fit

    def embed(self, texts: List[str]) -> np.ndarray:
        vecs = self.model.encode(texts, batch_size=32, normalize_embeddings=True,
                                 show_progress_bar=len(texts) > 64, convert_to_numpy=True)
        return vecs.astype(np.float32)

    def save(self, out_dir: Path) -> None:
        pass

    @classmethod
    def load(cls, out_dir: Path, meta: dict) -> "MiniLMEmbedder":
        return cls(meta["model"])


class LSAEmbedder:
    """TF-IDF + truncated SVD, fitted on the repository itself."""

    name = "lsa"

    def __init__(self, dim: int = LSA_DIM):
        self.dim = dim
        self.model_name = f"tfidf-svd-{dim}"
        self.vocab: Dict[str, int] = {}
        self.idf: Optional[np.ndarray] = None
        self.components: Optional[np.ndarray] = None    # (vocab x dim)

    @staticmethod
    def tokens(text: str) -> List[str]:
        return [w for w in split_identifiers(text).split() if len(w) > 1]

    def _tfidf(self, texts: List[str]) -> np.ndarray:
        m = np.zeros((len(texts), len(self.vocab)), dtype=np.float32)
        for i, t in enumerate(texts):
            for tok, n in Counter(self.tokens(t)).items():
                j = self.vocab.get(tok)
                if j is not None:
                    m[i, j] = 1.0 + math.log(n)          # sublinear tf
        return l2_normalise(m * self.idf)

    def fit(self, texts: List[str]) -> None:
        df = Counter()
        for t in texts:
            df.update(set(self.tokens(t)))
        terms = sorted(t for t, c in df.items() if c >= 1)
        self.vocab = {t: i for i, t in enumerate(terms)}
        n = len(texts)
        self.idf = np.array([math.log((1 + n) / (1 + df[t])) + 1 for t in terms], dtype=np.float32)
        x = self._tfidf(texts)
        _, s, vt = np.linalg.svd(x, full_matrices=False)
        k = min(self.dim, len(s))
        self.dim = k
        self.model_name = f"tfidf-svd-{k}"
        self.components = vt[:k].T.astype(np.float32)          # project: x @ components

    def embed(self, texts: List[str]) -> np.ndarray:
        return l2_normalise(self._tfidf(texts) @ self.components)

    def save(self, out_dir: Path) -> None:
        terms = np.array(sorted(self.vocab, key=self.vocab.get))
        np.savez_compressed(out_dir / "lsa_model.npz", terms=terms, idf=self.idf,
                            components=self.components)

    @classmethod
    def load(cls, out_dir: Path, meta: dict) -> "LSAEmbedder":
        data = np.load(out_dir / "lsa_model.npz", allow_pickle=False)
        obj = cls(int(meta["dim"]))
        obj.vocab = {str(t): i for i, t in enumerate(data["terms"])}
        obj.idf = data["idf"]
        obj.components = data["components"]
        return obj


BACKENDS = {"minilm": MiniLMEmbedder, "lsa": LSAEmbedder}


# --------------------------------------------------------------------------- vector store

class VectorStore:
    """Chunk-embedding pairs: row i of ``embeddings`` belongs to ``chunks[i]``."""

    def __init__(self, embedder, embeddings: np.ndarray, chunks: List[dict], meta: dict):
        self.embedder = embedder
        self.embeddings = embeddings
        self.chunks = chunks
        self.meta = meta

    @classmethod
    def build(cls, chunks: List[dict], backend: str) -> "VectorStore":
        embedder = BACKENDS[backend]()
        texts = [embedding_text(c) for c in chunks]
        embedder.fit(texts)
        emb = embedder.embed(texts)
        meta = {
            "backend": backend,
            "model": embedder.model_name,
            "dim": int(emb.shape[1]),
            "n_chunks": len(chunks),
            "normalised": True,
            "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
        return cls(embedder, emb, chunks, meta)

    def save(self, out_dir: Path) -> None:
        out_dir.mkdir(parents=True, exist_ok=True)
        np.save(out_dir / "embeddings.npy", self.embeddings)
        with (out_dir / "chunks.jsonl").open("w", encoding="utf-8") as fh:
            for c in self.chunks:
                fh.write(json.dumps(c, ensure_ascii=False) + "\n")
        (out_dir / "meta.json").write_text(json.dumps(self.meta, indent=2), encoding="utf-8")
        self.embedder.save(out_dir)

    @classmethod
    def load(cls, out_dir: Path) -> "VectorStore":
        out_dir = Path(out_dir)
        meta = json.loads((out_dir / "meta.json").read_text(encoding="utf-8"))
        embedder = BACKENDS[meta["backend"]].load(out_dir, meta)
        emb = np.load(out_dir / "embeddings.npy")
        chunks = load_chunks(out_dir / "chunks.jsonl")
        if len(chunks) != emb.shape[0]:
            raise ValueError("vector store is inconsistent: chunk count != embedding rows")
        return cls(embedder, emb, chunks, meta)

    def embed_query(self, text: str) -> np.ndarray:
        """Embed free text (e.g. a task description) into the store's space."""
        return self.embedder.embed([text])[0]


# --------------------------------------------------------------------------- CLI

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--backend", choices=sorted(BACKENDS), default="minilm")
    ap.add_argument("--chunks", type=Path, default=DEFAULT_CHUNKS, help="chunks.jsonl from Task 2")
    ap.add_argument("--out", type=Path, default=None,
                    help="output directory (default: vector_store/<backend>)")
    args = ap.parse_args()

    chunks = load_chunks(args.chunks)
    store = VectorStore.build(chunks, args.backend)
    out = args.out or (DEFAULT_OUT / args.backend)
    store.save(out)

    print(f"Embedded {len(chunks)} chunks with {store.meta['model']} -> {store.embeddings.shape}")
    print(f"Saved vector store to {out}")

    # quick sanity check: nearest neighbours of one task-like query
    q = "OrderStatus is_terminal: True when the status ends further transitions."
    sims = store.embeddings @ store.embed_query(q)
    print(f"\nTop 5 for query: {q!r}")
    for i in np.argsort(-sims)[:5]:
        print(f"  {sims[i]:.3f}  {store.chunks[i]['id']}")


if __name__ == "__main__":
    main()
