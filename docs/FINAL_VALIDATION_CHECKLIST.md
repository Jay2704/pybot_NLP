# Final runtime validation — local Docker (before Hugging Face push)

Assumes the container is running with **host port 7860** mapped to the app (e.g. `docker run -p 7860:7860 …`).

---

## 1. API — copy/paste

**Health**

```bash
curl -sS http://127.0.0.1:7860/health
```

**Verify:** JSON includes `"status":"ok"` (or your `HealthResponse` shape).

**Chat**

```bash
curl -sS -X POST http://127.0.0.1:7860/chat \
  -H 'Content-Type: application/json' \
  -d '{"message":"What is list comprehension in Python?"}'
```

**Verify:** HTTP **200**; JSON has **`answer`** (string), **`alternate`**, **`qid`**, **`aid`** (numbers). No HTML error page.

---

## 2. Browser — what to check

| Check | Pass criteria |
|--------|----------------|
| Load | **http://127.0.0.1:7860/** opens without blank screen or console **red** errors |
| Chat | Send a message → user bubble + bot reply appear |
| Loading | Brief loading state, then clears; no stuck spinner |
| Error UX | If you break the API (stop container), UI shows a clear error (not silent failure) |
| Same origin | No CORS errors in DevTools **Network** for `POST /chat` (single-container deploy) |

---

## 3. Five Python questions (manual)

Ask these one at a time; expect a coherent, on-topic **answer** text each time.

1. What is list comprehension in Python?
2. How does a Python decorator work?
3. What is the difference between `is` and `==` in Python?
4. Explain Python's Global Interpreter Lock (GIL).
5. How do you handle exceptions in Python?

---

## 4. Recruiter-demo readiness (green flags)

- **`/health`** and **`/chat`** succeed with the commands above.
- UI is readable, responsive enough for a live walkthrough, no obvious layout bugs.
- Responses relate to the question (retrieval working); no 500s under normal use.
- You can explain in one sentence: **TF-IDF + cosine similarity** over **Stack Overflow–style data**, **FastAPI** API, **React** UI, **one Docker** image.

**Optional polish:** Open **`/docs`** if you want to show OpenAPI during the demo.

---

## 5. Last step before push

- [ ] Same checks repeated against the **Space URL** after deploy (replace host with your `*.hf.space` URL; use **https**).
- [ ] `README` Space card YAML (`sdk: docker`, `app_port: 7860`) matches reality.
