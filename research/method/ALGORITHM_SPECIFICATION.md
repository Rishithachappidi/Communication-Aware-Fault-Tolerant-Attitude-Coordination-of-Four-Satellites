# V4 uncertainty-aware optical diagnosis specification

## Problem and inputs

Estimate a constant two-axis pointing offset and a local affine log-gain trend
from measured encoder angle and scalar received power. Decide whether to probe
before collecting the new window. The method receives only a nominal whitelist:
beam range, power bounds, sensor scales, receiver threshold, horizon, finite
actuator set, offset prior, gain-slope bound, confidence level, probe library and
diagnostic thresholds. Scenario name, true gain/offset, true actuator mismatch,
sensor bias and fault timing are excluded from the decision interface.

The selected method is called UAD in code solely as a label. The research
contribution is the reference-relative certificate and uncertainty-aware mode
gate in `relative_power_bound`, `power_envelope` and `uad_plan`. It is not the
invention of constrained AFD, GLS, Kalman filtering or extremum seeking.

## Offline construction

1. Generate eight balanced dwells for each amplitude {2,4,6,8} urad and dwell
   {.36,.50} s. Both dwells are sampling aligned at 20 ms.
2. Compute the exact unsaturated RK4 state/input map for the nominal PID under
   each of six declared true actuator models. The controller parameters remain
   nominal. From the finite impulse responses, bound angle error and torque/
   rate at every RK4 stage under the mission-wise sensor event.
3. Mark a candidate invalid if the enclosure permits saturation or rate limiting;
   its linear predictor then has no certificate. This rule may remove useful
   candidates and is not relaxed when the method loses performance.
4. Compute projected information from predicted settled angular motion. Use a
   first-order variance including angle noise to estimate the diagnostic radius.
   This is a statistical feasibility heuristic, separate from the service bound.

## Online algorithm

```
Observe measured angle qm and received power pm.
Apply the common three-sample anomaly trigger after warmup.
If no trigger, keep normal operation.
If detector is dark, abstain; do not identify a unique physical cause.
Construct simultaneous [pLow,pHigh] using known noise scale and mission horizon.
If pHigh < sensitivity: allow acquisition budget.
Else: retain working-link budget, including when status is uncertain.
Bound the current optical-error ball using offset prior and pLow/gain upper bound.
For each valid candidate with acceptable predicted information:
    express predicted motion relative to measured current angle;
    add predictor and current-angle uncertainty to a delivered-increment tube;
    compute the conditional lower-power sequence;
    count predicted below-threshold sampled duration;
    keep the candidate only if duration <= the applicable outage budget.
Select minimum duration + weighted angular excitation from the feasible library.
If none is feasible: record abstention, no diagnosis credit.
Execute the selected causal held reference; collect measured angles/powers.
Fit offset and local log gain with iterated feasible GLS.
Reject censored/rank-deficient/inconsistent/imprecise windows.
If accepted, correct pointing only if its confidence-adjusted magnitude is
    meaningful and estimated aligned power has sufficient lower margin.
Otherwise retain diagnosis/uncertainty without a futile correction.
```

There is one attempt per run. The tube assumes the known zero-reference history
before that attempt; repeated diagnosis after a correction would need a
history-initialized predictor and is outside this implementation.

## Objective, constraints and guarantees

The score is `T + 0.03/(urad^2) * E`, where T is seconds and E is angular
excitation in urad^2*s. It is a weighted tradeoff, not a lexicographic objective
or an electrical-energy model. Selection is exact over the finite library,
not over all feasible waveforms.

On the declared mission event, and if the actual actuator is in the finite set,
the stage bounds hold, alpha and fixed offset are within their declared sets,
and gain obeys the future ratio bound, actual sampled probe outage is bounded
by the selected count. The probability of falsely enabling acquisition is at
most delta under the known Gaussian marginal/scaling model. No unconditional
continuous-time, flight, arbitrary-model or post-probe guarantee is asserted.

Noise-aware GLS uses small-noise approximations, not a proved exact confidence
model. First-order information feasibility does not guarantee an accepted fit.
The saved data separately records whether each certificate premise held and
whether actual power/tube/budget violations occurred.

## Baselines and ablations

Original comparator classes remain available in the shared causal wrapper.
`projected_noise` isolates the noise-aware fit with fixed excitation.
`UAD_no_tube` removes delivered-motion uncertainty; `UAD_point_gate` removes
the simultaneous measurement gate. These ablations do not inherit the full
certificate. The parameter KF and ES are disclosed generic implementations,
selected on separate development seeds. ES's larger time budget and lack of
diagnostic acceptance are explicit in tables.

Online search costs O(KH), the fit O(I N p^2+p^3), and candidate storage O(KH).
Offline tube work is O(K M N) for fixed four-state matrices. Online wall time
and retained array bytes are measured separately from simulation cost; neither
is embedded worst-case timing or process peak memory.
