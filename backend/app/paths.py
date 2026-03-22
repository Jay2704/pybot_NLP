"""
Single source of truth for backend layout.

All locations are derived from this file's path (``backend/app/paths.py``), never from
the process current working directory — so Hugging Face Spaces, Docker, and local runs
behave the same as long as ``backend/app`` is laid out correctly.
"""

from __future__ import annotations

import os
from pathlib import Path

# Anchor: backend/app/paths.py -> backend/ is two levels up from this file
_APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = _APP_DIR.parent
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
ARTIFACTS_DIR = BACKEND_DIR / "artifacts"

# Resolved absolute paths (files may not exist yet; existence is checked at load time)
ARTIFACT_VECTORIZER_PATH = (ARTIFACTS_DIR / "vectorizer.pkl").resolve()
ARTIFACT_QUESTION_VECTORS_PATH = (ARTIFACTS_DIR / "question_vectors.pkl").resolve()
ARTIFACT_CHATBOT_DF_PATH = (ARTIFACTS_DIR / "chatbot_df.pkl").resolve()

RETRIEVAL_ARTIFACT_FILES: tuple[tuple[str, Path], ...] = (
    ("vectorizer.pkl", ARTIFACT_VECTORIZER_PATH),
    ("question_vectors.pkl", ARTIFACT_QUESTION_VECTORS_PATH),
    ("chatbot_df.pkl", ARTIFACT_CHATBOT_DF_PATH),
)
PYBOT_DATA_DIR = REPO_ROOT / "pybot_data"
SCRIPTS_DIR = BACKEND_DIR / "scripts"
DEBUG_DIR = BACKEND_DIR / "debug"


def resolve_frontend_dist_dir() -> Path | None:
    """
    Directory containing the React production build (e.g. ``index.html``, ``assets/``).

    Resolution order:

    1. ``FRONTEND_DIST_DIR`` or ``FRONTEND_BUILD_DIR`` env (absolute or relative to cwd)
    2. ``<repo>/frontend/dist`` (Vite default)
    3. ``<repo>/frontend/build`` (CRA default)
    4. ``backend/static/dist`` (Docker / copy-into-backend layouts)

    Returns ``None`` if no existing directory is found.
    """
    for key in ("FRONTEND_DIST_DIR", "FRONTEND_BUILD_DIR"):
        raw = os.environ.get(key, "").strip()
        if raw:
            p = Path(raw).expanduser().resolve()
            return p if p.is_dir() else None

    candidates = (
        REPO_ROOT / "frontend" / "dist",
        REPO_ROOT / "frontend" / "build",
        BACKEND_DIR / "static" / "dist",
    )
    for c in candidates:
        if c.is_dir():
            return c
    return None


def ensure_data_and_artifacts_dirs() -> None:
    """Ensure ``backend/data`` and ``backend/artifacts`` exist (idempotent)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
