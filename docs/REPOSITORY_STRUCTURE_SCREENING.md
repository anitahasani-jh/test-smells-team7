# Repository structure screening

## Purpose

Run a lightweight GitHub API screen on the candidate repositories before cloning them.
It records the default branch's current commit SHA, repository metadata, an estimated
count of Java test files, Java files, and Maven/Gradle build-file paths.

This is a **preliminary screen only**. It does not establish that:
- a project builds or its tests pass;
- every counted Java file is an executable unit test;
- Test Smell detectors support the project's test framework or language features;
- PIT can run successfully or produce comparable mutation scores;
- a repository is an independent, representative study subject.

## Run locally

From the repository root, with the project virtual environment active:

```cmd
python src/screen_repository_structure.py
```

Default input:
`data/repository_candidates.csv`

Default output:
`results/repository_structure_screening.csv`

Optional paths:

```cmd
python src/screen_repository_structure.py --input data/repository_candidates.csv --output results/repository_structure_screening.csv
```

The script uses only the Python standard library. An optional `GITHUB_TOKEN` environment
variable can increase GitHub API rate limits; never commit the token or put it in a source file.

## Important interpretation notes

- `java_test_file_count_estimate` counts Java paths containing `/test/`, `/tests/`,
  or beginning with `test/` or `tests/`. It can miss nonstandard layouts and can include
  helper files that are not tests.
- `tree_truncated=true` means GitHub did not return the complete recursive tree; do not
  rely on the file counts until the repository is checked another way.
- `head_commit_sha` records the current default-branch SHA at the time of screening.
  For a reproducible study, select and pin a SHA after eligibility checks, then collect
  history/outcomes at the same revision or explicitly document the sampling window.
- Testing frameworks and testing libraries (for example JUnit, Mockito, Spock, Truth,
  Awaitility, and PIT) may have atypical test suites compared with ordinary application
  repositories. Keep them as candidates only until the inclusion criteria and project
  population are approved.
- Do not exclude a repository solely because it has fewer stars. Apply predeclared
  eligibility criteria such as test volume, Java test framework support, build success,
  detector validation, license, and PIT feasibility.

## Next validation stage

For each candidate retained after metadata screening:
1. Clone or otherwise retrieve the pinned revision.
2. Inspect Maven/Gradle instructions and identify Java test source roots.
3. Run the project's documented test command and record success/failure and environment.
4. Pilot the selected Test Smell detector and manually validate a sample of detections.
5. Pilot PIT on a manageable subset and record runtime, mutation score availability, and failures.
6. Record every exclusion reason in the project manifest before causal analysis.
