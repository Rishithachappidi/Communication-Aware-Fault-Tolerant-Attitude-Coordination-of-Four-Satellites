# Pre-specified V4 evaluation protocol

Written before final V4 execution on 23 October 2026. Final output is placed in
`research/v4/results/final`; all V3 source/results stay unchanged. The runner
records final configuration, source hashes, environment and test results before
executing the first evaluation seed. Changes after that point require disclosure
and a separately labeled run; unfavorable outcomes may not be discarded.

## Research questions and method

1. Does a simultaneous measurement envelope prevent the noisy acquisition-mode
   error observed in V3?
2. Does the reference-relative certificate bound sampled probe outage when its
   finite-model, optical and measurement hypotheses hold?
3. What diagnosis/energy/outage/abstention tradeoffs result from enforcing those
   hypotheses and from a first-order noise-aware estimator?
4. Where do increased noise, beam error, bias, actuator mismatch and fast gain
   changes defeat diagnosis or invalidate the certificate?

The advance under test is the reference-relative uncertainty certificate and
acquisition gate, not the invention of safe active diagnosis, GLS, a Kalman
filter or extremum seeking. Statistical information feasibility remains an
approximation, separate from the conditional service certificate.

## Development separation

V3 used seeds 1001--1100 and 2001--2100. Those outcomes informed the scientific
question and are not untouched validation data for V4. V4 software checks use
17,19,31 and 901. Baseline development uses 41--45 on all nine scenarios and
noise factors one/five, with ES gains {0.1,0.3,0.6} and parameter-filter process
variances {0,1e-4,1e-2}. Minimum mean outage across these development conditions
selects ES gain 0.3 and filter process variance 0; false-correction count then
smaller numerical value break ties. All development records remain available.

An attempted generic nonlinear EKF diverged for a development pointing case.
It is retained as source/development evidence but excluded as an obviously
poorly conditioned baseline. The included linear parameter filter uses the
exact transformed observation and standard Kalman updates. Neither baseline
is falsely described as a reproduction of a published complete optical system.

During development, the actuator constraint check was tightened algebraically
by preserving the signed impulse response through the torque/rate output before
taking absolute values. This reduces interval wrapping without changing physical
limits. No final evaluation outcomes informed this choice.

## Primary evaluation: 10,800 trials

Nine V3 scenario definitions are retained, with fixed gain/offset schedules from
`v3_truth`, except that the new wrapper explicitly separates controller parameters
from true actuator parameters. The primary model has no actuator mismatch.
Fault onset remains 2 s and is not passed to decisions. Each 14-s run is sampled
at 20 ms and scored over [2,14). Angle and power noise are sampled independently
per channel/time using the source scales. All methods get the same time-indexed
noise within each scenario, seed and configuration.

100 new seeds, 3001--3100, are used for each scenario and each of 12 methods:
passive, constant fit, sequential projected fixed probe, balanced projected fixed
probe, unconstrained DAP, original DAP, fixed probe with noise-aware GLS, linear
parameter Kalman filter, lock-in extremum seeking, complete UAD, UAD without
its trajectory tube, and UAD with a point-valued acquisition gate.

The fixed diagnostic probe is 6 urad with eight 0.36-s dwells, aligned to the
sample grid. The historical DAP library retains its 0.35/0.50-s timing so that
its algorithm remains identifiable as the old method in the new shared wrapper.
The proposed library uses amplitudes {2,4,6,8} urad and dwell {0.36,0.50} s,
excluding candidates for which the finite-model clamp-containment check fails.
The information radius target remains 1 urad. All diagnostic methods have one
attempt and the same observable residual trigger. The ES tracker is allowed
eight seconds of excitation after that trigger and is assessed separately as
a tracker without certified diagnosis; this is a larger sensing/excitation
budget, disclosed rather than disguised as a matched single-window comparison.

The physical source torque/rate limits, power, aperture, range and receiver
threshold are unchanged. A causal held-reference convention is used for all
methods: observe at the current sample, choose the next interval's reference,
then integrate with that reference. New numerical results are not substituted
for the historical V3 values.

## Sensitivity evaluation: 18,450 trials

New seeds 4001--4050 are paired within configuration/scenario. Default methods
are sequential projection, DAP, noise-aware fixed fit, parameter KF, ES and UAD.
Smaller ablation families are explicitly listed below.

|Sweep|Values|Scenarios|Methods when different|
|---|---|---|---|
|Noise multiplier|1,2,5,10|pointing, affine drift, near threshold|default|
|Affine decline slope /s|0,.045,.09,.15,.25|affine drift|default|
|Quadratic coefficient /s^2|.004,.008,.02|quadratic drift|default|
|Fading log amplitude|.04,.16,.30|fast fading|default|
|True/nominal divergence|.9,1,1.1,1.2|pointing, affine drift|default|
|Pointing magnitude scale|.5,1,1.2|pointing, affine drift|default|
|True J/J0, tau/tau0|(.8,1),(1.25,1.5),(1.5,2)|affine drift, near threshold|default|
|Encoder bias [v,-v/2] urad|v=0,.5,2|affine drift, near threshold|default|
|Gain near threshold|.385,.41,.5,.7|near threshold|default|
|First K library members|2,4,8|affine drift|UAD and no-tube ablation|
|Mission event failure delta|.001,.01,.1 with fivefold noise|near threshold|UAD and point-gate ablation|
|Working-link outage budget /s|0,.5,1,2,4|near threshold|DAP,UAD,no-tube ablation|
|Sample/integration step multiplier|1,.5|affine drift, near threshold|default|

Some sweeps deliberately violate assumptions: divergence 1.2 lies outside the
declared [.9,1.1] range; actuator (1.5,2) lies outside the six finite models;
sensor bias is absent from the sensor-noise premise; slopes above .15 and some
fast/quadratic trajectories violate the gain condition. Report these as
out-of-model tests and count bound violations, not as counterexamples to a
theorem whose hypotheses are false. The half-step experiment changes sampling
and feedback as well as integration; it is not an independent model replication.

## Metrics and raw evidence

Each row reports all finite-fit error, accepted-fit error, attempt status, fit
rejection, plan abstention, missed diagnosis, false correction, total outage,
tail availability, probe count/time, angular excitation, diagnosis time,
counterfactual probe-induced outage, mode errors, budget/bound/tube violations,
confidence radius/coverage, online planner/fit wall time, and retained numerical
buffer bytes. Compute median and 95th-percentile outage as well as mean.

The passive counterfactual shares the same exogenous disturbances and physical
configuration. Probe-induced outage is the simulated potential-outcome count
where the active method is down while passive is up. It is not observed causal
evidence from hardware. Angular energy is not electrical energy. Retained buffer
bytes are not process peak memory. ES performs tracking and therefore does not
receive diagnosis acceptance credit.

Every main/sensitivity run saves measured and true powers/angles, probe masks,
conditional bounds/tubes and evaluator truth in per-condition MAT chunks.
Metrics are stored separately as CSV. Code must generate figures/tables from
these final records. Acceptance, rejection and abstention denominators are
reported separately. Empty conditional metrics remain NaN.

## Statistics and precision

The independent unit is the seeded run. Comparisons preserve within-condition
pairing; time samples are never counted as independent trials. Main UAD--DAP
outage differences use 5,000 paired bootstrap resamples, 95% descriptive intervals,
and Bonferroni-adjusted percentile limits for the nine-scenario family. The
adjusted bootstrap is an approximate inferential procedure, not an exact finite-
sample familywise guarantee. Sensitivity results are exploratory, with sample
sizes and distributions reported without a selective significance narrative.

Zero empirical violations in 100 trials cannot confirm a 1% risk target. Report
the binomial upper confidence bound and the number of selected probes, along
with the narrower conditional theorem. For rare events, the final discussion
must state the remaining precision limitation. No post-hoc exclusion based on
acceptance, diagnosis accuracy or whether the method wins is permitted.

## Validation and environment

Run the mathematical/model tests before final evaluation, preserve source hashes,
and verify every source hash afterwards. The original benchmark and protected
files are checked against their before-work hashes. MATLAB/Simulink versions,
commands, initial Git state and all logs are retained. No optical hardware is
available in the connected environment. Independent aperture quadrature checks
the model approximation, not physical calibration. No publication claim will
describe the new single-terminal simulations as satellite-network or flight
validation.
