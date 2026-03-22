#!/usr/bin/env python3
"""
Inspect backend/artifacts and backend/data — read-only; no data modification.

Run:
  python backend/debug/check_files.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# backend/debug/check_files.py -> parents[2] = repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = REPO_ROOT / "backend" / "artifacts"
DATA_DIR = REPO_ROOT / "backend" / "data"

SCAN_TARGETS = [
    ("artifacts", ARTIFACTS_DIR),
    ("data", DATA_DIR),
]


def _size_mb(path: Path) -> float:
    return path.stat().st_size / (1024 * 1024)


def _collect_files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    return sorted(p for p in root.rglob("*") if p.is_file())


def _primary_category(path: Path) -> str:
    """Single bucket per file for the summary report."""
    name = path.name.lower()
    suf = path.suffix.lower()

    if suf == ".pkl" and "vectorizer" in name:
        return "vectorizer files (.pkl)"

    if suf == ".pkl":
        if (
            "question_vector" in name
            or ("vector" in name and "vectorizer" not in name)
            or "matrix" in name
            or "tfidf" in name
        ):
            return "tfidf / vector files (.pkl)"
        if any(x in name for x in ("chatbot", "final", "dataset")) or name.endswith(
            "_df.pkl"
        ):
            return "dataframe / dataset files (.csv or .pkl)"
        if "data" in name and "vector" not in name:
            return "dataframe / dataset files (.csv or .pkl)"
        return "other (.pkl)"

    if suf == ".csv":
        return "dataframe / dataset files (.csv or .pkl)"

    return f"other ({suf or 'no extension'})"


def _likely_vectorizer(paths: list[Path]) -> list[Path]:
    return sorted(p for p in paths if "vectorizer" in p.name.lower())


def _likely_vectors(paths: list[Path]) -> list[Path]:
    out = []
    for p in paths:
        low = p.name.lower()
        if "vectorizer" in low:
            continue
        if "vector" in low or "matrix" in low:
            out.append(p)
    return sorted(out)


def _likely_dataset(paths: list[Path]) -> list[Path]:
    return sorted(
        p for p in paths if any(x in p.name.lower() for x in ("data", "df", "chatbot"))
    )


def _summary_line(paths: list[Path]) -> str:
    if not paths:
        return "<not found>"
    if len(paths) == 1:
        return str(paths[0])
    return f"{paths[0]}  (+ {len(paths) - 1} more)"


def main() -> int:
    print(f"Repo root: {REPO_ROOT}")
    print("Scanning (read-only): backend/artifacts/, backend/data/\n")

    all_files: list[Path] = []

    for label, directory in SCAN_TARGETS:
        print(f"=== {label}: {directory} ===")
        if not directory.exists():
            print("  (folder missing — skipped)\n")
            continue
        if not directory.is_dir():
            print("  (not a directory — skipped)\n")
            continue

        found = _collect_files(directory)
        if not found:
            print("  (no files)\n")
            continue

        for f in found:
            all_files.append(f)
            try:
                mb = _size_mb(f)
            except OSError as exc:
                print(f"  ERROR stat {f}: {exc}", file=sys.stderr)
                continue
            print(f"  File: {f.name}")
            print(f"    Path: {f}")
            print(f"    Size: {mb:.4f} MB")
            print()

    # Categorization
    by_cat: dict[str, list[Path]] = {}
    for p in all_files:
        cat = _primary_category(p)
        by_cat.setdefault(cat, []).append(p)

    print("=== Categorization ===")
    if not all_files:
        print("  (no files to categorize)\n")
    else:
        for cat in sorted(by_cat.keys()):
            print(f"  {cat}:")
            for p in sorted(by_cat[cat], key=lambda x: str(x)):
                print(f"    - {p}")
            print()

    lv = _likely_vectorizer(all_files)
    lvec = _likely_vectors(all_files)
    lds = _likely_dataset(all_files)

    print("=== Likely role (by filename) ===")
    print(f"  vectorizer (name contains 'vectorizer'): {len(lv)} file(s)")
    for p in lv:
        print(f"    - {p}")
    print(
        f"  vectors (name contains 'vector' or 'matrix', excluding vectorizer): "
        f"{len(lvec)} file(s)"
    )
    for p in lvec:
        print(f"    - {p}")
    print(
        f"  dataset (name contains 'data', 'df', or 'chatbot'): {len(lds)} file(s)"
    )
    for p in lds:
        print(f"    - {p}")
    print()

    print("=== Summary ===")
    print(f"  vectorizer: {_summary_line(lv)}")
    print(f"  vectors:    {_summary_line(lvec)}")
    print(f"  dataset:    {_summary_line(lds)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
