#!/usr/bin/env python3
"""
Inspect and print the structure of data files in a folder.

CSV/TSV uses the standard library only (no pandas), so it runs in minimal
Python installs (e.g. Code Runner) and streams large files without loading
them entirely into memory.

Usage:
  python view_data_structure.py
  python view_data_structure.py --data-dir "pybot_data"
  python view_data_structure.py --data-dir "/full/path/to/data"
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Iterable


SUPPORTED_EXTENSIONS = {".csv", ".json", ".txt", ".tsv"}


def format_size(size_in_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_in_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size_in_bytes} B"


def get_files(data_dir: Path) -> Iterable[Path]:
    return sorted(
        [p for p in data_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS],
        key=lambda p: p.name.lower(),
    )


def _truncate_cell(value: str, max_len: int = 120) -> str:
    value = value.replace("\n", "\\n").replace("\r", "\\r")
    if len(value) <= max_len:
        return value
    return value[: max_len - 3] + "..."


def inspect_csv_tsv(path: Path, delimiter: str) -> None:
    """Stream CSV/TSV with stdlib only (no pandas) — works in minimal Python envs."""
    encodings = ("utf-8", "latin-1", "cp1252")
    last_decode_error: UnicodeDecodeError | None = None
    used_encoding: str | None = None
    header: list[str] = []
    num_cols = 0
    data_rows = 0
    sample_rows: list[list[str]] = []

    for encoding in encodings:
        try:
            with path.open("r", encoding=encoding, newline="") as f:
                reader = csv.reader(f, delimiter=delimiter)
                try:
                    header = next(reader)
                except StopIteration:
                    header = []
                    num_cols = 0
                    data_rows = 0
                    sample_rows = []
                    used_encoding = encoding
                    break
                num_cols = len(header)
                sample_rows = []
                data_rows = 0
                for row in reader:
                    data_rows += 1
                    if len(sample_rows) < 3:
                        sample_rows.append(row)
            used_encoding = encoding
            break
        except UnicodeDecodeError as exc:
            last_decode_error = exc
            continue

    if used_encoding is None:
        raise RuntimeError(
            f"Could not decode with encodings {encodings}: {last_decode_error}"
        ) from last_decode_error

    if used_encoding != "utf-8":
        print(f"  - Encoding: {used_encoding} (fallback)")

    print(f"  - Shape: {data_rows} data rows x {num_cols} columns")
    print("  - Columns:")
    for col in header:
        print(f"      * {col}")
    print("  - Sample rows (cells truncated for display):")
    if not sample_rows and data_rows == 0:
        print("      (no data rows)")
    for i, row in enumerate(sample_rows, start=1):
        shown = [_truncate_cell(c) for c in row]
        print(f"      Row {i}: {shown}")


def inspect_json(path: Path) -> None:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        print(f"  - Top-level type: list ({len(data)} items)")
        if data and isinstance(data[0], dict):
            keys = sorted(data[0].keys())
            print(f"  - Item type: object with keys: {', '.join(keys)}")
        elif data:
            print(f"  - Item type: {type(data[0]).__name__}")
    elif isinstance(data, dict):
        keys = sorted(data.keys())
        print(f"  - Top-level type: object with {len(keys)} keys")
        print(f"  - Keys: {', '.join(keys[:20])}{' ...' if len(keys) > 20 else ''}")
    else:
        print(f"  - Top-level type: {type(data).__name__}")


def inspect_txt(path: Path) -> None:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    print(f"  - Lines: {len(lines)}")
    preview = "".join(lines[:3]).strip()
    if preview:
        print("  - Preview:")
        for line in preview.splitlines():
            print(f"      {line}")


def inspect_file(path: Path) -> None:
    print(f"\nFile: {path.name}")
    print(f"  - Type: {path.suffix.lower()[1:] or 'unknown'}")
    print(f"  - Size: {format_size(path.stat().st_size)}")

    suffix = path.suffix.lower()
    try:
        if suffix == ".csv":
            inspect_csv_tsv(path, delimiter=",")
        elif suffix == ".tsv":
            inspect_csv_tsv(path, delimiter="\t")
        elif suffix == ".json":
            inspect_json(path)
        elif suffix == ".txt":
            inspect_txt(path)
        else:
            print("  - No inspector implemented for this format.")
    except Exception as exc:  # noqa: BLE001 - user-facing utility script
        print(f"  - Could not inspect file details: {exc}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="View data structure in a dataset folder.")
    parser.add_argument(
        "--data-dir",
        default="pybot_data",
        help="Path to data folder (default: pybot_data)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_dir = Path(args.data_dir).expanduser().resolve()

    print("=" * 70)
    print("PyBot Data Structure Viewer")
    print("=" * 70)
    print(f"Data directory: {data_dir}")

    if not data_dir.exists():
        print("\nThe data directory does not exist.")
        print("Create it or pass another path with --data-dir.")
        return

    if not data_dir.is_dir():
        print("\nThe provided path is not a directory.")
        return

    files = list(get_files(data_dir))
    if not files:
        print("\nNo supported data files found.")
        print("Supported extensions: .csv, .tsv, .json, .txt")
        return

    print(f"\nFound {len(files)} supported file(s).")
    for file_path in files:
        inspect_file(file_path)

    print("\nDone.")


if __name__ == "__main__":
    main()
