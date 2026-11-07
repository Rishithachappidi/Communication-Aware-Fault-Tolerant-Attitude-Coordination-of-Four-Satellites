# Research assessment and route to submission

## The present contribution

The project now has an implemented mathematical research question and executed
evidence, rather than a claim that connecting two existing controllers creates
novelty. The specific question is whether time-varying scalar attenuation can be
eliminated algebraically from received-power-based pointing diagnosis, and what
diagnostic information can be obtained without sacrificing a usable link.

The derivation gives three propositions: identifiability after eliminating the
temporal nuisance subspace; a deterministic model-mismatch error bound; and a
two-axis angular-energy information bound attained by a particular eight-dwell
sequence in the quasi-static affine-drift case. The algorithm evaluates a finite
set of dynamically predicted probes and explicitly abstains when constraints
cannot be met. These are concrete, reviewable technical statements. They do not
automatically constitute sufficient novelty for an IEEE Transactions article.

## Prior art checked on 23 October 2026

|Primary source|Already established|What this draft may claim|
|---|---|---|
|[Guelman et al., TAES 2004](https://doi.org/10.1109/TAES.2004.1386877)|Power-based cooperative extremum-seeking optical pointing|An explicit drift-projected fault-estimation analysis and evaluated service-refusal tradeoff; not the invention of optical dither|
|[Cheong and Manchester, ACC 2014](https://arxiv.org/abs/1310.7262)|Constrained input design for discrimination and fault detection|A specialized closed-form optical regression, balanced sequence and finite candidate implementation; not the invention of constrained active diagnosis|
|[Palmer and Bollas, ISA Transactions 2019](https://doi.org/10.1016/j.isatra.2019.02.034)|Test design that separates fault sensitivity from uncertain nuisance parameters|An explicit temporal-nuisance/optical-power specialization; not a new general nuisance-rejection framework|
|[Milasevicius and Maciulis, Aerospace 2024](https://doi.org/10.3390/aerospace11010005)|Fine-steering hardware and practical actuator constraints|Simulation on the existing terminal model; no hardware performance claim|

This is a targeted search, not a systematic review. Searches covered optical
power dither, extremum-seeking tracking, attenuation fluctuations, active fault
diagnosis, nuisance parameters and constrained input design. Some publisher
full text was inaccessible; author preprints, publisher abstracts and available
primary pages were used. A missing search result is not evidence of novelty.

Orthogonal projection and balanced experimental sequences are elementary known
tools. A reviewer may judge the present specialization incremental. A defensible
stronger claim requires an independent expert to compare the exact equations,
probe construction and practical advantages against earlier optical trackers and
fault-diagnosis designs, including patents and recent work.

## What the evidence supports

1. In the stated model, affine log-gain drift is exactly eliminated if the
   projected angular design has rank two.
2. A matched-input ablation demonstrates why drift projection helps a
   constant-gain comparator on the specified affine-drift trajectory.
3. A lower-energy selected probe trades a small recovery-delay penalty for
   reduced angular excitation.
4. Refusing probes can avoid self-induced outage while sacrificing diagnosis.
5. Fast fading and fivefold noise defeat most fits. Power-limited outages are
   irrecoverable by pointing. These remain part of the findings.

No results establish the world's best algorithm, arbitrary simultaneous-fault
isolation, hardware reliability, a flight-safe supervisor, improved constellation
throughput, or journal acceptance. The full planner has not been deployed in the
old network supervisor. Its separate projection-only compatibility check is
reported without treating it as validation of the complete method.

## Work that remains before a serious Transactions submission

|Need|Concrete experiment or analysis|Why it matters|
|---|---|---|
|Independent novelty assessment|Compare the exact derivation to optical lock-in/nutation tracking, drift-rejecting extremum seeking and robust experiment design|Distinguishes a publishable advance from a useful specialization|
|Literature baselines|Reproduce a tuned optical extremum-seeking/lock-in tracker, joint parameter filter, and robust constrained diagnostic design under matched measurements and actuator budgets|Current ablations establish attribution, not state-of-the-art superiority|
|High-noise estimator|Analyze errors in variables and correlated angle/power noise; evaluate on new held-out seeds and physically calibrated noise levels|Fivefold-noise recovery currently fails almost completely|
|Service certificate|Include bounded power-measurement error and a verified actuator tracking tube; analyze switching between service and acquisition budgets|The current outage surrogate is not a robust guarantee|
|Physical test|Run an optical bench or hardware-in-the-loop setup with a power detector, two-axis steering, controllable gain drift and a real receiver threshold|Checks beam shape, calibration, delay and controller assumptions|
|Full network integration|Integrate the complete planner, not just its estimator, then test geometry, queues, correlated link faults and routing with a sufficient scenario distribution|Required for constellation-level claims|
|Authorship and provenance|Confirm contributors, source licenses, external code attribution, institutional requirements, and AI-use disclosure|The local Git remote differs from the supplied GitHub URL|

The most useful next research direction is a measurement-uncertainty-aware
information/service bound with independent bench validation. It addresses the
observed high-noise and service-gate failures directly. Adding a transformer,
reinforcement-learning agent or another controller without resolving these
specific failures would not establish a stronger contribution.

## Venue and manuscript status

[IEEE Transactions on Aerospace and Electronic Systems](https://ieee-aess.org/publications/taes)
has a direct spacecraft/system scope. Industrial Informatics should be considered
only if a substantial industrial-informatics contribution is developed; its
[published scope](https://www.ieee-ies.org/pubs) is not determined by visual
similarity to a supplied paper. Venue selection remains provisional.

The current PDF is a research draft in IEEE-style two-column format. Its authors
and affiliations are intentionally unassigned. It contains the model, proofs,
algorithm, experiments, ablations, sensitivity findings, limitations and verified
source links. The reference PDFs informed its broad structure and presentation;
their prose, results, affiliations and acceptance markings were not copied.

The draft includes substantive AI assistance disclosure consistent with
[IEEE's published guidance](https://ieee-cas.org/publications/using-ai-generated-content-ieee-article).
Human authors still need to verify the claims, citations, code, provenance and
data before submitting. The evidence package is ready for technical assessment;
the current research should not be represented as submission-ready.
