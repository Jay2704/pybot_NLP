#!/usr/bin/env python3
"""
Verify retrieval artifact files exist under backend/artifacts/, print sizes, and test read.

Run from repo root or backend/:
  python3 backend/debug/verify_artifacts_for_deploy.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# backend/debug/ -> backend/
BACKEND = Path(__file__).resolve().parent.parent
ARTIFACTS = BACKEND / "artifacts"
REQUIRED = (
    "vectorizer.pkl",
    "question_vectors.pkl",
    "chatbot_df.pkl",
)


def main() -> int:
    print(f"backend root: {BACKEND}")
    print(f"artifacts dir: {ARTIFACTS}")
    if not ARTIFACTS.is_dir():
        print("ERROR: artifacts directory does not exist")
        return 1

    ok = True
    for name in REQUIRED:
        p = ARTIFACTS / name
        if not p.is_file():
            print(f"MISSING: {p}")
            ok = False
            continue
        size = p.stat().st_size
        print(f"OK  {p}  ({size:,} bytes)")
        try:
            with open(p, "rb") as f:
                f.read(1)
            print("    readable: yes")
        except OSError as e:
            print(f"    readable: NO — {e}")
            ok = False

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
