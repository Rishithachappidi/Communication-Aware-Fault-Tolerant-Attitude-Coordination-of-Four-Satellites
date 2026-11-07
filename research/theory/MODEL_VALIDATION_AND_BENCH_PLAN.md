# Physical-model assessment and independent validation plan

## What was actually verified

The optical kernel is a displaced far-field Gaussian intensity sampled by a
small circular receiver. Its `divergence` parameter is the angular 1/e^2
intensity radius, not an unspecified full-angle divergence. With L=800km and
alpha=20urad, beam radius is 16m; receiver radius is 0.05m, giving a/w=0.003125.
Nominal captured power is 3.9062uW for 0.5W optical power and efficiency 0.4.

An independent disk-aperture quadrature evaluates

`P=Pt*eta*(4/w^2)*exp(-2d^2/w^2)*integral_0^a r exp(-2r^2/w^2) I0(4rd/w^2) dr`

at 20 offsets from zero to 60urad. Its maximum relative disagreement with the
retained approximation is 1.7576e-4. This validates the numerical optical
approximation in this geometry, not its correspondence to a physical terminal.

The independently constructed linear sampled-PID state map matches the imported
RK4 derivative implementation under unsaturated conditions for the six declared
actuator models. The old deterministic half-step check gives an angle change of
about 2.17e-13rad. The sensitivity half-step experiment additionally changes
sampling/noise/feedback and therefore does not isolate numerical integration.

## Parameter evidence and limitations

|Quantity|Evidence status|Consequence|
|---|---|---|
|Gaussian angular power law|Consistent analytical model; numerical aperture approximation checked|Not verified against a measured beam profile|
|800km range, 0.10m receiver|Inherited scenario assumptions|No orbit/range dynamics, receiver attitude or obstruction model|
|20urad divergence|Declared 1/e^2 half-angle; plausible optical scale, not hardware calibrated|Published divergence definitions must be converted before comparison|
|0.5W and efficiency0.4|Inherited optical-budget assumptions|Not measured electrical consumption; no wall-plug energy claim|
|J=.002kg m^2, tau=.08s, torque2uNm|Numerical gimbal/controller surrogate from supplied source|No identified mirror/gimbal hardware with these simultaneous parameters|
|Encoder sigma=.08urad, rate sigma=.16urad/s|Assumed independent Gaussian scales|Not sensor specifications; no validated rare-tail or bias model|
|Relative power sigma=.008|Assumed multiplicative sensor error|No photon-counting/background/ADC/shot-noise calibration|
|Sensitivity1.5uW|Binary receiver abstraction|No measured BER, coding, background, wavelength or sensitivity curve|
|Gain slope/curvature|Prespecified test disturbances|No thermal/laser calibration or on-orbit probability distribution|
|Finite six-member actuator set|Explicit discrete hypotheses|Does not enclose a continuous uncertain hardware parameter interval|

[NASA's current communications survey](https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/)
and the [actuator review](https://doi.org/10.3390/aerospace11010005) establish
hardware context and diversity, not calibration of these exact values. For
example, published total terminal electrical powers cannot be substituted for
the model's optical transmit power. The source has no specified wavelength or
transmitter waist, so a complete diffraction/link budget cannot be reconstructed.

## Minimal independent optical-bench study

No optical hardware, external telemetry or laboratory acquisition connection is
available in this environment. The following is an executable experimental
design for a laboratory, not a claim that measurements have been collected.

1. Use an existing characterized Gaussian optical source, two-axis steering or
   translation stage with an independently calibrated position reference, a
   variable attenuator, and a scalar receive-power detector. A reference detector
   may measure injected attenuation for evaluation, but must not be provided to
   the diagnostic algorithm if scalar-only comparisons are intended.
2. Measure beam shape and the relationship between stage angle/translation and
   received intensity. Choose a receiver sampling aperture or fiber arrangement
   appropriate to that beam. Match dimensionless displacement q/alpha rather
   than claiming the laboratory literally reproduces an 800km link. If fiber
   coupling changes the observation law, derive and test that law explicitly.
3. Record dark response, power noise, encoder bias, rate noise, drift, saturation,
   time synchronization and complete actuator transients using independent
   calibration data. Check autocorrelation and tails. A short Gaussian-looking
   calibration record cannot validate mission-wide rare-tail bounds of order
   delta/(5N); use defensible hardware bounds or a separately justified
   statistical envelope instead of importing the simulated Gaussian claim.
4. Declare a real receiver-quality/service threshold from a calibrated link
   measurement, or explicitly label an imposed power threshold as a surrogate.
   Freeze the noise/beam/actuator sets and confidence levels before validation.
5. Apply randomized pointing offsets and independent attenuation ramps under
   held-out run identifiers. Match reference schedules, sensing budgets and
   limits for all algorithms. Log independent truth only to the evaluation side.
6. Include near-threshold healthy links, biased sensing, partial occlusion,
   abrupt faults during probing, continuous actuator uncertainty and loss of
   aligned optical budget. Report all exclusions and instrument failures.
7. Compare predicted lower power with measured power using a calibrated
   measurement-uncertainty allowance. Report certificate applicability and
   violations separately from estimator accuracy and recovery. Do not silently
   remove trials whose hypotheses fail; distinguish those failures explicitly.

At least one independently identified actuator must replace the finite-model
assumption before claiming a hardware service guarantee. A continuous-parameter
reachability enclosure and an online change-of-fault monitor are additional
research requirements. A hardware-in-the-loop run of the same unvalidated
optical equation would check timing/interfaces, not independently validate
that optical model.
