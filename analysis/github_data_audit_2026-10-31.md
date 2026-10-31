# GitHub empirical-data audit — 2026-10-31

## Scope

Audited the public repository `anitahasani-jh/test-smells-team7` and the visible branches:
- `main`
- `analyst-workspace`
- `feat/detector-output-validation`
- `fix/collect-history-return-count`

Also inspected the open/merged pull requests visible in the repository and searched the repository for the expected handoff filenames.

## Finding: the final empirical handoff is not present in the accessible GitHub repository

The following required files were not found in the repository tree or GitHub code search:
- `tests.csv`
- `smells.csv`
- `outcomes.csv`
- `commit_events.csv`
- `manifest.json`
- a measured, attributable PIT result CSV

The committed files under `data/` are templates/candidate inputs, not the final study dataset:
- `manual_validation_template.csv`
- `outcome_metrics_template.csv`
- `repository_manifest_template.csv`
- `repository_candidates.csv`
- `test_history.csv` (one row from the research repository's own setup history)

The committed `contracts/pit-results.example.csv` contains only a header/example contract. It contains no mutation measurements.

The visible branches do not expose additional empirical handoff files. The open PR #1 concerns structural validation of detector CSVs. PR #3 adds pipeline files and is merged; neither is a scientific dataset handoff.

## What can currently be reported

### Repository screening

The current screening frame contains 8 candidate repositories. The structure-screening file reports 2,692 estimated Java test-file candidates across these repositories (mean 336.5; median 323.5; range 45–767). It reports 6,189 Java files in total (mean 773.6; median 716; range 124–1,805).

These are repository-tree estimates for candidate selection only. They are not confirmed detector scans, not verified test classes, and not the final study sample.

### Engineering/pilot evidence (keep separate from study results)

The existing pilot notes report:
- JUnit 4 pilot: 205 discovered candidates; detector output for 204; one detector failure; 4,284 long-format smell observations, of which 3,950 were measured and 334 were missing/not-applicable; 10 future file-change events.
- Two-repository engineering replication: 245 discovered test-file candidates; 5,124 long-format smell values, of which 4,724 were measured and 400 not-applicable; 13 future test-file commit events; six normalized CSV outputs matched across two runs on the same machine.

These figures are copied from the repository's engineering/pilot documentation, not recomputed from raw run artifacts, because the raw run directories and detector JAR are not committed. They are not population prevalence estimates, confirmed bug-fix counts, PIT scores, or causal results.

## Statistics that cannot responsibly be calculated yet

The following teacher-requested analyses require actual validated row-level data and cannot be inferred from templates or pilot summaries:
- smell-specific prevalence with valid denominators across the selected repositories;
- detector precision/recall and inter-rater agreement from manual labels;
- mutation-score comparisons by smell at the agreed test-class/test-file unit;
- change-proneness and verified bug-fix co-change rates in the preregistered follow-up window;
- adjusted mixed-effects estimates;
- propensity-score matching and overlap diagnostics;
- DoubleML estimates;
- E-value sensitivity analysis.

No placeholder, missing, failed, or not-applicable value has been converted to zero.

## Required next handoff from the team

Place one completed run under `results/<RUN_ID>/` and include:
1. `tests.csv`
2. `smells.csv`
3. `outcomes.csv`
4. `commit_events.csv`
5. `manifest.json`
6. raw detector output and run logs (or a stable, access-controlled artifact location plus checksums)
7. PIT CSV with exact baseline keys and a defensible attribution method, if PIT was run
8. manual-validation labels with reviewer IDs, adjudication, and notes

The manifest must identify each repository, immutable baseline SHA, follow-up ref/window, detector name/version/hash, runtime, run ID, exclusions, and failures.

## Design issues to resolve before inferential statistics

1. The teacher's project description asks for mutation score per test class, while the current internal research contract keys observations at test-file level. The team must agree on the primary unit and document any class-to-file mapping before joining PIT outcomes.
2. The primary outcome and estimand must be fixed. A file-change count, a verified production defect, and a PIT mutation score are different outcomes and cannot be silently substituted for one another.
3. Commit-message regex matches remain potential bug-fix proxies, not verified bug fixes.
4. Project-level PIT scores cannot be duplicated across files and analyzed as independent file-level outcomes.
5. The current 8-repository screening list is far below the teacher's suggested large-scale target; it is a candidate-screening frame, not the final sample.

## Analyst status

Completed: GitHub branch/data inventory, existing screening summary, literature synthesis workbook, provisional statistical analysis plan.

Blocked pending team data: final dataset QA, empirical descriptive tables, manual detector validation metrics, DAG sign-off, causal models, matching, DoubleML, and E-value analysis.

**Conclusion:** the repository currently supports screening and engineering/pilot reporting only. It does not yet contain the committed empirical handoff required for the teacher-requested statistical results.
