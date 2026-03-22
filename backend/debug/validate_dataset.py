#!/usr/bin/env python3
"""
Read-only validation for the processed chatbot dataset (.csv or .pkl).

Discovers a dataset under backend/data/ or backend/artifacts/ and prints checks.
Does not modify any files.
"""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd

# backend/debug/validate_dataset.py -> parents[2] = repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "backend" / "data"
ARTIFACTS_DIR = REPO_ROOT / "backend" / "artifacts"

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

TEXT_TRUNCATE = 150
SAMPLE_N = 5
NULL_WARN_FRACTION = 0.05  # warn if more than 5% of rows are null in a column


def _is_vector_artifact(path: Path) -> bool:
    """Exclude TF-IDF / vectorizer pickles from dataset auto-pick."""
    low = path.name.lower()
    if low == "vectorizer.pkl" or low == "question_vectors.pkl":
        return True
    if "vectorizer" in low:
        return True
    if "question_vector" in low or "question_vectors" in low:
        return True
    return False


def discover_dataset_path() -> Path:
    """
    Prefer chatbot_df.pkl, then final_chatbot_data.csv, then other csv/pkl in data/artifacts.
    """
    preferred = [
        ARTIFACTS_DIR / "chatbot_df.pkl",
        DATA_DIR / "final_chatbot_data.csv",
    ]
    for p in preferred:
        if p.is_file():
            return p

    if DATA_DIR.is_dir():
        csvs = sorted(DATA_DIR.glob("*.csv"))
        if csvs:
            return csvs[0]

    if ARTIFACTS_DIR.is_dir():
        pkls = sorted(ARTIFACTS_DIR.glob("*.pkl"))
        for p in pkls:
            if _is_vector_artifact(p):
                continue
            return p

    raise FileNotFoundError(
        "No dataset file found. Expected e.g.\n"
        f"  {ARTIFACTS_DIR / 'chatbot_df.pkl'}\n"
        f"  {DATA_DIR / 'final_chatbot_data.csv'}\n"
        "or another .csv under backend/data/ or .pkl under backend/artifacts/ "
        "(excluding vectorizer / question_vectors)."
    )


def load_dataset(path: Path) -> pd.DataFrame:
    suf = path.suffix.lower()
    if suf == ".pkl":
        obj = joblib.load(path)
        if not isinstance(obj, pd.DataFrame):
            raise TypeError(
                f"Expected pandas.DataFrame from {path}, got {type(obj).__name__}"
            )
        return obj
    if suf == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported extension: {path}")


def _memory_usage_mb(df: pd.DataFrame) -> float:
    return float(df.memory_usage(deep=True).sum()) / (1024 * 1024)


def _truncate(val: object, width: int = TEXT_TRUNCATE) -> str:
    s = str(val)
    if len(s) <= width:
        return s
    return s[: width - 3] + "..."


def _empty_text_mask(series: pd.Series) -> pd.Series:
    """True where value is non-null but empty/whitespace string."""
    return series.notna() & series.map(
        lambda x: isinstance(x, str) and len(x.strip()) == 0
    )


def main() -> int:
    print(f"Repo root: {REPO_ROOT}\n")

    try:
        path = discover_dataset_path()
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Detected dataset file: {path}\n")

    try:
        df = load_dataset(path)
    except (OSError, TypeError, ValueError, UnicodeDecodeError) as exc:
        print(f"ERROR: Failed to load dataset: {exc}", file=sys.stderr)
        return 1

    warnings: list[str] = []

    # 1. Dataset info
    print("=== Dataset info ===")
    print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"  Columns ({len(df.columns)}): {list(df.columns)}")
    print(f"  Memory usage (deep): {_memory_usage_mb(df):.4f} MB")
    print()

    # 2. Required columns
    print("=== Required columns ===")
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        msg = f"Missing required columns: {missing}"
        print(f"  FAIL: {msg}")
        warnings.append(msg)
    else:
        print("  OK: all required columns present")
    print()

    if missing:
        print("=== Warnings ===")
        for w in warnings:
            print(f"  - {w}")
        return 1

    subset = df[REQUIRED_COLUMNS]

    # 3. Nulls
    print("=== Null values (per column) ===")
    null_counts = subset.isna().sum()
    for col in REQUIRED_COLUMNS:
        n = int(null_counts[col])
        frac = n / len(df) if len(df) else 0.0
        print(f"  {col}: {n:,} ({100.0 * frac:.4f}%)")
        if frac > NULL_WARN_FRACTION:
            warnings.append(
                f"Too many nulls in '{col}': {n:,} ({100.0 * frac:.2f}% > {100 * NULL_WARN_FRACTION:.0f}%)"
            )
    print()

    # Empty strings in Question / Answer
    print("=== Empty / whitespace-only text ===")
    eq = _empty_text_mask(df["Question"])
    ea = _empty_text_mask(df["Answer"])
    n_eq = int(eq.sum())
    n_ea = int(ea.sum())
    print(f"  Question (non-null but empty after strip): {n_eq:,}")
    print(f"  Answer (non-null but empty after strip): {n_ea:,}")
    if n_eq:
        warnings.append(f"Empty Question text in {n_eq:,} row(s)")
    if n_ea:
        warnings.append(f"Empty Answer text in {n_ea:,} row(s)")
    print()

    # Duplicate QId
    print("=== Duplicate QId ===")
    dup_rows = df.duplicated(subset=["QId"], keep=False)
    n_dup_rows = int(dup_rows.sum())
    n_unique_qid = df["QId"].nunique()
    print(f"  Unique QId values: {n_unique_qid:,}")
    print(f"  Rows that share a QId with another row: {n_dup_rows:,}")
    if n_dup_rows:
        warnings.append(
            f"Duplicate QId: {n_dup_rows:,} rows appear in non-unique QId groups"
        )
    print()

    # 4. Samples
    print(f"=== Sample rows (first {SAMPLE_N}, Question/Answer truncated to {TEXT_TRUNCATE} chars) ===")
    sample = subset.head(SAMPLE_N)
    for idx, row in sample.iterrows():
        print(f"  --- index {idx} ---")
        for col in REQUIRED_COLUMNS:
            if col in ("Question", "Answer"):
                print(f"    {col}: {_truncate(row[col])}")
            else:
                print(f"    {col}: {row[col]}")
        print()

    # 5. Warnings summary
    print("=== Warnings ===")
    if not warnings:
        print("  (none)")
    else:
        for w in warnings:
            print(f"  - {w}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
