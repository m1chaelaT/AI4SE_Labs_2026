"""Solve the missing-method tasks with the RAG pipeline and compare unit tests.

For every entry in missing_code.json the pipeline
  1. builds a query from the task (Task 4: task_to_query),
  2. retrieves the top-5 chunks from the vector store (Task 4: Retriever),
  3. sends a prompt with the task, the current stub and the chunks to an LLM,
  4. extracts the method from the answer and writes it into the target file.

Unit tests are run before (no API needed) and after generation, the two
runs are compared, and the token usage of every LLM call is logged.

Usage:
    python solve_tasks.py --baseline         # back up sources + run tests, no API
    python solve_tasks.py --dry-run          # build and save prompts, no API
    python solve_tasks.py [--model gpt-5-mini] [--n 5]   # full run (uses API)
    python solve_tasks.py --reset            # restore the original stub files

The API key is read from the OPENAI_API_KEY environment variable or from a
.env file (OPENAI_API_KEY=...) in this folder or in Solutions/.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
SOLUTIONS = SCRIPT_DIR.parent
WEEK_DIR = SOLUTIONS.parent
REPO = WEEK_DIR / "AI4SE_Playground"
PKG_ROOT = REPO / "playground"                 # contains playground/ and tests/
SRC_DIR = PKG_ROOT / "playground"
TASKS_FILE = WEEK_DIR / "Assignments" / "missing_code.json"
BACKUP_DIR = SCRIPT_DIR / "original_backup"
LOG_DIR = SCRIPT_DIR / "logs"

sys.path.insert(0, str(SOLUTIONS / "Task_4"))
sys.path.insert(0, str(SOLUTIONS / "Task_3"))

DEFAULT_MODEL = "gpt-5-mini"
ALLOWED_MODELS = ["gpt-6-luna", "gpt-5.6-luna", "gpt-5.4-nano", "gpt-5-nano",
                  "gpt-5-mini", "gpt-4.1-nano", "gpt-4o-mini"]

SYSTEM_PROMPT = (
    "You are an expert Python developer working in an existing code base. "
    "You implement exactly one method. Reply with a single ```python code block "
    "that contains only the complete method definition (decorators, signature, "
    "docstring and body). Do not include the class, imports, tests or explanations."
)


# =========================================================================== backup / reset

def backup_sources() -> None:
    if BACKUP_DIR.exists():
        return
    shutil.copytree(SRC_DIR, BACKUP_DIR, ignore=shutil.ignore_patterns("__pycache__"))
    print(f"Backed up original sources to {BACKUP_DIR}")


def restore_sources() -> None:
    if not BACKUP_DIR.exists():
        print("No backup found - nothing to restore.")
        return
    for f in BACKUP_DIR.rglob("*.py"):
        shutil.copy2(f, SRC_DIR / f.relative_to(BACKUP_DIR))
    print(f"Restored original sources from {BACKUP_DIR}")


# =========================================================================== unit tests

_RUNNER = r'''
import json, sys, unittest
class R(unittest.TextTestResult):
    def __init__(s, *a, **k):
        super().__init__(*a, **k); s.outcomes = {}
    def _set(s, t, v): s.outcomes[t.id()] = v
    def addSuccess(s, t): super().addSuccess(t); s._set(t, "ok")
    def addFailure(s, t, e): super().addFailure(t, e); s._set(t, "FAIL")
    def addError(s, t, e): super().addError(t, e); s._set(t, "ERROR")
    def addSkip(s, t, r): super().addSkip(t, r); s._set(t, "skipped")
    def addExpectedFailure(s, t, e): super().addExpectedFailure(t, e); s._set(t, "ok")
    def addUnexpectedSuccess(s, t): super().addUnexpectedSuccess(t); s._set(t, "FAIL")
log = open(sys.argv[1], "w", encoding="utf-8")
suite = unittest.TestLoader().discover("tests", top_level_dir=".")
res = unittest.TextTestRunner(stream=log, verbosity=2, resultclass=R).run(suite)
log.close()
json.dump(res.outcomes, open(sys.argv[2], "w", encoding="utf-8"), indent=1, sort_keys=True)
'''


def run_tests(tag: str) -> Dict[str, str]:
    """Run the repository's unittest suite in a fresh process; save text + JSON log."""
    LOG_DIR.mkdir(exist_ok=True)
    txt, js = LOG_DIR / f"tests_{tag}.txt", LOG_DIR / f"tests_{tag}.json"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    subprocess.run([sys.executable, "-c", _RUNNER, str(txt), str(js)],
                   cwd=PKG_ROOT, env=env, check=False)
    outcomes = json.loads(js.read_text(encoding="utf-8"))
    c = summarise(outcomes)
    print(f"Tests [{tag}]: {c['total']} run, {c['ok']} passed, {c['FAIL']} failed, "
          f"{c['ERROR']} errors  (log: {txt.name})")
    return outcomes


def summarise(outcomes: Dict[str, str]) -> Dict[str, int]:
    c = {"total": len(outcomes), "ok": 0, "FAIL": 0, "ERROR": 0, "skipped": 0}
    for v in outcomes.values():
        c[v] = c.get(v, 0) + 1
    return c


# =========================================================================== source helpers

def find_method(tree: ast.AST, cls: str, method: str) -> Optional[ast.FunctionDef]:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == cls:
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and item.name == method:
                    return item
    return None


def node_start(node) -> int:
    return min([node.lineno] + [d.lineno for d in node.decorator_list])


def stub_source(task: dict) -> Tuple[str, int]:
    """Current source of the stub (with decorators) and its indentation."""
    path = REPO / task["file"]
    src = path.read_text(encoding="utf-8")
    node = find_method(ast.parse(src), task["class"], task["method"])
    if node is None:
        raise LookupError(f"{task['class']}.{task['method']} not found in {task['file']}")
    lines = src.splitlines()
    return textwrap.dedent("\n".join(lines[node_start(node) - 1:node.end_lineno])), node.col_offset


def clean_docstring(task: dict) -> str:
    return task["docstring"].strip().strip('"').strip()


# =========================================================================== prompt

def build_prompt(task: dict, matches) -> str:
    stub, _ = stub_source(task)
    doc = clean_docstring(task)
    parts = [
        "## Task",
        f"Implement the method `{task['method']}` of class `{task['class']}` "
        f"in file `{task['file']}`.",
        f"Description: {doc}",
        "",
        "Current stub in the file:",
        "```python", stub, "```",
        "",
        f"## Relevant code from the repository (top {len(matches)} retrieved chunks)",
    ]
    for m in matches:
        parts += [f"### {m.rank}. {m.id} (similarity {m.score:.3f})",
                  "```python", m.chunk["text"], "```"]
    parts += [
        "",
        "## Requirements",
        "- Keep the exact name, signature and decorators of the stub.",
        f'- Include this docstring: """{doc}"""',
        "- Use only names already imported or defined in the module; do not add imports.",
        "- Follow the conventions visible in the retrieved code (attribute names, "
        "validation, exceptions).",
        "- Return only the method in one ```python block.",
    ]
    return "\n".join(parts)


# =========================================================================== LLM

def load_api_key() -> str:
    if os.environ.get("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    for env in (SCRIPT_DIR / ".env", SOLUTIONS / ".env", WEEK_DIR / ".env"):
        if env.exists():
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("OPENAI_API_KEY not found (set the variable or create a .env file).")


class LLM:
    def __init__(self, model: str, reasoning_effort: Optional[str] = None):
        from openai import OpenAI
        self.client = OpenAI(api_key=load_api_key())
        self.model = model
        self.reasoning_effort = reasoning_effort

    def ask(self, prompt: str) -> Tuple[str, dict]:
        kwargs = {}
        if self.reasoning_effort:
            kwargs["reasoning_effort"] = self.reasoning_effort
        t0 = time.time()
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": prompt}],
            **kwargs,
        )
        u = resp.usage
        details = getattr(u, "completion_tokens_details", None)
        usage = {
            "prompt_tokens": u.prompt_tokens,
            "completion_tokens": u.completion_tokens,
            "reasoning_tokens": getattr(details, "reasoning_tokens", 0) or 0,
            "total_tokens": u.total_tokens,
            "seconds": round(time.time() - t0, 2),
        }
        return resp.choices[0].message.content or "", usage


# =========================================================================== code extraction + writing

_FENCE = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)


def extract_method(reply: str, method: str) -> str:
    """Return the source of ``def method`` from the reply, dedented to column 0."""
    candidates = _FENCE.findall(reply) or [reply]
    for block in candidates:
        code = textwrap.dedent(block).strip("\n")
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == method:
                lines = code.splitlines()
                return textwrap.dedent("\n".join(lines[node_start(node) - 1:node.end_lineno]))
    raise ValueError(f"no valid definition of {method!r} found in the reply")


def ensure_docstring_and_decorators(code: str, task: dict, stub: str) -> str:
    tree = ast.parse(code)
    node = tree.body[0]
    lines = code.splitlines()
    # keep the stub's decorators (e.g. @property) if the model dropped them
    stub_node = ast.parse(stub).body[0]
    stub_decos = stub.splitlines()[:stub_node.lineno - node_start(stub_node)]
    if stub_decos and not node.decorator_list:
        lines = stub_decos + lines
        node = ast.parse("\n".join(lines)).body[0]
    # make sure the docstring from missing_code.json is present
    if ast.get_docstring(node) is None and node.body[0].lineno > node.lineno:
        body_line = node.body[0].lineno - 1
        indent = re.match(r"\s*", lines[body_line]).group(0)
        lines.insert(body_line, f'{indent}"""{clean_docstring(task)}"""')
    return "\n".join(lines)


def write_method(task: dict, code: str) -> None:
    """Replace the stub of task's method in its file with ``code``."""
    path = REPO / task["file"]
    src = path.read_text(encoding="utf-8")
    node = find_method(ast.parse(src), task["class"], task["method"])
    lines = src.splitlines()
    pad = " " * node.col_offset
    new = [pad + l if l.strip() else "" for l in code.splitlines()]
    updated = lines[:node_start(node) - 1] + new + lines[node.end_lineno:]
    text = "\n".join(updated) + "\n"
    ast.parse(text)                                   # never write a broken file
    path.write_text(text, encoding="utf-8")


# =========================================================================== pipeline

def solve(task: dict, retriever, llm: Optional[LLM], n: int, retries: int = 1) -> dict:
    """Solve one textual task: retrieve top-n chunks, prompt the LLM, write the code."""
    from retrieve import task_to_query
    matches = retriever.search(task_to_query(task), n)
    prompt = build_prompt(task, matches)
    stub, _ = stub_source(task)
    record = {"task": f"{task['class']}.{task['method']}", "file": task["file"],
              "chunks": [(round(m.score, 3), m.id) for m in matches],
              "prompt_chars": len(prompt), "calls": [], "status": "dry-run"}
    name = f"{task['class']}.{task['method']}"
    (LOG_DIR / "prompts").mkdir(parents=True, exist_ok=True)
    (LOG_DIR / "prompts" / f"{name}.md").write_text(prompt, encoding="utf-8")
    if llm is None:
        return record

    current = prompt
    for attempt in range(retries + 1):
        reply, usage = llm.ask(current)
        record["calls"].append(usage)
        (LOG_DIR / "responses").mkdir(parents=True, exist_ok=True)
        (LOG_DIR / "responses" / f"{name}_{attempt + 1}.md").write_text(reply, encoding="utf-8")
        try:
            code = ensure_docstring_and_decorators(extract_method(reply, task["method"]), task, stub)
            write_method(task, code)
            record.update(status="written", code=code, attempts=attempt + 1)
            break
        except (ValueError, SyntaxError) as exc:
            record.update(status="failed", error=str(exc), attempts=attempt + 1)
            current = (prompt + f"\n\nYour previous answer could not be used ({exc}). "
                       "Return only the method in one ```python block.")
    return record


def token_totals(records: List[dict]) -> dict:
    keys = ["prompt_tokens", "completion_tokens", "reasoning_tokens", "total_tokens"]
    tot = {k: 0 for k in keys}
    tot["calls"] = 0
    for r in records:
        for c in r["calls"]:
            tot["calls"] += 1
            for k in keys:
                tot[k] += c.get(k, 0)
    return tot


def compare(before: Dict[str, str], after: Dict[str, str]) -> dict:
    fixed = sorted(t for t, v in after.items() if v == "ok" and before.get(t) != "ok")
    broken = sorted(t for t, v in after.items() if v != "ok" and before.get(t) == "ok")
    still = sorted(t for t, v in after.items() if v != "ok" and before.get(t) != "ok")
    return {"before": summarise(before), "after": summarise(after),
            "fixed": fixed, "newly_failing": broken, "still_failing": still}


def write_summary(meta: dict, records: List[dict], cmp: dict, tokens: dict) -> Path:
    b, a = cmp["before"], cmp["after"]
    out = [f"# Task 5 run summary ({meta['time']})", "",
           f"Model: `{meta['model']}`, retrieved chunks per task: {meta['n']}, "
           f"vector store: `{meta['store']}`", "",
           "## Unit tests", "",
           "| | run | passed | failed | errors |", "|---|---|---|---|---|",
           f"| before (stubs) | {b['total']} | {b['ok']} | {b['FAIL']} | {b['ERROR']} |",
           f"| after (generated) | {a['total']} | {a['ok']} | {a['FAIL']} | {a['ERROR']} |", "",
           f"Fixed tests: {len(cmp['fixed'])}, newly failing: {len(cmp['newly_failing'])}, "
           f"still failing: {len(cmp['still_failing'])}", ""]
    if cmp["still_failing"]:
        out += ["Still failing:", ""] + [f"- `{t}`" for t in cmp["still_failing"]] + [""]
    if cmp["newly_failing"]:
        out += ["Newly failing:", ""] + [f"- `{t}`" for t in cmp["newly_failing"]] + [""]
    out += ["## Tasks and token usage", "",
            "| Task | Status | Calls | Prompt | Completion | (reasoning) | Total |",
            "|---|---|---|---|---|---|---|"]
    for r in records:
        p = sum(c["prompt_tokens"] for c in r["calls"])
        c_ = sum(c["completion_tokens"] for c in r["calls"])
        rz = sum(c["reasoning_tokens"] for c in r["calls"])
        t = sum(c["total_tokens"] for c in r["calls"])
        out.append(f"| `{r['task']}` | {r['status']} | {len(r['calls'])} | {p} | {c_} | {rz} | {t} |")
    out.append(f"| **total** | | {tokens['calls']} | {tokens['prompt_tokens']} | "
               f"{tokens['completion_tokens']} | {tokens['reasoning_tokens']} | "
               f"**{tokens['total_tokens']}** |")
    path = LOG_DIR / "summary.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default=DEFAULT_MODEL, choices=ALLOWED_MODELS)
    ap.add_argument("--n", type=int, default=5, help="chunks per prompt")
    ap.add_argument("--store", type=Path, default=SOLUTIONS / "Task_3" / "vector_store" / "minilm")
    ap.add_argument("--reasoning-effort", choices=["minimal", "low", "medium", "high"], default=None,
                    help="only for reasoning models (gpt-5 family); lower = fewer tokens")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--baseline", action="store_true", help="back up sources and run tests only")
    mode.add_argument("--dry-run", action="store_true", help="build prompts without calling the API")
    mode.add_argument("--reset", action="store_true", help="restore the original stub files")
    args = ap.parse_args()
    LOG_DIR.mkdir(exist_ok=True)

    if args.reset:
        restore_sources()
        return
    backup_sources()
    if args.baseline:
        run_tests("before")
        return

    from retrieve import Retriever
    tasks = json.loads(TASKS_FILE.read_text(encoding="utf-8"))
    retriever = Retriever.load(args.store)

    if args.dry_run:
        restore_sources()
        recs = [solve(t, retriever, None, args.n) for t in tasks]
        for r in recs:
            print(f"{r['task']}: prompt {r['prompt_chars']} chars (~{r['prompt_chars'] // 4} tokens)")
        print(f"Prompts saved to {LOG_DIR / 'prompts'}")
        return

    llm = LLM(args.model, args.reasoning_effort)
    restore_sources()                                   # every run starts from the stubs
    before = run_tests("before")
    records = []
    for i, t in enumerate(tasks, 1):
        r = solve(t, retriever, llm, args.n)
        used = sum(c["total_tokens"] for c in r["calls"])
        print(f"[{i}/{len(tasks)}] {r['task']}: {r['status']} ({used} tokens)")
        records.append(r)
    after = run_tests("after")

    cmp = compare(before, after)
    tokens = token_totals(records)
    meta = {"time": datetime.now().isoformat(timespec="seconds"), "model": args.model,
            "n": args.n, "store": args.store.name, "reasoning_effort": args.reasoning_effort}
    (LOG_DIR / "results.json").write_text(json.dumps(
        {"meta": meta, "tokens": tokens, "comparison": cmp, "tasks": records}, indent=2),
        encoding="utf-8")
    summary = write_summary(meta, records, cmp, tokens)

    print(f"\nTokens used: {tokens['total_tokens']} total "
          f"({tokens['prompt_tokens']} prompt + {tokens['completion_tokens']} completion, "
          f"of which {tokens['reasoning_tokens']} reasoning) in {tokens['calls']} calls")
    print(f"Tests passed: {cmp['before']['ok']} -> {cmp['after']['ok']} of {cmp['after']['total']}; "
          f"fixed {len(cmp['fixed'])}, newly failing {len(cmp['newly_failing'])}")
    print(f"Summary: {summary}")


if __name__ == "__main__":
    main()
