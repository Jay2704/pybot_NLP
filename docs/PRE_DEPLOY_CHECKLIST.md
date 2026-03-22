# Pre-deployment checklist — Hugging Face Docker Space (React + FastAPI)

Run these **before** pushing to a Space or tagging a release. Order is suggested, not strict.

---

## 1. Artifacts exist (retrieval)

From repo root, verify files are present and non-empty:

```bash
ls -la backend/artifacts/vectorizer.pkl \
       backend/artifacts/question_vectors.pkl \
       backend/artifacts/chatbot_df.pkl
```

**Pass:** All three exist with non-zero size.  
**If missing:** Build locally per `backend/RUN_STEPS.md` / `scripts/run_all_build_steps.py` (or your pipeline), then re-check.

---

## 2. Dataset / artifact paths (notebook-aligned layout)

Paths are resolved from `backend/app/paths.py` (not shell `cwd`). Quick sanity check:

```bash
cd backend && python -c "
from app.paths import (
    ARTIFACT_VECTORIZER_PATH,
    ARTIFACT_QUESTION_VECTORS_PATH,
    ARTIFACT_CHATBOT_DF_PATH,
    DATA_DIR,
    ARTIFACTS_DIR,
)
print('ARTIFACTS_DIR:', ARTIFACTS_DIR)
print('DATA_DIR:     ', DATA_DIR)
for p in (ARTIFACT_VECTORIZER_PATH, ARTIFACT_QUESTION_VECTORS_PATH, ARTIFACT_CHATBOT_DF_PATH):
    print(p, 'OK' if p.is_file() else 'MISSING')
"
```

**Pass:** Each artifact prints `OK`.  
**Note:** `backend/data/` should contain your pipeline outputs if the app expects them at runtime.

---

## 3. FastAPI starts locally

```bash
cd backend
python -c "from app.main import app; print('import ok')"
```

Optional full smoke (loads artifacts):

```bash
cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What is a list comprehension in Python?"}'
```

**Pass:** `GET /health` returns JSON with `"status":"ok"`. `POST /chat` returns JSON with `answer`, `alternate`, `qid`, `aid`. Stop uvicorn with Ctrl+C.

---

## 4. React builds successfully

```bash
cd frontend
npm ci
npm run build
```

**Pass:** Completes with no errors; `frontend/dist/` contains `index.html` and `assets/`.

---

## 5. Frontend + backend locally (integrated)

**Option A — Vite dev + API (recommended for UI dev)**

Terminal 1:

```bash
cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd frontend && npm run dev
```

Open the URL Vite prints (e.g. `http://localhost:5173`). Send a message; confirm a bot reply.  
**Pass:** No console CORS errors if using default relative API + Vite proxy (`vite.config.js`).  
If you use `VITE_API_URL` in `.env.local`, confirm backend **CORS** allows your dev origin.

**Option B — Same as Docker (optional)**

Build UI and point backend at static files (if `backend/static/dist` exists):

```bash
cd frontend && npm run build
mkdir -p ../backend/static/dist && cp -r dist/* ../backend/static/dist/
cd ../backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/`. **Pass:** SPA loads and chat works against same origin.

---

## 6. Docker build works locally

From **repository root** (where `Dockerfile` lives):

```bash
docker build -t pybot-hf-test .
```

Run (maps HF-style port):

```bash
docker run --rm -p 7860:7860 pybot-hf-test
```

Smoke:

```bash
curl -s http://127.0.0.1:7860/health
curl -s -X POST http://127.0.0.1:7860/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"test"}'
```

Open `http://127.0.0.1:7860/` in a browser — UI should load; send one chat.  
**Pass:** Build succeeds; container stays up; health + chat + UI OK.  
**Remind:** Image must include `backend/data` and `backend/artifacts` if those directories are in the build context (not excluded by `.dockerignore`).

---

## 7. Git / Space push (quick)

- [ ] `README.md` has Hugging Face YAML (`sdk: docker`, `app_port: 7860`) if you use card metadata  
- [ ] No secrets in repo (`.env`, API keys)  
- [ ] Large files: confirm Space / Git limits; use Git LFS or external storage if needed  

---

## One-line summary

**Artifacts OK → paths OK → uvicorn OK → `npm run build` OK → dev or Docker smoke OK → then push.**
