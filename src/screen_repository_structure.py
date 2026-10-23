#!/usr/bin/env python3
"""Screen candidate GitHub repositories by tree metadata without cloning them.

This is an initial structural screen, not proof that tests build or that a smell
detector / PIT can run. GitHub's recursive tree response may be truncated for
very large repositories; check tree_truncated before relying on counts.
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
DEFAULT_OUTPUT = ROOT / "results" / "repository_structure_screening.csv"
API_BASE = "https://api.github.com"


def github_get(url: str, token: str | None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "test-smells-team7-repository-screening",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def count_paths(paths: list[str]) -> tuple[int, int, int, int]:
    java_test_files = [
        p for p in paths
        if p.lower().endswith(".java")
        and (
            "/test/" in f"/{p.lower()}"
            or p.lower().startswith("test/")
            or "/tests/" in f"/{p.lower()}"
            or p.lower().startswith("tests/")
        )
    ]
    java_files = [p for p in paths if p.lower().endswith(".java")]
    pom_files = [p for p in paths if p.rsplit("/", 1)[-1] == "pom.xml"]
    gradle_files = [
        p for p in paths
        if p.rsplit("/", 1)[-1] in {
            "build.gradle", "build.gradle.kts", "settings.gradle",
            "settings.gradle.kts", "gradlew", "gradlew.bat"
        }
    ]
    return len(java_test_files), len(java_files), len(pom_files), len(gradle_files)


def screen_one(repo_name: str, token: str | None) -> dict:
    checked_at = datetime.now(timezone.utc).isoformat()
    result = {
        "repo_full_name": repo_name,
        "checked_at_utc": checked_at,
        "default_branch": "",
        "head_commit_sha": "",
        "archived": "",
        "language": "",
        "stars": "",
        "forks": "",
        "license_spdx_id": "",
        "tree_truncated": "",
        "java_test_file_count_estimate": "",
        "java_file_count": "",
        "pom_xml_count": "",
        "gradle_file_count": "",
        "test_paths_sample": "",
        "screening_status": "",
        "error": "",
        "interpretation_note": (
            "Tree-based estimate only; not a build, detector-compatibility, "
            "or PIT execution result."
        ),
    }
    try:
        repo = github_get(f"{API_BASE}/repos/{repo_name}", token)
        branch = repo.get("default_branch", "")
        result.update({
            "default_branch": branch,
            "archived": repo.get("archived", ""),
            "language": repo.get("language") or "",
            "stars": repo.get("stargazers_count", ""),
            "forks": repo.get("forks_count", ""),
            "license_spdx_id": (repo.get("license") or {}).get("spdx_id", ""),
        })
        branch_info = github_get(
            f"{API_BASE}/repos/{repo_name}/branches/{branch}", token
        )
        sha = branch_info.get("commit", {}).get("sha", "")
        result["head_commit_sha"] = sha
        if not sha:
            raise ValueError("GitHub did not return the branch head commit SHA")

        tree = github_get(
            f"{API_BASE}/repos/{repo_name}/git/trees/{sha}?recursive=1", token
        )
        paths = [
            item.get("path", "")
            for item in tree.get("tree", [])
            if item.get("type") == "blob"
        ]
        test_count, java_count, pom_count, gradle_count = count_paths(paths)
        test_paths = [
            p for p in paths
            if p.lower().endswith(".java")
            and (
                "/test/" in f"/{p.lower()}"
                or p.lower().startswith("test/")
                or "/tests/" in f"/{p.lower()}"
                or p.lower().startswith("tests/")
            )
        ]
        result.update({
            "tree_truncated": tree.get("truncated", ""),
            "java_test_file_count_estimate": test_count,
            "java_file_count": java_count,
            "pom_xml_count": pom_count,
            "gradle_file_count": gradle_count,
            "test_paths_sample": " ; ".join(test_paths[:10]),
            "screening_status": (
                "tree_truncated_review_required"
                if tree.get("truncated")
                else "structure_metadata_collected"
            ),
        })
    except HTTPError as exc:
        result["screening_status"] = "http_error"
        result["error"] = f"HTTP {exc.code}: {exc.reason}"
    except (URLError, TimeoutError) as exc:
        result["screening_status"] = "network_error"
        result["error"] = str(exc)
    except (json.JSONDecodeError, ValueError, KeyError) as exc:
        result["screening_status"] = "response_error"
        result["error"] = str(exc)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate Java test/build structure for candidate repositories."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--delay", type=float, default=0.25,
        help="Seconds to wait between repositories (default: 0.25)."
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Input CSV not found: {args.input}", file=sys.stderr)
        return 2

    token = os.environ.get("GITHUB_TOKEN")
    with args.input.open("r", encoding="utf-8-sig", newline="") as source:
        candidates = list(csv.DictReader(source))

    if not candidates or "repo_full_name" not in candidates[0]:
        print("Input CSV must contain a repo_full_name column.", file=sys.stderr)
        return 2

    output_rows = []
    for index, candidate in enumerate(candidates):
        repo_name = (candidate.get("repo_full_name") or "").strip()
        if not repo_name:
            continue
        row = screen_one(repo_name, token)
        output_rows.append(row)
        print(
            f"[{row['screening_status']}] {repo_name}: "
            f"Java test files≈{row['java_test_file_count_estimate']}, "
            f"pom.xml={row['pom_xml_count']}, "
            f"Gradle files={row['gradle_file_count']}, "
            f"SHA={row['head_commit_sha'][:12]}"
        )
        if index < len(candidates) - 1 and args.delay > 0:
            time.sleep(args.delay)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    columns = [
        "repo_full_name", "checked_at_utc", "default_branch",
        "head_commit_sha", "archived", "language", "stars", "forks",
        "license_spdx_id", "tree_truncated", "java_test_file_count_estimate",
        "java_file_count", "pom_xml_count", "gradle_file_count",
        "test_paths_sample", "screening_status", "error", "interpretation_note",
    ]
    with args.output.open("w", encoding="utf-8-sig", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=columns)
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nFinished: {len(output_rows)}/{len(candidates)} candidates processed.")
    print(f"Output: {args.output}")
    print("Next: inspect candidate builds and run a real clone/build/detector pilot.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
