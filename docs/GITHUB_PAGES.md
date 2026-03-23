# GitHub Pages (frontend only)

The workflow **`.github/workflows/deploy.yml`** builds **`frontend/`** with Vite and publishes **`frontend/dist`** to **GitHub Pages**. The FastAPI backend stays deployed separately (e.g. Hugging Face); the static site calls it using **`VITE_API_URL`** baked in at build time.

**Live site (this repo):** [https://jay2704.github.io/pybot_NLP/](https://jay2704.github.io/pybot_NLP/)

---

## One-time setup

1. **Repository → Settings → Pages**
   - **Source:** **GitHub Actions** (not “Deploy from a branch”).

2. **`VITE_API_URL`** for the build (Settings → Secrets and variables → Actions)
   - Add a **Variable** named **`VITE_API_URL`**, or a **Secret** with the same name.
   - Value: your live API origin, **HTTPS**, **no trailing slash**, e.g. `https://your-space.hf.space`  
   - Injected at build time into the client (`frontend/src/services/api.js`). The workflow fails the build if this is missing.

3. **Backend CORS**
   - Allow **`https://jay2704.github.io`** (GitHub Pages sends the browser origin as `https://jay2704.github.io`, not the full path).

4. Push to **`main`** (with changes under `frontend/` or the workflow), or run **Actions → Deploy frontend to GitHub Pages → Run workflow**.

---

## How it works

| Item | Purpose |
|------|---------|
| **`VITE_BASE`** | Set in CI to `/pybot_NLP/` so assets and routes match the project URL. |
| **`VITE_API_URL`** | Repository variable or secret; chat `fetch` goes to `VITE_API_URL` + `/chat`. |
| **`BrowserRouter` `basename`** | Derived from Vite `import.meta.env.BASE_URL` so React Router matches the subpath. |
| **`.nojekyll`** | Disables Jekyll so static files are served as-is. |
| **`404.html`** | Copy of `index.html` so refreshes on deep links (e.g. `/repo/chat`) still load the SPA. |

Local development is unchanged: leave **`VITE_API_URL`** unset and use **`npm run dev`** with the Vite proxy.

---

## Verify

- Open **https://jay2704.github.io/pybot_NLP/** after the workflow succeeds.
- Hard refresh; open DevTools → Network and confirm chat **POST** goes to your **`VITE_API_URL`** host.
- If chat fails with CORS, fix **`CORS_EXTRA_ORIGINS`** on the API to include `https://<username>.github.io`.

---

## Common issues

| Issue | What to check |
|--------|----------------|
| Blank page or wrong assets | `VITE_BASE` must match the repo name segment in the URL; rebuild after changing it. |
| Chat always fails | `VITE_API_URL` missing or wrong variable; CORS on backend. |
| 404 on refresh on `/chat` | Workflow must copy **`404.html`**; re-run latest workflow. |

See also **`docs/FRONTEND_DEPLOY_HF.md`** for the full-stack Docker / Hugging Face flow.
