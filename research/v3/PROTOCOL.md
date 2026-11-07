# Frozen evaluation protocol, 23 October 2026

This protocol was written before the first evaluation run. Bug fixes must be
recorded; changes made after evaluation must be disclosed as exploratory.

Research question: can attenuation drift be separated from a constant two-axis
pointing offset, while refusing diagnostic excitation that cannot meet an
explicit conservative service budget?

The method is a research candidate. Its novelty is not established by an acronym,
and no acceptance by any journal is promised.

Nine persistent scenarios, six methods, 100 paired seeds (1001--1100), 14 s per
trial, 20 ms sampling. Seed 17--18 is a software smoke check only. All cases,
including fast fading, deep loss, detector darkness and near-threshold links,
must appear in the report. One diagnosis attempt per trial is allowed for every
active method. No method sees injection timing, future attenuation or true offset.

Development record: the first two-seed software check used 6--12 urad offsets,
which usually did not cause an outage and thus did not test recovery. Before
the full evaluation, offset magnitude was set to 20+6*cos(seed) urad (14--26),
covering recoverable outages around the original project's 25 urad fault scale.
This is a disclosed development choice, not a post-evaluation modification.
The smoke check also motivated suppressing probes below the detector floor
for every method and keeping undefined errors as NaN. Full-evaluation results
will use these final rules. Smoke results are excluded from all paper tables.

The original `terminal_kernel.m` is integrated using fixed-step RK4. Its optical
power equation, 800 km range, 20 urad divergence, 0.5 W transmitted power,
0.1 m aperture, 1.5 uW receiver threshold, inertia, damping, torque/rate limits,
and noise scales are retained. The controller is the project's existing PID
option for every method. This is a new one-terminal benchmark, not a rerun of
the historical Simulink network experiments and not a constellation simulation.

Methods: passive; constant-fit sequential probe (adaptation of the V2 optical
regression, not the full V2 supervisor); projected-fit sequential fixed probe;
projected-fit balanced fixed probe; proposed planner without service constraint;
proposed planner with service constraint (DAP). All fixed probes are 6 urad,
eight dwells of 0.35 s. Candidate probes use balanced schedules, amplitudes
1,2,4,6 urad and dwell 0.35 or 0.5 s. The planner uses the nominal predicted
actuator trajectory to check information. The estimator uses measured angles.

Metrics: absolute offset error; number of accepted/rejected diagnoses; outage
seconds over [2,14); probe duration and angular energy; final two-second link
availability; false pointing corrections on zero-offset scenarios; conditional
coverage of accepted fits. Report sample sizes for every conditional metric.
Report 2,000-resample paired bootstrap intervals for outage differences relative
to constant fit. These intervals are descriptive, without multiplicity correction.
The Gaussian confidence ellipse is valid only for the specified log-linear model
and iid noise; the original plant has multiplicative power and angle noise.
Coverage in that plant is empirical, not guaranteed.

No atmospheric scintillation is asserted for a vacuum intersatellite path.
Time-varying gain here represents an abstract laser/channel calibration change;
fast fading is a deliberately mismatched stress case. Physical validation of
these gain rates remains necessary. The risk bound assumes offset <=30 urad,
log-gain slope <=0.15 /s, initially centered pointing, and nominal actuator
prediction. Quadratic drift and fast fading can violate that slope assumption.

The detector trigger and all estimator/planner constants are fixed in v3_config.
The new evaluation must not be described as evidence of arbitrary multifault
diagnosis, sensor-bias isolation, hardware reliability or network routing gains.
