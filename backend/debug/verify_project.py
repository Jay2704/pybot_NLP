#!/usr/bin/env python3
"""
Full project verification (read-only): folders, expected files, dataset/vectors
consistency, one retrieval smoke test. Does not modify data or application logic.

Run:
  python backend/debug/verify_project.py
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

from app.paths import ARTIFACTS_DIR, DATA_DIR, REPO_ROOT

from app.services.retriever import getAnswerWithHighestScore  # noqa: E402

REQUIRED_DATASET_COLUMNS = [
    "QId",
    "Question",
    "AId",
    "Answer",
    "Score",
    "latest_score",
    "alternate",
    "date",
]

EXPECTED_FILES: list[tuple[str, Path]] = [
    ("AnswersV2.csv", DATA_DIR / "AnswersV2.csv"),
    ("final_chatbot_data.csv", DATA_DIR / "final_chatbot_data.csv"),
    ("vectorizer.pkl", ARTIFACTS_DIR / "vectorizer.pkl"),
    ("question_vectors.pkl", ARTIFACTS_DIR / "question_vectors.pkl"),
    ("chatbot_df.pkl", ARTIFACTS_DIR / "chatbot_df.pkl"),
]

TEST_QUERY = "What is list comprehension in Python?"


def _size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def _print_file_line(label: str, path: Path) -> bool:
    if not path.is_file():
        print(f"  {label}: MISSING (expected {path})")
        return False
    try:
        mb = _size_mb(path)
    except OSError as exc:
        print(f"  {label}: ERROR stat {path}: {exc}")
        return False
    print(f"  {label}: OK")
    print(f"    path: {path}")
    print(f"    size: {mb:.4f} MB")
    return True


def main() -> int:
    print("=== Project verification (paths resolved from this script) ===\n")
    print(f"This script: {Path(__file__).resolve()}")
    print(f"Repo root:   {REPO_ROOT}")
    print(f"Data dir:    {DATA_DIR}")
    print(f"Artifacts:   {ARTIFACTS_DIR}\n")

    issues: list[str] = []

    # 1. Folders
    print("--- Folders ---")
    for label, p in [("backend/data/", DATA_DIR), ("backend/artifacts/", ARTIFACTS_DIR)]:
        if p.is_dir():
            print(f"  {label} OK: {p}")
        else:
            print(f"  {label} MISSING or not a directory: {p}")
            issues.append(f"folder missing: {p}")
    print()

    # 2–3. Expected files
    print("--- Expected files ---")
    all_files_ok = True
    for name, path in EXPECTED_FILES:
        if not _print_file_line(name, path):
            all_files_ok = False
            issues.append(f"missing file: {name}")
        print()
    if not all_files_ok:
        print("--- Backend ready for React frontend integration: NO ---")
        print("Reason: one or more expected files are missing.")
        for i in issues:
            print(f"  - {i}")
        return 1

    # 4. Dataset columns, row counts, vector alignment (use same artifacts as FastAPI)
    print("--- Dataset & vectors validation ---")
    df_path = ARTIFACTS_DIR / "chatbot_df.pkl"
    v_path = ARTIFACTS_DIR / "vectorizer.pkl"
    qv_path = ARTIFACTS_DIR / "question_vectors.pkl"

    try:
        df = joblib.load(df_path)
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"chatbot_df.pkl must be DataFrame, got {type(df).__name__}")
        Question_vectors = joblib.load(qv_path)
    except Exception as exc:
        print(f"ERROR: failed to load dataframe or vectors: {exc}", file=sys.stderr)
        traceback.print_exc()
        print("\n--- Backend ready for React frontend integration: NO ---")
        return 1

    missing_cols = [c for c in REQUIRED_DATASET_COLUMNS if c not in df.columns]
    if missing_cols:
        print(f"  FAIL: missing columns: {missing_cols}")
        issues.append(f"missing columns: {missing_cols}")
    else:
        print(f"  OK: required columns present ({len(REQUIRED_DATASET_COLUMNS)} fields)")

    n_rows = len(df)
    print(f"  Dataframe row count: {n_rows:,}")

    try:
        n_vec = int(Question_vectors.shape[0])
    except Exception as exc:
        print(f"  FAIL: question_vectors shape: {exc}")
        issues.append("invalid question_vectors")
        n_vec = -1

    if n_vec >= 0:
        print(f"  Question_vectors rows: {n_vec:,}")
        if n_vec == n_rows:
            print("  OK: vector row count matches dataframe row count")
        else:
            print(
                f"  FAIL: row mismatch (dataframe {n_rows:,} vs vectors {n_vec:,})"
            )
            issues.append("vector rows != dataframe rows")

    if missing_cols or n_vec != n_rows or n_vec < 0:
        print("\n--- Backend ready for React frontend integration: NO ---")
        for i in issues:
            print(f"  - {i}")
        return 1

    print()

    # 5. One test query (same pipeline as retriever / test_artifacts)
    print(f"--- Test query ---")
    print(f"  Query: {TEST_QUERY!r}\n")
    try:
        vectorizer = joblib.load(v_path)
        input_question = BeautifulSoup(TEST_QUERY).get_text()
        input_question_vector = vectorizer.transform([input_question])
        similarities = cosine_similarity(input_question_vector, Question_vectors)
        closest = np.argmax(similarities, axis=1)
        row = int(closest[0])
        qid = df.iloc[row, 0]
        answers = df.loc[df["QId"] == qid]
        triple = getAnswerWithHighestScore(answers, df)
        print(f"  OK: inference completed (QId={int(qid)}, AId={int(triple[1])})")
        print(f"  Answer preview: {str(triple[0])[:200]}{'...' if len(str(triple[0])) > 200 else ''}")
    except Exception as exc:
        print(f"  FAIL: {exc}", file=sys.stderr)
        traceback.print_exc()
        print("\n--- Backend ready for React frontend integration: NO ---")
        print("Reason: test query failed.")
        return 1

    print()
    print("--- Backend ready for React frontend integration: YES ---")
    print("  All expected artifacts present, dataset validates, vectors align,")
    print("  and a smoke retrieval query succeeded. Start the API with uvicorn")
    print("  (e.g. from backend/: uvicorn app.main:app --host 127.0.0.1 --port 8000).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
