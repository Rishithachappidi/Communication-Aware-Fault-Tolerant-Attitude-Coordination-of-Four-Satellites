# Requested research checkpoints

Updated 23 October 2026. These statuses summarize executed evidence; they are not journal acceptance claims.

| Requested phase | Status | Delivered evidence and remaining gap |
|---|---|---|
| 1. Project forensic audit | Complete | [Claim-to-evidence audit](audit/PROJECT_FORENSIC_AUDIT.md); 9,000 original rows reproduced; 141 protected original files unchanged. |
| 2. Literature and research gap | Partial | [Review](literature/LITERATURE_REVIEW.md), [comparison matrix](literature/RELATED_WORK_MATRIX.csv), [novelty assessment](literature/NOVELTY_ASSESSMENT.md). Narrow candidate contribution identified; priority over all close work is unconfirmed. |
| 3. Mathematical audit | Complete within stated scope | [Derivations, assumptions and counterexamples](theory/MATHEMATICAL_AUDIT.md). Conditional sampled-model statements; no flight or continuous-uncertainty guarantee. |
| 4. Select a substantive advance | Implemented; novelty unresolved | Reference-relative optical power certificate, measurement envelope and adaptive acquisition gate. These are candidate contributions, not established global priority. |
| 5. Strong comparison framework | Partial | [Algorithm specification](method/ALGORITHM_SPECIFICATION.md), [MATLAB source and guide](v4/README.md): twelve methods including stronger parameter-filter and extremum-seeking architectures, ablations and separate development seeds. Faithful reproductions of close published complete systems remain missing. |
| 6. Experiments and comparisons | Complete for declared simulation protocol; partial against all desired published systems | [Frozen protocol](experiments/EXPERIMENT_PROTOCOL.md), [results](experiments/RESULTS_REPORT.md): 10,800 primary + 18,450 sensitivity trials. Published complete-system reproductions remain missing. |
| 7. Implementation and physical model | Partial | Ten mathematical/model test categories, four analysis tests and nine legacy tests passed; all 29,250 raw traces audited. [Model/bench plan](theory/MODEL_VALIDATION_AND_BENCH_PLAN.md). No bench, HIL or flight validation. |
| 8. Research manuscript | Complete draft | [Ten-page PDF](v4/paper.pdf), [editable LaTeX](v4/paper.tex); figures/tables generated from executed results, including adverse outcomes. |
| 9. Ethics, provenance and requirements | Reviewed; unresolved items | [Sources and rights](reproducibility/SOURCES_AND_RIGHTS.md), [provenance](audit/REPOSITORY_PROVENANCE.json). Source rights, human authorship and submission approvals require confirmation. AI assistance is disclosed. |
| 10. Reproducible delivery | Complete locally; GitHub publication recorded in release | [Reproduction instructions](reproducibility/REPRODUCIBILITY.md), source/data manifests, machine-readable records, code/report and raw-data archives. |
| 11. Three reviewer perspectives | Complete as self-review; external review pending | [Critical review](audit/FINAL_REVIEW.md). Three perspectives by the same assistant, not independent reviewers. |

## Findings that constrain the conclusion

- Affine-drift mean outage: proposed UAD 4.9730 s versus original DAP 4.2462 s. This is a deterioration.
- Fivefold-noise near-threshold case: UAD 0/50 false acquisitions versus DAP 2/50; zero outage here is service preservation, not successful diagnosis.
- Stronger parameter-filter and extremum-seeking comparators outperform the affine-fit methods in some conditions.
- Of 474 selected primary UAD probes, 382 met checked premises, with zero observed bound failures in those 382 cases. Sensitivity includes 100 UAD bound failures outside those premises; all remain reported.
- Ninety-four premise labels were corrected transparently and replayed. Original exports and exact frozen source remain available; performance outcomes were not changed.

## Overall acceptance checkpoint

**Partially complete against the full Transactions research goal.** Engineering, simulation, mathematical audit and manuscript delivery are complete. Defensible absolute novelty, physical validation, faithful close published-system comparisons, source-rights confirmation and independent external assessment remain open. No acceptance probability or journal-readiness claim is made.

GitHub publication does not constitute IEEE submission or physical validation.
