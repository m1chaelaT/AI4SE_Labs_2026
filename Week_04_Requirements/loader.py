"""Deterministic loader node (ANS2 - no AI).

Reads every supported text file under an input directory (recursively),
assigns each one a stable document ID (D01, D02, ...) used for tracing (OS4),
extracts light metadata, and splits long documents into overlapping chunks so
that later LLM extraction calls stay within a comfortable context size.

Usable as a LangGraph node (`load_documents`) or standalone:
    python loader.py Task_1/data/corpus
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from schemas import DocumentChunk, SourceDocument

SUPPORTED_EXTENSIONS = {".txt", ".md", ".eml", ".text"}
MAX_CHUNK_CHARS = 12_000   # ~3k tokens; the largest corpus file (~30k chars) becomes 3 chunks
CHUNK_OVERLAP_CHARS = 800  # overlap so a requirement split at a boundary is not lost (OS8)

_SEPARATOR_LINE = re.compile(r"^[\s=\-_*#~]+$")
_DATE_PATTERNS = [
    re.compile(r"^Date:\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^(?:Interview\s+)?Date:\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^[\w ]*Period:\s*(.+)$", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
]

# Ordered keyword heuristics on file name / content -> coarse document type.
_TYPE_RULES = [
    ("email", lambda name, text: name.endswith(".eml") or re.search(r"^From:.*\n(?:.*\n){0,3}?Subject:", text, re.M)),
    ("meeting", lambda name, text: "meeting" in name or "minutes" in name),
    ("interview", lambda name, text: "interview" in name),
    ("survey", lambda name, text: "survey" in name),
    ("specification", lambda name, text: "srs" in name or "requirements specification" in text[:2000].lower()),
    ("reference", lambda name, text: "reference" in name or "documentation" in name),
]


def _read_text(path: Path) -> str:
    """Read a file as text, tolerating the usual encodings of hand-collected corpora."""
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _normalise(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)       # trailing whitespace
    text = re.sub(r"\n{4,}", "\n\n\n", text)      # collapse long blank runs
    return text.strip()


def _detect_type(rel_path: str, text: str) -> str:
    name = rel_path.lower()
    for doc_type, rule in _TYPE_RULES:
        if rule(name, text):
            return doc_type
    return "other"


def _detect_title(text: str, fallback: str) -> str:
    subject = re.search(r"^Subject:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
    if subject:
        return subject.group(1).strip()
    for line in text.splitlines():
        line = line.strip()
        if line and not _SEPARATOR_LINE.match(line):
            return line[:150]
    return fallback


def _detect_date(text: str) -> str | None:
    header = text[:3000]
    for pattern in _DATE_PATTERNS:
        match = pattern.search(header)
        if match:
            return match.group(1).strip()
    return None


def chunk_text(text: str, max_chars: int = MAX_CHUNK_CHARS, overlap: int = CHUNK_OVERLAP_CHARS) -> list[str]:
    """Split text into chunks of at most `max_chars`, preferring paragraph boundaries."""
    if len(text) <= max_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        if end < len(text):
            # Cut at the last paragraph break (or line break) inside the window.
            cut = text.rfind("\n\n", start + max_chars // 2, end)
            if cut == -1:
                cut = text.rfind("\n", start + max_chars // 2, end)
            if cut != -1:
                end = cut
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
        # Start the overlap on a line boundary for readability.
        newline = text.find("\n", start, end)
        if newline != -1:
            start = newline + 1
    return [c for c in chunks if c]


def load_corpus(input_dir: str | Path) -> tuple[list[SourceDocument], list[DocumentChunk]]:
    """Load all supported files under `input_dir`. Ordering (and so IDs) is deterministic."""
    root = Path(input_dir).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(f"Input directory not found: {root}")

    files = sorted(
        (p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS),
        key=lambda p: p.relative_to(root).as_posix().lower(),
    )
    if not files:
        raise FileNotFoundError(f"No supported files ({', '.join(sorted(SUPPORTED_EXTENSIONS))}) in {root}")

    width = max(2, len(str(len(files))))
    documents: list[SourceDocument] = []
    chunks: list[DocumentChunk] = []
    for number, path in enumerate(files, start=1):
        rel_path = path.relative_to(root).as_posix()
        text = _normalise(_read_text(path))
        if not text:
            continue  # skip empty files
        doc_id = f"D{number:0{width}d}"
        documents.append(SourceDocument(
            doc_id=doc_id,
            path=rel_path,
            doc_type=_detect_type(rel_path, text),
            title=_detect_title(text, fallback=path.stem),
            date=_detect_date(text),
            char_count=len(text),
            text=text,
        ))
        parts = chunk_text(text)
        for index, part in enumerate(parts, start=1):
            chunks.append(DocumentChunk(
                chunk_id=f"{doc_id}#{index}", doc_id=doc_id, index=index, total=len(parts), text=part,
            ))
    return documents, chunks


def load_documents(state: dict) -> dict:
    """LangGraph node: reads `state["input_dir"]`, returns `documents` and `chunks`."""
    documents, chunks = load_corpus(state["input_dir"])
    return {"documents": documents, "chunks": chunks}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python loader.py <input_dir>")
        sys.exit(1)
    docs, doc_chunks = load_corpus(sys.argv[1])
    print(f"Loaded {len(docs)} documents -> {len(doc_chunks)} chunks\n")
    print(f"{'ID':<4} {'type':<14} {'chars':>6} {'chunks':>6}  path / title")
    for d in docs:
        n = sum(1 for c in doc_chunks if c.doc_id == d.doc_id)
        print(f"{d.doc_id:<4} {d.doc_type:<14} {d.char_count:>6} {n:>6}  {d.path}\n{'':<34}{d.title[:70]}  [{d.date or '-'}]")
