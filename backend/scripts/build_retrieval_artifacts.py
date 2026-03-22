#!/usr/bin/env python3
"""
Build TF-IDF retrieval artifacts from final_chatbot_data.csv.

Parity with Chatbot-V5.ipynb (cells 14–15): TfidfVectorizer fit on concatenated
Question and Answer columns; transform Questions only.

Default input:  backend/data/final_chatbot_data.csv
Default outputs: backend/artifacts/vectorizer.pkl, question_vectors.pkl, chatbot_df.pkl

Paths resolve from this script file location (not the process working directory).
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.paths import ARTIFACTS_DIR, DATA_DIR, ensure_data_and_artifacts_dirs

DEFAULT_INPUT_CSV = DATA_DIR / "final_chatbot_data.csv"
DEFAULT_ARTIFACTS_DIR = ARTIFACTS_DIR

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
        help=f"Path to final_chatbot_data.csv (default: {DEFAULT_INPUT_CSV})",
    )
    p.add_argument(
        "--artifacts-dir",
        type=Path,
        default=DEFAULT_ARTIFACTS_DIR,
        help=f"Directory for .pkl outputs (default: {DEFAULT_ARTIFACTS_DIR})",
    )
    return p.parse_args()


def main() -> int:
    ensure_data_and_artifacts_dirs()
    args = parse_args()
    input_csv = args.input_csv.resolve()
    artifacts_dir = args.artifacts_dir.resolve()

    v_path = artifacts_dir / VECTORIZER_NAME
    qv_path = artifacts_dir / QUESTION_VECTORS_NAME
    df_path = artifacts_dir / CHATBOT_DF_NAME

    if not input_csv.is_file():
        print(f"ERROR: input CSV not found: {input_csv}", file=sys.stderr)
        return 1

    try:
        df = load_final_dataset(input_csv)
        vectorizer, Question_vectors = build_retrieval_artifacts(df)
        save_artifacts(vectorizer, Question_vectors, df, artifacts_dir)
    except KeyError as exc:
        print(
            f"ERROR: dataset must include Question and Answer columns ({exc})",
            file=sys.stderr,
        )
        return 1
    except UnicodeDecodeError as exc:
        print(f"ERROR: failed to decode CSV: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"ERROR: file read/write failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        logger.exception("Failed to build retrieval artifacts")
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"input:              {input_csv}")
    print(f"output vectorizer:  {v_path}")
    print(f"output vectors:     {qv_path}")
    print(f"output dataframe:   {df_path}")
    print(f"dataframe shape:    {df.shape}")
    print(f"vectors shape:      {Question_vectors.shape}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
