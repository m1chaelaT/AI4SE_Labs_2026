"""Central configuration: model choices per node and a shared LLM factory.

Keeping model names here makes the use of several different models (ANS4)
visible in one place and easy to change.
"""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

# Model per agentic node. The extractor runs once per chunk (many calls), so it
# uses a cheap, fast model; nodes reasoning over the whole corpus will use
# stronger ones.
EXTRACTOR_MODEL = "gpt-5-mini"
# The merger must judge semantic similarity across many candidates, so it uses
# a stronger model.
MERGER_MODEL = "gpt-5.6-luna"
# Detecting and resolving contradictions needs reasoning over the whole list
# and the source context, so the conflict checker uses the strongest model.
CONFLICT_MODEL = "gpt-6-luna"
# Prioritisation is a per-requirement judgement over prepared evidence, done per
# area in parallel; the mid-sized model is a good balance of quality and cost.
PRIORITISER_MODEL = "gpt-5.6-luna"
# The reviewer judges the whole specification against the output spec, so it
# uses the strongest model; the reviser applies its focused instructions.
REVIEWER_MODEL = "gpt-6-luna"
REVISER_MODEL = "gpt-5.6-luna"
MAX_REVIEW_ROUNDS = int(os.getenv("MAX_REVIEW_ROUNDS", "4"))

# Maximum number of candidates sent to the merger LLM in one call. Larger
# areas are split; duplicates across the splits are caught by the global pass.
MERGE_GROUP_SIZE = int(os.getenv("MERGE_GROUP_SIZE", "60"))

# How many extraction calls run in parallel.
MAX_CONCURRENCY = int(os.getenv("MAX_CONCURRENCY", "5"))


def get_llm(model: str, **kwargs):
    """Return a ChatOpenAI client configured from .env (key and optional base URL)."""
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL") or None,
        timeout=180,
        max_retries=3,
        **kwargs,
    )


def raise_if_interrupted(results: list) -> list:
    """`batch(return_exceptions=True)` also captures Ctrl+C (KeyboardInterrupt); re-raise it
    so that the pipeline stops cleanly instead of treating it as a failed LLM call."""
    for r in results:
        if isinstance(r, BaseException) and not isinstance(r, Exception):
            raise r
    return results
