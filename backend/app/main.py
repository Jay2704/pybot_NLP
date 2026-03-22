"""
FastAPI entrypoint: loads retrieval artifacts at startup (Chatbot-V5.ipynb parity).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.schemas import HealthResponse
from .paths import ensure_data_and_artifacts_dirs
from .routes import chat
from .services import retriever

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


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
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
async def health():
    return HealthResponse(status="ok")
