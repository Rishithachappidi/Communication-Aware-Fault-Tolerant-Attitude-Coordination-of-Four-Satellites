# V5: response to the submission-critical review

V5 is a separate revision. V4 source, data and manuscript are preserved: 225 hashes remain unchanged. The earlier V3/original preservation record also remains available. Read **review/REVIEW_RESPONSE.md** for all ten requested issues and **review/RESULTS.md** for the executed comparison.

The central negative result is explicit: **UAD and the simpler 2-urad fixed-margin selector have exactly identical power, angle and probe trajectories in all 2,800 paired comparison/grid cases.** The experiments show no practical recovery advantage for the more elaborate enclosure on this test set. Its distinction is a conditional finite-model justification. Absolute novelty and Transactions readiness remain unestablished.

## Executed work

- Separate Python boundary optimization: 1,200 angular cases, 9,600 direct optical-ratio/unit checks.
- Measurement-event stress test: 10,000 missions, 700 samples, five channels, exact union-tail calibration; adversarial time selection explicitly differs from the plant trigger.
- Separate Python actuator construction: all six finite maps, eight candidate tubes and 33,024 stage checks agree with MATLAB to floating-point tolerance.
- Separate Python raw audit: all 29,250 V4 traces; every primary table entry; optical model, actual trigger, power bound, premises and adverse cases reconstructed without MATLAB function calls.
- New evaluation: 7,200 time-budget comparisons, 3,000 finite/interior actuator-grid trials, 1,800 paired native ES runs = **12,000 trials**, all directly audited using logged offset/noise histories.
- Five new MATLAB regression requirements passed, including trajectory equivalence with inherited UAD, time-limited ES, common noise and complete truth logging.

These are independent implementations/calculations by the same assistant, not independent external reviewers, hardware measurements or a flight validation campaign.

## Paper

`paper.pdf` and editable `paper.tex`; additional content is in `review_revision.tex` and `closest_work.tex`. The manuscript deliberately retains the original experiment and contrasts it with the new experiment rather than replacing outcomes. It imports the preserved V4 macros, table and figures, and uses its own references. Compile from this folder with `tectonic --keep-logs paper.tex`.

## Reproduce

MATLAB R2026a Update 3 was used on Apple M5, MACA64. MATLAB is required for the new plant simulations; Simulink is not required for V5. Python checks require NumPy, SciPy, h5py and Matplotlib. Exact executed versions are in `requirements.txt`. Install them into a virtual environment, then from the project root:

```text
python research/v5/independent_checks.py algebra
python research/v5/independent_checks.py probability
python research/v5/independent_checks.py v4
python research/v5/non_gaussian_stress.py
python research/v5/actuator_checks.py
python research/v5/analyze_v5.py
python research/v5/plot_v5.py
python research/v5/final_integrity.py --package
```

The raw checks need the raw archives extracted at their recorded paths. `final_integrity.py --package` checks available protected files and explicitly lists unavailable historical files; it does not turn missing traces into a fresh raw-data audit. The strict original-workspace check verifies all 141 original and 225 V4 protected files. `actuator_checks.py` also reads the shipped `results/verification/actuator_reference.mat`, or recreate it in MATLAB with `export_actuator_reference`.

For fresh simulation outputs, use a fresh copy of the project and remove **only that copy's** `research/v5/results/final` and `research/v5/results/native` before running. The launchers refuse to overwrite existing result folders:

```matlab
start_research_v5
test_v5
run_v5
run_v5_native
```

The native extension was declared after the main experiment and before its own outcomes; no settings were selected from those results. It uses the same seeds for paired time/native interpretation. The original frozen `protocol.json` is retained. Its descriptor did not explicitly exempt DAP's historical library: DAP still has 0.35/0.50-s choices, but every selected DAP probe here lasts 2.8 s. UAD, fixed margin and matched ES use the enforced 2.88-s limit. `protocol_clarification.json` documents this without changing outcomes. Energy is measured, never claimed matched.

## Records and guarantee scope

`results/final` contains 7,200 comparison and 3,000 grid records and traces. `results/native` contains 1,800 native ES records and traces. Each MAT chunk stores every scientific trace and the passive counterfactual. V5 additionally stores `offset_truth` and `standardized_noise`; V4 did not log those full histories. Its offset reconstruction therefore uses a separately implemented documented injection formula, and its missing rate-channel noise relies on the logged maximum scalar. Those limitations remain explicit.

The fixed-margin baseline shares the measured gate, approximate information filter and precomputed constraint validity, but substitutes a fixed motion margin. It is simpler at the radius calculation, not free of all offline modelling. Its logged `certified_probe` means a bound was calculated, and `certificate_premises` is an inherited model-hypothesis flag. **Neither confers the UAD theorem on an unproved fixed margin.** For UAD, continuous interior actuator values remain outside the finite-model theorem even when no empirical tube failure occurs.

`summary.csv` separates selection/model flags, bound/tube violations, acceptance, abstention, fit rejection, missed diagnosis, false correction, accepted error >1um and confidence misses. Those last two measure different failures and are not invented fault-class labels. `paired.csv` resamples whole seeds; its family-36 adjustment is per comparator's condition/scenario family. Grid summaries pool prespecified parameter points descriptively; no homogeneous reliability population is inferred.

## Remaining gaps

External mathematical review, physical validation, continuous-interval reachability, faithful close published-system reproductions, absolute novelty, rights confirmation and human submission approvals remain open. Public author code for Massa--Paulson was found in this review, correcting the earlier access assessment; required CORA/YALMIP/Gurobi functions were absent in this MATLAB environment. Neither code access nor these local checks constitute a reproduction of that paper's complete system.
