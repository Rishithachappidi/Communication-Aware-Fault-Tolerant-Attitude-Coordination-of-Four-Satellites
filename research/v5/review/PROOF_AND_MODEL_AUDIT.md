# Proof, event and actuator audit addendum

This is an independent implementation and a separate derivation check by the same assistant. It is not an external human review. Numerical checks do not replace the analytic proof or enclose floating-point roundoff.

## 1. Angular bound and units

Write e=c+u and d=dbar+v, with ||u||<=R and ||v||<=r. The exact expansion is

`2 e'd+||d||² = 2 c'dbar+||dbar||² +2 u'dbar +2(c+dbar)'v +2u'v+||v||²`.

Each remaining scalar product is bounded by its norm product, producing the implemented expression. For c=0, put v on the ray through dbar with length r and u on the same ray with length R. Then both inequalities are attained and the maximum is `2R(||dbar||+r)+(||dbar||+r)²`. If dbar=0, any common direction suffices. Zero radii and R=0 cause no exception. For c!=0 the expression is an upper bound, not an asserted exact maximum.

All five terms have angle-squared units. Converting every angle from microradians to radians multiplies D by 1e-12 and alpha² by 1e-12; the exponent is invariant. The independent direct-ratio checks test this equality explicitly.

The exact power ratio requires fixed offset and divergence over the window. With pstart>=lo, log(g/gstart)>=-Lt and alpha>=alpha_min, replacing D by max(D,0) gives a valid conservative lower bound. If D<0, using alpha_min directly without this replacement could reverse the intended inequality. The tests include noncentered cases with negative loss. Centered angular sharpness is not global tightness of a power certificate: lo, gain, divergence and the optical-error radius can be coupled.

Independent evidence: `results/verification/algebra.json` records 1,200 directional boundary optimizations and 9,600 direct power checks. The largest centered sharpness discrepancy is 4.55e-13 urad², numerical roundoff scale.

## 2. Adaptive event and censoring

For five channels and N samples, kappa=Phi^-1(1-delta/(10N)). Thus each two-sided Gaussian tail equals delta/(5N), and the union bound gives Pr(E complement)<=delta. Independence is unnecessary to that inequality; the stated marginal tail distributions/scales are necessary.

For ANY selected sample index tau (even an adversarial noncausal selection), interval coverage at all samples on E implies coverage at tau on E. Therefore `{upper_tau<threshold <= true_power_tau}` is contained in E complement. This set inclusion, not an assertion of pointwise confidence after selection, establishes the false acquisition-enablement bound. It does not establish diagnosis accuracy, fit confidence coverage, or safety after the probe.

For eta=kappa*sigma_p<1 and p>0, on E the multiplier 1+sigma_p Z is positive. Consequently the source zero-clamp does not censor power on E and the multiplicative interval inversion is valid. At p=0, pm=0 and [0,0] encloses it. At eta>=1 or nonfinite/invalid measurement, the implementation leaves an infinite upper bound and does not unlock acquisition through that interval. The separate detector-floor rule refuses dark probes.

The 10,000-mission stress test observes 100 global-event failures. Its one-sided 95% exact-binomial upper reference is about 0.0118, so the simulation is compatible with the declared model but cannot empirically prove a 0.01 upper failure rate. Eight false acquisition decisions at the adverse selected time occur outside E. A pointwise 99% interval used at that selected minimum fails dramatically (9,680 false acquisitions). This selection stress test is clearly separate from the actual plant algorithm; the saved-trace checker independently reconstructs the plant's exact adaptive residual trigger.

A separate unit-variance Student-t5 stress has 997/1,000 global-event failures and 477/1,000 false acquisitions at the adverse selected minimum; it deliberately violates the Gaussian premise and is not an optical-plant run. Equal variance alone is insufficient. Bias, wrong scale and non-Gaussian tails are outside this probability calibration. The event argument does not repair those assumptions.

## 3. Finite actuator construction

The Python calculation derives the unsaturated state slopes directly in [q,v,torque,integral], builds the RK4 map by four explicit slope evaluations, and separately evaluates finite impulse convolutions and all intermediate stage maps. It imports no MATLAB predictor. The six discrete maps agree to 1.78e-15 maximum entry error; all candidate tube radii agree to 2.29e-20 rad, and 33,024 stage checks agree.

The induction argument is conditional: the zero-reference pre-trigger history and bounded disturbances put the state within the finite impulse enclosure. If every RK4 stage torque/rate enclosure lies strictly inside its clamps, the saturated source model equals the unsaturated map for that step. Induct over held intervals. The mission-length impulse sum overbounds all shorter histories; taking absolute values after each impulse product retains cancellation within that product. No independence of feedback-selected reference and sensor disturbances is needed for this set bound.

For increments relative to the measured starting angle, the tube includes both future absolute tracking uncertainty and the starting encoder envelope. The initial true angle is not assumed zero; the reference history is zero before the single permitted probe. A retry after an accepted correction would require a newly initialized predictor and is not covered.

The proof is for one of the six actual parameter pairs, with fixed nominal PID gains and the modeled sensor disturbances. It is not an endpoint-interpolation theorem, a continuous-time guarantee, an electrical-energy bound, a floating-point proof or a flight certificate. The 25-point actuator grid and 169-map numerical inspection are stress/consistency checks. No finite sample of interior parameters proves all intermediate parameters safe.

## 4. Physical and timing scope

The independent raw audit recalculates received power using the declared aperture/range/divergence model and recorded angles/gain. Agreement checks implementation consistency. It does not calibrate a laser, receiver curve, divergence, torque actuator or thermal environment. The retained aperture quadrature check is also an independent calculation within a Gaussian optical model.

V5 uses MATLAB R2026a Update3 on Apple M5/MACA64. Per-run planner and fit wall times are saved; their group means/P95 are in summary.csv. Timing excludes offline library generation and plant simulation, depends on JIT/load, and is not an embedded worst-case bound or process peak-memory measurement. The fixed-margin method retains common precomputed constraint validity, so it is not described as removing all offline analysis.
