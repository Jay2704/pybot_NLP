# Local Docker testing (Hugging Face–style)

Same image as the Space: **port 7860**, **0.0.0.0** inside the container. No application code changes—only how you build and run the container.

**Prerequisites:** Docker Desktop or Docker Engine (Mac/Linux), repo at machine-readable paths; `backend/data` and `backend/artifacts` must be present in the build context if the app needs them at runtime.

---

## 1. Build the image

From the **repository root** (where `Dockerfile` is):

```bash
docker build -t pybot-hf:local .
```

---

## 2. Run the container

**Foreground** (logs in terminal; stop with Ctrl+C):

```bash
docker run --rm -p 7860:7860 -e PORT=7860 pybot-hf:local
```

**Detached** (background):

```bash
docker run -d --name pybot-hf -p 7860:7860 -e PORT=7860 pybot-hf:local
```

Stop and remove later:

```bash
docker stop pybot-hf && docker rm pybot-hf
```

---

## 3. Test in the browser

1. Open: **http://127.0.0.1:7860/**  
2. Confirm the chat UI loads.  
3. Send a message and verify a reply.

Optional API checks in another terminal:

```bash
curl -s http://127.0.0.1:7860/health
curl -s -X POST http://127.0.0.1:7860/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What is a list comprehension in Python?"}'
```

---

## Optional: Docker Compose (same behavior)

From the repo root:

```bash
docker compose up --build
```

Then open **http://127.0.0.1:7860/** . Stop with Ctrl+C, or:

```bash
docker compose down
```

(See `docker-compose.yml` in the repo root.)

---

## Troubleshooting

| Issue | What to check |
|--------|----------------|
| Build fails | Run from repo root; ensure `frontend/package-lock.json` exists. |
| 500 on `/chat` | Image may lack `backend/artifacts` or `backend/data`; confirm they are not excluded and are committed or copied into the context. |
| Blank page | Confirm `backend/static/dist` was produced in the image (Dockerfile copies Vite `dist` there). |
| Port in use | Change host mapping: `-p 8080:7860` and open `http://127.0.0.1:8080/`. |
