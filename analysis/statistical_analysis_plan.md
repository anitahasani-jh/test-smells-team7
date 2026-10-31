# Statistical analysis plan — Team 7 (working draft)

**Basis:** Team-provided `papers_table_completed.xlsx`, especially `Synthesis and Gap` and `Full-Text Extraction`, combined with the project's existing research contract and data dictionary.

**Status:** Provisional plan. It must be reconciled with the actual schema, approved research contract, and available observations before inferential analysis. This document does not claim that the required raw dataset is currently present.

## 1. Research question and estimand

Working question: To what extent are validated test-smell types associated with subsequent production-code defects after accounting for plausible confounders, and what evidence would support a causal interpretation rather than simple correlation?

Before modeling, the team must select:
- one primary smell exposure (or a pre-specified family of smell-specific exposures);
- one primary production-defect outcome;
- a baseline snapshot and a fixed follow-up window;
- the unit of analysis and eligible population.

A causal estimand cannot be finalized until these choices and the causal diagram are agreed. If the available data only support prediction/association, report that rather than a causal effect.

## 2. Unit of analysis and joins

Follow the project research contract: one Java test file at a baseline snapshot. Use the composite key:

`repository_id + snapshot_sha + test_file`

Join test, smell and file-level outcome data only on this key where their measurement levels truly match. Preserve project- or repository-level outcomes as project-level unless a validated attribution method supports file-level attribution. Do not duplicate project-level outcomes across files and then treat them as independent file-level events.

## 3. Variables

### Exposure
For each smell type, retain separately:
- detector-reported value;
- validated presence/absence if manual validation supports it;
- raw count;
- density with an explicitly defined denominator.

A missing, failed, blank or not-applicable detector result is unknown/not measured—not absence (zero). Record detector version, configuration and snapshot.

### Outcome
Use a future production-code defect measure after the baseline snapshot. Specify:
- what qualifies as a defect (verified bug fix, issue-linked fix, or proxy);
- whether outcome is binary, count or severity;
- start/end of follow-up and ancestor-chain rules;
- whether attribution to a test file is defensible.

A commit-message regex such as `potential_bugfix_commits` is a proxy, not a verified bug label. PIT mutation score is project-level unless test-file attribution has been validated.

### Candidate confounders
The workbook suggests production-code size/complexity, test-code size, churn, prior defects, coupling, coverage, project/version, language/framework and code ownership where available. The research contract also warns that placeholder variables such as `test_loc`, `assert_count` and `project_age_days` alone are insufficient confounder adjustment.

Do not mechanically include every available variable. Draw a DAG, define the causal role of each variable, and avoid adjusting for mediators/colliders. Document unavailable confounders.

## 4. Data-quality checks before statistics

1. Confirm schema, data provenance, pinned snapshot SHA and follow-up reference.
2. Count rows and unique composite keys in every input.
3. Check duplicate keys, invalid types, impossible values and failed detector/build records.
4. Summarize missingness by repository, smell type and detector status.
5. Distinguish measured zero, positive count, not applicable, failed and unknown.
6. Validate temporal order: exposure snapshot precedes outcome window.
7. Confirm outcome attribution and avoid mixing project-level with file-level metrics.
8. Record exclusions with explicit reasons; do not silently drop failed or incomplete cases.

## 5. Descriptive analysis

Report:
- eligible repositories, snapshots and test files;
- smell-specific prevalence among measured observations, with denominator;
- smell counts/density distributions (median, IQR, range; mean/SD if informative);
- missing/not-applicable/failed detector rates;
- outcome frequency/count and follow-up completeness;
- distributions of candidate confounders.

Use plots for distributions and missingness. For clustered data, show repository-level variation rather than only pooled totals.

## 6. Association and predictive analyses

Only after data-quality checks and a pre-specified analysis:
- binary outcome: logistic regression may be considered;
- count outcome: Poisson or negative-binomial models depending on dispersion and assumptions;
- time-to-event outcome: survival analysis only if event times and censoring are reliable;
- repeated files/snapshots within repositories: account for clustering (e.g. mixed effects, cluster-robust uncertainty, or an appropriate multilevel design).

Compare a confounder-only baseline model with a model adding smell measures if prediction is an explicit objective. Use project-aware or time-aware validation splits to avoid leakage across versions of the same repository. Report calibration and discrimination, not AUC alone.

Do not select model families until outcome distribution, sample size, clustering and assumptions are inspected.

## 7. Causal interpretation

A regression coefficient adjusted for observed covariates is not automatically a causal effect. A causal interpretation requires, at minimum:
- defensible temporal ordering;
- a pre-specified DAG and estimand;
- adequate measurement of relevant confounders;
- positivity/overlap and consistency assumptions appropriate to the exposure;
- no major unaddressed selection or measurement bias;
- sensitivity analysis for plausible unmeasured confounding and detector misclassification.

If these conditions are not supportable, label findings as adjusted associations or predictive results. Do not present propensity-score matching or other causal methods as a cure for missing confounders.

## 8. Sensitivity and robustness checks

Where data permit:
- repeat analysis using validated-only versus all detector labels;
- compare presence, count and density exposures;
- vary reasonable follow-up windows specified before outcome inspection;
- assess influence of individual repositories;
- compare verified defect labels with proxy outcomes, clearly separated;
- examine alternate confounder sets justified by the DAG;
- report uncertainty and failed/inconclusive model fits.

## 9. Results tables to produce

1. Dataset and sample-flow table (included/excluded/missing/failed).
2. Measurement-quality table by smell type (manual audit, precision/recall/agreement if available).
3. Descriptive table by smell type and outcome.
4. Missingness and follow-up completeness table.
5. Model table with estimate, uncertainty interval, p-value where appropriate, sample size and covariates.
6. Sensitivity-analysis table.
7. Repository-level plots and diagnostic plots.

## 10. Current blockers

The repository's previously inspected branches did not contain the complete empirical handoff files (`tests.csv`, `smells.csv`, `outcomes.csv`, `commit_events.csv`, and `manifest.json`) or a verified per-file PIT result set. The documented pilot/replication counts are engineering/pilot summaries and must not be treated as the final analysis dataset.

The research contract also records that the proposal has not yet been approved by all team members. Confirm the final outcome definition, follow-up window, confounders and attribution rules with the team.

## 11. Go/no-go rule

Proceed to inferential analysis only when:
- the composite join key is present and validated;
- baseline and follow-up snapshots are pinned;
- exposure and outcome are temporally ordered;
- detector missingness is represented correctly;
- outcome attribution matches the unit of analysis;
- the primary outcome, exposure and DAG are agreed.

Otherwise, deliver descriptive data-quality results and state precisely why causal estimation is not yet defensible.
