#!/usr/bin/env python3
"""
Standalone HTTP checks against the local FastAPI backend.

Assumes the server is running at http://127.0.0.1:8000 (e.g. uvicorn app.main:app).

Usage:
  cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000
  python test_api.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from typing import Any

BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT_S = 120

SAMPLE_PYTHON_QUESTIONS = [
    "How do I read a file in Python?",
    "What is a list comprehension?",
    "How do I install packages with pip?",
    "How do I parse JSON in Python?",
    "What is a virtual environment?",
    "What is the difference between == and is?",
]


def _request_json(
    method: str,
    path: str,
    body: dict[str, Any] | None = None,
) -> tuple[int, Any | str]:
    """Return (status_code, parsed_json) or (status_code, raw_body_str) if JSON decode fails."""
    url = f"{BASE_URL.rstrip('/')}{path}"
    data: bytes | None = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, method=method, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
            raw = resp.read().decode("utf-8")
            status = resp.status
    except urllib.error.HTTPError as exc:
        status = exc.code
        raw = exc.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise ConnectionError(f"Cannot reach {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise ConnectionError(f"Request timed out: {url}") from exc

    if not raw.strip():
        return status, None
    try:
        return status, json.loads(raw)
    except json.JSONDecodeError:
        return status, raw


def _print_response(label: str, status: int, payload: Any) -> None:
    print(f"{label}")
    print(f"  Status: {status}")
    print(f"  JSON:   {json.dumps(payload, indent=2) if isinstance(payload, (dict, list)) else payload!r}")
    print()


def main() -> int:
    print(f"Testing backend at {BASE_URL}\n")

    try:
        status, payload = _request_json("GET", "/health")
    except ConnectionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print("Is the server running? Example: cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8000", file=sys.stderr)
        return 1

    _print_response("GET /health", status, payload)
    if status != 200:
        print("ERROR: /health did not return 200", file=sys.stderr)
        return 1

    for i, question in enumerate(SAMPLE_PYTHON_QUESTIONS, start=1):
        print(f"POST /chat - sample {i}/{len(SAMPLE_PYTHON_QUESTIONS)}")
        print(f"  Question: {question}")
        try:
            status, payload = _request_json(
                "POST",
                "/chat",
                body={"message": question},
            )
        except ConnectionError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 1

        _print_response("  Response", status, payload)
        if status != 200:
            print(f"ERROR: /chat returned {status} for sample {i}", file=sys.stderr)
            return 1

    print("All checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
