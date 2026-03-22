"""
Single source of truth for backend layout (resolved from this file, not cwd).

Use for scripts: add ``backend/`` to ``sys.path``, then ``from app.paths import ...``
"""

from __future__ import annotations

from pathlib import Path

# backend/app/paths.py -> parent.parent == backend/
BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
ARTIFACTS_DIR = BACKEND_DIR / "artifacts"
PYBOT_DATA_DIR = REPO_ROOT / "pybot_data"
SCRIPTS_DIR = BACKEND_DIR / "scripts"
DEBUG_DIR = BACKEND_DIR / "debug"


def ensure_data_and_artifacts_dirs() -> None:
    """Ensure ``backend/data`` and ``backend/artifacts`` exist (idempotent)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
