# Tool Scope and Research Pipeline

## Tools named in the course instructions
The current notes identify **PyDriller** and **DoWhy**. Their responsibilities are different:

- **PyDriller** extracts Git repository history and change metadata (commits, changed files, authors, dates, and related history features).
- **DoWhy** supports causal modeling and causal-effect estimation using an explicitly specified treatment, outcome, causal graph/assumptions, and data.

## Important gap: Test Smell detection
Neither PyDriller nor DoWhy is a Test Smell detector. The study still needs an agreed method/tool to label test classes/files with smell presence and smell type. Do not silently assume that tsDetect, TestSmellDetector, or a custom AST detector is approved. Ask the instructor/team to confirm the detector and its version, or record a documented decision to implement a small, validated detector.

## Current pipeline
1. Freeze repository inclusion/exclusion criteria and sampling frame.
2. Record repository URL and pinned commit SHA in the repository manifest.
3. Use PyDriller to collect commit history for each selected repository and the agreed time window.
4. Run the approved Test Smell detection method on the exact revisions being studied; preserve raw output and normalize it only after inspecting its actual schema.
5. Measure outcomes and confounders under definitions agreed by the team. Coordinate mutation testing with the infrastructure owner.
6. Join tables using repository identity plus pinned commit SHA (not commit hash alone across multiple repositories).
7. Use DoWhy only after the treatment, outcome, DAG/confounders, estimand, and missing-data rules are agreed and the real dataset is validated.
8. Save commands, versions, failures, exclusions, and collection dates for reproducibility.

## Research integrity
- Do not treat the team's own sample project as study evidence.
- A detector failure is not a negative detection; missing mutation results are not zero.
- Do not report a causal conclusion merely because a DoWhy model ran. State assumptions and diagnostics.
- Confirm the final toolchain and sampling targets with the instructor/team before scaling up.
