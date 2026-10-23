"""Join commit history to real output from a selected Test Smell detector.

The detector CSV must contain 'commit_hash'. This script never infers smell labels.
"""
import argparse
from pathlib import Path
import pandas as pd


def build_dataset(history_path: str, detector_path: str, output_path: str) -> int:
    history_file, detector_file, output_file = map(
        Path, (history_path, detector_path, output_path)
    )
    if not history_file.is_file():
        raise FileNotFoundError(f"Commit history CSV not found: {history_file}")
    if not detector_file.is_file():
        raise FileNotFoundError(
            f"Detector output CSV not found: {detector_file}. Run the approved "
            "Test Smell detector first; this script does not create labels."
        )

    history = pd.read_csv(history_file, dtype={"commit_hash": "string"})
    detector = pd.read_csv(detector_file, dtype={"commit_hash": "string"})
    for label, frame in (("history", history), ("detector output", detector)):
        if "commit_hash" not in frame.columns:
            raise ValueError(f"The {label} CSV must contain 'commit_hash'.")
        frame["commit_hash"] = frame["commit_hash"].str.strip()
        if frame["commit_hash"].isna().any() or frame["commit_hash"].eq("").any():
            raise ValueError(f"The {label} CSV contains empty commit_hash values.")

    merged = history.merge(
        detector, on="commit_hash", how="inner",
        suffixes=("_history", "_detector"), validate="many_to_many"
    )
    if merged.empty:
        raise ValueError("No matching commit hashes found in the input CSV files.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"Dataset rows: {len(merged)}")
    print(f"Dataset saved to: {output_file.resolve()}")
    return len(merged)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--history", default="results/commit_history.csv")
    parser.add_argument("--detector", default="results/test_smell_detections.csv")
    parser.add_argument("--output", default="data/processed_dataset.csv")
    args = parser.parse_args()
    try:
        build_dataset(args.history, args.detector, args.output)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
