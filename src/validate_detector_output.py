"""Validate real Test Smell detector CSV output before dataset construction.

This tool checks structure only. It never creates, changes, or infers smell labels.
"""
import argparse
import csv
from pathlib import Path


def validate_detector_csv(path: str) -> dict:
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Detector CSV not found: {file_path}")

    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = reader.fieldnames
        if not fields:
            raise ValueError("Detector CSV is empty or has no header.")
        if "commit_hash" not in fields:
            raise ValueError("Detector CSV must contain a 'commit_hash' column.")

        row_count = 0
        empty_hash_rows = []
        commit_hashes = set()
        for row_number, row in enumerate(reader, start=2):
            row_count += 1
            commit_hash = (row.get("commit_hash") or "").strip()
            if not commit_hash:
                empty_hash_rows.append(row_number)
            else:
                commit_hashes.add(commit_hash)

    if row_count == 0:
        raise ValueError("Detector CSV has a header but no data rows.")
    if empty_hash_rows:
        preview = ", ".join(map(str, empty_hash_rows[:10]))
        suffix = " ..." if len(empty_hash_rows) > 10 else ""
        raise ValueError(f"Empty commit_hash at CSV row(s): {preview}{suffix}")

    return {
        "path": str(file_path),
        "rows": row_count,
        "unique_commits": len(commit_hashes),
        "columns": fields,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "detector_csv",
        nargs="?",
        default="results/test_smell_detections.csv",
        help="CSV exported by the approved detector",
    )
    args = parser.parse_args()
    try:
        report = validate_detector_csv(args.detector_csv)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))

    print("Detector CSV structure: OK")
    print(f"Rows: {report['rows']}")
    print(f"Unique commits: {report['unique_commits']}")
    print(f"Columns: {', '.join(report['columns'])}")
    print("Note: this validates structure only; it does not verify detector correctness.")


if __name__ == "__main__":
    main()
