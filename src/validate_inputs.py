"""Validate study CSV inputs without manufacturing missing measurements.

Usage:
    python src/validate_inputs.py --manifest data/repository_manifest.csv
    python src/validate_inputs.py --detections results/test_smell_detections.csv
    python src/validate_inputs.py --outcomes data/outcome_metrics.csv
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

REQUIRED = {
    "manifest": {"repo_full_name", "clone_url", "pinned_commit_sha", "inclusion_status"},
    "detections": {"repo_full_name", "commit_sha", "test_file_path", "smell_name", "detector_name", "detector_version"},
    "outcomes": {"repo_full_name", "commit_sha", "test_file_path", "smell_present", "mutation_run_status"},
}

def validate_csv(path: Path, kind: str) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"File not found: {path}"]
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = REQUIRED[kind] - headers
            if missing:
                errors.append("Missing required columns: " + ", ".join(sorted(missing)))
                return errors
            count = 0
            for line_no, row in enumerate(reader, start=2):
                count += 1
                for key in REQUIRED[kind]:
                    if not (row.get(key) or "").strip():
                        errors.append(f"Line {line_no}: required field {key!r} is blank")
            if count == 0:
                errors.append("CSV has a header but no data rows.")
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"Could not read CSV: {exc}")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--manifest", type=Path)
    group.add_argument("--detections", type=Path)
    group.add_argument("--outcomes", type=Path)
    args = parser.parse_args()
    path = args.manifest or args.detections or args.outcomes
    kind = "manifest" if args.manifest else "detections" if args.detections else "outcomes"
    errors = validate_csv(path, kind)
    if errors:
        print(f"Validation FAILED for {path}:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validation passed for {path}. This checks structure only, not research validity.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
