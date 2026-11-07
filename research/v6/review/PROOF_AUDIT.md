# Complete analytic audit and independent algebra checks

The six-page manuscript contains the full argument. This file states exactly what is and is not established. No independent external human reviewer or formal proof assistant was available. The new SymPy check is exact algebra, not a complete mechanically formalized analysis theorem.

## General noncentered balls

Let e0=c+u, d=dbar+v, ||u||<=R, ||v||<=r; radii are nonnegative Euclidean radii in radians. Set A=||dbar|| and B=||c+dbar||. The difference between the proposed bound and actual loss is exactly

`2(RA-u'dbar)+2(rB-(c+dbar)'v)+2(Rr-u'v)+(r²-||v||²)`.

1. Exact expansion verifies the identity, with no linearization.
2. Cauchy gives u'dbar<=||u||A<=RA.
3. Cauchy gives (c+dbar)'v<=B||v||<=Br.
4. Cauchy gives u'v<=||u||||v||<=Rr.
5. The radius assumption gives ||v||²<=r².
6. Each displayed summand is nonnegative, proving the general bound. No claim of noncentered sharpness follows.

SymPy verifies the expansion identity exactly. It also verifies the2D Gram determinant `(a'a)(b'b)-(a'b)²=(a1*b2-a2*b1)²`, the algebra underlying the used Cauchy inequality. Ordering nonnegative square roots is a stated mathematical step, not something the polynomial checker independently axiomatizes.

## Centered sharpness and zero cases

For c=0 and A>0, choose u=R*dbar/A and v=r*dbar/A. Both ball conditions hold, and the expression attains `2R(A+r)+(A+r)²`. For A=0, choose u=R*w and v=r*w for any unit vector w. This attains `2Rr+r²`. These constructions remain valid for either radius zero; for both radii zero they reduce to the singleton loss. Exact symbolic reduction checks attainment using dbar'dbar=A², plus the separate A=0 construction.

## Optical conversion and units

The exact relative-power identity requires positive starting power and a constant offset/divergence through the window. Lower gain slope and lower starting power then yield the stated bound. For nonnegative upper angular loss, alpha>=alpha_min makes alpha_min conservative. For negative upper loss, replacing it by zero discards guaranteed improvement and avoids a reversed divergence inequality. Dark/censored cases are not silently put into a positive-power logarithm.

Every angular-loss term is radians squared. Scaling angles by1e-6 scales numerator and divergence squared equally. SymPy verifies this exact ratio identity. The prior separate optimization/power checks remain corroboration, not the proof.

## Sensor event and adaptive start

For5N scalar marginal Gaussian errors, kappa=Phi^-1(1-delta/(10N)). Each two-sided tail is delta/(5N); summation gives Pr(E complement)<=delta with no independence requirement. Simultaneous power intervals hold at any selected index. A false acquisition-enable event is therefore contained in E complement. This is not a claim of exact conditional fit coverage or of safety after the probe.

On E, eta=kappa*sigma_p<1 makes the multiplicative noise factor positive, so positive power is not clipped. At true zero power, measured power is zero and the detector-floor rule refuses probing. At eta>=1 the upper interval is unbounded; no acquisition permission follows. Wrong tails/scales and sensor bias are outside the calibration. Heavy-tail failures are retained.

## Finite actuator and service implication

The existing induction proof uses exact held-input RK4 maps for only six actual model pairs. Finite impulse and stage bounds reject possible clamp activation. A mission-length noise sum overbounds shorter histories; the zero pre-probe reference and single-attempt restriction are required. The starting measurement uncertainty is included when forming actual increments from a measured starting angle. Independent stage/tube calculations and the new complete state-step replay check implementation consistency.

There is no continuous interval proof and no formal rounding enclosure. New parameter-grid experiments do not add one. If true power is above every calculated lower bound, sampled actual outage is pointwise bounded by the predicted lower-bound outage count; summing and imposing the budget gives the corollary. No part of that summation guarantees correct diagnosis, electrical energy reduction or post-correction recovery.

## Unresolved independent assessment

The derivation now has explicit nonnegative slacks, exact-algebra checks, separate optimization tests and complete plant replay. Independent external expert review is still absent. The manuscript and review response explicitly preserve that gap.
