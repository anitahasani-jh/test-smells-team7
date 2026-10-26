import csv
import tempfile
import unittest
from pathlib import Path

from src.validate_detector_output import validate_detector_csv


class ValidateDetectorOutputTests(unittest.TestCase):
    def write_csv(self, directory, name, headers, rows):
        path = Path(directory) / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)
        return path

    def test_valid_detector_csv_reports_rows_and_unique_commits(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self.write_csv(
                temp_dir,
                "detector.csv",
                ["commit_hash", "smell_name", "test_file"],
                [["abc123", "Eager Test", "ExampleTest.java"],
                 ["abc123", "Mystery Guest", "OtherTest.java"],
                 ["def456", "Eager Test", "ThirdTest.java"]],
            )
            report = validate_detector_csv(str(path))
            self.assertEqual(report["rows"], 3)
            self.assertEqual(report["unique_commits"], 2)
            self.assertIn("smell_name", report["columns"])

    def test_missing_commit_hash_column_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self.write_csv(temp_dir, "detector.csv", ["smell_name"], [["Eager Test"]])
            with self.assertRaisesRegex(ValueError, "commit_hash"):
                validate_detector_csv(str(path))

    def test_blank_commit_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self.write_csv(
                temp_dir, "detector.csv", ["commit_hash", "smell_name"], [[" ", "Eager Test"]]
            )
            with self.assertRaisesRegex(ValueError, "Empty commit_hash"):
                validate_detector_csv(str(path))

    def test_header_only_csv_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = self.write_csv(temp_dir, "detector.csv", ["commit_hash"], [])
            with self.assertRaisesRegex(ValueError, "no data rows"):
                validate_detector_csv(str(path))


if __name__ == "__main__":
    unittest.main()
