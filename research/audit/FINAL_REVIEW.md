# Final critical review and completion assessment

Date: 23 October 2026. These are three deliberately separate **self-review
perspectives by the same assistant**, not three independent external reviewers
and not IEEE editorial decisions. Independent human subject-matter assessment
remains absent. No acceptance probability is assigned.

## Reviewer A: mathematics and control

|Serious criticism|Correction / evidence|Remaining limitation|
|---|---|---|
|Nominal power surrogate does not enclose noisy starting power or delivered motion|Derived reference-relative inequality, simultaneous sensor envelope, finite-model impulse tube and adaptive acquisition gate; mathematical audit and numerical tests|Only conditional sampled-probe guarantee under explicit sets/scales|
|Linear predictor cannot be trusted if torque/rate limits engage|Exact sampled/RK4-stage output bounds reject such candidates; direct predictor-versus-kernel test passed for all six models|Not continuous-parameter nonlinear reachability; floating-point proof absent|
|Offset might change during probing|Raw audit discovered94 wrongly eligible premise labels; original export retained, corrected derived labels issued, current logger fixed,94 cases replayed with all non-timing metrics matching|100 total UAD sensitivity bound failures remain, including unmodeled mid-probe faults; theorem cannot cover arbitrary future jumps|
|Projected covariance assumes exact angles and Gaussian log noise|Retained exact conditional derivation; added explicitly approximate feasible GLS and coverage reporting|No exact EIV likelihood or guarantee; bias destroys coverage|
|Residual consistency can hide nuisance aligned with angular input|Added explicit zero-residual/biased-offset counterexample test|Cannot diagnose every drift process from this sensing budget|
|Balanced design theorem is elementary and quasi-static|Narrowed claim; dynamic motion calculated separately|Not globally optimal constrained waveform design or a new general theory|
|Safe probe does not ensure diagnosis|Separated information heuristic, fit rejection and certificate; reported coverage/abstention|Predicted statistical information is not a robust identification guarantee|

Verdict: the conditional mathematical statements are defensible within their
stated discrete/model premises. Their assumptions are restrictive and must not
be converted into a field safety claim. The finite-model construction and
conditional-noise model are substantial barriers to hardware applicability.

## Reviewer B: experimental science

|Serious criticism|Correction / evidence|Remaining limitation|
|---|---|---|
|Original results may be unverified|9000 fresh reruns matched every scalar field; independent trace outage/energy reconstruction; binary/representative trace audit|Same kernel, not independent physical replication|
|Weak original comparison set|Retained original classes, added parameter-filter and ES architecture baselines, fit/tube/gate ablations; selected baseline settings on separate development seeds|Published complete optical/cooperative/robust-AFD systems not faithfully reproduced|
|Tuning leakage|Final3001--3100 and4001--4050 seed sets frozen before execution, with source hashes; no decision/estimation parameter changed after outcomes|Research question was informed by V3 failures; this is disclosed, not pristine discovery data|
|Only successful/accepted errors reported|Both all finite-fit and accepted-fit metrics exported, with counts, abstention, rejection and missed diagnoses|Error is undefined where no estimate exists; coverage does not replace diagnosis availability|
|Averages hide catastrophic failures|P95 outage and all adverse conditions retained; original UAD can have12s upper-tail outage|100 primary/50 sensitivity seeds give limited rare-event precision|
|Metric labels overstate safety|Conditional premise flag corrected; all observed bound failures retained, even outside assumptions|Operational failures outside assumptions still matter; no guarantee against changing faults|
|Raw traces missing|Saved every new scientific trace in77 MAT chunks; raw-audited all29250 traces; saved3400 regenerated passive masks|Large raw dataset; development exploratory EKF evidence is logs/source rather than a full measurement campaign|
|Counterfactual or sampling independence overstated|Shared-noise passive potential outcomes defined; seed is unit; half-step not an independent model|Not hardware causal evidence or a flight fault distribution|
|Timing/memory claims unsupported|Measured online wall times and selected retained buffer bytes, clearly scoped|No embedded worst-case timing, process peak-memory or energy-consumption measurements|

Verdict: the dataset and adverse comparisons are informative and reproducible.
They do **not** demonstrate universal performance improvement. On nominal affine
drift UAD is worse than DAP, the parameter filter and fixed projection; at high
noise it often refuses diagnosis. ES and the parameter filter recover fast-gain
conditions that the original affine fits reject. These findings are central,
not footnotes.

## Reviewer C: Transactions editorial perspective

|Serious criticism|Action taken|Status|
|---|---|---|
|Projection, dither and safe AFD are already established|15-source matrix with verified DOI/publisher metadata, including2023--2026 close work; claim-by-claim novelty classes|Resolved as an overclaiming problem, not as proof of absolute priority|
|Exact proposed contribution may still be incremental|Narrowed contribution to sharp optical-relative ball loss and adaptive-start measurement/acquisition semantics|Originality over recent acquisition/patent literature remains unconfirmed|
|Model has no physical calibration|Independent aperture quadrature and predictor checks, parameter-evidence table and minimal bench protocol|Physical validation absent; same-model checks cannot substitute|
|Source ownership/licensing unclear|GitHub API confirms supplied repository is a fork of renamed upstream; neither API response identifies a license; local source attribution retained|Redistribution/publication rights and human contributions need confirmation|
|Current IEEE requirements and AI disclosure|Official TAES and IEEE policy reviewed; ten-page two-column10pt manuscript uses requested margins; actual substantive assistance disclosed|Human author list, author approvals, submission rights and final verification remain outstanding|
|Requested independent review not delivered|Three self-review perspectives explicitly labeled|External independent human review is still required|

Verdict: **further research is needed before a serious TAES submission**. The
mathematical specialization might support a focused contribution if independent
novelty analysis and practical validation establish its value, but the present
evidence does not justify declaring Transactions novelty or readiness. A shorter
correspondence or a control/optical methods venue is only a possible future fit,
not a guaranteed fallback acceptance.

## Official publication checks

The current [TAES author instructions](https://ieee-aess.org/publications/transactions-aes/author-information)
specify a two-column/single-spaced10pt PDF,1in top/bottom margins,.7in side
margins,3.45in columns and.2in gutter. They state no hard regular-paper page cap
and published overlength charges beyond10 printed pages. The delivered paper
has10 locally compiled pages; final IEEE production length is not guaranteed.
The inspected page did not establish a universal public-data-deposit mandate;
the supplied reproducibility package is supporting evidence, not a claim of
meeting an unverified repository policy.

The same instructions define human authorship/contribution and approval
responsibilities. [IEEE's AI-use policy](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/)
requires disclosure of substantive generated content. The acknowledgement covers
the actual formulation, implementation, analysis, figures and drafting, and does
not invent human verification. No manuscript was submitted or publicly posted.

## Acceptance-criteria status

|Requested criterion|Assessment|
|---|---|
|Claims traced to code/equations/evidence|Completed, with explicit model/premise limits|
|Original preserved and checked|Completed:141 protected hashes unchanged;9000 original rows reproduced|
|Defensible novelty established by literature|**Partial:** narrow candidate identified; absolute priority not substantiated|
|Substantive implemented contribution|Completed as a conditional optical certificate and gate|
|Mathematical audit|Completed analytically and numerically; external independent expert review absent|
|Executable experiments and records|Completed for29250 new runs, all raw scientific traces and adverse cases|
|Relevant baselines completed or blockers documented|Completed at architecture/ablation level; missing faithful system reproductions explicitly documented|
|Figures/tables generated from final data|Completed through provided scripts|
|Failures/abstention/violations honest|Completed; corrected labels and all adverse outcomes retained|
|Manuscript matches implementation|Completed with explicit approximation, finite-set and sampled-time scope|
|Provenance/citations/disclosure reviewed|Reviewed; source-rights and human authorship unresolved|
|Organized for independent verification|Completed with source/data archives and instructions|

**Overall status: partially complete against the entire research/publication
request.** The engineering/audit/evaluation deliverables are complete. A journal
novelty determination, physical validation, source-rights confirmation and
independent external assessment are not completed and are not simulated away.
