#!/usr/bin/env python3
"""
Simulate the full chatbot pipeline: load artifacts, preprocess, TF-IDF, similarity,
answer selection (same flow as retriever / notebook).

Does not modify application code or retriever modules.

Run:
  python backend/debug/test_pipeline.py
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity

_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.services.retriever import getAnswerWithHighestScore

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "backend" / "artifacts"
DATA_DIR = REPO_ROOT / "backend" / "data"

TEXT_TRUNCATE = 150

# Topics: list comprehension, file handling, exceptions, lambda functions, dictionaries
TEST_QUERIES = [
    "How do I use list comprehension in Python?",
    "How can I read and write files in Python?",
    "How do I handle exceptions with try and except in Python?",
    "What are lambda functions in Python and when should I use them?",
    "How do I iterate over keys and values in a dictionary in Python?",
]


def _find_vectorizer_path() -> Path:
    p = ARTIFACTS_DIR / "vectorizer.pkl"
    if p.is_file():
        return p
    raise FileNotFoundError(f"vectorizer.pkl not found under {ARTIFACTS_DIR}")


def _find_question_vectors_path() -> Path:
    preferred = ARTIFACTS_DIR / "question_vectors.pkl"
    if preferred.is_file():
        return preferred
    if ARTIFACTS_DIR.is_dir():
        for p in sorted(ARTIFACTS_DIR.glob("*.pkl")):
            low = p.name.lower()
            if "vectorizer" in low:
                continue
            if "vector" in low or "matrix" in low or "tfidf" in low:
                return p
    raise FileNotFoundError(
        f"No question_vectors (or similar) .pkl found under {ARTIFACTS_DIR}"
    )


def _find_dataset_path() -> Path:
    p = ARTIFACTS_DIR / "chatbot_df.pkl"
    if p.is_file():
        return p
    csv_path = DATA_DIR / "final_chatbot_data.csv"
    if csv_path.is_file():
        return csv_path
    if DATA_DIR.is_dir():
        csvs = sorted(DATA_DIR.glob("*.csv"))
        if csvs:
            return csvs[0]
    raise FileNotFoundError(
        f"No chatbot_df.pkl or dataset .csv found under {ARTIFACTS_DIR} or {DATA_DIR}"
    )


def _load_dataset(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".pkl":
        obj = joblib.load(path)
        if not isinstance(obj, pd.DataFrame):
            raise TypeError(f"Expected DataFrame from {path}, got {type(obj).__name__}")
        return obj
    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported dataset file: {path}")


def _truncate(text: object, width: int = TEXT_TRUNCATE) -> str:
    s = str(text)
    if len(s) <= width:
        return s
    return s[: width - 3] + "..."


def _run_one_query(
    raw_input: str,
    vectorizer,
    Question_vectors,
    df: pd.DataFrame,
) -> tuple[str, str, str]:
    """
    Preprocess → vectorize → cosine similarity → top row → getAnswerWithHighestScore.
    Returns (matched_question_text, answer_text, error_message_or_empty).
    """
    try:
        input_question = BeautifulSoup(raw_input).get_text()
        input_question_vector = vectorizer.transform([input_question])
        similarities = cosine_similarity(input_question_vector, Question_vectors)
        closest = np.argmax(similarities, axis=1)
        row = int(closest[0])

        matched_question = df.iloc[row]["Question"]
        qid = df.iloc[row][0]
        answers = df.loc[df["QId"] == qid]
        triple = getAnswerWithHighestScore(answers, df)
        answer_text = triple[0]
        return str(matched_question), str(answer_text), ""
    except Exception as exc:
        traceback.print_exc()
        return "", "", f"{type(exc).__name__}: {exc}"


def main() -> int:
    print(f"Repo root: {REPO_ROOT}")
    print("Full pipeline simulation (dataset + vectorizer + question_vectors)\n")

    try:
        v_path = _find_vectorizer_path()
        qv_path = _find_question_vectors_path()
        ds_path = _find_dataset_path()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print("Resolved paths:")
    print(f"  vectorizer:     {v_path}")
    print(f"  question vecs:  {qv_path}")
    print(f"  dataset:        {ds_path}\n")

    try:
        vectorizer = joblib.load(v_path)
        Question_vectors = joblib.load(qv_path)
        df = _load_dataset(ds_path)
    except Exception as exc:
        print(f"ERROR: Failed to load artifacts: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1

    if len(df) == 0:
        print("ERROR: Dataset is empty.", file=sys.stderr)
        return 1

    try:
        nv = Question_vectors.shape[0]
    except Exception as exc:
        print(f"ERROR: question_vectors invalid: {exc}", file=sys.stderr)
        return 1

    if nv != len(df):
        print(
            f"ERROR: question_vectors rows ({nv}) != dataset rows ({len(df)}).",
            file=sys.stderr,
        )
        return 1

    if "Question" not in df.columns:
        print("ERROR: Dataset missing 'Question' column.", file=sys.stderr)
        return 1

    failures = 0
    for i, query in enumerate(TEST_QUERIES, start=1):
        print(f"========== Query {i}/5 ==========")
        print(f"Input:\n  {query}\n")

        mq, ans, err = _run_one_query(query, vectorizer, Question_vectors, df)
        if err:
            print(f"ERROR: {err}\n", file=sys.stderr)
            failures += 1
            continue

        print(f"Matched question (truncated):\n  {_truncate(mq)}\n")
        print(f"Answer (truncated):\n  {_truncate(ans)}\n")

    if failures:
        print(f"Completed with {failures} failed query(s).", file=sys.stderr)
        return 1

    print("Pipeline run finished (all queries OK).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
