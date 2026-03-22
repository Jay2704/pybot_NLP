#!/bin/sh
set -e
# Hugging Face Spaces: bind all interfaces; PORT is usually 7860.
export PORT="${PORT:-7860}"
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT"
