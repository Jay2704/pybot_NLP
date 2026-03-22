"""
FastAPI entrypoint: loads retrieval artifacts at startup (Chatbot-V5.ipynb parity).
"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .frontend_spa import register_frontend_spa
from .models.schemas import HealthResponse
from .paths import ensure_data_and_artifacts_dirs, resolve_frontend_dist_dir
from .routes import chat
from .services import retriever

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def _cors_allow_origins() -> list[str]:
    """Local dev origins plus optional comma-separated production origins (CORS_EXTRA_ORIGINS)."""
    base = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    extra = os.environ.get("CORS_EXTRA_ORIGINS", "")
    if not extra.strip():
        return base
    more = [o.strip() for o in extra.split(",") if o.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for o in base + more:
        if o not in seen:
            seen.add(o)
            out.append(o)
    return out


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_data_and_artifacts_dirs()
    logger.info(
        "Startup: loading retrieval artifacts from %s (data dir: %s)",
        retriever.ARTIFACTS_DIR,
        retriever.DATA_DIR,
    )
    retriever.load_artifacts()
    logger.info("Startup complete")
    yield
    logger.info("Shutdown")


app = FastAPI(
    title="PyBot API",
    description="REST API mirroring Chatbot-V5.ipynb retrieval flow",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins(),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    return HealthResponse(status="ok")


# React SPA after all API routes: /chat, /health, /docs, openapi.json, etc. stay on FastAPI.
_spa_dir = resolve_frontend_dist_dir()
if _spa_dir is not None:
    register_frontend_spa(app, _spa_dir)
else:
    logger.warning(
        "No React build found — API only. Build to frontend/dist or frontend/build, "
        "or set FRONTEND_DIST_DIR (see app.paths.resolve_frontend_dist_dir).",
    )
