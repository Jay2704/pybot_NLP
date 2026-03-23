# Frontend-only deployment workflow (Hugging Face Docker Space)

This project ships as **one Docker image**: stage 1 runs `npm ci` + `npm run build` in `frontend/`; stage 2 copies `frontend/dist` → `backend/static/dist` and runs FastAPI. **Backend Python code is unchanged** when you only edit React; the image still rebuilds, but the meaningful diff is under `frontend/`.

See also: **`docs/HF_SPACE.md`** (architecture), **`docs/DOCKER_LOCAL.md`** (full local Docker test).

---

## 1. Local development (daily)

1. **Install once (or after `package-lock.json` changes):**

   ```bash
   cd frontend && npm ci
   ```

2. **Run the API** (chat + same-origin behavior in prod):

   ```bash
   cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

3. **Run Vite** (separate terminal):

   ```bash
   cd frontend && npm run dev
   ```

4. Open the URL Vite prints (usually **http://127.0.0.1:5173**). The dev server **proxies** API traffic to the backend; deep links to routes like `/chat` and `/docs` are handled by the SPA (see `vite.config.js`).

**Optional:** If you only change static copy and never hit the API, you can run `npm run dev` alone; chat will fail until the API is up.

---

## 2. How to test React locally (before pushing)

| Goal | Command / action |
|------|------------------|
| **Lint / type sanity** | `cd frontend && npm run build` — must finish with no errors. |
| **Production bundle** | Same: `npm run build` produces `frontend/dist/` (hash-named JS/CSS). |
| **Prod-like preview** | `npm run preview` — serves the built files; **start the API** on `:8000` if you need chat (configure proxy if you use preview). |
| **Full stack like HF** | From repo root: `docker build -t pybot-hf:local .` then `docker run --rm -p 7860:7860 -e PORT=7860 pybot-hf:local` — open **http://127.0.0.1:7860** (same as Space). |

**Manual checks:** Home, Chatbot, Features, Docs, Login/Signup — navigate and refresh on each; confirm no blank screen and console errors.

---

## 3. Pushing “frontend-only” updates to Hugging Face

Hugging Face **Docker Spaces** rebuild from your **Git** repository; there is no separate “upload frontend only” button for this image.

1. **Change only what you need** under `frontend/` (and commit `frontend/package-lock.json` if dependencies changed).

2. **Verify locally:** `cd frontend && npm run build`.

3. **Commit and push** to the branch your Space tracks (usually `main`):

   ```bash
   git add frontend/
   git status   # confirm no accidental backend edits
   git commit -m "Describe UI change"
   git push origin main
   ```

4. In the **Space → Settings / Logs**, wait for the **Build** to finish and the app to show **Running**.

**Note:** The Dockerfile always runs the **Node** stage; a frontend-only commit still triggers a **full image build**, but the backend layer is often cached. The important part is that `COPY frontend/` and `npm run build` pick up your latest UI.

---

## 4. Verifying the live frontend deployed successfully

1. **Open the Space URL** (e.g. `https://<user>-<space>.hf.space`).

2. **Hard refresh** once: **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (macOS) to avoid a cached old `index.html`.

3. **DevTools → Network:**
   - **JS/CSS** under `assets/` should load with **200** (not 404).
   - Filenames should include **content hashes** (e.g. `index-xxxxx.js`), and they **change** when you deploy a new build.

4. **Spot-check** the UI change you shipped (copy, layout, new route).

5. **Smoke-test chat** if you touched the chat page or API client.

---

## 5. Common issues

### Stale assets (old UI after deploy)

- **Cause:** Browser or CDN caching `index.html` or old hashed chunks.
- **Fix:** Hard refresh; try incognito; wait a minute and retry; confirm the build log shows a successful **npm run build** and new image.

### Broken routes (404 on refresh, or `/chat` not loading)

- **Production (Docker / HF):** FastAPI serves the SPA with **`StaticFiles(..., html=True)`**, so unknown paths get `index.html`. If you see 404 on refresh, the SPA mount may be missing or the build is old.
- **Local dev:** Vite must not proxy **GET** requests for SPA routes to the API; this repo uses **proxy bypass** for `/chat` and `/docs` (see `vite.config.js`).

### Missing CSS or wrong styles

- **Cause:** Build failed partially; wrong `dist/` copied; or cached HTML pointing at old hashed CSS.
- **Fix:** Run `npm run build` locally and confirm `dist/assets/*.css` exists; redeploy; hard refresh.

### Chat works in dev but not on Space

- **Cause:** `VITE_API_URL` set to localhost in a **production** build; or CORS / wrong origin.
- **Fix:** For same-origin HF, **leave `VITE_API_URL` unset** in the build so the browser calls the same host as the page.

### OpenAPI vs React “Docs” in dev

- On **Vite** (`:5173`), **`/docs`** is the **React** documentation page. FastAPI Swagger is on the API host directly (e.g. **http://127.0.0.1:8000/docs**).

---

## Summary checklist (frontend-only change)

- [ ] `cd frontend && npm run build` passes  
- [ ] `git push` only includes intended `frontend/` (and lockfile if needed)  
- [ ] Space build completes; hard refresh live URL  
- [ ] Routes + styles + chat smoke-test on live URL  

No backend logic changes are required for a typical UI-only release.
