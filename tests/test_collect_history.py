import csv
import subprocess
import tempfile
import unittest
from pathlib import Path

from src.collect_history import collect_history


class CollectHistoryTests(unittest.TestCase):
    def _git(self, repo: Path, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True, capture_output=True, text=True,
        )

    def test_collects_commit_metadata_and_changed_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            repo = root / "sample-repo"
            repo.mkdir()
            self._git(repo, "init")
            self._git(repo, "config", "user.name", "Test User")
            self._git(repo, "config", "user.email", "test@example.com")

            sample_file = repo / "Example.java"
            sample_file.write_text("class Example {}\n", encoding="utf-8")
            self._git(repo, "add", "Example.java")
            self._git(repo, "commit", "-m", "Add example")
            sample_file.write_text("class Example { int x = 1; }\n", encoding="utf-8")
            self._git(repo, "add", "Example.java")
            self._git(repo, "commit", "-m", "Update example")

            output = root / "results" / "history.csv"
            count = collect_history(str(repo), str(output))
            self.assertEqual(count, 2)

            with output.open(newline="", encoding="utf-8-sig") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertIn("changed_file_paths", rows[0])
            self.assertTrue(all(row["commit_hash"] for row in rows))
            self.assertTrue(all("Example.java" in row["changed_file_paths"] for row in rows))


if __name__ == "__main__":
    unittest.main()
