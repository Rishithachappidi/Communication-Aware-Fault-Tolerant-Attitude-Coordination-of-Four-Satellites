# V7 — research-structure redesign with matched baseline extension

Start with [review checkpoints](review/REVIEW_RESPONSE.md), the editable [main manuscript](paper.tex) and [supplement](supplement.tex). The compiled PDFs are `paper.pdf` and `supplement.pdf`.

This is a 12-page regular-paper candidate with four-page supplement, not a submission-ready or novelty-approved claim. It preserves V4/V5/V6 and adds substantive method development and7200new matched baseline runs.

## Deliverables and results

- Separate angle/rate noise scales resolved against source: σq radians, σv radians/s, numeric source policy γv=2s⁻¹.2100direct-kernel sensor samples agree exactly. No inherited sensor output changed; hardware calibration remains absent.
- Explicit δ=.01, N=700,5channels, κ=4.680831082738rounded.
- Main ten-section story: motivation/related work; model/assumptions; central theorem; finite-model enclosure/algorithm; protocol; results; discussion; limitations; conclusion. Five source-supported figures and six tables. Historical corrections are in supplement.
- 7200original certificate/guard confirmation +7200later, separately frozen KF/ES extension =14400matched records,600per setting/method. The four methods were not jointly predeclared.
- R1midpoint: UAD594accepted/600 (26accepted-radius misses), guard0, KF600(15misses). Mean angular excitation UAD8.331 versusKF74.747μrad²s. ES provides tracking, no diagnostic fits.
- R2midpoint: guard41accepted whileUAD0; KF528completed acceptances plus30incomplete; ES also30incomplete. All methods have zero sampled outage in these selected settings.
- Separate calculation replays5,040,000new actuator steps (max absolute state error1.3553e-20); combined with preserved original audit10,080,000steps. Shadow interface replays original UAD authorizations, not physical operation.
- Twenty-two tests cover refusal, remaining mission time, rate units, monitor bounds and statistical tails.

## Reproduction

Use MATLAB R2026a and the pinned Python environment in `../v6/requirements.txt`. From project root, `start_research_v7` sets paths. `audit_measurement_units` performs direct sensor checks. `run_matched_baselines` refuses an existing result directory to prevent overwriting evidence: use a fresh extracted copy when regenerating plant data.

Analysis commands from project root:

```
python research/v7/analyze_baselines.py
python research/v7/audit_shadow.py
python research/v7/symbolic_proof_audit.py
python research/v7/build_outputs.py
PYTHONPATH=research/v7:research/v6 python -m unittest discover -s research/v7/tests -v
tectonic -X compile research/v7/paper.tex --outdir research/v7 --keep-logs
tectonic -X compile research/v7/supplement.tex --outdir research/v7 --keep-logs
python research/v7/final_integrity.py
```

`analyze_baselines.py` uses independent optical/trigger/metric checks and NumPy actuator replay, and combines independently checked original rows with the new extension. `check_trace_v7.py` preserves the older check except for finite-horizon completion: an unfinished probe has no completed fit to reject. This changes a checker assumption, not raw outcomes. `supervisor.py` additionally refuses a request exceeding remaining mission time; that new wrapper was not retroactively controlling the recorded plant experiments.

Extract V7 raw data at the project root. The original confirmation MAT files remain in the separate V6 raw archive, also extracted at the same root. V4/V5 raw archives are needed only for full historical reruns. The V7 code/report archive contains the complete inherited source/report lineage and new documents, audits and summaries; large trace chunks are separate.

## Scope

The physical values are assumptions. No hardware calibration/HIL, continuous actuator enclosure, exact accepted-fit confidence, robust post-correction guarantee, external expert review or certified novelty is claimed. KF/ES are adapted conventional architectures; faithful full published AFD/safety-filtered ES and closest optical comparisons remain incomplete. `review/BASELINE_MAPPING.md` documents why. `review/RIGHTS_AND_DISCLOSURE.md` records source identity, null license metadata and IEEE AI disclosure; human rights/authorship approvals remain open.
