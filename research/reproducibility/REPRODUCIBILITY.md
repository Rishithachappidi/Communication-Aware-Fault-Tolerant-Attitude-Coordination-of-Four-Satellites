# Reproducing the audit, experiments and manuscript

## Environment

Executed: macOS, MATLAB R2026a Update 3 (26.1.0.3276743), Simulink available for
the legacy regression. Core V4 simulations require base MATLAB, its normal JVM
for source hashing, graphics, `gammaincinv`, and standard numerical functions.
No optimization, statistics, machine-learning or external solver toolbox is used
by the new estimator/planner. The inherited model uses MATLAB graphs/configs.
Python 3.14 standard library performs CSV/metadata analysis, hashing and tests;
NumPy/SciPy are not required. Tectonic compiles the multi-file IEEEtran source;
fontspec uses installed Times New Roman. Poppler's pdfinfo/pdftoppm verifies the
PDF. Initial TeX package fetching may require internet. Use an installed serif
equivalent if building on a host without that font.

## Read first

- `research/audit/PROJECT_FORENSIC_AUDIT.md`: original claims and verified defects.
- `research/theory/MATHEMATICAL_AUDIT.md`: proofs, assumptions and guarantee scope.
- `research/experiments/EXPERIMENT_PROTOCOL.md`: before-outcome final experiment.
- `research/experiments/RESULTS_REPORT.md`: automatically generated aggregates.
- `research/literature`: verified references, comparison matrix and novelty limits.
- `research/v4/paper.tex`, `paper.pdf`: revised manuscript and generated figures.

The earlier V3 version remains at `research/v3`. Its files were hashed before
work. The final original-preservation audit checks all 141 recorded files in
the working directory, including source, data and historical intermediates.
The downloadable research package deliberately omits old private/intermediate
rendering files; its own package manifest identifies the files actually shipped.

## Completed executions

|Execution|Count / result|Evidence|
|---|---|---|
|Original V3 reproduction|5400 primary +3600 sensitivity, all scalar fields match|`research/audit/reproduction`, `REPRODUCTION_COMPARISON.json`|
|Saved V3 binary audit|9000 table rows, 54 representative traces, four saved Simulink metric reconstructions|`research/audit/SAVED_BINARY_AUDIT.json`|
|Legacy V2 regression|9/9 tests passed, including Simulink sizes4/6/8/10 and recovery cases|`research/audit/V2_REGRESSION.csv/.mat`|
|Final V4 primary|10800 runs, 100 paired seeds per scenario/method|`research/v4/results/final/primary.csv`|
|Final V4 sensitivity|18450 runs, 50 paired seeds per configuration/scenario/method|`sensitivity.csv` in the same folder|
|Full scientific raw-trace audit|10800 primary +18450 sensitivity traces, 77 MAT chunks; 3400 passive counterfactuals regenerated|`raw_audit.json` and counterfactual MAT masks|
|Evaluator repair replay|94 affected runs reexecuted; all non-timing metrics match corrected rows|`evaluator_repair_replay.json`|
|Final mathematical/model test categories|10 passed|`final_tests.json/.mat`|
|Postprocessing regression tests|4 passed|`research/v4/tests/test_analysis.py` and test log|

The 3400 passive regenerations are validation/counterfactual work, not 3400
additional independent primary trials. Source/kernel reuse is not an independent
model replication. Baseline-development data are separate in
`research/v4/results/baseline_development.csv`.

## Generate the supplied figures/tables and paper

From the extracted project root:

```text
python3 research/v4/analyze_v4.py
python3 -m unittest discover -s research/v4/tests -p 'test_*.py'
```

From MATLAB at the project root:

```matlab
start_research_v4
report=test_v4;
plot_v4;
```

Then:

```text
python3 research/v4/build_paper.py
```

When using a package that excludes historical intermediates, append `--package`
to the analysis command. It lists unavailable historical hashes explicitly and
still refuses any changed available source. In the original workspace, the
strict check passes for all 141 protected files. Analysis compares the exact
frozen source with the recorded source hashes and permits only the documented
evaluator-only source repair.

## Repeat the full final protocol without overwriting supplied results

In MATLAB:

```matlab
start_research_v4
folder=run_v4('replication_01');
```

This runs all 29250 final-protocol trials in a new folder. Existing output
directories are protected against overwrite. The current source has the
corrected premise logger; decisions and performance are unchanged from the
archived final-run algorithm. Source hashes and the complete protocol are saved
before evaluation. Raw files consume several GB before compression.

For a separate regenerated analysis/paper:

```text
python3 research/v4/analyze_v4.py replication_01 --package
```

```matlab
plot_v4('replication_01');
```

```text
python3 research/v4/build_paper.py replication_01
```

The separate paper is `paper_replication_01.pdf`; canonical final results are
not replaced. Runtime values depend on host/JIT/load and should not be expected
to match byte for byte.

## Exact pre-repair source versus corrected reporting

The source that produced the original final run is archived in
`research/v4/frozen_source`, with the original **nine-category** pre-evaluation
test file. The delivered current suite has ten categories because
it adds the discovered mid-probe-fault regression. To rerun that exact source,
copy the contents of `frozen_source` (including `tests`) into a new sibling folder
such as `research/v4_replay`, add that folder to MATLAB, and call `run_v4` there.
The sibling location is important because the setup resolves the project root
two levels above the method directory. Avoid putting both versions ahead of one
another on the path; use a fresh MATLAB process.

The frozen evaluator omitted offset constancy from its *premise logging*.
`primary.csv` and `sensitivity.csv` remain its immutable original exports.
`primary_corrected.csv` and `sensitivity_corrected.csv` retain every outcome and
add `certificate_premises_recorded` while explicitly correcting 94 labels.
`premise_flag_corrections.json` lists every changed key. The current source fixes
the logger; `evaluator_source_repair.json` records that narrow source change.
All 94 affected runs were replayed and all non-timing metrics match the corrected
records. Neither an outcome nor an unfavorable violation was deleted.

## Raw data dictionary

- Primary chunks: `primary_<scenario>.mat`; `traces{seed_index,method_index}`
  follows the ordering in `protocol.mat` / `protocol.json`.
- Sensitivity chunks: `sensitivity_<sweep>_<value>_<scenario>.mat`; methods and
  seed order follow the corresponding sweep declaration in the protocol.
- Each trace stores times, true/measured power and angle, actuator torque,
  probe mask, delivered-increment prediction/tube, power bound, fitted parameters,
  selected plan, true injected gain and evaluator-only noise summary.
- Counterfactual files store passive `down` masks by seed for exact reconstruction
  of the reported simulated causal-outage metric.
- `certified_probe` in the frozen export means a lower-bound sequence was
  calculated. For ablations, that sequence omits part of the certificate.
  The full theorem applies only to complete UAD with all corrected premises.
- Coverage among accepted fits is conditional. The all-fit field also includes
  rejected finite fits. Neither field turns approximate GLS/KF statistics into
  an exact confidence guarantee.
- `trace_buffer_bytes` is the retained numeric array footprint, not process peak
  memory. Online timing excludes the offline library and plant simulation.

## Commands used in this environment

The saved logs record MATLAB `-batch` calls to `reproduce_v3`,
`audit_saved_binary`, the legacy `runtests('revisions/v2/tests')`, `test_v4`,
`develop_baselines`, `run_v4('final')`, `audit_v4_raw`, `verify_evaluator_repair`
and `plot_v4`, plus Python analysis/tests and Tectonic. All final experiment
settings are in the frozen JSON; no fault schedule enters decision functions.
The raw-audit script is configured for the supplied final folder and does not
overwrite its scientific traces.
