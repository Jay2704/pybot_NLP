#!/usr/bin/env python3
"""
Build final_chatbot_data.csv from Questions.csv and AnswersV2.csv.

Parity with Chatbot-V5.ipynb: same reads, renames, filter, merge, drops, renames,
and BeautifulSoup HTML stripping (no TF-IDF / UI).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

# --- Path configuration (defaults; override via CLI) ---------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_DIR = REPO_ROOT / "pybot_data"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "backend" / "data" / "final_chatbot_data.csv"

QUESTIONS_FILENAME = "Questions.csv"
ANSWERS_V2_FILENAME = "AnswersV2.csv"
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
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help=f"Directory with {QUESTIONS_FILENAME} and {ANSWERS_V2_FILENAME} (default: %(default)s)",
    )
    p.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output CSV path (default: %(default)s)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_path = args.output.resolve()

    questions_path = input_dir / QUESTIONS_FILENAME
    answers_path = input_dir / ANSWERS_V2_FILENAME

    if not input_dir.is_dir():
        logger.error("Input directory does not exist: %s", input_dir)
        return 1
    if not questions_path.is_file():
        logger.error("Missing file: %s", questions_path)
        return 1
    if not answers_path.is_file():
        logger.error("Missing file: %s", answers_path)
        return 1

    try:
        q = read_questions(questions_path)
        an = read_answers_v2(answers_path)
        df = build_final_dataset(q, an)
        save_final(df, output_path)
    except Exception as exc:
        logger.exception("Build failed: %s", exc)
        return 1

    print(f"Done. Final dataset: {output_path} ({len(df):,} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
