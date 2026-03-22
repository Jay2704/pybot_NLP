#!/usr/bin/env python3
"""
Read-only validation of processed chatbot data (pickle or CSV).

Does not modify data or retrieval logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd

# backend/test_processed_data.py -> parents[1] = repo root
REPO_ROOT = Path(__file__).resolve().parents[1]
CHATBOT_DF_PKL = REPO_ROOT / "backend" / "artifacts" / "chatbot_df.pkl"
FINAL_CSV = REPO_ROOT / "backend" / "data" / "final_chatbot_data.csv"

REQUIRED_COLUMNS = [
    "QId",
    "Question",
    "AId",
    "Answer",
    "Score",
    "latest_score",
    "alternate",
    "date",
]

TEXT_TRUNCATE = 120
SAMPLE_N = 5


def _load_dataframe() -> tuple[pd.DataFrame, str]:
    """Load chatbot_df.pkl if present, else final CSV."""
    if CHATBOT_DF_PKL.is_file():
        df = joblib.load(CHATBOT_DF_PKL)
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f"Expected DataFrame from {CHATBOT_DF_PKL}, got {type(df).__name__}")
        return df, str(CHATBOT_DF_PKL)

    if FINAL_CSV.is_file():
        df = pd.read_csv(FINAL_CSV)
        return df, str(FINAL_CSV)

    raise FileNotFoundError(
        f"Neither artifact nor CSV found:\n  {CHATBOT_DF_PKL}\n  {FINAL_CSV}"
    )


def _truncate(val: object, width: int = TEXT_TRUNCATE) -> str:
    s = str(val)
    if len(s) <= width:
        return s
    return s[: width - 3] + "..."


def _non_empty_string_series(s: pd.Series) -> pd.Series:
    """True where value is a non-empty string (after strip); False for null or non-string."""
    def ok(v: object) -> bool:
        if pd.isna(v):
            return False
        if isinstance(v, str):
            return len(v.strip()) > 0
        return False

    return s.map(ok)


def main() -> int:
    print("Processed chatbot data validation")
    print(f"Repo root: {REPO_ROOT}")

    try:
        df, source = _load_dataframe()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except (OSError, TypeError, ValueError) as exc:
        print(f"ERROR: Failed to load data: {exc}", file=sys.stderr)
        return 1

    print(f"Source: {source}")
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"Column names ({len(df.columns)}): {list(df.columns)}")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns: {missing}", file=sys.stderr)
        return 1
    print("Required columns: OK (all present)")

    subset = df[REQUIRED_COLUMNS]
    null_counts = subset.isna().sum()
    print("\nNull counts (required columns):")
    for col in REQUIRED_COLUMNS:
        print(f"  {col}: {int(null_counts[col]):,}")

    print(f"\nSample ({SAMPLE_N} rows, text truncated to {TEXT_TRUNCATE} chars):")
    sample = subset.head(SAMPLE_N)
    for idx, row in sample.iterrows():
        print(f"  --- row index {idx} ---")
        for col in REQUIRED_COLUMNS:
            val = row[col]
            if col in ("Question", "Answer"):
                print(f"    {col}: {_truncate(val)}")
            else:
                print(f"    {col}: {val}")

    bad_q = ~_non_empty_string_series(df["Question"])
    bad_a = ~_non_empty_string_series(df["Answer"])
    n_bad_q = int(bad_q.sum())
    n_bad_a = int(bad_a.sum())

    if n_bad_q or n_bad_a:
        print(
            f"\nERROR: Question/Answer must be non-empty strings. "
            f"Bad Question rows: {n_bad_q:,}; bad Answer rows: {n_bad_a:,}",
            file=sys.stderr,
        )
        if n_bad_q:
            q_idx = df.index[bad_q][:5].tolist()
            print(f"  First bad Question indices (up to 5): {q_idx}", file=sys.stderr)
        if n_bad_a:
            a_idx = df.index[bad_a][:5].tolist()
            print(f"  First bad Answer indices (up to 5): {a_idx}", file=sys.stderr)
        return 1

    print("\nValidation: Question and Answer are non-empty strings for all rows (OK)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
