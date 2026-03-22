#!/usr/bin/env python3
"""
Smoke-test retrieval artifacts using the same functions as the FastAPI backend.

Read-only with respect to retrieval logic; delegates to app.services.retriever.
Run from repo root:  python backend/test_retriever.py
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Ensure `app` package resolves when executing this file directly
_BACKEND_DIR = Path(__file__).resolve().parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.services import retriever

ANSWER_TRUNCATE = 200

SAMPLE_PYTHON_QUESTIONS = [
    "How do I read a text file in Python?",
    "What is a list comprehension and how do I use it?",
    "How do I install third-party packages with pip?",
    "What is the difference between == and is in Python?",
    "How do I catch and handle exceptions with try/except?",
    "What is a virtual environment and why use one?",
    "How can I load and parse JSON from a string or file?",
    "What is a Python decorator?",
    "How do I loop over keys and values in a dictionary?",
    "What is the Global Interpreter Lock in CPython?",
]


def _truncate(text: object, width: int = ANSWER_TRUNCATE) -> str:
    s = str(text)
    if len(s) <= width:
        return s
    return s[: width - 3] + "..."


def main() -> int:
    print("Retriever smoke test (vectorizer + question_vectors + chatbot_df)")
    print(f"Artifacts dir: {retriever.ARTIFACTS_DIR}")

    try:
        retriever.load_artifacts()
        _v, _qv, df = retriever._require_artifacts()
    except FileNotFoundError as exc:
        print(f"ERROR: Missing artifact(s): {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: Could not load artifacts: {exc}", file=sys.stderr)
        return 1

    print(
        "Loaded: vectorizer.pkl, question_vectors.pkl, chatbot_df.pkl "
        f"(df rows: {len(df):,})\n"
    )

    for i, question in enumerate(SAMPLE_PYTHON_QUESTIONS, start=1):
        print(f"--- Sample {i}/10 ---")
        print(f"Input: {question}")
        try:
            answer, _alternate, qid, aid = retriever.chatbot_response_for_api(question)
        except Exception as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            traceback.print_exc()
            return 1

        print(f"Matched QId: {qid}")
        print(f"Matched AId: {aid}")
        print(f"Answer (truncated): {_truncate(answer)}")
        print()

    print("All 10 samples completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
