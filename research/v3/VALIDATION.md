# Executed validation record

Environment: MATLAB R2026a Update 3 (26.1.0.3276743), macOS. Simulink was available
for the separate network compatibility check. Results were produced on 23 October
2026. System-wall-clock time is not an embedded implementation benchmark.

|Work|Executed outcome|
|---|---|
|Primary evaluation|5,400 unique scenario/seed/method records; all nine scenarios and six methods completed|
|Additional sensitivities|3,600 unique condition/scenario/seed/method records; all three conditions completed|
|Mathematical/software checks|Nine categories passed; includes a duplicate-time temporal-rank rejection check|
|Gaussian-model confidence experiment|393/400 true offsets inside the conservative reported confidence ball (98.25%)|
|Half-step deterministic integration|Final angle difference about 2.1682e-13 rad|
|Simulink compatibility|Original V2 and estimator-only adapter each executed on healthy and pointing scenarios; four simulations completed|
|Independent metric audit|9,000 unique metric rows; correct group sizes, bounds, acceptance counts and primary aggregate outage means|
|Manuscript|IEEEtran source compiled with Tectonic; all eight PDF pages visually reviewed; no unresolved references, overflowing boxes or out-of-page annotations in the final build|

The software checks validate specific algebraic/model properties, not a complete
flight system. The 400-draw confidence experiment uses the ideal Gaussian log
noise model; the main experiments use the original sensor-noise equations.

Development fixes before primary evaluation: recovery-scenario magnitude aligned
to the original project's fault scale; darkness probe suppression applied to all
methods; undefined errors retained as NaN. Development choices are recorded in
PROTOCOL.md. After evaluation, the estimator gained explicit rejection of
rank-deficient temporal timestamps; all executed primary/stress windows have
distinct increasing timestamps, so that guard does not change their results.
The check was rerun on final code. A Simulink export wrapper initially omitted
the runtime field required by the original metric function; the wrapper was
fixed and both compatibility scenarios rerun to completion. Formatting changes
regenerated figures/tables from the existing saved records without resimulating
or modifying primary scientific values.

`results/integrity_audit.json` records delivery hashes and the independent audit.
It is not a claim of independent peer review. Original source/model files were
not intentionally edited; generated supervisors and the new Simulink model are
separate copies under `generated/`. Existing staged/user changes were retained.
