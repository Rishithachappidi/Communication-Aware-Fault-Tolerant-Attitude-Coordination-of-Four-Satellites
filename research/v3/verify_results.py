"""Independent standard-library audit of saved research metric records."""
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent


def read(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def audit():
    primary = read(HERE / "results/full/trials.csv")
    stress = read(HERE / "results/stress/trials.csv")
    assert len(primary) == 5400 and len(stress) == 3600
    assert len({(r["scenario"], r["seed"], r["method"]) for r in primary}) == 5400
    assert len({(r["condition"], r["scenario"], r["seed"], r["method"]) for r in stress}) == 3600
    groups = Counter((r["scenario"], r["method"]) for r in primary)
    assert len(groups) == 54 and set(groups.values()) == {100}
    groups_stress = Counter((r["condition"], r["scenario"], r["method"]) for r in stress)
    assert len(groups_stress) == 36 and set(groups_stress.values()) == {100}
    for rows in (primary, stress):
        for row in rows:
            assert 0 <= float(row["outage_s"]) <= 12.00001
            assert 0 <= float(row["tail_availability"]) <= 1
            assert not (int(row["accepted"]) and int(row["rejected"]))
            if row["scenario"] == "dark":
                assert not int(row["accepted"]) and float(row["probe_s"]) == 0
    summaries = read(HERE / "results/full/summary.csv")
    for row in summaries:
        raw = [r for r in primary if r["scenario"] == row["scenario"] and r["method"] == row["method"]]
        assert int(row["n"]) == len(raw)
        assert int(row["accepted"]) == sum(int(r["accepted"]) for r in raw)
        mean = sum(float(r["outage_s"]) for r in raw) / len(raw)
        assert math.isclose(mean, float(row["mean_outage_s"]), abs_tol=1e-10)
    for name in ("dap_fit.m", "dap_plan.m", "dap_sequences.m", "v3_designs.m"):
        text = (HERE / name).read_text()
        assert "v3_truth(" not in text and "fault_input(" not in text
    paths = [*HERE.glob("*.m"), HERE / "paper.tex", HERE / "PROTOCOL.md", HERE / "STRESS_PROTOCOL.md"]
    hashes = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    root = HERE.parent.parent
    source_hashes = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
                     for p in sorted((root / "matlab").rglob("*.m"))}
    source_hashes["simulink/terminal_kernel.m"] = hashlib.sha256((root / "simulink/terminal_kernel.m").read_bytes()).hexdigest()
    report = {"status": "passed", "primary_rows": len(primary), "stress_rows": len(stress),
              "primary_groups": len(groups), "stress_groups": len(groups_stress),
              "summary_mean_and_count_checks": len(summaries), "research_source_sha256": hashes,
              "upstream_source_sha256_at_delivery": source_hashes,
              "note": "Delivery hashes record current source; they are not a before/after preservation proof."}
    (HERE / "results/integrity_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: 9,000 unique trial rows, matched group sizes, ranges, aggregate counts/means, and estimator input boundaries.")


if __name__ == "__main__":
    audit()
