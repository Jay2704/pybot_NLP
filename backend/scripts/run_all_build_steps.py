#!/usr/bin/env python3
"""
Run the data/artifact build pipeline in order (subprocess, sequential).

Steps:
  1. build_answers_v2.py
  2. build_final_dataset.py
  3. build_retrieval_artifacts.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(_BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(_BACKEND_DIR))

from app.paths import ARTIFACTS_DIR, DATA_DIR, SCRIPTS_DIR

_STEPS: list[tuple[str, Path]] = [
    ("build_answers_v2.py", SCRIPTS_DIR / "build_answers_v2.py"),
    ("build_final_dataset.py", SCRIPTS_DIR / "build_final_dataset.py"),
    ("build_retrieval_artifacts.py", SCRIPTS_DIR / "build_retrieval_artifacts.py"),
]


def _list_files(root: Path, label: str) -> None:
    print(f"\n--- Files under {label} ({root}) ---")
    if not root.exists():
        print("  (directory does not exist)")
        return
    if not root.is_dir():
        print("  (not a directory)")
        return
    files = sorted(p for p in root.rglob("*") if p.is_file())
    if not files:
        print("  (no files)")
        return
    for f in files:
        print(f"  {f}")


def main() -> int:
    print(f"Backend directory: {_BACKEND_DIR}")
    print("Running build steps sequentially (subprocess)...\n")

    for i, (name, script_path) in enumerate(_STEPS, start=1):
        if not script_path.is_file():
            print(f"[{i}/3] FAIL: script not found: {script_path}", file=sys.stderr)
            return 1

        print(f"[{i}/3] Running {name} ...")
        print(f"        command: {sys.executable} {script_path}")
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(_BACKEND_DIR),
        )
        if result.returncode != 0:
            print(
                f"[{i}/3] FAIL: {name} exited with code {result.returncode}",
                file=sys.stderr,
            )
            return result.returncode

        print(f"[{i}/3] OK: {name}\n")

    print("All build steps completed successfully.\n")
    _list_files(DATA_DIR, "backend/data/")
    _list_files(ARTIFACTS_DIR, "backend/artifacts/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
