# Deployment (Hugging Face Space — primary)

This repo is set up for a **single Docker Space**: one container runs **FastAPI** and the **Vite-built React** app. No separate frontend host is required.

| Topic | Doc |
|--------|-----|
| Space layout, files, troubleshooting | **`docs/HF_SPACE.md`** |
| Local Docker build & run | **`docs/DOCKER_LOCAL.md`** |
| **Frontend-only workflow (dev, test, HF push, verify)** | **`docs/FRONTEND_DEPLOY_HF.md`** |
| **GitHub Pages (static frontend + remote API)** | **`docs/GITHUB_PAGES.md`** |
| Pre-push checklist | **`docs/PRE_DEPLOY_CHECKLIST.md`** |

**Entrypoints:** root **`Dockerfile`**, **`docker/entrypoint.sh`**, **`docker-compose.yml`** (local testing only).

**Environment:** `CORS_EXTRA_ORIGINS` is optional for same-origin Spaces; set comma-separated origins if the browser hits the API from a different host (e.g. split deploy).

---

## Optional: frontend and API on different hosts

If you host the static UI and the API separately (not the default for this repo):

1. Set **`VITE_API_URL`** at the **frontend build** to the public API origin (no trailing slash).
2. On the API, set **`CORS_EXTRA_ORIGINS`** to every origin that serves the UI (scheme + host + port). Local dev origins are already listed in `backend/app/main.py`.

The frontend client is **`frontend/src/services/api.js`** — `VITE_API_URL` overrides same-origin API calls when set.

---

## `backend/runtime.txt`

Optional **local** Python version hint (e.g. pyenv). The **Docker** image uses the Python version in **`Dockerfile`**, not this file.
