# Literature investigation through 23 October 2026

## Search scope and evidence quality

Searches covered optical acquisition/tracking/pointing, scalar-power alignment,
lock-in/extremum seeking, joint estimation, temporal nuisance rejection,
active fault diagnosis, risk-constrained input design, safe extremum seeking,
receiver thresholds, actuator uncertainty and link-margin-aware acquisition.
Searches included explicit 2022--2026 filters and the exact existing manuscript
concepts, plus foundational references. Primary publisher pages, original
author manuscripts, author institutional records, Crossref DOI records and IEEE
policies were used. Search date and source access limitations matter: this is
a focused technical investigation, not a claim to have exhaustively searched
every database or patent family.

`RELATED_WORK_MATRIX.csv` contains 15 source-specific comparisons and records
what is and is not established by accessible material. `DOI_METADATA.json`
contains verified titles, authors and bibliographic fields. All cited DOI titles
were checked against DOI/publisher metadata; the 2004 TAES record was checked
against its publisher page when the metadata API failed. Full author PDFs were
available for Krstic/Wang's foundational ES analysis and Williams/Krstic/Scheinker's
safe-ES paper. Several Elsevier pages exposed abstracts but blocked full text.
Unverified implementation details are labeled unknown rather than inferred.

## What is already established

Optical alignment by extremum seeking predates this project: the
[2004 intersatellite pointing work](https://doi.org/10.1109/TAES.2004.1386877)
uses a cooperative architecture, while
[Cai et al. (2020)](https://doi.org/10.1016/j.ifacol.2020.12.1519)
describe coarse vision/PD alignment and fine perturbation-based tracking.
These systems differ in sensing and optical controls, but decisively rule out
claiming optical power dither as new. The generic architecture follows
[Krstic and Wang (2000)](https://doi.org/10.1016/S0005-1098(99)00183-1);
its stability theorem cannot simply be inherited by a sampled, clipped two-axis
implementation. The [2024 survey](https://doi.org/10.1016/j.automatica.2023.111481)
also documents the maturity of constrained ES research.

Fault-oriented input design with uncertainty is likewise established.
[Cheong and Manchester (2014)](https://doi.org/10.1109/ACC.2014.6859400)
address constrained model-discrimination inputs, and
[Palmer and Bollas (2019)](https://doi.org/10.1016/j.isatra.2019.02.034)
explicitly separate sensitivity to faults from uncertain nuisance parameters.
Therefore nuisance rejection and information-versus-control optimization are
not independent novelty claims for DAP.

Recent work narrows the defensible claim further.
[Guo et al. (2023)](https://doi.org/10.1016/j.automatica.2023.111194)
study risk allocation for stochastic linear AFD under chance constraints.
[Cao et al. (2024)](https://doi.org/10.1109/TCYB.2023.3331971)
reconcile diagnostic and control objectives through trajectory design.
[Massa and Paulson (2024)](https://doi.org/10.1016/j.conengprac.2024.106118)
describe constrained nonlinear guaranteed diagnosis under bounded uncertainty.
These are direct precedents for robust or chance-constrained AFD; adding such
terminology to a nominal planner would not constitute a new contribution.

[Williams et al.](https://doi.org/10.1109/TAC.2024.3469785), published online
in 2024 and in TAC volume 70 in 2025, establish practical safety-filtered ES
under their stated hypotheses. Their guarantee concerns an estimated-gradient
CBF framework. A distinct finite-horizon sampled optical-power certificate is
not interchangeable with that guarantee, and cannot claim priority over safe
ES as a general idea.

The [October 2026 link-margin-aware acquisition paper](https://doi.org/10.1016/j.optcom.2026.133342)
is especially relevant to any claim involving optical scanning and availability.
Its existence makes a broad 'link-margin-aware probing' claim untenable. Only
abstract and metadata were accessible here, so its detailed assumptions and
possible overlap with the proposed exact bound remain a material novelty-review
gap. The manuscript must not treat incomplete access as proof of distinction.

## Measurement and physical validation precedents

[Mai and Kim (2023)](https://doi.org/10.1016/j.optcom.2022.128963)
demonstrate an integrated positioning/data-detector architecture on a terrestrial
optical link. Their hardware evidence is stronger than this project's numerical
validation, but its additional observables do not fit a scalar-power/encoder-only
comparison. [Baeck et al. (2024)](https://doi.org/10.1016/j.optcom.2024.130419)
provide a two-stage nanosatellite pointing-budget analysis, underscoring the
gap between a fine-terminal model and a complete spacecraft link.

The [fine-pointing actuator review](https://doi.org/10.3390/aerospace11010005)
and [NASA's current small-spacecraft communications overview](https://www.nasa.gov/smallsat-institute/sst-soa/soa-communications/)
show that terminal hardware varies substantially. They do not calibrate the
project's inertia, 80-ms lag, 0.08-urad encoder noise, receiver threshold or
gain-drift slopes. Published electrical terminal consumption must not be
confused with the simulation's optical transmit power or angular excitation
metric. Those numerical values remain explicit model assumptions.

## Baseline decisions and reproducibility limits

The new evaluation preserves the V3 comparator classes and adds a noise-aware
fixed-fit ablation, a standard transformed-parameter Kalman filter, and a generic
washout/demodulation ES adaptation. Their equations and development selection
are supplied. They use the same physical terminal and causal measurements.
ES is allowed longer excitation and is reported as a tracker, not credited with
a fault diagnosis. The KF/ES implementations are independently written
architecture adaptations, not reproductions of Guelman's cooperative terminal,
Cai's vision system, or a published flight tracker.

A faithful implementation of the three general constrained-AFD publications
was not completed: their full implementation details/code were not retrieved,
and translating their model-class discrimination objectives to this continuous
optical parameter problem requires a separate verified implementation. The
accessible safe-ES theorem also requires a validated system adaptation before
it can serve as a guarantee-bearing baseline. These are explicitly missing
comparisons. The supplied code should not be represented as having beaten the
state of the art because it beats its own ablations.

## Selected gap

The defensible focused question is: can the exact ratio of current and future
Gaussian received power yield a computable bound in **delivered angular
increment**, with a sharp ball-uncertainty loss, finite-horizon measurement
envelopes and an acquisition switch valid at an adaptively chosen trigger?
The proposed work derives and tests this specific certificate and its cost in
diagnostic coverage. Its contribution is narrower than generic safe AFD and
does not depend on a new acronym. Evidence of absolute priority remains
incomplete, especially for the latest acquisition literature and patents.
