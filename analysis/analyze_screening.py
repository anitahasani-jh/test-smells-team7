"""Reproduce descriptive statistics for the repository screening CSVs.

These are repository-screening statistics, not Test Smell or causal-study results.
Run from the repository root: python analysis/analyze_screening.py
"""
from __future__ import annotations

import csv
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCREENING = ROOT / "results" / "repository_screening.csv"
STRUCTURE = ROOT / "results" / "repository_structure_screening.csv"
OUTPUT = ROOT / "analysis" / "screening_summary.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def describe(label: str, values: list[int]) -> dict[str, str | int | float]:
    return {
        "measure": label,
        "n": len(values),
        "total": sum(values),
        "mean": round(statistics.mean(values), 3),
        "median": statistics.median(values),
        "minimum": min(values),
        "maximum": max(values),
    }


def main() -> None:
    metadata = read_csv(SCREENING)
    structure = read_csv(STRUCTURE)
    if not metadata or not structure:
        raise SystemExit("Screening input CSV is empty.")
    if len(metadata) != len(structure):
        raise SystemExit("Metadata and structure files have different row counts.")

    by_repo = {row["repo_full_name"]: row for row in structure}
    if set(by_repo) != {row["repo_full_name"] for row in metadata}:
        raise SystemExit("Repository names do not match between screening files.")

    measures = {
        "estimated_java_test_files": [int(r["java_test_file_count_estimate"]) for r in structure],
        "java_files": [int(r["java_file_count"]) for r in structure],
        "github_stars": [int(r["stars"]) for r in metadata],
        "github_forks": [int(r["forks"]) for r in metadata],
        "maven_files": [int(r["pom_xml_count"]) for r in structure],
        "gradle_files": [int(r["gradle_file_count"]) for r in structure],
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["measure", "n", "total", "mean", "median", "minimum", "maximum"],
        )
        writer.writeheader()
        for label, values in measures.items():
            writer.writerow(describe(label, values))

    print(f"Repositories analyzed: {len(metadata)}")
    print(f"Summary written to: {OUTPUT.relative_to(ROOT)}")
    for label, values in measures.items():
        result = describe(label, values)
        print(
            f"{label}: n={result['n']}, total={result['total']}, "
            f"mean={result['mean']}, median={result['median']}, "
            f"min={result['minimum']}, max={result['maximum']}"
        )


if __name__ == "__main__":
    main()
