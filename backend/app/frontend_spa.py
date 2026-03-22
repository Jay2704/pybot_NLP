"""
Mount the production React build as a static SPA after API routes.

Uses Starlette StaticFiles(html=True) so unknown paths receive index.html (client-side routing).
Does not touch retrieval or chat routes.
"""

from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger(__name__)


def register_frontend_spa(app: FastAPI, dist_dir: Path) -> None:
    """
    Serve files from ``dist_dir`` at URL prefix ``/``. Register only after all API routes.

    ``html=True`` maps missing paths to ``index.html`` for SPA navigation.
    """
    if not dist_dir.is_dir():
        logger.warning(
            "React build not found at %s — API only (set FRONTEND_DIST_DIR or build frontend)",
            dist_dir,
        )
        return

    app.mount(
        "/",
        StaticFiles(directory=str(dist_dir), html=True),
        name="spa",
    )
    logger.info("Serving React SPA from %s", dist_dir)
