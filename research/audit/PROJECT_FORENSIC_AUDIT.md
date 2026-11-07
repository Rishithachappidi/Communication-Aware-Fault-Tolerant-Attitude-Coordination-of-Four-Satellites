# Forensic audit of optical diagnosis research V3

Audit date: 23 October 2026. Baseline: local commit
`0bc453ffa0ad9127583abfa0e5496d70769c78e5`, with pre-existing staged, modified and
untracked work. The research V3 source itself was untracked. No Git reset,
checkout, remote change, commit, push or publication was performed. Before-work
SHA-256 records and complete initial Git status are in `ORIGINAL_STATE.json`.
All new method development is isolated in `research/v4`.

## Material inspected

The complete V3 manuscript source, eight-page PDF, protocols, implementation,
tests, CSV tables, binary result records and logs were read. The shared terminal
kernel, physical/controller configurations, sensor map, V2 optical estimator,
V2 supervisor, projection adapter, separate Simulink model-builder and original
metric definitions were traced. The original project includes additional
attitude/network studies; their documented limitations were inspected, but they
are not evidence for the new single-terminal method.

## Claim-to-evidence table

|Manuscript claim|Equation / implementation|Experimental evidence|Verification status|Required action|
|---|---|---|---|---|
|Log Gaussian observation is linear in an offset parameter after transformation|`v3/dap_fit.m`: z, Q, h; source `simulink/terminal_kernel.m` optical equation|Algebraic rederivation; noiseless `test_v3`|Verified under known divergence, constant offset, positive power and exact angles|Retain conditional assumptions|
|Offset identifiable iff projected information has rank two|`F=(P_V Q)'(P_V Q)`|Projection-nullspace argument; rank tests|Verified structurally; threshold 1e-5 is numerical, not a structural theorem|Separate structural rank from numerical conditioning|
|95% confidence radius|`dap_fit.m`: alpha^2 sigma^2 F^-1/16 and chi-square 5.991...|400 ideal-model draws; coverage 393/400|Formula valid for fixed exact regressors, iid Gaussian log errors and valid variance bound; observed sensor model differs|Do not claim confidence validity after adaptive acceptance or with errors in variables|
|Mismatch bound alpha ||P rho||/(4 sqrt(lambda_min F))|Projected least-squares pseudoinverse|Independent norm argument; new aligned-remainder counterexample test|Verified for deterministic additive remainder and exact angles|State that a nuisance in span(Q) creates undetectable bias|
|Balanced sequence reaches energy information bound|`dap_sequences.m`; eight equal quasi-static dwells|Temporal moments and F=4(a/alpha)^2 I|Verified; elementary experiment-design specialization|Do not call dynamic actuator design globally optimal|
|Affine-drift constant-fit outage 11.7604 s|`v3_trial.m`, `run_v3.m`|100 saved records and fresh matched rerun|Exact match|Retain as V3 historical result only|
|Affine-drift sequential projection outage 4.1716 s|Same wrapper, `projected_fixed`|100 saved records and fresh matched rerun|Exact match|Retain; this comparator outperforms full DAP on outage|
|Affine-drift DAP outage 4.2652 s|Same wrapper, DAP|100 saved records and fresh matched rerun|Exact match|Retain with energy/recovery tradeoff|
|DAP energy 28.54998 vs fixed 60.59913 urad^2 s|Sum actual angle squared over probe samples|100 traces regenerated and energy independently recomputed|Verified|Call angular excitation, not electrical energy|
|Near-threshold DAP has zero outage and no diagnosis|`dap_plan` service veto|100 saved and rerun records|Verified at nominal noise|No recovery success may be inferred from abstention|
|Fivefold-noise DAP accepts 1/100 affine-drift fits|`run_v3_stress.m`|100 saved and freshly rerun records|Exact match|Retain failure; do not hide it in nominal averages|
|Fast fading defeats accepted fits|Affine drift model and fixed residual cutoff|All six primary methods, 100 seeds|Verified|Retain adverse condition|
|Service constraint is a conservative surrogate|`dap_plan.m`, scalar current-power gate|No measurement envelope or delivered-motion tube in V3|Correctly described as surrogate in text; cannot support robust safety|Replace with conditional reference-relative certificate and uncertainty-gated mode|
|Simulink compatibility|`v3_optical_fit` adapter; unchanged V2 scheduling|`network_integration/*.mat` and JSON, normal/pointing seed101|Original and adapted results are distinct; pointing adapter 3.92 vs 3.82 s outage, 74.67% vs 76.33% isolation|Never report as full-planner network validation|
|9000 metric records|Primary 5400, separate sensitivity 3600|CSV uniqueness, binary T records, fresh reproduction|Verified, every scalar field matched|Maintain disjoint units and datasets|
|All histories stored|README actually states representative primary histories only|54 primary representative traces; other primary/stress traces absent from original archive|No false universal-history claim in README; original audit cannot recover missing traces from saved files alone|Fresh rerun regenerates all traces; V4 saves complete selected scientific trace arrays for all new runs|

## Reproduction actually executed

`reproduce_v3.m` calls original V3 functions without changing them. It repeats
5,400 primary and 3,600 sensitivity trials using the original seed lists, checks
outage and angular energy directly against each regenerated trace, and writes
new records under `research/audit/reproduction`. A separate Python comparison
checked every scalar CSV field, treating NaNs correctly. **All 9,000 rows match.**
`REPRODUCTION_COMPARISON.json` records the result. This is reproduction using the
same equations and kernel, not an independent physical or simulation-model
replication. The original nine-category test also ran successfully. The exact
commands and output logs are preserved.

## Verified defects and limitations

1. **Noisy mode switch:** `dap_plan` unlocks the four-second acquisition budget
   using one `pNow < sensitivity` sample. A working link can therefore be probed
   under a budget intended for a down link. Fivefold-noise sensitivity already
   contains 0.091 s mean near-threshold outage for DAP. This is a scientific
   limitation to correct, not a number to suppress.
2. **Unmodeled delivered trajectory:** candidate simulation starts from zero;
   the wrapper stores `q0` but never uses it in the planner. The source controller
   has noisy angle/rate feedback, whereas the planner is noiseless and nominal.
   The power surrogate consequently has no robust tracking-error allowance.
3. **Errors in variables and log noise:** the covariance treats measured angles
   as exact. Multiplicative Gaussian power noise is not exactly additive
   Gaussian log noise. Measured angle noise enters both response transformation
   and regressors, and feedback creates temporal dependence in motion. The
   fixed 0.06 residual cutoff is not noise-normalized. A small residual can hide
   drift aligned with the angular regressors.
4. **Conditional coverage:** coverage among accepted fits is selected by the
   same data. A fixed-design Gaussian confidence result does not imply 95%
   conditional coverage after data-dependent acceptance. The 400-draw test
   counts the enclosing ball, not the exact ellipse, and uses a variance floor
   at least as large as nominal variance. Its 98.25% is plausible conservative
   coverage in that ideal experiment, not sensor calibration.
5. **Timing convention:** V3 labels the first probe sample when the old
   reference is still being integrated; the reference is updated for the next
   call. Nominal predictor and realized reference therefore differ by one
   sample. A 0.35-s dwell is not an integer multiple of the 20-ms step, producing
   unequal realized dwell lengths. V4 uses a documented causal hold convention
   and sampling-aligned 0.36/0.50-s dwell options. New and historical results
   are kept separate.
6. **Objective comment:** the code says duration dominates the score, but a
   numerical energy term can outweigh duration. Only the stated weighted
   tradeoff is justified. Units and coefficients must be explicit.
7. **Comparator interpretation:** constant fitting is an adaptation inside a
   shared wrapper, not the full V2 supervisor. Original active comparators
   consist largely of estimator/planner ablations. They do not establish
   superiority over published optical tracking or robust AFD methods.
8. **Sampling versus integration:** the half-step sensitivity changes sensor
   sampling, feedback holding and measurement count as well as RK4 step. It is
   not an independent integrator-only convergence test. The deterministic
   half-step unit check has much narrower scope.
9. **Statistics:** 100 seeds are the units, not 700 time samples per trial.
   Descriptive pointwise bootstrap intervals have no multiplicity adjustment.
   The deterministic sinusoidal severity/direction map is reproducible but not
   a flight failure distribution. Independent seeds do not make the physical
   model independent.
10. **Provenance:** the configured GitHub upstream URL now redirects to
    `Rishithachappidi/Communication-Aware-Fault-Tolerant-Attitude-Coordination-of-Four-Satellites`.
    The user-supplied repository is publicly identified as its fork. Thus the
    names are related, not evidence of unrelated ownership. Local history has
    one packaging commit; V3 was untracked. No LICENSE/COPYING file was found
    locally or displayed on the inspected repository page. Fork status and
    public availability do not resolve redistribution rights or authorship.
11. **Physical evidence:** no optical bench, receiver hardware, calibrated
    telemetry or flight dataset is connected. The model lacks a wavelength,
    measured receiver BER/sensitivity curve, actuator calibration and a thermal
    gain-drift model. Physical parameters remain declared assumptions.

## Audit scope boundaries

The immutable snapshot permits a before/after preservation check. The old
`integrity_audit.json` was only a delivery hash, not such a preservation proof.
Static checks for truth-function names are helpful but do not prove
noninterference. V4 adds an explicit decision-input whitelist and separately
tests the predictor against the physical equations.

No independent human reviewers have examined this work. The final review report
will distinguish three critical review perspectives from actual external peer
review. Hardware validation, source rights and complete reproduction of several
published system-level baselines remain external gaps, not completed tasks.
