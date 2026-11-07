# Optical diagnosis research V4

V4 is a separately implemented and evaluated research extension. Its candidate
contribution is a **reference-relative conditional service certificate** and an
uncertainty-aware acquisition gate. It is not a claim of globally new safe AFD,
best optical recovery, hardware validation or Transactions readiness.

Open **paper.pdf** for the revised ten-page manuscript and **paper.tex** for
editable source. All numbers/figures/tables are generated from executed records.
The original V3 remains intact in `research/v3`.

## What changed scientifically

- Received-power ratio uses delivered angular increment from the actual starting
  condition, rather than assuming an exactly zero initial angle.
- A sharp centered-ball angular loss bounds optical error and actuator motion
  uncertainty; an explicit simultaneous sensor envelope remains valid at an
  adaptively selected trigger.
- A working link cannot enter acquisition mode merely because one noisy sample
  is low. Uncertain service status retains the working-link budget.
- A finite-model PID/RK4 impulse enclosure checks sampled torque/rate constraints
  before granting a conditional candidate certificate.
- Noise-aware GLS is an engineering correction and ablation. Parameter Kalman
  filtering and lock-in ES provide stronger, disclosed comparator architectures.

The certificate requires a constant offset through the complete window, bounded
gain evolution and optics, correct sensor tails/scales, and one of six finite
actuator models. It is not a continuous uncertain-parameter or flight guarantee.
Information feasibility and approximate statistical confidence remain separate
from the conditional service result.

## Executed evidence

- Original V3: **9000 reruns**, every saved scalar field matched; binary tables,
  representative traces and saved Simulink metrics also checked.
- New final evaluation: **10800 primary +18450 sensitivity =29250 trials**,
  with source hashes/configuration saved before final outcomes.
- Scientific raw-data audit: all **29250 traces**, plus **3400 regenerated
  passive reference masks** for sensitivity counterfactual metrics.
- **10 final mathematical/model test categories**, **4 Python regression tests**,
  and **9 original V2 regression tests** passed. The latter execute seven
  Simulink simulations across network sizes and recovery cases.
- **94 evaluator-label corrections** were disclosed, preserved as original and
  corrected fields, fixed in current source, and replayed. All non-timing
  outcomes match the corrected records. No unfavorable result was removed.

## Main findings, including failures

|Condition|Original DAP in new wrapper|Complete UAD|Interpretation|
|---|---:|---:|---|
|Affine drift, mean outage|4.2462s|4.9730s|Conservatism costs recovery/coverage; UAD accepts93/100|
|Constant pointing, mean outage|2.7338s|3.5980s|UAD is slower and sometimes abstains|
|Fivefold noise, near threshold|0.0524s;2/50 false acquisitions|0s;0/50 false acquisitions|Service preservation with no diagnosis; several mechanisms differ|
|Fivefold noise, affine drift|11.5224s|11.9980s|UAD has no accepted diagnosis|
|Fast gain, mean outage|11.7712s|11.8744s|Parameter KF2.8116s and ES2.4452s recover cases these fits reject|
|Deep optical loss|12s|12s|Pointing cannot restore insufficient aligned power|

Complete UAD selected474 primary probes;382 satisfied the checked premises and
had zero observed bound violations. This conditional count is not proof of a
one-percent flight risk. The sensitivity sweep contains100 UAD bound failures,
including faults that start during an early probe. Those failures stay in the
report; the static-offset certificate does not apply to them. Unmodeled sensor
bias can destroy confidence coverage even when a fit is accepted.

## Start and reproduce

From MATLAB at the extracted project root:

```matlab
start_research_v4
test_v4
% Full fresh dataset; supplied final results are never overwritten:
run_v4('replication_01')
```

Read `research/reproducibility/REPRODUCIBILITY.md` for exact analysis, plotting,
paper-generation, replay, raw-data layout and dependency instructions. Normal
MATLAB suffices for V4; Simulink is needed for the inherited network regression.
Python uses only the standard library. Tectonic and an installed Times New Roman
font compile the paper; Poppler renders it for inspection.

Final results live in `research/v4/results/final`. Code/report packages include
CSV/JSON tables and protocol. The separate raw-data archive contains full MAT
traces; extract both archives at the same root. Raw data occupy several GB
uncompressed. They may also be used directly from the existing workspace folder.

## Research map

|Purpose|File|
|---|---|
|Claim/evidence audit|`research/audit/PROJECT_FORENSIC_AUDIT.md`|
|Literature and novelty|`research/literature/LITERATURE_REVIEW.md`, `RELATED_WORK_MATRIX.csv`, `NOVELTY_ASSESSMENT.md`|
|Corrected mathematics|`research/theory/MATHEMATICAL_AUDIT.md`|
|Physical assessment/bench design|`research/theory/MODEL_VALIDATION_AND_BENCH_PLAN.md`|
|Complete algorithm|`research/method/ALGORITHM_SPECIFICATION.md`|
|Frozen experiment plan|`research/experiments/EXPERIMENT_PROTOCOL.md`|
|Generated results|`research/experiments/RESULTS_REPORT.md`|
|Critical review and readiness|`research/audit/FINAL_REVIEW.md`|
|Reproduction instructions|`research/reproducibility/REPRODUCIBILITY.md`|

## Status

**Partially complete against the full research/publication request.** The
implementation, derivations, experiments, trace audits and revised manuscript
are complete. Absolute priority is not established; matched published complete
system/constrained-AFD reproductions, physical validation and source-rights
confirmation remain unresolved. Three self-review perspectives are provided,
with no claim of independent external peer review. No PR, public release or
paper submission has been made.
