# Preliminary repository-screening analysis

**Status:** Preliminary descriptive analysis only  
**Source branch:** `main`  
**Source files:**
- `results/repository_screening.csv`
- `results/repository_structure_screening.csv`

**Important:** These files describe repository metadata and tree-based structural estimates. They do not contain per-test Test Smell detections, PIT mutation scores, or validated file-level outcome observations. Therefore, the statistics below are screening statistics, not evidence for the causal hypotheses.

## 1. Dataset scope and completeness

- Repositories with metadata: **8**
- Repositories with structural screening records: **8**
- All records report successful metadata/structure collection.
- All 8 repositories are labeled Java in the screening metadata.
- Structural scan reports no truncated Git trees.
- These are candidate repositories, not a confirmed representative sample.

## 2. Descriptive statistics

| Measure | N | Total | Mean | Median | Minimum | Maximum |
|---|---:|---:|---:|---:|---:|---:|
| Estimated Java test-file candidates | 8 | 2,692 | 336.5 | 323.5 | 45 | 767 |
| Java files | 8 | 6,189 | 773.6 | 714.0 | 124 | 1,805 |
| GitHub stars at screening | 8 | 52,112 | 6,514 | 5,545.5 | 1,877 | 15,454 |
| GitHub forks at screening | 8 | 10,980 | 1,372.5 | 1,096 | 268 | 3,249 |
| Maven build-file count | 8 | 70 | 8.75 | 4 | 0 | 47 |
| Gradle build-file count | 8 | 165 | 20.625 | 2.5 | 0 | 100 |

The mean Java-file count is 773.6 (6,189 / 8). Medians are computed over the eight repository-level values.

## 3. Repository-level structure

| Repository | Estimated Java test files | Java files | Maven files | Gradle files |
|---|---:|---:|---:|---:|
| junit-team/junit4 | 252 | 471 | 1 | 0 |
| junit-team/junit-framework | 767 | 1,805 | 7 | 30 |
| mockito/mockito | 487 | 1,015 | 0 | 30 |
| testcontainers/testcontainers-java | 395 | 758 | 0 | 100 |
| hcoles/pitest | 598 | 1,158 | 47 | 0 |
| spockframework/spock | 65 | 674 | 0 | 5 |
| google/truth | 83 | 184 | 7 | 0 |
| awaitility/awaitility | 45 | 124 | 8 | 0 |

## 4. Interpretation and limitations

1. The estimated test-file count is a tree-based repository screening estimate. It is not a count of files successfully analyzed by tsDetect.
2. The structural screening notes explicitly state that these records are not build, detector-compatibility, or PIT execution results.
3. The candidate set is small (8 repositories) and the files do not establish a representative sampling design. Population-level prevalence claims are not supported.
4. The repository screening data cannot answer whether Test Smells are associated with mutation score, future file changes, or bug-fix outcomes.
5. No per-file smell labels, validated PIT attribution, or complete outcome table are present in these two screening CSVs.
6. Repository metadata such as stars and forks is descriptive context only; it is not a causal adjustment set.

## 5. What is required for the final Analyst results

The following study-level inputs are still required in the accessible repository before inferential or causal analysis can be reproduced:

- Detector output with repository, pinned baseline SHA, test-file path, smell name/flag, detector version, and explicit failure/missingness status.
- Outcome observations joined on the agreed baseline test-file key and a defined follow-up window.
- PIT mutation results with validated per-file attribution method, or a documented alternative outcome.
- Confounder measurements and the team-approved DAG/estimand.
- Manual validation labels for detector accuracy and reviewer agreement.
- Raw-run manifests and provenance.

## 6. Reproduction

Run from the repository root:

```bash
python analysis/analyze_screening.py
```

The script reads the two screening CSVs and writes `analysis/screening_summary.csv`.

---

**Conclusion:** The accessible repository supports a reproducible descriptive report of the 8 candidate repositories and their structural screening metadata. It does not currently support final Test Smell prevalence estimates, outcome association tests, mutation-score analysis, or causal estimates. Do not present this preliminary report as completion of the causal study.
