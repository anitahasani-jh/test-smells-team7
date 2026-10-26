# Team 7 Research Pipeline — Working Guide

Use this guide before changing the Developer/Implementation Owner pipeline. It summarizes project-specific constraints; it is not a substitute for the instructor-approved research protocol.

## Read before coding
- `README.md`
- `docs/DEVELOPER_GUIDE.md`
- `docs/DETECTOR_INTEGRATION.md`
- `docs/TOOL_SCOPE_AND_PIPELINE.md`
- `docs/MEASUREMENT_DICTIONARY.md`
- `docs/REPOSITORY_STRUCTURE_SCREENING.md`

If the team later adds an approved research contract, roadmap, or reproducibility protocol, update this list to include those files.

## Current project boundaries
- `src/collect_history.py` collects Git history; it does not detect Test Smells.
- `src/build_dataset.py` joins collected history to real detector output. It must not create or infer smell labels.
- PyDriller is for repository history; DoWhy is for causal analysis after the treatment, outcome, assumptions, and validated dataset are defined. Neither is a Test Smell detector.
- The detector and study protocol are not considered approved until confirmed by the instructor/team.
- PIT/mutation-testing measurements belong to the Experimenter. Do not attribute a project-level PIT score to an individual test file without an agreed, documented attribution method.
- Statistical analysis and causal-effect claims belong to the Analysis workstream and require an approved design, real data, stated assumptions, and diagnostics.

## Unit of observation and keys
Before creating the final dataset, the team must explicitly approve its unit of observation (for example, test file at a pinned repository snapshot). Do not silently switch between repository-, commit-, class-, and test-file-level rows.
- Commit hashes are not globally unique across repositories. For multi-repository data, use a composite identity such as `repository_id + snapshot_sha`; include `test_file` when the approved observation unit is a file.
- The current `build_dataset.py` join uses `commit_hash`. Confirm whether it must be extended to a repository-aware composite key before combining multiple repositories. Do not assume the current join is sufficient for a multi-repository causal study.
- A detection result must identify the exact source revision scanned. A latest-checkout scan cannot be assigned to every historical commit.

## Data integrity rules
1. Record repository URL/ID and the exact scanned commit SHA for each detector run.
2. Preserve original detector output unchanged; normalize it separately after inspecting its real schema.
3. A detector failure, unsupported file, or blank/not-applicable detector result is missing/failed evidence, not a negative smell detection.
4. Missing mutation results are not zero. Never invent smell labels, metrics, or causal conclusions.
5. Keep raw outputs, cloned repositories, credentials, and other local artifacts out of Git unless explicitly approved and safe to publish.
6. Record tool/version, command, date, commit SHA, configuration, failures, and exclusions to support reproducibility.
7. Keep development smoke tests separate from research evidence; the team's sample project is not study evidence.

## Detector integration checklist
- Confirm the detector name, version, supported Java/JUnit versions, license, and command with the team/instructor.
- The current candidate documented in `docs/DETECTOR_INTEGRATION.md` is tsDetect / TestSmellDetector; this remains a candidate until approved.
- Run a small pilot on an approved Java repository and manually inspect a sample of detections and failures.
- Save the unmodified output and a run manifest.
- Inspect actual columns and semantics before transforming anything. Do not assume output columns or that a blank value means “no smell.”
- Validate the normalized CSV with `src/validate_detector_output.py` on the feature branch where it exists. This validator checks file structure and `commit_hash`; it does not validate detector accuracy or prove the scanned revision matches the hash.
- Ensure the join key identifies the same scanned revision; do not join a latest-checkout scan to every historical commit.
- Build the dataset only after the schema, observation unit, join keys, and historical sampling approach are agreed.
- Report failures, unmatched revisions, duplicates, missingness, and detector coverage to the team.

## Sampling and historical revisions
- Pin immutable commit SHAs for any selected snapshots and retain an exclusion log with reasons.
- If a fixed-date sampling strategy is chosen, document the date rule, random seed (if applicable), search/source method, and exclusions. GitHub search results can be biased and should not be described as a representative sample without justification.
- Historical smell evolution requires scanning each selected historical revision or using another explicitly approved measurement strategy. A scan of the current checkout cannot reconstruct earlier smell status.

## Reproducibility and tests
- Run `python -m unittest discover -s tests -v` after relevant changes.
- Do not report tests as passing unless they were actually run.
- Keep changes small and use a feature branch/PR for review before merging to `main`.
- Do not commit unreviewed detector binaries/JARs or claim scalability (for example, 1,000 repositories) without a measured benchmark.
- Resumable checkpoints, retry-failed workflows, atomic shards, and large-scale performance claims are not assumed to exist in this repository. Treat them as future engineering work unless implemented, tested, and documented here.

## Reference and adaptation note
This guide was informed by the publicly shared Team 7 research-pipeline notes:
https://github.com/urmiaking/test-smell-causal-study/tree/main/.matemcp/skills/test7-research-pipeline

It selectively adapts relevant research-integrity and reproducibility guidance to this repository's current files. Upstream-specific stages, run results, binary checksums, local environment details, and performance claims are not imported as facts about this project.
