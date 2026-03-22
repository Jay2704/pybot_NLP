"""
Chatbot retrieval aligned with Chatbot-V5.ipynb.

Helpers (same names and behavior as the notebook):
  getAnswerWithHighestScore, get_answer, chatbot_response

Artifacts map to notebook globals: vectorizer, Question_vectors, df.
The notebook also uses `an` (AnswersV2) for CSV writes in the date-threshold branch;
that frame is not loaded here — only `df` is updated in memory.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from sklearn.metrics.pairwise import cosine_similarity

from ..paths import (
    ARTIFACTS_DIR,
    ARTIFACT_CHATBOT_DF_PATH,
    ARTIFACT_QUESTION_VECTORS_PATH,
    ARTIFACT_VECTORIZER_PATH,
    BACKEND_DIR,
    DATA_DIR,
    RETRIEVAL_ARTIFACT_FILES,
)

logger = logging.getLogger(__name__)

# Re-export for callers that use retriever.ARTIFACTS_DIR / retriever.DATA_DIR

THRESHOLD = 30

_vectorizer: Any = None
_question_vectors: Any = None
_df: pd.DataFrame | None = None


def load_artifacts() -> None:
    """Load vectorizer, Question_vectors, and df from backend/artifacts (startup)."""
    global _vectorizer, _question_vectors, _df

    backend_root = BACKEND_DIR.resolve()
    artifacts_root = ARTIFACTS_DIR.resolve()
    data_root = DATA_DIR.resolve()

    logger.info(
        "Path anchor: app.paths from %s -> backend root %s (not cwd)",
        Path(__file__).resolve(),
        backend_root,
    )
    logger.info("Artifacts directory (absolute): %s", artifacts_root)
    logger.info("Data directory (absolute):     %s", data_root)
    for logical_name, abs_path in RETRIEVAL_ARTIFACT_FILES:
        logger.info(
            "Expected retrieval artifact: %s -> %s",
            logical_name,
            abs_path,
        )

    missing = [(name, p) for name, p in RETRIEVAL_ARTIFACT_FILES if not p.is_file()]
    if missing:
        lines = "\n".join(f"  - {p}  ({name})" for name, p in missing)
        raise RuntimeError(
            "Missing required retrieval artifact file(s). "
            "Paths are resolved from backend/app/paths.py (not the process working directory).\n"
            f"{lines}\n\n"
            f"backend root:    {backend_root}\n"
            f"artifacts dir:   {artifacts_root}\n"
            "Ensure vectorizer.pkl, question_vectors.pkl, and chatbot_df.pkl are present. "
            "Generate them with: backend/scripts/build_retrieval_artifacts.py "
            "(after build_answers_v2.py and build_final_dataset.py)."
        )

    v_path = ARTIFACT_VECTORIZER_PATH
    qv_path = ARTIFACT_QUESTION_VECTORS_PATH
    df_path = ARTIFACT_CHATBOT_DF_PATH

    logger.info("Loading joblib: %s", v_path)
    _vectorizer = joblib.load(str(v_path))
    logger.info("Loading joblib: %s", qv_path)
    _question_vectors = joblib.load(str(qv_path))
    logger.info("Loading joblib: %s", df_path)
    _df = joblib.load(str(df_path))
    assert _df is not None
    logger.info(
        "Loaded vectorizer, Question_vectors (shape=%s), chatbot_df (%s rows)",
        getattr(_question_vectors, "shape", "?"),
        f"{len(_df):,}",
    )


def _require_artifacts() -> tuple[Any, Any, pd.DataFrame]:
    if _vectorizer is None or _question_vectors is None or _df is None:
        raise RuntimeError("Artifacts not loaded; call load_artifacts() at startup")
    return _vectorizer, _question_vectors, _df


def getAnswerWithHighestScore(answers: pd.DataFrame, df: pd.DataFrame) -> list:
    """
    Notebook getAnswerWithHighestScore (cell 17).

    Uses columns: latest_score, alternate, date, QId; mutates `df` when the date
    threshold is exceeded (same intent as notebook; `an` / CSV not available here).
    """
    r = np.argmax(answers["latest_score"] - answers["alternate"])
    date_cell = answers["date"].iloc[0]
    if isinstance(date_cell, str):
        parsed = datetime.strptime(date_cell, "%Y-%m-%d")
    else:
        parsed = datetime.strptime(str(date_cell)[:10], "%Y-%m-%d")

    if (
        datetime.strptime(str(date.today()), "%Y-%m-%d") - parsed
    ).days > THRESHOLD:
        qid0 = answers["QId"].iloc[0]
        mask = df["QId"] == qid0
        df.loc[mask, "date"] = date.today()
        df.loc[mask, "alternate"] = df.loc[mask, "latest_score"]

    return [
        answers.iloc[r]["Answer"],
        answers.iloc[r]["AId"],
        answers.iloc[r]["alternate"],
    ]


def get_answer(row: int, df: pd.DataFrame) -> list:
    """
    Notebook get_answer (cell 18).

    Returns [answer[0], answer[2]] from getAnswerWithHighestScore (answer text,
    alternate score), matching the notebook return value.
    """
    qid = df.iloc[row, 0]
    answers = df.loc[df["QId"] == qid]
    answer = getAnswerWithHighestScore(answers, df)
    return [answer[0], answer[2]]


def chatbot_response(msg: str) -> list:
    """
    Notebook chatbot_response (cell 19).

    Returns [a[0], a[1]] where `a` is the return of get_answer (answer text, alternate).
    """
    vectorizer, Question_vectors, df = _require_artifacts()

    input_question = BeautifulSoup(msg).get_text()

    input_question_vector = vectorizer.transform([input_question])

    similarities = cosine_similarity(input_question_vector, Question_vectors)

    closest = np.argmax(similarities, axis=1)
    a = get_answer(int(closest[0]), df)
    return [a[0], a[1]]


def chatbot_response_for_api(msg: str) -> tuple[Any, Any, int, int]:
    """
    Same inference path as the notebook (one TF-IDF pass + one getAnswerWithHighestScore).

    Returns (answer, alternate, qid, aid) for FastAPI ChatResponse without calling
    get_answer/chatbot_response twice (avoids duplicate score / date updates).
    """
    vectorizer, Question_vectors, df = _require_artifacts()

    input_question = BeautifulSoup(msg).get_text()
    input_question_vector = vectorizer.transform([input_question])
    similarities = cosine_similarity(input_question_vector, Question_vectors)
    closest = np.argmax(similarities, axis=1)
    row = int(closest[0])

    qid = df.iloc[row, 0]
    answers = df.loc[df["QId"] == qid]
    triple = getAnswerWithHighestScore(answers, df)
    return triple[0], triple[2], int(qid), int(triple[1])
