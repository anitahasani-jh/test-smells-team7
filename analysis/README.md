# Analyst Workspace

This directory contains the analysis work for Team 7's study of test smells.

## Current status

This is an analysis workspace scaffold. No new empirical findings are claimed here. Analyses must use the pipeline's real outputs and preserve failed, missing, and not-applicable observations.

## Observation unit and join key

The proposed research contract defines one Java test file at a pinned baseline snapshot as the observation unit. The composite key is:

`repository_id + snapshot_sha + test_file`

Join Analyst and Experimenter outputs only on this key. Do not join on `commit_hash` alone or assume that one test file is one class or method.

The research contract is still a proposal requiring approval from all three team members. Confirm the treatment, outcome, time window, confounders, and DAG before causal interpretation.

## Pipeline datasets

The pipeline currently defines these outputs:

| Dataset | Purpose |
| --- | --- |
| `tests.csv` | Baseline test-file metadata and detector status |
| `smells.csv` | Long-form smell labels, values, and measurement status |
| `commit_events.csv` | Post-baseline file-level commit events |
| `outcomes.csv` | Follow-up change and potential bug-fix proxy counts |
| `analysis_ready.csv` | Joined baseline and follow-up fields |
| `repository_status.csv` | Repository-level collection status |

Expected output location: `results/<RUN_ID>/`. Confirm the actual run directory and manifest before analysis.

## Analyst workflow

1. **Data inventory:** record run ID, manifest, repository status, pinned SHAs, row counts, schemas, and tool versions.
2. **Data quality:** inspect missingness by status, duplicate composite keys, invalid values, orphan smell rows, and join cardinality. Do not delete legitimate repeated smell types or failed observations.
3. **Descriptive analysis:** summarize repositories, test frameworks, test-file size, assertion counts, smell prevalence, and follow-up outcomes. Report denominators and missingness.
4. **Measurement review:** distinguish measured true/false labels from not-applicable, failed, skipped, and missing detector outputs. Review detector failures and manually validate a sample where feasible.
5. **Outcome review:** treat commit-message regex matches as potential bug-fix proxies, not verified bugs. Treat project-level PIT scores as project-level unless test-level attribution is demonstrated.
6. **Causal design:** pre-register the DAG, hypotheses, treatment, outcome, adjustment set, time ordering, and identification assumptions with the team.
7. **Sensitivity and robustness:** assess alternative definitions, missing-data handling, repository influence, and unmeasured confounding where justified.
8. **Reporting:** retain negative/null findings, uncertainty intervals, effect sizes, code, and exact run provenance.

## Important interpretation limits

- A detector failure or unmeasured smell is not equivalent to absence of a smell.
- The collector validates data structure and joins; it does not establish causal identification, sampling validity, or detector accuracy.
- Commit-message matches are only potential bug-fix commits.
- Mutation scores require validated test-level attribution before they can be interpreted as test-file outcomes.
- If baseline and follow-up refs are identical, the follow-up is empty and is only a smoke test, not a valid outcome sample.
- The current placeholder covariates are not automatically a sufficient confounder adjustment set.
- Do not report causal effects until the research contract is approved and assumptions are defensible.

## Planned notebooks

Create notebooks only after a real run directory is available:

- `01_data_quality.ipynb`
- `02_descriptive_analysis.ipynb`
- `03_smell_distribution.ipynb`
- `04_outcome_analysis.ipynb`
- `05_causal_model_DAG.ipynb`
- `06_sensitivity_analysis.ipynb`

Keep generated figures, tables, and reports in dedicated subdirectories. Do not commit raw research datasets, detector binaries, credentials, or large temporary artifacts unless the team explicitly approves a data-sharing policy.
