# Questions to Confirm with the Instructor / Team

The following points are not settled by naming PyDriller and DoWhy alone.

1. **Test Smell detection:** Which detector is approved, and which smell taxonomy/version should be used? If no tool is mandated, may the team implement and manually validate a lightweight detector?
2. **Study unit:** Is the unit of analysis a test method, test class, test file, or repository at a pinned commit?
3. **Historical scope:** Must smell status be reconstructed for historical commits, or is a current-revision cross-sectional study acceptable?
4. **Sampling frame:** What languages, project activity, repository size, license, and minimum test counts qualify a repository?
5. **Outcome data:** Is PIT mutation score required for every selected repository or only a feasible subset? What is the planned subset and failure-handling rule?
6. **Causal model:** Which treatment/outcome and estimand are primary? Confirm the DAG and adjustment set before model fitting.
7. **Validation:** Confirm the target and review protocol for manually checking detector precision/recall.
8. **Deliverables:** Confirm expected dataset schema, minimum number of repositories, and whether raw repository metadata can be committed publicly.

Do not delay coding that is already well-defined (PyDriller history extraction and CSV validation), but do not invent answers to these unresolved questions.
