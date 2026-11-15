"""Split a Python repository into structure-aware chunks for RAG.

Python files are parsed with the ``ast`` module and split along their
natural units: a module header (docstring, imports, module-level
statements), one header chunk per class, and one chunk per function or
method (test methods included). Every chunk carries a short context
prefix with its file path and enclosing class. Chunks longer than
MAX_LINES are split into overlapping windows. Other text files are split
into overlapping line windows.

Usage:
    python chunk_repo.py [--repo PATH] [--out PATH]
                         [--max-lines N] [--overlap N]
"""

from __future__ import annotations

import argparse
import ast
import json
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, List, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO = SCRIPT_DIR.parent.parent / "AI4SE_Playground"
DEFAULT_OUT = SCRIPT_DIR / "chunks.jsonl"

MAX_LINES = 60
OVERLAP = 10
TEXT_SUFFIXES = {".md", ".txt", ".rst", ".toml", ".cfg", ".ini", ".yaml", ".yml", ".json"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", ".mypy_cache"}


@dataclass
class Chunk:
    id: str
    file: str
    kind: str                      # module | class | method | function | test | text
    name: str
    cls: Optional[str]
    start_line: int
    end_line: int
    is_stub: bool
    signature: str
    docstring: str
    code: str                      # raw source of the unit
    text: str                      # context prefix + code (what gets embedded/prompted)
    part: Optional[str] = None     # "1/2" etc. when a long unit was split
    extra: dict = field(default_factory=dict)


# --------------------------------------------------------------------------- helpers

def is_abstract(node: ast.AST) -> bool:
    """True if a function is decorated with ``@abstractmethod``."""
    for d in getattr(node, "decorator_list", []):
        name = d.attr if isinstance(d, ast.Attribute) else getattr(d, "id", "")
        if name == "abstractmethod":
            return True
    return False


def is_stub(node: ast.AST) -> bool:
    """True if a function body has no real implementation.

    Abstract methods are intentionally empty, so they are not stubs.
    """
    if is_abstract(node):
        return False
    body = list(node.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(getattr(body[0], "value", None), ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]                                   # skip docstring
    if not body:
        return True
    if len(body) != 1:
        return False
    stmt = body[0]
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant) and stmt.value.value is Ellipsis:
        return True
    if isinstance(stmt, ast.Raise) and stmt.exc is not None:
        exc = stmt.exc.func if isinstance(stmt.exc, ast.Call) else stmt.exc
        return isinstance(exc, ast.Name) and exc.id == "NotImplementedError"
    return False


def node_start(node: ast.AST) -> int:
    """First line of a definition, including its decorators."""
    decos = getattr(node, "decorator_list", [])
    return min([node.lineno] + [d.lineno for d in decos])


def signature_of(node: ast.AST, lines: List[str]) -> str:
    """Source text of the ``def``/``class`` header (may span several lines)."""
    first = node.lineno - 1
    body_first = node.body[0].lineno - 1 if node.body else first
    header = lines[first:max(body_first, first + 1)]
    text = "\n".join(l.strip() for l in header)
    # cut at the colon that ends the header
    depth, cut = 0, len(text)
    for i, ch in enumerate(text):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == ":" and depth == 0:
            cut = i + 1
            break
    return " ".join(text[:cut].split())


def prefix(file: str, cls: Optional[str], kind: str) -> str:
    out = f"# file: {file}\n"
    if cls:
        out += f"# class: {cls}\n"
    out += f"# kind: {kind}\n"
    return out


def windows(start: int, end: int, size: int, overlap: int) -> Iterable[tuple]:
    """Yield (start, end) 1-based inclusive line windows."""
    if end - start + 1 <= size:
        yield start, end
        return
    step = max(1, size - overlap)
    s = start
    while True:
        e = min(s + size - 1, end)
        yield s, e
        if e >= end:
            break
        s += step


# --------------------------------------------------------------------------- chunkers

class PythonChunker:
    def __init__(self, rel: str, source: str, max_lines: int, overlap: int):
        self.rel = rel
        self.source = source
        self.lines = source.splitlines()
        self.max_lines = max_lines
        self.overlap = overlap
        self.is_test_file = Path(rel).name.startswith("test_") or "/tests/" in f"/{rel}"
        self.chunks: List[Chunk] = []

    # emit one logical unit, splitting it when it is too long
    def emit(self, kind, name, cls, start, end, stub, sig, doc, header_text=None):
        base_id = f"{self.rel}::{cls + '.' if cls else ''}{name}"
        code_full = header_text if header_text is not None else "\n".join(self.lines[start - 1:end])
        code_lines = code_full.splitlines()
        parts = list(windows(1, max(1, len(code_lines)), self.max_lines, self.overlap))
        for i, (s, e) in enumerate(parts, 1):
            code = "\n".join(code_lines[s - 1:e])
            part = f"{i}/{len(parts)}" if len(parts) > 1 else None
            cid = base_id + (f"#part{i}" if part else "")
            self.chunks.append(Chunk(
                id=cid, file=self.rel, kind=kind, name=name, cls=cls,
                start_line=start + s - 1 if header_text is None else start,
                end_line=start + e - 1 if header_text is None else end,
                is_stub=stub, signature=sig, docstring=doc, code=code,
                text=prefix(self.rel, cls, kind) + code, part=part,
            ))

    def func_kind(self, node, cls) -> str:
        if self.is_test_file and node.name.startswith("test"):
            return "test"
        return "method" if cls else "function"

    def run(self) -> List[Chunk]:
        tree = ast.parse(self.source)
        top_defs = [n for n in tree.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))]

        # 1) module header: everything that is not a top-level def/class
        covered = set()
        for n in top_defs:
            covered.update(range(node_start(n), n.end_lineno + 1))
        header_lines = [l for i, l in enumerate(self.lines, 1) if i not in covered]
        header = "\n".join(header_lines).strip("\n")
        if header.strip():
            self.emit("module", Path(self.rel).stem, None, 1, len(self.lines), False, "",
                      ast.get_docstring(tree) or "", header_text=header)

        # 2) top-level definitions
        for n in top_defs:
            if isinstance(n, ast.ClassDef):
                self.class_chunks(n)
            else:
                self.emit(self.func_kind(n, None), n.name, None, node_start(n), n.end_lineno,
                          is_stub(n), signature_of(n, self.lines), ast.get_docstring(n) or "")
        return self.chunks

    def class_chunks(self, cls: ast.ClassDef):
        methods = [n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        # class header = class source with method bodies removed, plus a method index
        method_lines = set()
        for m in methods:
            method_lines.update(range(node_start(m), m.end_lineno + 1))
        start = node_start(cls)
        body = [self.lines[i - 1] for i in range(start, cls.end_lineno + 1) if i not in method_lines]
        while body and not body[-1].strip():
            body.pop()
        indent = " " * (cls.col_offset + 4)
        if methods:
            body.append(f"{indent}# methods:")
            for m in methods:
                body.append(f"{indent}#   {signature_of(m, self.lines)}")
        self.emit("class", cls.name, None, start, cls.end_lineno, False,
                  signature_of(cls, self.lines), ast.get_docstring(cls) or "",
                  header_text="\n".join(body))
        for m in methods:
            self.emit(self.func_kind(m, cls.name), m.name, cls.name, node_start(m), m.end_lineno,
                      is_stub(m), signature_of(m, self.lines), ast.get_docstring(m) or "")


def text_chunks(rel: str, source: str, max_lines: int, overlap: int) -> List[Chunk]:
    lines = source.splitlines()
    parts = list(windows(1, max(1, len(lines)), max_lines, overlap))
    out = []
    for i, (s, e) in enumerate(parts, 1):
        code = "\n".join(lines[s - 1:e])
        if not code.strip():
            continue
        part = f"{i}/{len(parts)}" if len(parts) > 1 else None
        out.append(Chunk(id=f"{rel}#lines{s}-{e}", file=rel, kind="text", name=Path(rel).name,
                         cls=None, start_line=s, end_line=e, is_stub=False, signature="",
                         docstring="", code=code, text=prefix(rel, None, "text") + code, part=part))
    return out


# --------------------------------------------------------------------------- driver

def iter_files(repo: Path) -> Iterable[Path]:
    for p in sorted(repo.rglob("*")):
        if not p.is_file() or any(part in SKIP_DIRS for part in p.relative_to(repo).parts):
            continue
        if p.name.startswith("."):
            continue
        if p.suffix == ".py" or p.suffix.lower() in TEXT_SUFFIXES:
            yield p


def chunk_repository(repo: Path, max_lines: int = MAX_LINES, overlap: int = OVERLAP) -> List[Chunk]:
    chunks: List[Chunk] = []
    for path in iter_files(repo):
        rel = path.relative_to(repo).as_posix()
        source = path.read_text(encoding="utf-8")
        if not source.strip():
            continue
        if path.suffix == ".py":
            try:
                chunks.extend(PythonChunker(rel, source, max_lines, overlap).run())
                continue
            except SyntaxError as exc:
                print(f"[warn] {rel}: {exc}; falling back to line windows")
        chunks.extend(text_chunks(rel, source, max_lines, overlap))

    # guarantee unique ids (e.g. property getter + setter share a name)
    seen = Counter()
    for c in chunks:
        seen[c.id] += 1
        if seen[c.id] > 1:
            c.id = f"{c.id}~{seen[c.id]}"
    return chunks


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", type=Path, default=DEFAULT_REPO, help="repository root to chunk")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output .jsonl file")
    ap.add_argument("--max-lines", type=int, default=MAX_LINES)
    ap.add_argument("--overlap", type=int, default=OVERLAP)
    args = ap.parse_args()

    chunks = chunk_repository(args.repo.resolve(), args.max_lines, args.overlap)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")

    kinds = Counter(c.kind for c in chunks)
    sizes = sorted(c.code.count("\n") + 1 for c in chunks)
    print(f"Wrote {len(chunks)} chunks to {args.out}")
    print("By kind:", dict(sorted(kinds.items())))
    print(f"Lines per chunk: min {sizes[0]}, median {sizes[len(sizes)//2]}, max {sizes[-1]}")
    print("Split (multi-part) chunks:", sum(1 for c in chunks if c.part))
    print("Stub chunks:", [c.id for c in chunks if c.is_stub])


if __name__ == "__main__":
    main()
