# V7 response and checkpoints

V7 rebuilds V6 as a regular-paper **candidate** with a complete technical narrative. It does not establish IEEE Transactions novelty, acceptance, physical safety or submission readiness. Original files and all V4–V6 records are preserved.

|Requested checkpoint|Action / reviewable evidence|Status and remaining boundary|
|---|---|---|
|1. Resolve angle/rate units from implementation|`audit_measurement_units.m`, `results/measurement_units.json`; main III-B; supplement II. 2,100 direct sensor-kernel samples agree exactly. Separate σq rad, σv rad/s; legacy numeric coupling γv=2 s⁻¹ explicitly declared.|Completed as source/numerical and dimensional audit. Independent sensor hardware calibration remains absent. No old simulated noise values changed.|
|2. Numeric δ, N, quantile|Main IV-B: δ=.01, N=700 (0:.02:13.98), five channels, κ=4.6808310827377051 in MATLAB, rounded 4.680831082738; exact formula and two-sided tail supplied.|Completed for the declared Gaussian mission. No biased/heavy-tail extension.|
|3. Derivation and real-source enclosure|Main IV–V gives central theorem, explicit nonnegative slack proof, centered equality/zero cases, finite RK4 maps and stage-clamp induction. New exact symbolic checks plus preserved independently calculated six-model/tube audit. New 5,040,000-step replay; combined distinct studies 10,080,000 steps.|Completed as written proof/algebra and independent calculation. No external human proof review, formal rounding or continuous-parameter proof.|
|4. Accepted-radius misses|Main VII-D exposes 26/594 at first midpoint; explains noisy regressors, transformed noise, estimated weights and acceptance selection. Source-level approximations distinguished from exact-regressor covariance. Bias sensitivity shows 39/39 misses.|Completed as honest interpretation. No causal attribution of individual misses or claim of calibrated conditional coverage.|
|5. Matched prior-art comparisons|New 7,200 runs: adapted parameter KF and conventional ES, same six settings/100 seeds/six models/2.88-s cap. Complete 24-row table, all raw traces, paired seed statistics, incompletion counts. Main II, VI, VII-F and `BASELINE_MAPPING.md` distinguish architectural adaptation from original-paper reproduction.|Partially completed. Two feasible architectures run; faithful Guo/Massa/safety-filtered ES and closest optical reproductions remain incomplete; dependencies/access/mapping blockers documented.|
|6. Separate history/provenance|Main ten-section scientific narrative; V4/V5/V6 names and correction details moved to four-page supplement. Preservation and corrected historical exports retained in package.|Completed. Main still identifies distinct evidence categories and does not silently merge data.|
|7. Rights, version and AI policy|Original terminal commit, public V4 release commit/tag, frozen source hashes, package manifest and repository license metadata recorded. Substantive AI disclosure in Acknowledgments identifies system and affected sections. Official IEEE policy verified 2026-10-23.|Partially completed. GitHub reports no license. Human rights ownership/permissions, author list and final approval cannot be inferred; no license or author/approval invented.|
|8. Add substance rather than padding|Ten sections, explicit assumptions/notation, central theorem, algorithm and complexity, five source-supported figures, six tables, two new matched architectures and independent replay. Main 12 pages; supplement four pages.|Completed as a structural and evidential research revision. Not grounds alone for regular-paper submission.|

## Results that limit the claim

- First midpoint: certificate selects600/600, accepts594 (26 accepted-radius misses); fixed guard selects0. Both have zero sampled outage.
- Parameter KF accepts600 with15 approximate-radius misses, with mean angular excitation74.747 versus8.331 μrad² s for the certificate. No claim of universal superiority survives this comparison.
- Reverse midpoint: guard accepts41 while certificate refuses all, again no sampled outage. These heuristic admissions are not demonstrated unsafe.
- At that midpoint KF/ES each select558, including30 probes unfinished at14s. They are separate from completed rejected fits; raw data retained.
- Every row in the restricted 14,400-run study has zero sampled outage; this is not a field risk estimate.
- The 1,421 complete UAD-bound records all pass numeric premises under the declared simulator. The7,200 added noncertificate runs do not enlarge that certificate denominator.

## Supervisor change versus experiment

V7 adds remaining-mission-horizon and rate-unit validation and refuses a nonfinite monitor bound. Twenty-two tests pass; all1,421 original UAD authorizations are shadow-replayed using actual start times. This interface improvement does not retroactively modify any recorded plant run. The extension checker changes only its fit-rejection predicate to recognize unfinished probes.

## Structure/reference verification

Official TAES guidance: https://ieee-aess.org/publications/transactions-aes/author-information (accessed2026-10-23). Scope and complete treatment matter; page count alone is not qualification. Charges beyond ten printed pages apply under current guidance.

Lei et al.: publisher DOI10.1109/TAES.2023.3340636; https://ieeexplore.ieee.org/document/10349913/. The linked arXiv2305.19644 manuscript is earlier and differently titled, used as an organizational example only. It is not verified identical to the 2024 published article.

Oh–Noh: https://ieeexplore.ieee.org/abstract/document/11690955/, DOI10.1109/TAES.2026.3733932. Publisher metadata and abstract verified; full text unavailable. No faithful-reproduction or priority claim follows.

IEEE AI policy: https://open.ieee.org/author-guidelines-for-artificial-intelligence-ai-generated-text/. Generated text, figures and code require substantive acknowledgment; the manuscript identifies OpenAI Codex and scope across Sections I–X and supplement. Human responsibility and rights approvals remain open.
