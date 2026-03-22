#!/usr/bin/env python3
"""
Build AnswersV2.csv from Answers.csv using the same logic as Preprocessing.ipynb.

Reads Questions.csv and Answers.csv from a configurable directory (notebook parity:
only Answers rows are transformed). Output: AnswersV2.csv in the same directory
unless --output-dir is set.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ANSWERS_FILENAME = "Answers.csv"
QUESTIONS_FILENAME = "Questions.csv"
OUTPUT_FILENAME = "AnswersV2.csv"
CSV_ENCODING = "latin-1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build AnswersV2.csv from Answers.csv (Preprocessing.ipynb logic)."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        required=True,
        help="Directory containing Questions.csv and Answers.csv.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=f"Directory for {OUTPUT_FILENAME} (defaults to --input-dir).",
    )
    return parser.parse_args()


def read_csv_checked(path: Path, *, label: str) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"{label}: file not found: {path}")

    try:
        df = pd.read_csv(path, encoding=CSV_ENCODING)
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"{label}: failed to decode {path} with encoding={CSV_ENCODING!r}"
        ) from exc

    print(f"{label}: loaded {len(df):,} rows, {len(df.columns)} columns from {path}")
    return df


def build_answers_v2(answers: pd.DataFrame) -> pd.DataFrame:
    """Mirror Preprocessing.ipynb: add latest_score, alternate, date; preserve all else."""
    out = answers.copy()
    out["latest_score"] = out["Score"]
    out["alternate"] = out["Score"]
    out["date"] = date.today()
    return out


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = (args.output_dir or input_dir).resolve()

    if not input_dir.is_dir():
        print(f"ERROR: input directory does not exist or is not a directory: {input_dir}", file=sys.stderr)
        return 1

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(f"ERROR: cannot create output directory {output_dir}: {exc}", file=sys.stderr)
        return 1

    questions_path = input_dir / QUESTIONS_FILENAME
    answers_path = input_dir / ANSWERS_FILENAME
    out_path = output_dir / OUTPUT_FILENAME

    try:
        _questions = read_csv_checked(questions_path, label="Questions")
        answers = read_csv_checked(answers_path, label="Answers")
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if answers.empty:
        print("WARNING: Answers dataframe is empty; writing empty AnswersV2.csv.", file=sys.stderr)

    if "Score" not in answers.columns:
        print("ERROR: Answers.csv must contain a 'Score' column.", file=sys.stderr)
        return 1

    built = build_answers_v2(answers)

    try:
        built.to_csv(out_path, index=False)
    except OSError as exc:
        print(f"ERROR: failed to write {out_path}: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {len(built):,} rows to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
