# Team 7 Research Pipeline — Working Guide

Use this guide before changing the Developer/Implementation Owner pipeline. It summarizes project-specific constraints; it is not a substitute for the instructor-approved research protocol.

## Read before coding
- `README.md`
- `docs/DEVELOPER_GUIDE.md`
- `docs/DETECTOR_INTEGRATION.md`
- `docs/TOOL_SCOPE_AND_PIPELINE.md`
- `docs/MEASUREMENT_DICTIONARY.md`
- `docs/REPOSITORY_STRUCTURE_SCREENING.md`

## Current project boundaries
- `src/collect_history.py` collects Git history; it does not detect Test Smells.
- `src/build_dataset.py` joins collected history to real detector output. It must not create or infer smell labels.
- The detector and study protocol are not considered approved until confirmed by the instructor/team.
- PIT/mutation-testing measurements belong to the Experimenter. Do not fabricate or attribute project-level PIT scores to individual test files without an agreed attribution method.
- Statistical analysis and causal-effect claims belong to the Analysis workstream and require an approved design, real data, stated assumptions, and diagnostics.

## Data integrity rules
1. Record repository URL/ID and the exact scanned commit SHA for each detector run.
2. Preserve original detector output unchanged; normalize it separately after inspecting its real schema.
3. A scan of the current checkout does not describe historical commits. For commit-level research, scan each selected revision or use a team-approved alternative.
4. A detector failure or unsupported file is missing/failed evidence, not a negative smell detection.
5. Missing mutation results are not zero. Never invent smell labels, metrics, or causal conclusions.
6. Keep raw outputs, cloned repositories, credentials, and other local artifacts out of Git unless explicitly approved and safe to publish.
7. Record tool/version, command, date, commit SHA, failures, exclusions, and configuration to support reproducibility.

## Detector integration checklist
- Confirm the detector name, version, supported Java/JUnit versions, license, and command with the team/instructor.
- Run a small pilot on an approved Java repository.
- Save the unmodified output and a run manifest.
- Inspect actual columns and semantics before transforming anything.
- Validate the normalized CSV with `src/validate_detector_output.py` on the feature branch where it exists.
- Ensure the join key identifies the same scanned revision; do not join a latest-checkout scan to every historical commit.
- Build the dataset only after the schema and historical sampling approach are agreed.
- Report failures, unmatched revisions, duplicates, missingness, and detector coverage to the team.

## Reproducibility and tests
- Run `python -m unittest discover -s tests -v` after relevant changes.
- Do not report tests as passing unless they were actually run.
- Keep changes small and use a feature branch/PR for review before merging to `main`.
- Do not commit unreviewed detector binaries/JARs or claim 1000-project scalability without a measured benchmark.

## Reference
Inspired by the publicly shared Team 7 research-pipeline notes at:
https://github.com/urmiaking/test-smell-causal-study/tree/main/.matemcp/skills/test7-research-pipeline

This file is adapted to this repository's current structure and does not assert that every upstream tool, stage, or result is already implemented here.
