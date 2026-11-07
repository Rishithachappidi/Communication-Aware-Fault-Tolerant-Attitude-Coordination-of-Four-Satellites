# Drift-projected optical fault diagnosis: research V3

This extension implements a focused research candidate, executes its evaluation,
and supplies an IEEE-style manuscript. It does not establish that the work is
ready for journal submission or that the algorithm is globally new.

Start with **paper.pdf**, then **NOVELTY_AND_SUBMISSION.md**. The existing V2 and
attitude/optical integration projects remain available separately.

## What changed

The constant-gain optical regression is replaced by an estimator that explicitly
removes a temporal attenuation subspace before estimating two-axis pointing
offset. An eight-dwell probe has zero constant and linear temporal moments. The
manuscript derives its identifiability condition, uncertainty and mismatch
bounds, and a quasi-static information/energy equality. A new finite-library
planner checks predicted actuator motion, confidence radius, angular energy,
and a service-cost surrogate. It can refuse a diagnostic action.

This is original implementation and mathematical development for this task.
Projection, optical dither and optimal input design are established research
tools; the exact contribution still needs independent novelty assessment.

## What actually ran

- **5,400 primary MATLAB trials:** nine scenarios, six methods, 100 paired seeds.
- **3,600 additional sensitivity trials:** four scenarios, three methods,
  three perturbations, 100 new paired seeds.
- **Nine software/mathematical checks**, including exact affine-drift invariance,
  rank/darkness rejection, information equality and step convergence.
- **Four Simulink executions:** original V2 versus a projection-only adapter on
  healthy and pointing cases, four satellites, seed 101. This compatibility
  check does not integrate the full new planner into the network supervisor.

MATLAB R2026a Update 3 executed these experiments. The primary and stress tests
integrate the project's existing `terminal_kernel` directly with fixed-step
RK4. They are new single-terminal experiments, not multi-satellite Monte Carlo
results. Both main simulations and derivative calculations execute real code;
no result is a promised or invented number.

## Main findings

|Condition|Constant fit|Proposed DAP|Interpretation|
|---|---:|---:|---|
|Affine gain drift: mean outage|11.7604 s|4.2652 s|63.73% lower; fixed projected probing is slightly faster still|
|Steady-gain pointing: mean outage|2.6892 s|2.7404 s|Small delay cost for lower angular energy|
|Near-threshold gain: mean outage|2.2028 s|0 s|DAP refuses diagnosis; this is service preservation, not recovery|
|Fast fading: accepted fits|0/100|0/100|Affine model fails|
|Deep loss: mean outage|12 s|12 s|Aligned optical power is physically insufficient|
|Fivefold noise, affine drift: accepted fits|0/100|1/100|Major remaining robustness limitation|

Under affine drift, fixed sequential projected probing reaches 4.1716 s mean
outage, better than DAP's 4.2652 s, while DAP uses 52.89% less angular excitation
energy than the fixed sequential probe. DAP is not the best method on every
metric. Declining power eventually interrupts service even after successful
pointing correction. All errors, failures, acceptance counts and abstentions
are retained in the result tables.

The estimator-only Simulink copy matches healthy operation. For the pointing
case it recovers but is slightly worse than original V2: affected-link outage
3.92 versus 3.82 s and exact isolation 74.67% versus 76.33%. This is a compatibility
result, not evidence that the full DAP algorithm improves the network.

## Open and reproduce

From the project root in MATLAB:

```matlab
start_research_v3
test_v3
% Existing result folders are protected against accidental overwrite.
run_v3('replication_01')   % 5,400 primary trials, new folder
% run_v3_stress('replication_stress_01') % new 3,600-trial sensitivity batch
% name=build_v3_projection_model(4); open_system(name)
```

Primary code is `dap_fit.m`, `dap_plan.m`, `dap_sequences.m`, `v3_designs.m`,
`v3_trial.m` and `v3_advance.m`. `v3_truth.m` is exclusively injection/evaluation;
neither estimator nor planner receives it or a fault schedule.

`run_v3` defaults to the protected `results/full` directory. Any mode name
other than `smoke` executes the full seed set in its own directory. `smoke`
uses two development seeds and is excluded from paper evidence. The supplied
smoke records predate the disclosed severity/censoring corrections and must not
be combined with final results. The diagnostic wrapper is intentionally common
to all methods. The constant-fit comparator is an adaptation of the V2 optical
regression, not a full rerun of the V2 supervisor.

## Results and paper

- `results/full/trials.csv`: all 5,400 primary trial metric records.
- `results/full/summary.csv`: all 54 scenario/method aggregates and paired
  bootstrap outage intervals.
- `results/full/all_results.mat`: trial metrics, nominal candidate trajectories,
  protocol and representative time histories for the first evaluation seed.
- `results/stress/trials.csv`, `summary.csv`, `records.mat`: all 3,600 additional
  sensitivity metric records; separate from the primary experiment.
- `results/network_integration`: full original/new Simulink records for two
  scenarios and their comparison metrics.
- `results/full/comparison.pdf`, `traces.pdf`: vector figures; PNG versions
  are available for viewing.
- `paper.tex`, `paper.pdf`: editable source and compiled two-column manuscript.
- `PROTOCOL.md`, `STRESS_PROTOCOL.md`: scenario definitions and development
  decisions, with primary and exploratory evaluation kept distinct.

Full histories are saved for representative primary runs and all four Simulink
runs. Primary and stress metric records are saved for every run; full histories
for other seeds can be reproduced deterministically with `v3_trial`.

The paper uses IEEEtran and external generated figures/tables. Compile from this
directory with `tectonic paper.tex`. Times New Roman is used by the local
XeLaTeX-compatible build; another machine may need an installed equivalent.
The source is editable and has no publisher acceptance/copyright markings.

## Limits on interpretation

The service calculation is a nominal conservative surrogate, not a proved flight
safety certificate. It assumes bounded offset and gain slope, exact current
power, and predicted actuator tracking. The new benchmark has fixed range,
a simplified receiver, one diagnosis attempt, a constant offset per window,
and no orbital motion or network traffic. High noise and fast fading expose
substantial failures. The supplied source papers guide presentation structure;
their subject-specific datasets, models, claims and results are not reused.

The local Git remote points to a different repository than the URL supplied in
the request. No remote was changed and no code or manuscript was published.
The human authors must verify provenance and distribution rights. This extension
adds no license to the underlying project.
