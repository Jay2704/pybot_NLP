#!/usr/bin/env python3
"""
Verify TF-IDF artifacts (read-only on disk; may update in-memory df like production).

Uses the same retrieval steps as Chatbot-V5.ipynb / retriever: transform, cosine
similarity, argmax, then getAnswerWithHighestScore for the matched QId group.

Run:
  python backend/debug/test_artifacts.py
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

# backend/debug/test_artifacts.py -> parents[1] = backend/
_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.services.retriever import getAnswerWithHighestScore  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "backend" / "artifacts"
DATA_DIR = REPO_ROOT / "backend" / "data"

TEST_QUERY = "What is list comprehension in Python?"
ANSWER_TRUNCATE = 200


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


def _truncate(text: object, width: int = ANSWER_TRUNCATE) -> str:
    s = str(text)
    if len(s) <= width:
        return s
    return s[: width - 3] + "..."


def main() -> int:
    print(f"Repo root: {REPO_ROOT}")
    print("TF-IDF artifact verification (read-only files)\n")

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

    n_rows = len(df)
    if n_rows == 0:
        print("ERROR: Dataset has length 0", file=sys.stderr)
        return 1

    try:
        n_vec = Question_vectors.shape[0]
    except Exception as exc:
        print(f"ERROR: question_vectors has no shape: {exc}", file=sys.stderr)
        return 1

    if n_vec != n_rows:
        print(
            f"ERROR: Row mismatch — dataset has {n_rows:,} rows but "
            f"question_vectors has {n_vec:,} rows (first dimension).",
            file=sys.stderr,
        )
        return 1

    print(f"Validation: dataset rows = {n_rows:,}, question_vectors.shape[0] = {n_vec:,} (OK)")

    try:
        _ = vectorizer.transform(["sanity check transform"])
    except Exception as exc:
        print(f"ERROR: vectorizer.transform failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1

    print("Validation: vectorizer.transform() OK\n")

    print(f"Test query: {TEST_QUERY!r}\n")

    try:
        input_question = BeautifulSoup(TEST_QUERY).get_text()
        input_question_vector = vectorizer.transform([input_question])
        similarities = cosine_similarity(input_question_vector, Question_vectors)
        closest = np.argmax(similarities, axis=1)
        row = int(closest[0])

        qid = df.iloc[row][0]
        answers = df.loc[df["QId"] == qid]
        triple = getAnswerWithHighestScore(answers, df)
        answer_text = triple[0]
        aid = int(triple[1])
    except Exception as exc:
        print(f"ERROR: Inference failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 1

    print("Top match (same pipeline as notebook / retriever):")
    print(f"  Matched QId: {int(qid)}")
    print(f"  Matched AId: {aid}")
    print(f"  Answer (truncated): {_truncate(answer_text)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
