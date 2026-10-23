# Test Smell Detector Integration

## Purpose

This guide describes how to add real Test Smell detections to the Team 7 pipeline. Git history collection and smell detection are separate steps: `src/collect_history.py` does not detect smells.

## Candidate tool

The open-source **tsDetect / TestSmellDetector** project targets Java projects using JUnit and provides CSV output. Review the tool's current README, supported Java/JUnit versions, license, and command-line options before using it:

- Repository: https://github.com/TestSmells/TestSmellDetector
- Tool documentation: https://testsmells.org/pages/testsmelldetector.html

This is a candidate, not a claim that the course team has approved it. Confirm the tool and its version with the instructor/team before treating its output as study data.

## Recommended workflow

1. Confirm the target projects, study period, detector, detector version, and smell types with the team.
2. Clone each target repository and record the exact repository URL and checked-out commit SHA.
3. Run the approved detector on the relevant test files according to its official instructions.
4. Preserve the detector's original output unchanged in a separate raw-data location. Record the command, tool version, date, and target commit SHA.
5. Convert the detector output to the agreed project schema only after inspecting the actual output columns. Do not invent missing values.
6. Ensure the detection table has a `commit_hash` column that refers to the same commit whose test code was scanned. A detection result for the latest checkout must not be joined to every historical commit.
7. Save the normalized detection table as `results/test_smell_detections.csv`, with a `commit_hash` column and the agreed detection fields.
8. Run the dataset builder:
   ```bat
   python src\build_dataset.py --history results\commit_history.csv --detector results\test_smell_detections.csv --output data\processed_dataset.csv
   ```
9. Check unmatched commit hashes, missing values, duplicate rows, and detector coverage before handing data to the analysis teammate.

## Important limitation: historical analysis

Scanning a repository's current checkout only gives detections for that checkout. It does **not** reconstruct smell status for old commits. For a commit-level evolution/causal study, the team needs a reproducible plan to check out and scan each selected historical revision, or an approved alternative. Store the scanned commit SHA alongside every detector result.

## Do not fabricate results

Do not create placeholder smell labels, claim the detector ran when it did not, or report causal/statistical conclusions from the sample Java project. The sample project is only a pipeline smoke test, not research evidence.
