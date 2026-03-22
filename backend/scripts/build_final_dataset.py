#!/usr/bin/env python3
"""
Build final_chatbot_data.csv from Questions.csv and AnswersV2.csv.

Parity with Chatbot-V5.ipynb: same reads, renames, filter, merge, drops, renames,
and BeautifulSoup HTML stripping (no TF-IDF / UI).

Default inputs: Questions.csv from repo pybot_data/, AnswersV2.csv from backend/data/.
Default output: backend/data/final_chatbot_data.csv

Paths resolve from this script file location (not the process working directory).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.paths import DATA_DIR, PYBOT_DATA_DIR, ensure_data_and_artifacts_dirs

DEFAULT_QUESTIONS_PATH = PYBOT_DATA_DIR / "Questions.csv"
DEFAULT_ANSWERS_V2_PATH = DATA_DIR / "AnswersV2.csv"
DEFAULT_OUTPUT_PATH = DATA_DIR / "final_chatbot_data.csv"

CSV_ENCODING = "latin-1"

DROP_AFTER_MERGE = [
    "OwnerUserId_x",
    "CreationDate_x",
    "Score_x",
    "OwnerUserId_y",
    "CreationDate_y",
]

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def read_questions(path: Path) -> pd.DataFrame:
    logger.info("Loading Questions from %s", path)
    df = pd.read_csv(path, encoding=CSV_ENCODING)
    logger.info("Questions: %s rows, %s columns", f"{len(df):,}", len(df.columns))
    return df


def read_answers_v2(path: Path) -> pd.DataFrame:
    logger.info("Loading AnswersV2 from %s", path)
    df = pd.read_csv(path, encoding=CSV_ENCODING)
    logger.info("AnswersV2: %s rows, %s columns", f"{len(df):,}", len(df.columns))
    return df


def rename_answer_keys(an: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 4: ParentId -> QId."""
    out = an.rename(columns={"ParentId": "QId"})
    return out


def rename_ids(q: pd.DataFrame, an: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Notebook cell 5: Questions Id -> QId; Answers Id -> AId."""
    q = q.rename(columns={"Id": "QId"})
    an = an.rename(columns={"Id": "AId"})
    return q, an


def filter_answers_score_gt_five(an: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 6: an = an[an['Score']>5]."""
    before = len(an)
    out = an[an["Score"] > 5]
    logger.info("Filtered answers with Score > 5: %s -> %s rows", f"{before:,}", f"{len(out):,}")
    return out


def merge_on_qid(q: pd.DataFrame, an: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 8: df = q.merge(an, on='QId')."""
    df = q.merge(an, on="QId")
    logger.info("Merged on QId: %s rows", f"{len(df):,}")
    return df


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 9."""
    missing = [c for c in DROP_AFTER_MERGE if c not in df.columns]
    if missing:
        raise ValueError(f"Expected merge columns missing before drop: {missing}")
    return df.drop(columns=DROP_AFTER_MERGE)


def rename_body_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 10."""
    return df.rename(
        columns={"Body_x": "Question", "Body_y": "Answer", "Score_y": "Score"}
    )


def strip_html_question_answer(df: pd.DataFrame) -> pd.DataFrame:
    """Notebook cell 12 (same order: Answer, then Question)."""
    out = df.copy()
    out["Answer"] = out["Answer"].apply(lambda x: BeautifulSoup(x).get_text())
    out["Question"] = out["Question"].apply(lambda x: BeautifulSoup(x).get_text())
    return out


def save_final(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info("Wrote %s rows to %s", f"{len(df):,}", path)


def build_final_dataset(q: pd.DataFrame, an: pd.DataFrame) -> pd.DataFrame:
    """Full notebook data pipeline (cells 4–12)."""
    an = rename_answer_keys(an)
    q, an = rename_ids(q, an)
    an = filter_answers_score_gt_five(an)
    df = merge_on_qid(q, an)
    df = drop_columns(df)
    df = rename_body_columns(df)
    df = strip_html_question_answer(df)
    return df


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build final_chatbot_data.csv (Chatbot-V5.ipynb data flow).",
    )
    p.add_argument(
        "--questions",
        type=Path,
        default=DEFAULT_QUESTIONS_PATH,
        help=f"Path to Questions.csv (default: {DEFAULT_QUESTIONS_PATH})",
    )
    p.add_argument(
        "--answers-v2",
        type=Path,
        default=DEFAULT_ANSWERS_V2_PATH,
        help=f"Path to AnswersV2.csv (default: {DEFAULT_ANSWERS_V2_PATH})",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output CSV path (default: {DEFAULT_OUTPUT_PATH})",
    )
    return p.parse_args()


def main() -> int:
    ensure_data_and_artifacts_dirs()
    args = parse_args()
    questions_path = args.questions.resolve()
    answers_path = args.answers_v2.resolve()
    output_path = args.output.resolve()

    if not questions_path.is_file():
        print(f"ERROR: Questions.csv not found: {questions_path}", file=sys.stderr)
        return 1
    if not answers_path.is_file():
        print(f"ERROR: AnswersV2.csv not found: {answers_path}", file=sys.stderr)
        return 1

    try:
        q = read_questions(questions_path)
        an = read_answers_v2(answers_path)
        df = build_final_dataset(q, an)
        save_final(df, output_path)
    except UnicodeDecodeError as exc:
        print(f"ERROR: CSV decode failed (expected {CSV_ENCODING!r}): {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: file read/write failed: {exc}", file=sys.stderr)
        return 1
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        logger.exception("Build failed: %s", exc)
        return 1

    print(f"input (Questions):  {questions_path}")
    print(f"input (AnswersV2):  {answers_path}")
    print(f"output:              {output_path}")
    print(f"rows:                {len(df):,}")
    print(f"columns:             {list(df.columns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
