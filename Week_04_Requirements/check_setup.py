"""Step 1 sanity check: verifies that dependencies are installed, the API key
is loaded from .env, and that each model planned for the agentic network answers.

Usage:  python check_setup.py
"""
import os
import sys

from dotenv import load_dotenv

# Models planned for the network (at least 3 different ones are required - ANS4).
MODELS = ["gpt-5-mini", "gpt-5.6-luna", "gpt-6-luna"]


def main() -> int:
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    if not api_key or api_key.startswith("sk-..."):
        print("ERROR: OPENAI_API_KEY is missing. Copy .env.example to .env and add your key.")
        return 1

    try:
        import langgraph  # noqa: F401
        from langchain_openai import ChatOpenAI
    except ImportError as exc:
        print(f"ERROR: missing dependency ({exc}). Run: pip install -r requirements.txt")
        return 1
    print("Dependencies OK.")
    print(f"API base URL: {base_url or 'default (api.openai.com)'}")

    failed = []
    for model in MODELS:
        try:
            llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url, timeout=60)
            reply = llm.invoke("Reply with the single word: OK").content.strip()
            print(f"  [OK]   {model}: {reply[:40]}")
        except Exception as exc:  # report every model, don't stop at the first failure
            print(f"  [FAIL] {model}: {type(exc).__name__}: {str(exc)[:200]}")
            failed.append(model)

    if failed:
        print(f"\n{len(failed)} model(s) failed: {', '.join(failed)}")
        return 1
    print("\nSetup complete - all models reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
