# Additional sensitivity protocol

Specified after the primary evaluation but before the stress run. These are
exploratory robustness checks, not additions to the frozen primary test set.

Four scenarios (pointing, affine drift, near-threshold gain, fast fading), three
methods (constant fit, sequential projected fit, DAP), and 100 new matched seeds
(2001--2100), for each of three conditions: both measurement noise scales times
five; true inertia times 1.25 and true lag times 1.5 with the original nominal
design library retained; and a halved integration/sample step with a matching
nominal design library. Estimator thresholds and the design log-noise floor
remain fixed. Total 3,600 additional trials. Report all rows, acceptance,
rejection, offset error, outage, and conditional confidence coverage, including
failed cases. Do not pool these trials with the primary 5,400.
