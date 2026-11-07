"""Rebuild all tabulated V4 statistics from immutable per-run CSV records."""
import csv
import hashlib
import json
import math
import random
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
TAG = next((x for x in sys.argv[1:] if not x.startswith("--")), "final")
OUT = HERE / "results" / TAG


def load(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def nums(rows, key):
    return [float(r[key]) for r in rows if math.isfinite(float(r[key]))]


def mean(x):
    return st.mean(x) if x else math.nan


def quantile(x, p):
    if not x:
        return math.nan
    y = sorted(x)
    at = p * (len(y) - 1)
    i = int(at)
    return y[i] + (y[min(i + 1, len(y) - 1)] - y[i]) * (at - i)


def save(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)


def summarize(rows):
    out = []
    groups = defaultdict(list)
    for r in rows:
        groups[(r["condition"], r["condition_value"], r["scenario"], r["method"])].append(r)
    for (condition, value, scenario, method), x in groups.items():
        r = dict(condition=condition, condition_value=float(value), scenario=scenario, method=method, n=len(x))
        for key in ("attempted", "accepted", "abstained", "fit_rejected", "false_correction", "missed_diagnosis", "missed_pointing_diagnosis", "false_acquisition", "budget_violation", "bound_violation", "tube_violation", "certified_probe", "certificate_premises"):
            r[key] = sum(int(a[key]) for a in x)
        for key in ("outage_s", "probe_s", "energy_urad2s", "tail_availability", "probe_induced_outage_s", "avoided_outage_s", "plan_runtime_s", "fit_runtime_s", "trace_buffer_bytes"):
            r["mean_" + key] = mean(nums(x, key))
        r["median_outage_s"] = quantile(nums(x, "outage_s"), .5)
        r["p95_outage_s"] = quantile(nums(x, "outage_s"), .95)
        r["outage_sd_s"] = st.stdev(nums(x, "outage_s")) if len(x) > 1 else math.nan
        for key in ("error_um", "accepted_error_um", "attempt_error_um", "diagnosis_s", "radius_um"):
            r["median_" + key] = quantile(nums(x, key), .5)
            r["finite_" + key] = len(nums(x, key))
        r["coverage_all_fits"] = mean(nums(x, "coverage_all_fits"))
        r["coverage_accepted"] = mean(nums([a for a in x if int(a["accepted"])], "coverage_all_fits"))
        r["valid_certificate_violations"] = sum(int(a["bound_violation"]) for a in x if int(a["certificate_premises"]))
        r["valid_tube_violations"] = sum(int(a["tube_violation"]) for a in x if int(a["certificate_premises"]))
        out.append(r)
    return out


def paired(primary):
    rng = random.Random(20261023)
    scenarios = list(dict.fromkeys(r["scenario"] for r in primary))
    rows = []
    for scenario in scenarios:
        aa = {r["seed"]: float(r["outage_s"]) for r in primary if r["scenario"] == scenario and r["method"] == "UAD"}
        bb = {r["seed"]: float(r["outage_s"]) for r in primary if r["scenario"] == scenario and r["method"] == "DAP"}
        assert set(aa) == set(bb)
        d = [aa[s] - bb[s] for s in sorted(aa)]
        boot = [sum(rng.choices(d, k=len(d))) / len(d) for _ in range(5000)]
        rows.append(dict(scenario=scenario, n=len(d), estimand="UAD minus DAP outage seconds", mean_difference=mean(d), ci95_low=quantile(boot, .025), ci95_high=quantile(boot, .975), family9_low=quantile(boot, .05 / 18), family9_high=quantile(boot, 1 - .05 / 18)))
    return rows


def audit(primary, sensitivity):
    assert len(primary) == 10800 and len(sensitivity) == 18450
    for data, expected in ((primary, 10800), (sensitivity, 18450)):
        keys = {(r["condition"], r["condition_value"], r["scenario"], r["method"], r["seed"]) for r in data}
        assert len(keys) == expected
        for r in data:
            assert 0 <= float(r["outage_s"]) <= 12.00001
            assert not (int(r["accepted"]) and int(r["abstained"]))
            if r["method"] == "UAD" and int(r["certificate_premises"]):
                assert not int(r["bound_violation"]) and not int(r["tube_violation"]) and not int(r["budget_violation"])
    root = HERE.parent.parent
    original = json.loads((root / "research/audit/ORIGINAL_STATE.json").read_text())["sha256"]
    missing = [p for p in original if not (root / p).is_file()]
    assert not missing or "--package" in sys.argv, missing
    changed = [p for p, h in original.items() if (root / p).is_file() and hashlib.sha256((root / p).read_bytes()).hexdigest() != h]
    assert not changed, changed
    frozen = json.loads((OUT / "source_sha256.json").read_text())
    repair_path = OUT / "evaluator_source_repair.json"
    repairs = json.loads(repair_path.read_text())["current_sha256"] if repair_path.exists() else {}
    for key, digest in frozen.items():
        name = key[:-2] + ".m" if key.endswith("_m") else None
        current = hashlib.sha256((HERE / name).read_bytes()).hexdigest()
        if current != digest:
            original_source = HERE / "frozen_source" / name
            assert hashlib.sha256(original_source.read_bytes()).hexdigest() == digest, (key, name)
            assert name in repairs and current == repairs[name], (key, "unexpected source change")
    return dict(status="passed", primary_rows=len(primary), sensitivity_rows=len(sensitivity), original_files_preserved=len(original)-len(missing), original_files_unavailable_in_package=missing, original_changed=changed, frozen_matlab_sources_checked=len(frozen), note="Independent record/aggregate audit; raw-trace audit is a separate MATLAB execution. --package permits explicitly listed omitted historical intermediates, never a changed available source.")


def correct_premise_flags(rows):
    """Disclosed evaluator repair; raw outcomes/labels are never overwritten."""
    corrections = []
    offset_scenarios = {"pointing", "linear_drift", "quadratic_drift", "fast_fading", "deep_loss"}
    result = []
    for raw in rows:
        row = dict(raw)
        row["certificate_premises_recorded"] = row["certificate_premises"]
        starts = float(row["start_s"]);ends = float(row["finish_s"])
        spans_new_offset = row["scenario"] in offset_scenarios and starts < 2 and (math.isnan(ends) or ends > 2)
        if row["certificate_premises"] == "1" and spans_new_offset:
            row["certificate_premises"] = "0"
            corrections.append({k: row[k] for k in ("condition", "condition_value", "scenario", "seed", "method")})
        result.append(row)
    return result, corrections


def macros(summary, sensitivity, comparisons):
    index = {(r["scenario"], r["method"]): r for r in summary}
    vals = {"NPrimary": "10,800", "NSensitivity": "18,450", "NTotal": "29,250"}
    for scenario, label in (("linear_drift", "Drift"), ("pointing", "Pointing"), ("near_threshold", "Near"), ("fast_fading", "Fading")):
        for method, mlabel in (("UAD", "UAD"), ("DAP", "DAP"), ("projected_fixed", "Fixed"), ("parameter_kf", "KF"), ("lockin", "ES")):
            r = index[scenario, method]
            vals[mlabel + label + "Outage"] = f'{r["mean_outage_s"]:.4f}'
            vals[mlabel + label + "Accepted"] = str(r["accepted"])
            vals[mlabel + label + "Energy"] = f'{r["mean_energy_urad2s"]:.3f}'
            vals[mlabel + label + "Pninetyfive"] = f'{r["p95_outage_s"]:.3f}'
            vals[mlabel + label + "Abstained"] = str(r["abstained"])
            vals[mlabel + label + "Error"] = f'{r["median_accepted_error_um"]:.3f}'
    selected = [("noise", 5, "linear_drift", "NoisyDrift"), ("noise", 5, "near_threshold", "NoisyNear"), ("bias", 2, "linear_drift", "BiasDrift"), ("beam", .9, "pointing", "BeamEarly"), ("actuator", 2, "linear_drift", "MismatchDrift")]
    for condition, value, scenario, label in selected:
        for method, mlabel in (("UAD", "UAD"), ("DAP", "DAP"), ("projected_noise", "GLS"), ("parameter_kf", "KF"), ("lockin", "ES")):
            x = next(r for r in sensitivity if r["condition"] == condition and r["condition_value"] == value and r["scenario"] == scenario and r["method"] == method)
            vals[mlabel + label + "Outage"] = f'{x["mean_outage_s"]:.4f}'
            vals[mlabel + label + "Accepted"] = str(x["accepted"])
            vals[mlabel + label + "Coverage"] = f'{100*x["coverage_accepted"]:.1f}'
            vals[mlabel + label + "BoundFailures"] = str(x["bound_violation"])
    for method, lab in (("UAD", "UAD"), ("DAP", "DAP")):
        x = [r for r in sensitivity if r["condition"] == "noise" and r["condition_value"] == 5 and r["scenario"] == "near_threshold" and r["method"] == method][0]
        vals[lab + "NoiseNearOutage"] = f'{x["mean_outage_s"]:.4f}'
        vals[lab + "NoiseFalseAcq"] = str(x["false_acquisition"])
    full = [r for r in summary if r["method"] == "UAD"]
    vals["ValidCertificates"] = str(sum(r["certificate_premises"] for r in full))
    vals["ValidViolations"] = str(sum(r["valid_certificate_violations"] for r in full))
    vals["SelectedCertificates"] = str(sum(r["certified_probe"] for r in full))
    vals["SensitivityUADBoundFailures"] = str(sum(r["bound_violation"] for r in sensitivity if r["method"] == "UAD"))
    repair = json.loads((OUT / "premise_flag_corrections.json").read_text())
    vals["PremiseFlagRepairs"] = str(len(repair["primary_corrections"]) + len(repair["sensitivity_corrections"]))
    d = [r for r in comparisons if r["scenario"] == "linear_drift"][0]
    for k, v in (("DriftDifference", d["mean_difference"]), ("DriftCILow", d["ci95_low"]), ("DriftCIHigh", d["ci95_high"])):
        vals[k] = f"{v:.4f}"
    with (OUT / "numbers.tex").open("w") as f:
        for k, v in vals.items():
            f.write("\\newcommand{\\" + k + "}{" + v + "}\n")
    table = ["\\def\\PrimaryRows{"]
    for scenario in dict.fromkeys(r["scenario"] for r in summary):
        for method in ("projected_fixed", "parameter_kf", "DAP", "UAD"):
            r = index[scenario, method]
            error = "--" if math.isnan(r["median_accepted_error_um"]) else f'{r["median_accepted_error_um"]:.3f}'
            table.append(f'{scenario.replace("_", " ")} & {method.replace("_", " ")} & {r["accepted"]}/{r["n"]} & {error} & {r["mean_outage_s"]:.3f} & {r["p95_outage_s"]:.3f} & {r["mean_energy_urad2s"]:.2f} ' + "\\\\")
    table.append("}")
    (OUT / "primary_rows.tex").write_text("\n".join(table) + "\n")


def main():
    primary, first_corrections = correct_premise_flags(load(OUT / "primary.csv"))
    sensitivity, second_corrections = correct_premise_flags(load(OUT / "sensitivity.csv"))
    save(OUT / "primary_corrected.csv", primary);save(OUT / "sensitivity_corrected.csv", sensitivity)
    (OUT / "premise_flag_corrections.json").write_text(json.dumps({"reason": "The frozen evaluator omitted checking that boresight offset stays constant during the complete probe. The correction changes only this premise label; all observed outcomes and violations are retained.", "primary_corrections": first_corrections, "sensitivity_corrections": second_corrections}, indent=2) + "\n")
    evidence = audit(primary, sensitivity)
    s = summarize(primary);ss = summarize(sensitivity);c = paired(primary)
    save(OUT / "primary_summary.csv", s);save(OUT / "sensitivity_summary.csv", ss);save(OUT / "paired_comparisons.csv", c)
    macros(s, ss, c)
    (OUT / "integrity.json").write_text(json.dumps(evidence, indent=2) + "\n")
    report = ["# Executed V4 results", "", "Primary: 10,800 trials. Sensitivity: 18,450 trials. Seed is the paired statistical unit. Historical V3 reproduction is separate.", "", "## Primary outcomes", "", "|Scenario|Method|Accepted/n|Abstained|Mean outage s|P95 outage s|Accepted error urad|Angular energy urad^2 s|", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for r in s:
        report.append(f'|{r["scenario"]}|{r["method"]}|{r["accepted"]}/{r["n"]}|{r["abstained"]}|{r["mean_outage_s"]:.4f}|{r["p95_outage_s"]:.3f}|{r["median_accepted_error_um"]:.3f}|{r["mean_energy_urad2s"]:.3f}|')
    report += ["", "## Paired UAD minus DAP outage differences", "", "Intervals resample whole paired seeds (5,000 draws). Family limits use alpha/9 percentile tails; the bootstrap adjustment is approximate. Positive means UAD has more outage.", "", "|Scenario|Mean difference s|95% interval|Family-9 adjusted interval|", "|---|---:|---|---|"]
    for r in c:
        report.append(f'|{r["scenario"]}|{r["mean_difference"]:.4f}|[{r["ci95_low"]:.4f}, {r["ci95_high"]:.4f}]|[{r["family9_low"]:.4f}, {r["family9_high"]:.4f}]|')
    report += ["", "## Sensitivity evidence", "", "All 18,450 records and all group means/counts are in sensitivity.csv and sensitivity_summary.csv. No unfavorable group is omitted. These prespecified sweeps are exploratory and not a multiplicity-free set of confirmatory tests.", "", "## Certificate counts", ""]
    for r in s:
        if r["method"] == "UAD":
            n = r["certified_probe"]
            upper = (1 - .05 ** (1 / n)) if n and r["bound_violation"] == 0 else math.nan
            report.append(f'- {r["scenario"]}: selected {n}, premises verified {r["certificate_premises"]}, all observed bound violations {r["bound_violation"]}, violations with verified premises {r["valid_certificate_violations"]}; zero-event identical-Bernoulli reference upper bound {upper:.4f}.')
    report += ["", "The binomial reference is a precision illustration, not a flight risk estimate. Different fixed fault magnitudes and selection rules limit a homogeneous population interpretation. An observation of zero events in around 100 selected runs cannot empirically certify a one-percent target.", "", "## Timing and memory scope", "", "Online planner/fit wall time and retained numerical trace-buffer bytes are in both summary files. They exclude offline library generation and are not embedded worst-case timing or total process peak memory. Timing depends on host load/JIT and is not used to tune the method."]
    filename = "RESULTS_REPORT.md" if TAG == "final" else f"RESULTS_REPORT_{TAG}.md"
    (HERE.parent / "experiments" / filename).write_text("\n".join(report) + "\n")
    print(json.dumps(evidence))


if __name__ == "__main__":
    main()
