# Combined Work Plan — Experimenter + Literature Review & Validation

This document combines the Team 7 Experimenter and literature-review/manual-validation responsibilities into one traceable workflow. It is a working plan, not evidence that a task has been completed.

## Working rules

- Work on a feature branch; do not commit directly to `main`.
- Keep raw tool output immutable. Store normalized/derived files separately and record the transformation.
- Never replace a failed, skipped, unknown, or not-applicable measurement with zero or a negative label.
- Every run must record repository URL, immutable commit SHA, tool/version, exact command, configuration, environment, start/end time, exit status, and log path.
- Do not report pilot/synthetic engineering checks as empirical study findings.
- Freeze the sampling rules, unit of analysis, detector taxonomy/version, validation protocol, outcome definition, and causal estimand with the team/instructor before full-scale collection.
- Use pull requests for shared changes. Review diffs and run tests before merging.

## Phase 0 — Repository and protocol audit

Status: initial repository audit completed on 2026-11-01; continue checking before each change.

- [x] Confirm repository access and default branch.
- [x] Inspect existing README, setup scripts, configuration files, data templates, tests, and research documentation.
- [x] Create a dedicated work branch for this combined workstream.
- [ ] Confirm local operating system, Python, Git, Java, and Maven versions.
- [ ] Review current branch changes and coordinate with Developer/Analyst before touching shared contracts.

## Phase 1 — Literature review and research protocol

Outputs:
- `docs/literature_review/README.md`
- `docs/literature_review/search_protocol.md`
- `docs/literature_review/papers_table.csv` (or a versioned spreadsheet)
- `docs/literature_review/synthesis.md`
- `docs/literature_review/research_gaps.md`
- A source log with DOI/URL, database, search date, query, inclusion decision, and reason.

Tasks:
1. Define search strings and databases (e.g., Google Scholar, arXiv, publisher libraries).
2. Apply documented inclusion/exclusion criteria.
3. Verify each paper's bibliographic metadata and accessible source.
4. Extract problem, method, dataset, measures, findings, and limitations.
5. Synthesize evidence and distinguish established findings from open questions.
6. Link each claim in the report to a verifiable source.

Gate: the team agrees on the research questions, study unit, sampling frame, and operational definitions.

## Phase 2 — Environment and tool verification

Outputs:
- Updated setup instructions for Windows and Unix-like systems.
- `docs/TOOL_BASELINE_REGISTER.md`
- Environment/version record.

Tasks:
1. Verify Python and Git; verify Java and Maven only for the approved Java-based tools.
2. Inspect the existing setup scripts and run them in a clean environment.
3. Verify the detector JAR checksum and exact version against the approved source.
4. Confirm tsDetect/TestSmellDetector compatibility with the target JUnit versions and document known failures.
5. Verify PIT only after the team approves the mutation-testing outcome and attribution method.
6. Run a minimal smoke test; preserve both successful and failed logs.

Important: PyDriller extracts Git history; it does not detect Test Smells. A current-checkout detector result is not automatically valid for historical commits.

## Phase 3 — Baseline and pilot replication

Outputs:
- One immutable config per run under `configs/`.
- Raw logs and tool output under local `results/raw/<run_id>/`.
- Machine-readable run manifest and normalized CSV outputs.
- `docs/PILOT_RESULTS.md` updates only when supported by actual runs.

Tasks:
1. Use only team-approved repositories and pinned commit SHAs.
2. Run a small pilot before any expanded collection.
3. Record discovery counts, successes, failures, skipped files, missing values, and duration.
4. Validate output schema and repository/commit/test-file join keys.
5. Repeat the pilot in a fresh output directory to check process reproducibility.
6. Submit results and limitations to the team/instructor for a go/no-go decision.

Gate: no full-scale experiment until pilot, protocol, and resource budget are approved.

## Phase 4 — Manual validation of detector output

Outputs:
- `data/manual_validation_template.csv` (existing template; update only by agreement)
- Completed validation sample in a separate versioned data file.
- `docs/MANUAL_VALIDATION_PROTOCOL.md`
- Inter-rater agreement and adjudication summary, when a second reviewer is available.

Tasks:
1. Define sampling of detected and non-detected cases if precision and recall are both required.
2. Blind reviewers to detector predictions where feasible.
3. Apply written smell definitions and record evidence from source code.
4. Keep reviewer labels separate; adjudicate disagreements explicitly.
5. Calculate precision/recall only when the sampling design and ground-truth labels support them.
6. Document uncertain and unreviewable cases.

## Phase 5 — Full experiment execution

Outputs:
- Frozen configs and repository manifest.
- Raw detector/PIT outputs, logs, checkpoints, and run manifests.
- Normalized experiment CSVs and failure register.

Tasks:
1. Run only after approval of the pilot and protocol.
2. Preserve every run, including failed and partial runs.
3. Record exact environment, commit SHA, config hash, command, timestamps, exit code, and versions.
4. Checkpoint long jobs and resume only under documented rules.
5. Back up raw outputs and verify checksums.
6. Hand the Analyst the data dictionary, normalized files, missingness/failure report, and join-key validation.

## Phase 6 — Interpretation, reporting, and handoff

Outputs:
- Literature synthesis and limitations.
- Validation report.
- Reproducibility report.
- Experiment handoff package and final evidence-linked report.

Tasks:
1. Compare findings with prior literature without overstating agreement.
2. Separate detector validity, measurement results, associations, and causal estimates.
3. Do not claim causality without an approved DAG, estimand, measured confounders, diagnostics, and sensitivity analysis.
4. Record deviations from protocol and all known limitations.
5. Review the final report with Developer, Analyst, and instructor.

## Collaboration and GitHub handoff

- Developer owns repository discovery, source snapshots, detector execution/integration, and initial dataset construction.
- This workstream owns experiment environment/baseline execution, reproducibility records, literature review, and manual detector validation.
- Analyst owns statistical analysis and visualizations; agree on data contracts before collection.
- Share data through agreed schemas and pull requests. Do not overwrite another member's branch or commit raw, sensitive, very large, or locally ignored outputs without team approval.
- Use issue/PR references for decisions, and update this plan as work is completed.
