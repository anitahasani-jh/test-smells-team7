"""Screen candidate GitHub repositories and save metadata to CSV.

Usage:
    python src/screen_repositories.py
    python src/screen_repositories.py --input data/repository_candidates.csv --output results/repository_screening.csv

This script records GitHub metadata only. It does NOT prove that a repository
contains enough Java tests or that a smell detector/PIT can run successfully.
Those require subsequent validation.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "data" / "repository_candidates.csv"
DEFAULT_OUTPUT = ROOT / "results" / "repository_screening.csv"
API_ROOT = "https://api.github.com/repos/"


def github_get(repo_full_name: str, token: str | None = None) -> dict:
    """Fetch one repository's metadata from the GitHub REST API."""
    request = Request(
        API_ROOT + repo_full_name,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "test-smells-team7-research",
        },
    )
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def screen_repositories(input_csv: Path, output_csv: Path, token: str | None = None) -> int:
    if not input_csv.exists():
        raise FileNotFoundError(
            f"Candidate CSV not found: {input_csv}\n"
            "Run this script from the repository root or pass --input."
        )

    with input_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "repo_full_name" not in reader.fieldnames:
            raise ValueError("Input CSV must contain a 'repo_full_name' column.")
        candidates = list(reader)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "repo_full_name", "html_url", "description", "language", "stars",
        "forks", "open_issues", "archived", "disabled", "created_at",
        "pushed_at", "default_branch", "license_spdx_id", "size_kb",
        "metadata_checked_at_utc", "screening_status", "error",
    ]
    checked_at = datetime.now(timezone.utc).isoformat()
    successes = 0

    with output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in candidates:
            name = (row.get("repo_full_name") or "").strip()
            result = {field: "" for field in fields}
            result["repo_full_name"] = name
            result["metadata_checked_at_utc"] = checked_at

            if not name or "/" not in name:
                result["screening_status"] = "invalid_candidate_name"
                result["error"] = "Expected owner/repository format."
                writer.writerow(result)
                continue

            try:
                data = github_get(name, token)
                license_data = data.get("license") or {}
                result.update({
                    "html_url": data.get("html_url", ""),
                    "description": data.get("description") or "",
                    "language": data.get("language") or "",
                    "stars": data.get("stargazers_count", ""),
                    "forks": data.get("forks_count", ""),
                    "open_issues": data.get("open_issues_count", ""),
                    "archived": data.get("archived", ""),
                    "disabled": data.get("disabled", ""),
                    "created_at": data.get("created_at", ""),
                    "pushed_at": data.get("pushed_at", ""),
                    "default_branch": data.get("default_branch", ""),
                    "license_spdx_id": license_data.get("spdx_id", ""),
                    "size_kb": data.get("size", ""),
                    "screening_status": "metadata_collected",
                    "error": "",
                })
                successes += 1
                print(f"[OK] {name}: language={result['language']}, stars={result['stars']}")
            except HTTPError as exc:
                detail = "Not found or access denied." if exc.code in (403, 404) else f"HTTP {exc.code}"
                result["screening_status"] = "request_failed"
                result["error"] = detail
                print(f"[WARN] {name}: {detail}", file=sys.stderr)
                if exc.code == 403:
                    print("GitHub rate limit may be reached; set GITHUB_TOKEN and retry.", file=sys.stderr)
            except (URLError, TimeoutError, json.JSONDecodeError) as exc:
                result["screening_status"] = "request_failed"
                result["error"] = str(exc)
                print(f"[WARN] {name}: {exc}", file=sys.stderr)

            writer.writerow(result)
            handle.flush()
            time.sleep(0.15)

    print(f"\nFinished: {successes}/{len(candidates)} repositories fetched.")
    print(f"Output: {output_csv}")
    print("Next: inspect Java test files, build/test instructions, detector compatibility, and pin each chosen repository to a commit SHA.")
    return successes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Candidate CSV path")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output CSV path")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    try:
        screen_repositories(args.input, args.output, token)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
