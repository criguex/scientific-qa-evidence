import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import oracles
import sut
from suite import CASES, MUTANTS, OBSERVATION_FRACTIONS, REFINEMENTS, TOLERANCE

REFINED_MODELS = {"rc", "cooling", "chemical_second_order", "beer_lambert", "logistic"}


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z")


def finite(values):
    return all(math.isfinite(v) for v in values)


def invariants(case, values):
    model, p = case["model"], case["params"]
    if not finite(values):
        return False, "non_finite"
    if model == "rc":
        lo, hi = sorted((p["v0"], p["vin"]))
        ok = all(lo - 1e-12 <= x <= hi + 1e-12 for x in values) and all(a <= b + 1e-12 for a, b in zip(values, values[1:]))
    elif model == "cooling":
        lo, hi = sorted((p["t0"], p["ambient"]))
        ok = all(lo - 1e-12 <= x <= hi + 1e-12 for x in values) and all(abs(b-p["ambient"]) <= abs(a-p["ambient"])+1e-12 for a, b in zip(values, values[1:]))
    elif model in {"chemical_second_order", "beer_lambert"}:
        ok = all(x >= 0 for x in values) and all(a >= b - 1e-12 for a, b in zip(values, values[1:]))
    elif model == "snell":
        ok = all(0 <= x < math.pi / 2 for x in values) and all(a <= b + 1e-12 for a, b in zip(values, values[1:]))
    elif model == "thin_lens":
        ok = all(x < 0 for x in values) and all(a >= b - 1e-12 for a, b in zip(values, values[1:]))
    elif model == "acoustic_interface":
        pr, pt = values[-2:]
        energy = (pr / p["pi"]) ** 2 + (p["z1"] / p["z2"]) * (pt / p["pi"]) ** 2
        ok = abs(energy - 1) <= 1e-10
    elif model == "fechner":
        ok = all(x >= -1e-12 for x in values) and all(a <= b + 1e-12 for a, b in zip(values, values[1:]))
    elif model == "logistic":
        ok = all(0 < x <= p["capacity"] + 1e-12 for x in values) and all(a <= b + 1e-12 for a, b in zip(values, values[1:]))
    else:
        return False, "unknown_model"
    return ok, "ok" if ok else "invariant_violation"


def classify_variant(is_baseline, baseline_status, valid, error):
    if is_baseline:
        return "PASS" if valid and math.isfinite(error) and error <= TOLERANCE else "BASELINE_INVALID"
    if baseline_status != "PASS":
        return "BLOCKED_BASELINE"
    return "SURVIVED" if valid and math.isfinite(error) and error <= TOLERANCE else "KILLED"


def run_variant(case, variant, baseline_status=None):
    started = time.monotonic()
    started_utc = utc_now()
    resolutions = REFINEMENTS if case["model"] in REFINED_MODELS else (None,)
    refinements = {}
    error_by_refinement = {}
    reasons = {}
    oracle_invalid = False
    try:
        for n in resolutions:
            key = str(n) if n is not None else "N/A"
            got = sut.evaluate(case, variant, n or 1)
            expected = oracles.evaluate(case, n or 1)
            valid, reason = invariants(case, got)
            if len(got) != len(expected) or not finite(expected):
                oracle_invalid = True
                reasons[key] = "oracle_invalid_or_shape_mismatch"
                refinements[key] = got
                error_by_refinement[key] = math.inf
                continue
            error = max(abs(a-b) for a, b in zip(got, expected)) / case["scale"]
            if not math.isfinite(error):
                error = math.inf
            refinements[key] = got
            error_by_refinement[key] = error
            reasons[key] = reason
        fine_key = str(resolutions[-1]) if resolutions[-1] is not None else "N/A"
        fine_reason = reasons[fine_key]
        fine_error = error_by_refinement[fine_key]
        return_code = 0
        status = "INCONCLUSIVE" if oracle_invalid else classify_variant(variant == "baseline", "PASS" if variant == "baseline" else baseline_status, fine_reason == "ok", fine_error)
    except Exception as exc:
        return_code = 1
        status = "INCONCLUSIVE"
        reasons["exception"] = type(exc).__name__
    duration = time.monotonic() - started
    finished_utc = utc_now()
    if variant != "baseline":
        if baseline_status != "PASS":
            status = "BLOCKED_BASELINE"
        elif return_code != 0:
            status = "INCONCLUSIVE"
    non_finite = any(not math.isfinite(v) for vals in refinements.values() for v in vals) or any(not math.isfinite(v) for v in error_by_refinement.values())
    safe_values = {n: [v if math.isfinite(v) else None for v in vals] for n, vals in refinements.items()}
    safe_errors = {n: v if math.isfinite(v) else None for n, v in error_by_refinement.items()}
    return {"case_id": case["case_id"], "model": case["model"], "variant": variant, "params": case["params"], "units": case["units"], "scale": case["scale"], "horizon": case["horizon"], "seed": None, "refinement_applicable": case["model"] in REFINED_MODELS, "refinements": list(resolutions), "resolution": "64,128,256" if case["model"] in REFINED_MODELS else "N/A", "observations": list(OBSERVATION_FRACTIONS), "values": safe_values, "normalized_error": safe_errors, "non_finite_observed": non_finite, "oracle_valid": not oracle_invalid, "invariants": reasons, "status": status, "return_code": return_code, "started_utc": started_utc, "finished_utc": finished_utc, "duration_seconds": duration}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="nueva carpeta de evidencia; debe no existir")
    args = parser.parse_args(argv)
    out = Path(args.out).expanduser()
    if out.exists():
        parser.error("el directorio de salida ya existe; no se sobrescribe evidencia")
    out.mkdir(parents=True)
    cases = list(CASES)
    variants = []
    for case in cases:
        variants.append((case, "baseline"))
        variants.extend((case, m) for m in MUTANTS[case["model"]])
    results = []
    baselines = {}
    for case in cases:
        baseline = run_variant(case, "baseline")
        baselines[case["case_id"]] = baseline["status"]
        results.append(baseline)
        selected = [variant for candidate, variant in variants if candidate["case_id"] == case["case_id"] and variant != "baseline"]
        if case["model"] == "rc":
            selected.append("tau_tiny")
        for variant in selected:
            run_case = dict(case, case_id=case["case_id"] + "_tiny") if variant == "tau_tiny" else case
            result = run_variant(run_case, variant, baseline_status=baselines[case["case_id"]])
            results.append(result)
    files = [Path(__file__), Path(__file__).with_name("sut.py"), Path(__file__).with_name("oracles.py"), Path(__file__).with_name("suite.py"), Path(__file__).with_name("CONTRACT.md")]
    source_hashes = {p.name: sha256(p) for p in files}
    with (out / "observations.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["case_id", "model", "variant", "resolution", "fraction", "component", "value", "oracle", "point_normalized_error", "max_normalized_error", "invariant"])
        writer.writeheader()
        for r in results:
            for n in r["refinements"]:
                key = str(n) if n is not None else "N/A"
                values = r["values"].get(key, [])
                reference = oracles.evaluate(next(c for c in cases if c["case_id"] == r["case_id"].removesuffix("_tiny")), n or 1) if len(values) else []
                for i, value in enumerate(values):
                    observation_index = i // 2 if r["model"] == "acoustic_interface" else i
                    fraction = OBSERVATION_FRACTIONS[observation_index] if observation_index < len(OBSERVATION_FRACTIONS) else "N/A"
                    component = ("reflected_pressure" if i % 2 == 0 else "transmitted_pressure") if r["model"] == "acoustic_interface" else "scalar"
                    oracle_value = reference[i] if i < len(reference) else ""
                    oracle_finite = isinstance(oracle_value, (int, float)) and math.isfinite(oracle_value)
                    value_finite = isinstance(value, (int, float)) and math.isfinite(value)
                    point_error = abs(value - oracle_value) / r["scale"] if oracle_finite and value_finite else None
                    oracle_export = oracle_value if oracle_finite else None
                    writer.writerow({"case_id": r["case_id"], "model": r["model"], "variant": r["variant"], "resolution": key, "fraction": fraction, "component": component, "value": value, "oracle": oracle_export, "point_normalized_error": point_error, "max_normalized_error": r["normalized_error"].get(key, ""), "invariant": r["invariants"].get(key, "")})
    for index, result in enumerate(results, 1):
        (out / f"case_{index:03d}.json").write_text(json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    summary = {"collection_complete": len(results) == 84, "expected_variants": 84, "variant_evaluations": len(results), "process_invocations": 1, "all_expected_responses": None, "counts": counts, "tolerance": TOLERANCE, "refinements": list(REFINEMENTS), "started_utc": min(r["started_utc"] for r in results), "finished_utc": max(r["finished_utc"] for r in results), "duration_seconds": sum(r["duration_seconds"] for r in results), "source_sha256": source_hashes, "runtime": {"python": platform.python_version(), "os": sys.platform, "architecture": platform.machine()}, "seed": None, "command": "python3 runner.py --out <NEW_OUTPUT_DIR>"}
    artifact_hashes = {p.name: sha256(p) for p in sorted(out.iterdir()) if p.is_file() and p.name != "summary.json"}
    summary["artifact_sha256"] = artifact_hashes
    (out / "summary.json").write_text(json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (out / "summary.json.sha256").write_text(f"{sha256(out / 'summary.json')}  summary.json\n", encoding="ascii")
    print(json.dumps({"collection_complete": summary["collection_complete"], "actual_variants": len(results), "counts": counts}, sort_keys=True))
    return 0 if summary["collection_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
