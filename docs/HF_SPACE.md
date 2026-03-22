# Hugging Face Space (Docker) — single service

This repo can run as **one Docker Space**: FastAPI serves `POST /chat`, `GET /health`, and the **built React app** from the same process. Data and artifacts are read from `backend/data` and `backend/artifacts` inside the image (commit them to the Space repo, or populate via your own download step — not covered here).

Retrieval code, dataset schemas, and notebook-aligned paths are unchanged; only wiring (static files, Docker, frontend API base URL) is added.

---

## How the Space runs

1. **Build stage:** Node builds `frontend/` → `dist/`.
2. **Runtime image:** Python installs `backend/requirements.txt`, copies `backend/` (including `data/` and `artifacts/` if present in the build context), and copies the Vite output to **`backend/static/dist`**.
3. **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (HF sets `PORT`, default **7860**).
4. **Requests:** API routes (`/chat`, `/health`, `/docs`, …) are registered first; **`StaticFiles`** is mounted at `/` last so the SPA serves `index.html` and assets, while JSON API paths keep working.

The frontend production build uses **same-origin** API calls (`fetch("/chat")`) when `VITE_API_URL` is unset — no extra env vars required on the Space for a single deployment.

---

## Updated / relevant layout

```text
pybot_NLP/
├── Dockerfile                 # multi-stage: npm build → Python + static/dist
├── .dockerignore
├── backend/
│   ├── app/
│   │   ├── main.py            # + optional StaticFiles mount for SPA
│   │   └── paths.py           # + FRONTEND_DIST_DIR (static/dist)
│   ├── data/                  # processed CSVs (in repo for HF runtime)
│   ├── artifacts/             # pickles (in repo for HF runtime)
│   └── static/
│       └── dist/              # populated by Docker build (not required locally)
├── frontend/
│   ├── src/services/api.js    # prod: same-origin; dev: 127.0.0.1:8000
│   └── ...
└── docs/
    └── HF_SPACE.md            # this file
```

---

## Files added or modified (minimal)

| Action | Path |
|--------|------|
| **Add** | `Dockerfile` — Node build + Python runtime, copies `dist` → `backend/static/dist` |
| **Add** | `.dockerignore` — trims context (node_modules, venv, notebooks, etc.) |
| **Add** | `docs/HF_SPACE.md` — this guide |
| **Modify** | `backend/app/paths.py` — `FRONTEND_DIST_DIR` |
| **Modify** | `backend/app/main.py` — mount SPA if `FRONTEND_DIST_DIR` exists; log if missing |
| **Modify** | `frontend/src/services/api.js` — production default: same-origin; dev: `:8000` |

No changes to `retriever.py`, dataset builders, or column definitions.

---

## Space setup (dashboard)

1. New **Space** → **Docker** → connect this repository.
2. **SDK** is Docker; root `Dockerfile` is used automatically.
3. Ensure **`backend/data`** and **`backend/artifacts`** are in the branch the Space builds (or add a custom build step to fetch them — your choice).
4. **Hardware:** CPU is enough if inference matches your local stack; increase if load is high.

### Optional `README` card (YAML)

If you use a dedicated Space repo, put this at the **top** of `README.md`:

```yaml
---
title: PyBot NLP Chat
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---
```

---

## Local checks

- **API only (no UI files):** `cd backend && uvicorn app.main:app --reload` — works; log may warn that `static/dist` is missing.
- **Full stack locally:** Build `frontend/dist`, copy to `backend/static/dist`, run uvicorn — open `/` for the SPA, `/chat` for API.
- **Docker:** From repo root: `docker build -t pybot-hf .` then run with `-p 7860:7860` and open `http://localhost:7860`.

---

## Local Docker (Mac/Linux)

Exact **build / run / browser** steps: **`docs/DOCKER_LOCAL.md`**. Optional one-command run: `docker compose up --build` from the repo root (`docker-compose.yml`).

---

## Common issues

| Issue | Notes |
|-------|--------|
| **404 on `/`** | `backend/static/dist` empty — run Docker build or copy Vite `dist` there. |
| **Chat fails in UI** | Same-origin requires API on same host/port as the page; do not set `VITE_API_URL` to localhost in the production build. |
| **500 on `/chat`** | Missing or corrupt `data/` or `artifacts/` in the image — check Space build logs and repo contents. |
| **Huge git push** | Large CSVs/pickles may exceed HF limits — consider Git LFS or external artifact hosting (custom download in Dockerfile). |
