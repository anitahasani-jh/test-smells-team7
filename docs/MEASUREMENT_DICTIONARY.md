# Measurement Dictionary

Use this document to agree on operational definitions before analysis. Do not fill unknown values with zero.

| Measure | Meaning | Required provenance / notes |
|---|---|---|
| `repo_full_name` | Owner/name of the source repository | Keep stable even if repository is renamed; note URL |
| `commit_sha` | Exact revision scanned or measured | Pin each detector/outcome run to a commit |
| `test_file_path`, `test_class` | Test unit being studied | State how nested/parameterized tests are handled |
| `smell_present` | Whether at least one defined smell was detected for the unit | Detector/version and smell taxonomy must be fixed |
| `smell_count` | Number of smell instances for the unit | Define duplicate handling and aggregation |
| `mutation_score` | Mutants killed divided by valid mutants under the agreed PIT rules | Preserve raw PIT report; define treatment of no-coverage/equivalent mutants |
| `change_proneness_commits` | Number of distinct commits changing the test file in the preregistered time window | Specify time window, rename handling, and merge-commit policy |
| `bugfix_cochange_count` | Number of changes classified as bug fixes that modify the test file and its linked production file | Publish the bug-fix classification rule; do not infer from vague messages alone |
| `test_loc`, `production_loc` | Lines of code in test unit and linked production unit | Name the counting tool and comment/blank-line policy |
| `test_to_production_ratio` | Test LOC / production LOC | Undefined when production LOC is zero; retain missing/undefined |
| `complexity_metric` | Complexity of the test or linked production code | Name tool, version, and unit |
| `project_age_days` | Days between first observed commit and pinned commit | Define shallow-clone handling |
| `developer_count` | Distinct contributors in a defined time window | State whether bots are excluded |
| `domain` | Project domain/category | State coding source and handling of ambiguous cases |
| `flaky_test_status` | Measured status under a repeated-run protocol | Use unknown/not measured when no protocol was run |

## Important distinctions
- A failed detector run is not a negative detection.
- A failed or skipped mutation run is not a mutation score of zero.
- The research repo's own commits are pipeline smoke tests, not observations from the study population.
- A causal interpretation requires a defensible DAG, measured confounders, overlap/diagnostics, and sensitivity analysis. Regression adjustment alone does not prove causality.
