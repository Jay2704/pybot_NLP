import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

/**
 * `base` — public path the app is served from. Default `/` (root).
 *
 * **GitHub Pages (this repo, project site):** the Actions workflow sets
 * `VITE_BASE=/pybot_NLP/` so assets and `BrowserRouter` match
 * `https://jay2704.github.io/pybot_NLP/`. Local `npm run dev` leaves `VITE_BASE` unset → `/`.
 *
 * **Other deploys (e.g. Hugging Face single-container):** use `VITE_BASE=/` or omit.
 *
 * Dev server proxies API routes to FastAPI. Override target with `VITE_DEV_PROXY_TARGET` in `.env.local`.
 *
 * `/chat` and `/docs` are both React Router paths (GET) and FastAPI paths. We only proxy when
 * the browser is not doing a GET/HEAD page navigation. OpenAPI on the API host: e.g. :8000/docs.
 */
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const baseRaw = env.VITE_BASE || "/";
  const base =
    baseRaw === "/" || baseRaw === ""
      ? "/"
      : baseRaw.endsWith("/")
        ? baseRaw
        : `${baseRaw}/`;

  const proxyTarget = env.VITE_DEV_PROXY_TARGET || "http://127.0.0.1:8000";

  const proxy = {
    target: proxyTarget,
    changeOrigin: true,
  };

  /** Do not proxy GET/HEAD so the SPA (React Router) is served for deep links and refresh. */
  const spaAware = {
    target: proxyTarget,
    changeOrigin: true,
    bypass(req) {
      const m = req.method || "GET";
      if (m === "GET" || m === "HEAD") {
        return false;
      }
    },
  };

  const apiProxy = {
    "/chat": spaAware,
    "/health": proxy,
    "/docs": spaAware,
    "/openapi.json": proxy,
    "/redoc": proxy,
  };

  return {
    base,
    plugins: [react()],
    server: { proxy: apiProxy },
    preview: { proxy: apiProxy },
  };
});
