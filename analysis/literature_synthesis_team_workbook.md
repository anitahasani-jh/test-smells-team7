# Literature synthesis for Team 7 — Analyst notes

**Source:** team-provided workbook `papers_table_completed.xlsx` (updated 2026-10-30), especially the sheets `Papers Table`, `Synthesis and Gap`, `Source Log`, and `Full-Text Extraction`.

**Evidence status:** The workbook explicitly says most paper entries are at abstract/bibliographic screening level. The notes below preserve that limitation. They are a working synthesis, not a substitute for full-text extraction or independently verified effect estimates.

## 1. Working research question

To what extent are validated test-smell types associated with subsequent production-code defects after accounting for plausible confounders, and what evidence would support a causal interpretation rather than a simple correlation?

## 2. What the 12-paper matrix contributes

| Paper ID | Main contribution recorded in workbook | How Team 7 should use it | Important boundary |
|---:|---|---|---|
| 1 | Broad multivocal review of test smells, effects, detection and refactoring | Terminology, candidate smell catalogue, primary-study tracing | Literature synthesis, not a causal test; distinguish peer-reviewed and grey sources |
| 2 | Systematic mapping of 22 detection tools | Detector selection and comparison | Mapping does not independently benchmark every tool; verify final proceedings metadata |
| 3 | Manual validation of smell definitions and detector outputs | Measurement validity; manual audit and false-positive/negative assessment | Exact annotation protocol and per-smell metrics require full-text extraction |
| 4 | Distribution study plus controlled maintenance/comprehension experiment | Motivation and evidence about maintenance consequences | Comprehension outcomes are not future production defects; small student sample |
| 5 | Empirical study of prevalence and maintenance/comprehension; abstract reports 86% of examined JUnit tests had at least one smell | Historical context and comparison | Population and detector-specific; do not generalize to defect causation; check overlap with Paper 4 |
| 6 | Survey and repository mining on smell awareness, introduction/persistence, and relationships with production-code smells | Temporal/evolution context and observational design | Observational associations do not establish later defect causation; verify project-selection counts |
| 7 | Apache Ant study of test smells and fault-proneness | Closest prior work for Team 7's outcome question; compare definitions, windows, predictors and validation | One project; correlation/prediction are not causal proof |
| 8 | Longitudinal smell evolution and maintenance; workbook reports 83% incidental removals and average 8.25% AUC gain in a prediction setting | Temporal ordering and baseline-vs-augmented predictive comparison | Exact model and validation details require full text; AUC gain is not causal evidence |
| 9 | Large-scale Java repository mining; smell correlations with test-code size, complexity and coupling | Candidate covariates and data-source exploration | Java/tool-derived; structural correlations do not establish causal direction |
| 10 | ML-based smell detector evaluation | Detector landscape and measurement-error caution | Better detection does not validate smell as a causal exposure |
| 11 | Discovery and validation of six previously under-formalized smells; workbook reports 1,200 labeled instances and 919 projects | Check whether the project's smell catalogue omits relevant patterns | Java-focused and sample-specific; reported detector metrics/issue acceptance need denominator verification |
| 12 | Comparison of anomaly detection approaches; workbook reports best F-measure below 47% in evaluated setting | Evidence that automated labels may remain noisy | Limited smell types and Java; detector quality is not evidence of causal effect |

## 3. Synthesis and research gap

The workbook's synthesis supports four conclusions:

1. Test smells have been catalogued, and multiple detection tools exist, but supported smells, languages, frameworks and validation quality vary.
2. Prior empirical studies report associations with test-code quality, comprehension, maintenance, evolution and, in selected settings, production-code fault-proneness.
3. Detector output is not automatically ground truth. False positives, false negatives, smell definitions and manual-label uncertainty can affect exposure measurement.
4. The central unresolved question for Team 7 is whether *validated, temporally prior* test-smell measures are associated with *subsequent production-code defects* after addressing plausible confounding—and what assumptions would be needed for a causal interpretation.

The gap should be phrased cautiously. Paper 7 is especially close to the topic, while Paper 8 adds longitudinal and predictive evidence. Team 7 should not claim that no prior study examined smell/fault relationships. The defensible distinction is the project's specific operationalization, validation, temporal design, confounder strategy and causal framing—provided the final implementation actually delivers these.

## 4. Proposed constructs to operationalize

- **Exposure:** smell-type-specific validated presence, count or density measured at a pinned baseline snapshot. Keep presence, raw count and normalized density as distinct variables.
- **Outcome:** production-code defect presence/count/severity in a pre-specified future window after baseline. Choose one primary outcome before testing.
- **Candidate confounders:** production-code size/complexity, test-code size, change churn, prior defects, coupling, coverage, project/version, language/framework and code ownership where available.
- **Measurement quality:** detector version/configuration, manual annotation sample, positive and negative cases, reviewer agreement, precision/recall, and ambiguous cases.

These are candidate constructs from the workbook, not confirmation that all are present in the team's dataset. Include covariates only when justified by a causal diagram and actually measured.

## 5. Full-text extraction priorities

The workbook recommends reading Papers 3, 4, 6, 7 and 8 first. For each, fill the `Full-Text Extraction` sheet with:
- exact research question and study design;
- unit of analysis, sample and time span;
- smell definitions, detector/version and manual validation;
- outcome definition and temporal window;
- comparison group and baseline;
- covariates/confounders and model specification;
- quantitative estimates with confidence intervals, p-values and page/table numbers;
- threats to validity and limits on causal interpretation.

Also resolve the workbook's bibliographic cautions for Paper 2 and Paper 11 before final submission.

## 6. Reporting rules for Team 7

- Do not describe correlation, regression coefficients or AUC improvement as causal effects.
- Do not treat detector flags as validated exposure labels without a documented validation procedure.
- Do not turn missing or not-applicable detector values into zero.
- Do not mix project-level metrics with file-level outcomes unless attribution is justified.
- State the unit of analysis and temporal order explicitly.
- Report failed, missing and inconclusive observations rather than silently excluding them.
- Separate descriptive, predictive and causal analyses in the final paper.

## 7. Current status

This synthesis is based on the team workbook's abstract/bibliographic summaries. It does not add full-text findings, independently verified effect sizes, or new empirical results. It provides the scientific framing for the Analyst's next step: map the constructs above to the actual collected dataset and assess whether the planned causal analysis is identifiable with the available measurements.
