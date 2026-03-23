# Final runtime validation — local Docker (before Hugging Face push)

Assumes the container is running with **host port 7860** mapped to the app (e.g. `docker run -p 7860:7860 …`).

---

## 1. App behavior — browser

1. Open **http://127.0.0.1:7860/** (or your mapped host/port).
2. Navigate to the **chat** experience and send a short Python question.
3. **Verify:** You get a **200**-equivalent success in the UI: a bot reply with answer-style content (no HTML error page, no endless spinner).

Use DevTools **Network** only to confirm requests stay **same-origin** for a single-container deploy (no unexpected cross-origin failures).

---

## 2. Browser — what to check

| Check | Pass criteria |
|--------|----------------|
| Load | **http://127.0.0.1:7860/** opens without blank screen or console **red** errors |
| Chat | Send a message → user bubble + bot reply appear |
| Loading | Brief loading state, then clears; no stuck spinner |
| Error UX | If you break the API (stop container), UI shows a clear error (not silent failure) |
| Same origin | No CORS errors in DevTools **Network** for chat traffic (single-container deploy) |

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

- Chat sends and receives successfully in the browser after the container is up.
- UI is readable, responsive enough for a live walkthrough, no obvious layout bugs.
- Responses relate to the question (retrieval working); no 500s under normal use.
- You can explain in one sentence: **TF-IDF + cosine similarity** over **Stack Overflow–style data**, **FastAPI** API, **React** UI, **one Docker** image.

**Optional polish:** If your deployment exposes interactive API docs from FastAPI, you can show them during the demo.

---

## 5. Last step before push

- [ ] Same checks repeated against the **Space URL** after deploy (replace host with your `*.hf.space` URL; use **https**).
- [ ] `README` Space card YAML (`sdk: docker`, `app_port: 7860`) matches reality.
