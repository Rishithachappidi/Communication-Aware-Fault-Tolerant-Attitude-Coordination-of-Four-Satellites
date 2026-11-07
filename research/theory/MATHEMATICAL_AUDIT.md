# Mathematical audit and conditional reference-relative service certificate

## A. Observation and identifiability

For b,q in R^2 radians, alpha>0 radians and positive received power,

`p=p0*g*exp(-2||q+b||^2/alpha^2)` implies

`z=log(p/p0)+2||q||^2/alpha^2 = V beta + Q h + rho + epsilon`,

where Q has rows q_i^T/alpha, h=-4b/alpha, V contains the temporal basis, and
the constant nuisance term absorbs -2||b||^2/alpha^2. There is no small-angle
linearization in this algebra beyond the assumed Gaussian angular model.

Let P=I-UU^T for a thin orthonormal basis U of col(V). If V has full column
rank, F=Q^T P Q is positive definite iff P Q has column rank two. Sufficiency:
project, solve uniquely for h, then recover beta. Necessity: if P Q d=0 for a
nonzero d, Q d lies in col(V), and a different nuisance beta absorbs it. This
is a structural statement. A finite numerical eigenvalue cutoff detects weak
conditioning but is not equivalent to the exact rank theorem.

Increasing nuisance degree can only remove information: if col(V1) is included
in col(V2), Q^T P2 Q <= Q^T P1 Q in positive-semidefinite order. More samples
do not fix a probe whose projected angular columns remain dependent.

## B. Covariance, radius and selection

With fixed exact angles, rho=0, and epsilon~N(0,sigma^2 I),

`Cov(bhat)=alpha^2 sigma^2 F^-1/16`.

The 95% ellipse uses squared Mahalanobis radius chi-square(2,.95)=5.991464547.
A circumscribing Euclidean ball has radius

`R95=alpha*sigma/4 * sqrt(5.991464547/lambda_min(F))` radians.

The scaling is dimensionally correct: Q,F,h,z are dimensionless and b is in
radians. Replacing a valid known sigma by a larger random estimate does not
shrink that known-sigma ball, but a residual estimate alone is not necessarily
an upper bound on true noise. Conditioning on passing an acceptance rule does
not preserve nominal coverage. Errors in Q invalidate the exact covariance;
simultaneous power/angle noise and feedback are material here.

V4's feasible GLS is explicitly an approximation, not an exact errors-in-
variables maximum-likelihood estimator. For independent small encoder noise
with per-axis variance sigma_q^2 and small relative power noise sigma_p^2,
the transformed residual has first-order variance

`s_i^2 ~= sigma_p^2 +16 sigma_q^2 ||q_i+b||^2/alpha^4`.

Its second-order mean is approximately
`4 sigma_q^2/alpha^2 - sigma_p^2/2` in two axes. The implementation subtracts
this mean, iterates weighted least squares, reports an approximate covariance,
and uses a chi-square whitened-residual test. These approximations are evaluated
empirically; neither their coverage nor their residual test is an exact theorem
under biased sensors, colored noise, fast gain changes or beam-width error.

## C. Mismatch and balanced probes

For deterministic rho, bhat-b=-(alpha/4)(P Q)^+ P rho, hence

`||bhat-b|| <= alpha ||P rho||/[4 sqrt(lambda_min(F))]`.

This is valid with exact angles and no additional noise. A remainder in col(V)
is eliminated. A remainder Q d is indistinguishable from changing h and may
produce zero residual with nonzero offset bias; V4 explicitly tests this
counterexample. Fast fading is not made harmless by a polynomial basis.

For the eight rows `[+x,-x,-x,+x,+y,-y,-y,+y]` at equal dwell spacing, both
angular columns have zero zeroth and first temporal moments, and
`F=4(a/alpha)^2 I`. For any design energy E=||Q||_F^2,

`lambda_min(Q^T P Q) <= trace(Q^T P Q)/2 <= E/2`.

Equality requires isotropic information and P Q=Q. The specified quasi-static
sequence meets both conditions. This is an elementary optimal-design equality,
not a claim to have invented projection, balanced design, or dynamic actuator
optimality. Dynamic trajectories and a sampling/holding policy require their
own calculation.

## D. Existing power bound and its missing hypotheses

At q0=0, exact current power pc, fixed b with ||b||<=B and a future lower
log-gain slope -L, the old lower bound

`pc*exp(-L*t-[4 B ||q||+2||q||^2]/alpha^2)`

is valid for the actual q. V3 substitutes a noisy pc and a noiseless nominal q,
and does not enforce the initial-state assumption. It therefore implements a
surrogate, as its manuscript correctly acknowledges. Gaussian noise cannot
support an unconditional deterministic measurement bound.

## E. Conditional reference-relative angular theorem

Use the actual current optical error e0=q0+b and actual delivered increment
d=q(t)-q0. The exact ratio satisfies

`log(p(t)/p(0)) = log(g(t)/g(0)) -2[2 e0^T d+||d||^2]/alpha^2`.

The b^2 term cancels; no zero-initial-angle assumption is required. Suppose
e0 lies in ball(c,R) and d lies in ball(dbar,r). Expanding d=dbar+v and using
Cauchy-Schwarz gives the bound

`Dbar=2 c^T dbar+2R||dbar||+||dbar||^2
      +2(||c+dbar||+R)r+r^2`.

Thus `2e0^T d+||d||^2 <= Dbar`. Every term has units radians squared.
For c=0, the bound is **sharp over these two balls**:

`Dmax=2R(||dbar||+r)+(||dbar||+r)^2`.

Proof of sharpness: choose v collinear with dbar with length r and choose e0
in the same direction with length R. If dbar=0, choose any common direction.
These choices attain the upper bound. This angular sharpness does not imply
global tightness when optical gain, alpha and current power have additional
coupled constraints.

For alpha>=alpha_min and log(g(t)/g(0))>=-L*t, a conservative power lower bound is

`p_lower(t)=p_lower(0)*exp(-L*t-2 max(Dbar,0)/alpha_min^2)`.

Replacing a negative Dbar by zero avoids a sign error when bounding uncertain
alpha. It deliberately forgoes a guaranteed pointing improvement. Positive
power, a constant b and alpha over the window, and the delivered increment tube
are indispensable hypotheses. If a scalar gain jump violates the slope model,
the bound need not hold. The code checks actual lower-bound and tube violations
after simulation using truth in the evaluator only.

## F. Finite-horizon measurement event and adaptive start

There are N sampled times and five marginal standard Gaussian disturbances
(two encoder, two rate, one relative power). Set

`kappa=sqrt(2)*erfcinv(delta/(5N))`.

Because Pr(|Z|>kappa)=delta/(5N), a union bound gives a single event E with
Pr(E)>=1-delta on which all these disturbances are bounded over the whole
mission. No independence across channels/times is needed for that union bound;
correct Gaussian marginals and known scales are needed. For multiplicative
power noise and eta=kappa*sigma_p<1,

`pm/(1+eta) <= ptrue <= pm/(1-eta)` on E.

These simultaneous intervals remain valid at a start time selected from the
same observations. A pointwise 99% interval evaluated at an adaptively chosen
trigger would not establish this mission-wide statement.

Acquisition is enabled only if the upper bound is below receiver sensitivity.
If the interval straddles sensitivity, the working-link budget is retained.
Consequently the probability of any falsely enabled acquisition mode is at most
delta under E's model and the stated horizon, including adaptive trigger times.
This does not assert diagnosis success or bound outages outside a certified
probe window.

## G. Delivered-motion tube and discrete-model certificate

V4 includes the six *finite* parameter models given by J/J0 in {0.8,1,1.25}
and tau/tau0 in {1,1.5}. It does not interpolate this into a continuous robust
parameter interval. The nominal PID controller remains fixed when true inertia
or lag changes. One-axis unsaturated state is [q,v,a,I]. The exact A,B matrices
and their RK4 polynomial map are in `pid_discrete.m`; the input comprises
reference, encoder error and rate error.

For each parameter member, the effect of all past bounded sensor inputs at a
sample is enclosed by the finite impulse sum

`r_x <= sum_{j=0}^{N-1} |Ad^j Bd_noise| w_max`.

For torque and rate constraints at RK4 intermediate stages, V4 uses the exact
stage H,J matrices and their impulse sums, retaining cross-state cancellation
before taking absolute values. If the enclosure permits a torque or rate clamp,
the candidate receives no linear-model certificate. Otherwise induction shows
that the unsaturated discrete map agrees with the clipped simulator at every
stage, so the calculated tube encloses all noise realizations on E for that
finite model set. Floating-point roundoff is not formally enclosed.

The candidate tube encloses deviations from the nominal candidate mean. The
current measured angle adds its own sqrt(2)*kappa*sigma_q radius when expressing
delivered increments relative to the measured current angle. Before the first
probe the reference is zero, as assumed by the predictor. A future retry after
a nonzero correction would require a predictor initialized from its complete
reference history; the present method allows one attempt only.

For each candidate, C=sum dt*1{p_lower<pmin}. Under all hypotheses and on E,
sampled actual outage during the candidate is <=C. Selection with C<=budget
therefore gives a mission-event conditional sampled-outage certificate. It is
not a continuous-time certificate, a floating-point proof, a guarantee for
arbitrary actuator parameters, or a safety result after the probe ends. A
zero-budget probe cannot create a sampled outage on E if the tube and optical
premises hold. Those assumptions must not be elided from the manuscript.

## H. Information, optimization and limits

The objective is duration seconds plus 0.03 per urad^2 times angular energy
urad^2*s, yielding seconds. Library search is exact over the declared candidates
only. A first-order predicted statistical radius checks diagnostic feasibility;
it is **not** a robust lower information certificate for all uncertain motions.
Actual measured-angle rank and fit uncertainty are checked again after probing.
One can derive sigma_min(P Q_actual)>=max(0,sigma_min(P Q_nom)-||Delta Q||_F),
but that bound is often vacuous and is not misrepresented as an operative
guarantee. Safe-to-attempt does not mean guaranteed-to-diagnose.

The online bound/search cost is O(KH) and stored candidate trajectories O(KH),
for K candidates and H samples. Offline finite-model tube construction is
O(K M N) small-matrix operations. Feasible GLS with p<=5 coefficients takes
O(I N p^2+p^3) and O(Np) workspace. RK4 simulation cost is separate from online
planner/estimator timing. Runtime and retained buffer size are measured, not
claimed as embedded worst-case execution time or process peak memory.
