# Team 7 — Causal Study of Test Smells

## Project overview

This repository contains the engineering pipeline for a study of test smells. The developer workflow collects Git commit metadata, keeps detector output separate from raw history, and joins the two datasets by commit hash.

**Research integrity:** PyDriller collects Git history; it does not detect Test Smells. No smell labels, causal conclusions, or statistical results are invented by this repository. Select and document the approved detector and study protocol before producing research results.

## Project structure

- `src/collect_history.py` — export commit metadata and changed file paths to CSV.
- `src/build_dataset.py` — join commit metadata with CSV output from the selected Test Smell detector.
- `tests/` — automated tests for the developer pipeline.
- `data/` — prepared datasets (do not commit sensitive or unapproved data).
- `results/` — generated CSVs and local experiment outputs.
- `docs/DEVELOPER_GUIDE.md` — setup, commands, and pipeline details.
- `experiments/` — approved experiment scripts.
- `analysis/` — reserved for the research analysis workstream.

## Requirements

- Python 3.12 (tested in the project setup)
- Git
- Python dependencies listed in `requirements.txt`
- A Java runtime/build tool and an approved Test Smell detector only if required by the final study protocol

## Setup

Windows CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Collect commit history

```bat
python src\collect_history.py <path-to-git-repository> results\commit_history.csv
```

Example using the repository itself:

```bat
python src\collect_history.py . results\commit_history.csv
```

The CSV includes commit hash, author, author date, message, number of changed files, changed paths, insertions, and deletions.

## Build the combined dataset

First export the selected detector's real output to `results/test_smell_detections.csv`. It must include a `commit_hash` column. Then run:

```bat
python src\build_dataset.py --history results\commit_history.csv --detector results\test_smell_detections.csv --output data\processed_dataset.csv
```

The dataset builder stops with a clear error if the detector file or join key is missing. It does not generate detection labels.

## Run tests

```bat
python -m unittest discover -s tests -v
```

## Current status and limitations

- Initial repository and commit-history collection script are in place.
- Automated tests cover commit-history collection.
- Dataset join code is implemented but requires actual detector output.
- The Test Smell detector and causal-study protocol must be confirmed by the project team/instructor before interpreting results.
- No causal or statistical claim should be made from the small sample repository used for development checks.
