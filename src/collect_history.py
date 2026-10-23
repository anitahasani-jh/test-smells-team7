
import csv
import sys
from pathlib import Path

from pydriller import Repository


def collect_history(repo_path: str, output_path: str) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    columns = [
        "commit_hash",
        "author",
        "commit_date",
        "message",
        "files_changed",
        "insertions",
        "deletions",
    ]

    count = 0

    with output_file.open("w", newline="", encoding="utf-8-sig") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()

        for commit in Repository(repo_path).traverse_commits():
            writer.writerow(
                {
                    "commit_hash": commit.hash,
                    "author": commit.author.name,
                    "commit_date": commit.author_date.isoformat(),
                    "message": commit.msg.strip(),
                    "files_changed": len(commit.modified_files),
                    "insertions": commit.insertions,
                    "deletions": commit.deletions,
                }
            )
            count += 1

    print(f"Commits collected: {count}")
    print(f"CSV saved to: {output_file.resolve()}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python src/collect_history.py "
            "<repository_path> <output_csv>"
        )
        sys.exit(1)

    collect_history(sys.argv[1], sys.argv[2])
