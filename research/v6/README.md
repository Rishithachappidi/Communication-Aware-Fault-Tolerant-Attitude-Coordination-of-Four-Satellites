# V6: conditional admission, complete evidence and a supervisory interface

V6 addresses the twelve-issue review without overwriting V4 or V5. Start with **review/REVIEW_RESPONSE.md**. The focused editable manuscript is **paper.tex**, compiled to **paper.pdf**. It does not claim readiness for IEEE Transactions on Industrial Informatics.

## What changed materially

1. A deterministic 6,748-point development map identifies where UAD and the fixed 2-urad guard differ. A separately frozen, development-guided confirmation tests both directions and surrounding controls: **7,200 new runs** (100 paired seeds, six fixed actual actuator pairs, six settings, two selectors).
2. In region 1's middle case, UAD selects600/600 probes and accepts594/600 parameter fits; the fixed guard selectsnone. Both have zero sampled outage. This uses quarter nominal sensor standard deviations and a **nondeclining-gain bound L=0**. It is restricted diagnostic access on a usable link, not a new recovery-superiority result.
3. In the reverse middle case the guard selects/accepts41/600 and UAD refuses all, with zero sampled outage. These are not demonstrated unsafe guard admissions. All old2,800 identical V5 pairs remain.
4. Complete state/reference/offset/noise histories allow separate NumPy replay of **5,040,000 actuator steps**, including torque/rate clamps and anti-windup. Max state-step difference3.39e-21 in recorded coordinates.
5. Evidence categories distinguish within-premise, out-of-model and unverified. V4's1,564 reconstructed-compatible probes become **unverified** under the strict complete-record policy; old labels are preserved.
6. An exact symbolic audit checks the nonnegative slack identity, centered attainment/zero cases and units. A Python supervisory interface refuses missing/expired evidence, nonmember actuator models, invalid units/budgets and simulation evidence used for physical deployment. Seventeen tests pass. The interface is shadow-exercised with declared simulation evidence; it cannot verify a calibration document or future fault constancy itself.
7. **Statistics correction:** V5's family-adjusted upper percentile was wrong. `results/v5_paired_corrected.csv` changes63 of144 adjusted upper limits. Per-run outcomes, means, ordinary95% intervals and adjusted lower limits are unchanged. Use this corrected export instead of V5's `family36_high`. V4's family-nine implementation was correct.

## Evidence categories (UAD calculated-bound probes only)

|Dataset|Within-premise / failures|Out-of-model / failures|Unverified / failures|
|---|---:|---:|---:|
|V4|0 /0|557 /100|1564 /0|
|V5|402 /0|968 /350|0 /0|
|V6|1421 /0|0 /0|0 /0|

Known failed premises take precedence over missing data. An otherwise compatible historical record with incomplete histories is unverified. A within-premise label is conditional on the **declared simulator model and noise generator**; it does not prove a distribution or hardware calibration from a finite trace. No heterogeneous pooled count is a field reliability population. Refused/no-probe cases and noncertified fixed-guard bounds are reported separately.

## Four properties

- Probe service: conditional sampled probe-window budget only.
- Estimation: approximate GLS; error/coverage reported separately.
- Diagnosis: acceptance/rejection is not a guaranteed correct fault label.
- Recovery: subsequent observed availability is not implied by any of the above.

The strict actuator set remains six discrete pairs. No continuous uncertainty proof was added. The new supervisor does not authorize arbitrary pointing corrections or claim industrial/hardware deployment.

## Files

- `review/REVIEW_RESPONSE.md`: all twelve issues, actions and remaining gaps.
- `review/PROOF_AUDIT.md`: full line-by-line argument and probability/units/boundary scope.
- `review/OPERATIONAL_ROLE.md`: trust boundary, inputs, refusal/monitor policy and journal positioning.
- `results/development`: declared map protocol, all6,748 outcomes, every transition.
- `results/confirmation`: frozen confirmation protocol/source hashes,7,200 per-run records, raw MAT chunks, complete replay audit, summaries and paired intervals.
- `results/evidence_*.csv/json`: per-probe and per-condition categories with explicit policy.
- `results/statistical_correction.json`, `v5_paired_corrected.csv`: transparent V5 interval repair.
- `supervisor.py`, `tests`: executable policy and meaningful refusal/statistical regressions.

## Reproduce

MATLAB R2026a Update3 on Apple M5/MACA64 generated the new plant data. Python requirements are pinned in `requirements.txt`. Tectonic uses installed Times New Roman; Poppler renders the PDF. Core V6 needs base MATLAB; no CORA/optimization toolbox is used. Simulink is not needed for the new single-terminal study.

From the project root:

```text
python -m unittest discover -s research/v6/tests -p 'test_*.py'
python research/v6/symbolic_proof_audit.py
python research/v6/correct_v5_intervals.py
python research/v6/analyze_confirmation.py
python research/v6/classify_evidence.py
python research/v6/build_outputs.py
python research/v6/final_integrity.py
tectonic --keep-logs research/v6/paper.tex
```

The complete V4/V5 source/report archive and their relevant data/checker outputs are dependencies for the historical evidence and preservation checks. Extract code/report archives at the same root. New confirmation chunks contain both selectors and passive counterfactuals, every eight-state history, held reference, standardized disturbance, offset/gain, measured/actual optical records, plan, fit and outcomes. `state_history` is pre-step; `reference_history` is the causal held input used for that step, and `terminal_state` closes the last replay interval. Delivered torque is in state columns5--6 (MATLAB indexing); commanded torque is separate.

To rerun plant simulations, use a **new project copy** without the generated `research/v6/results/development` and `results/confirmation` directories. The launchers refuse to overwrite supplied data:

```matlab
start_research_v6
search_frontiers
run_confirmation
```

Confirmation selection is development-guided and explicitly amended from the initial suggestion to confirm every transition. No confirmation simulation outcome existed when the representative-band rule was frozen. Both disagreement directions and all controls are retained, including conditions where the actual trigger suppresses admission. Results do not establish global superiority.

`final_integrity.py --package` permits explicitly listed absent historical/private intermediates and checks every available protected hash. It does not count missing data as a fresh replay. The strict original-workspace audit separately verifies all protected originals. Earlier V5 reports keep their historical statistical bug for provenance; the new correction is the authoritative family-adjusted export.
