# Hugging Face Space (sdk: docker) — single container: FastAPI + Vite-built React SPA.
# Runtime listens on 0.0.0.0; default PORT=7860 (HF may set PORT).

# ---- Stage 1: build React (npm) ----
FROM node:20-bookworm-slim AS web-build
WORKDIR /frontend

COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# ---- Stage 2: FastAPI + static files ----
FROM python:3.12-slim-bookworm AS runtime
WORKDIR /app/backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./
# Matches backend/static/dist resolution in app.paths.resolve_frontend_dist_dir()
COPY --from=web-build /frontend/dist ./static/dist

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 7860

ENTRYPOINT ["/entrypoint.sh"]
