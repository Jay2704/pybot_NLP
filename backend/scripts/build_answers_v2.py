#!/usr/bin/env python3
"""
Build AnswersV2.csv from Answers.csv (Preprocessing.ipynb logic).

Adds columns: latest_score, alternate, date — unchanged from the notebook.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import pandas as pd

_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.paths import DATA_DIR, PYBOT_DATA_DIR, ensure_data_and_artifacts_dirs

DEFAULT_INPUT = PYBOT_DATA_DIR / "Answers.csv"
DEFAULT_OUTPUT = DATA_DIR / "AnswersV2.csv"
CSV_ENCODING = "latin-1"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build AnswersV2.csv from Answers.csv.")
    p.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Path to Answers.csv (default: {DEFAULT_INPUT})",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output path (default: {DEFAULT_OUTPUT})",
    )
    return p.parse_args()


def build_answers_v2(answers: pd.DataFrame) -> pd.DataFrame:
    """Mirror Preprocessing.ipynb: add latest_score, alternate, date; preserve all else."""
    out = answers.copy()
    out["latest_score"] = out["Score"]
    out["alternate"] = out["Score"]
    out["date"] = date.today()
    return out


def main() -> int:
    ensure_data_and_artifacts_dirs()
    args = parse_args()
    input_path = args.input.resolve()
    output_path = args.output.resolve()

    if not input_path.is_file():
        print(f"ERROR: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        answers = pd.read_csv(input_path, encoding=CSV_ENCODING)
    except UnicodeDecodeError as exc:
        print(
            f"ERROR: failed to decode {input_path} with encoding={CSV_ENCODING!r}: {exc}",
            file=sys.stderr,
        )
        return 1
    except OSError as exc:
        print(f"ERROR: cannot read {input_path}: {exc}", file=sys.stderr)
        return 1

    if "Score" not in answers.columns:
        print("ERROR: Answers.csv must contain a 'Score' column.", file=sys.stderr)
        return 1

    if answers.empty:
        print("WARNING: Answers.csv is empty; writing empty AnswersV2.csv.", file=sys.stderr)

    built = build_answers_v2(answers)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        built.to_csv(output_path, index=False)
    except OSError as exc:
        print(f"ERROR: cannot write {output_path}: {exc}", file=sys.stderr)
        return 1

    print(f"input:  {input_path}")
    print(f"output: {output_path}")
    print(f"rows:   {len(built):,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
