#!/usr/bin/env python3
"""
Build TF-IDF retrieval artifacts from final_chatbot_data.csv.

Parity with Chatbot-V5.ipynb (cells 14–15): TfidfVectorizer fit on concatenated
Question and Answer columns; transform Questions only.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# --- Path configuration (defaults; override via CLI) ---------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_CSV = REPO_ROOT / "backend" / "data" / "final_chatbot_data.csv"
DEFAULT_ARTIFACTS_DIR = REPO_ROOT / "backend" / "artifacts"

VECTORIZER_NAME = "vectorizer.pkl"
QUESTION_VECTORS_NAME = "question_vectors.pkl"
CHATBOT_DF_NAME = "chatbot_df.pkl"


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def load_final_dataset(path: Path) -> pd.DataFrame:
    logger.info("Loading dataset from %s", path)
    df = pd.read_csv(path)
    logger.info("Loaded %s rows, %s columns: %s", f"{len(df):,}", len(df.columns), list(df.columns))
    return df


def build_retrieval_artifacts(df: pd.DataFrame) -> tuple[TfidfVectorizer, object]:
    """Same as Chatbot-V5.ipynb cells 14–15."""
    vectorizer = TfidfVectorizer()
    vectorizer.fit(np.concatenate((df.Question, df.Answer)))
    Question_vectors = vectorizer.transform(df.Question)
    return vectorizer, Question_vectors


def save_artifacts(
    vectorizer: TfidfVectorizer,
    Question_vectors: object,
    df: pd.DataFrame,
    artifacts_dir: Path,
) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    v_path = artifacts_dir / VECTORIZER_NAME
    qv_path = artifacts_dir / QUESTION_VECTORS_NAME
    df_path = artifacts_dir / CHATBOT_DF_NAME

    logger.info("Writing %s", v_path)
    joblib.dump(vectorizer, v_path)

    logger.info("Writing %s (shape %s)", qv_path, getattr(Question_vectors, "shape", "?"))
    joblib.dump(Question_vectors, qv_path)

    logger.info("Writing %s", df_path)
    joblib.dump(df, df_path)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Build TF-IDF artifacts (Chatbot-V5.ipynb retrieval step).",
    )
    p.add_argument(
        "--input-csv",
        type=Path,
        default=DEFAULT_INPUT_CSV,
        help="Path to final_chatbot_data.csv (default: %(default)s)",
    )
    p.add_argument(
        "--artifacts-dir",
        type=Path,
        default=DEFAULT_ARTIFACTS_DIR,
        help="Directory for .pkl outputs (default: %(default)s)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    input_csv = args.input_csv.resolve()
    artifacts_dir = args.artifacts_dir.resolve()

    if not input_csv.is_file():
        logger.error("Input file not found: %s", input_csv)
        return 1

    try:
        df = load_final_dataset(input_csv)
        vectorizer, Question_vectors = build_retrieval_artifacts(df)
        save_artifacts(vectorizer, Question_vectors, df, artifacts_dir)
    except Exception:
        logger.exception("Failed to build retrieval artifacts")
        return 1

    logger.info("Done. Artifacts directory: %s", artifacts_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
