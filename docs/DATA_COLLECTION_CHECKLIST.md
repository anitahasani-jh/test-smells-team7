# Empirical Data Collection Checklist

This checklist distinguishes project setup from measured research evidence. Do not report placeholder rows as results.

## Study unit and scope
- [ ] Agree with the team on the unit of analysis (recommended: test class at a pinned commit; repository-level covariates stored separately).
- [ ] Freeze inclusion/exclusion criteria before collecting outcomes.
- [ ] Record the collection date and the exact commit SHA for each repository.
- [ ] Keep a repository manifest with clone URL, language, stars/forks if used for sampling, archived status, selection reason, and exclusion reason.

## Test-smell detections
- [ ] Select and document one detector/version and exact invocation.
- [ ] Save raw detector output unchanged under `results/raw/`.
- [ ] Normalize output to `results/test_smell_detections.csv`.
- [ ] Include detector name/version, commit SHA, file path, test class, smell name, and source location where available.
- [ ] If the detector fails, log the failure; never convert a failed run into zero smells.
- [ ] Manually label the planned validation sample (target 100 cases if feasible), with reviewer, decision, and notes. Report precision only after labels and detections exist.

## Git history and change-proneness
- [ ] Collect commits for each selected repository (not just this research repository).
- [ ] Store repository identity alongside commit hash, since hashes are only unique within practical repository context.
- [ ] Define the observation window before computing change-proneness.
- [ ] Count commits modifying each test file within that window; separately identify bug-fix co-change only if a reproducible classification rule exists.

## Outcomes and confounders
- [ ] Mutation score per test class for the infrastructure team's feasible subset; record PIT version, command, commit SHA, and build status.
- [ ] Record file size/LOC, complexity (name the tool), project age, contributor/developer count, test-to-production-code ratio, and domain if available.
- [ ] Track missingness and reasons. Missing is not the same as zero.
- [ ] Keep flakiness as unavailable unless measured with a defined repeated-run protocol.

## Before causal analysis
- [ ] Team agrees on a DAG and the exact treatment, outcome, confounders, and estimand.
- [ ] Save the correlation baseline separately from adjusted/causal estimates.
- [ ] Run propensity-score diagnostics, overlap checks, and sensitivity analysis only after a real analysis dataset exists.
- [ ] Record exclusions, failed builds, detector failures, and deviations from the preregistered protocol.

## Current repository status
The sample project and smoke tests are for pipeline development only. They are not empirical evidence for the study. No final study conclusion should be written until real repositories have been collected and validated.
