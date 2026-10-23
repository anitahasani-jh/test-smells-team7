# Developer guide

## Scope

The developer workstream owns runnable tooling, dependency setup, automated tests, and technical hand-off. Confirm research design, validation rules, and statistical interpretation with the team/instructor rather than guessing.

## Setup (Windows CMD)

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Collect Git history

```bat
python src\collect_history.py <repository-path> results\commit_history.csv
```

The CSV contains commit hash, author, author date, message, number of changed files, changed paths, insertions, and deletions. Output is UTF-8 with BOM for common Windows spreadsheet compatibility. Use repositories with meaningful history for real research; the tiny sample repository is for pipeline testing only.

## Run automated tests

```bat
python -m unittest discover -s tests -v
```

The test creates a temporary Git repository with two commits and checks the generated CSV. Git must be installed and available on PATH.

## Test Smell detection

PyDriller provides Git history metadata; it does not identify Test Smells. The team must confirm the detector/version, supported language and smell categories, command, and output schema. Preserve the detector's raw output.

Expected detector file: `results/test_smell_detections.csv`, with at least a `commit_hash` column and the real detector output columns.

## Build combined dataset

```bat
python src\build_dataset.py --history results\commit_history.csv --detector results\test_smell_detections.csv --output data\processed_dataset.csv
```

The script joins on commit hash and stops if inputs or matching hashes are missing. Duplicate rows should be handled according to the approved study protocol; the script does not infer smell labels or causal effects.

## Technical hand-off checklist

- [ ] Record Python, Java, Maven, and detector versions actually used.
- [ ] Run history collection on approved study repositories.
- [ ] Preserve raw detector output and document the exact command.
- [ ] Run automated tests.
- [ ] Verify that commit hashes join as expected.
- [ ] Document exclusions, failures, and limitations.
- [ ] Confirm detector schema and protocol with the team/instructor.
