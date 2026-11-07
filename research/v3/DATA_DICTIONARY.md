# Result fields

Every metric row is one scenario, seed and method. Stress rows additionally
identify the perturbation condition. Paired comparisons use identical seed
order and the same time-indexed random noise per method, within each condition.

|Field|Meaning|
|---|---|
|attempted|The common observable trigger requested one diagnosis attempt|
|rejected|The requested **probe plan** was refused; this does not count fit rejection after a probe|
|accepted|A completed fit passed all estimator checks|
|error_um|Euclidean offset error of a finite computed fit, whether accepted or rejected; NaN if no estimate|
|coverage|Truth lies inside the reported confidence ball, conditional on fit acceptance; NaN otherwise|
|outage_s|Physical received power below sensitivity integrated over [2,14), a fixed 12-s denominator|
|probe_s|Time for which a diagnostic reference was issued|
|energy_urad2s|Integral of squared actual two-axis terminal angle during probing, in urad^2 s; not electrical energy or torque energy|
|tail_availability|Available fraction over [12,14)|
|false_correction|A pointing correction exceeding 4 urad was applied in a zero-offset scenario|
|amplitude_um|Selected reference amplitude; zero when no plan exists|
|start_s, finish_s|Observed diagnostic start and end; NaN if absent|
|predicted_risk_s|Nominal lower-power surrogate time below sensitivity; NaN for fixed comparators|

Summary `median_error_um` includes finite rejected fits. It must always be read
alongside `accepted`. `conditional_coverage` concerns accepted fits only; it is
not a coverage result for rejected or unobserved faults. `delta_outage_s` is the
mean paired difference from the constant-fit comparator; negative is less
outage. `delta_ci_low/high` are 2,000-resample descriptive bootstrap limits with
no correction for multiple comparisons. The nominal Gaussian confidence model
does not exactly match the simulated angle/power noise model.

`trials.csv` contains every metric record. `all_results.mat` stores all primary
metric records and representative histories (seed 1001 only), not histories for
all 5,400 runs. The other histories can be rerun from saved seeds. Stress records
likewise contain all metrics, not every time series. Simulink compatibility
records contain complete histories for both original/new methods and scenarios.
