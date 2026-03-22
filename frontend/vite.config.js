import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

/**
 * Dev server proxies API routes to FastAPI so the browser uses relative URLs (no hardcoded
 * API host in the bundle). Override target with VITE_DEV_PROXY_TARGET in .env.local.
 */
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const proxyTarget = env.VITE_DEV_PROXY_TARGET || "http://127.0.0.1:8000";

  const proxy = {
    target: proxyTarget,
    changeOrigin: true,
  };

  const apiProxy = {
    "/chat": proxy,
    "/health": proxy,
    "/docs": proxy,
    "/openapi.json": proxy,
    "/redoc": proxy,
  };

  return {
    plugins: [react()],
    server: { proxy: apiProxy },
    preview: { proxy: apiProxy },
  };
});
