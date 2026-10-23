import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path


CASES = ("heat", "advection", "wave")
MUTANTS = ("baseline", "sign", "coefficient", "frozen", "boundary_zero", "equivalent_periodic_shift", "tiny_coefficient")
STATES = {"BASELINE_PASS", "KILLED", "SURVIVED", "EQUIVALENT", "INFRA_FAIL", "INCONCLUSIVE"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(root, source, contract):
    expected = {f"{case}_{mutant}" for case in CASES for mutant in MUTANTS}
    hosts, reports, inputs = {}, {}, {}
    verified_artifacts = 0
    for host in ("war", "guerra"):
        directory = root / host
        actual = {path.parent.name for path in directory.glob("*/run.json")}
        if actual != expected:
            raise ValueError(f"matriz incompleta o inesperada en {host}: {actual ^ expected}")
        counts, rows, environments = collections.Counter(), [], {}
        reports[host] = {}
        for name in sorted(expected):
            folder = directory / name
            report_path = folder / "run.json"
            report = json.loads(report_path.read_text(encoding="utf-8"))
            if f"{report['case']}_{report['mutant']}" != name or report["status"] not in STATES:
                raise ValueError(f"identidad o estado inválido: {host}/{name}")
            if report["source_sha256"] != sha(source) or report["contract_sha256"] != sha(contract):
                raise ValueError(f"fuente o contrato no coincide: {host}/{name}")
            for filename, expected_hash in report["artifact_sha256"].items():
                if Path(filename).name != filename or sha(folder / filename) != expected_hash:
                    raise ValueError(f"hash de artefacto no coincide: {host}/{name}/{filename}")
                verified_artifacts += 1
            payload = json.loads((folder / "worker_result.json").read_text(encoding="utf-8"))
            if payload != report["result"]:
                raise ValueError(f"resultado crudo diferente: {host}/{name}")
            if report["mutant"] != "baseline" and report["status"] in {"KILLED", "SURVIVED", "EQUIVALENT"}:
                baseline_path = directory / f"{report['case']}_baseline" / "run.json"
                baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
                if not all([
                    report["baseline_valid"], baseline["status"] == "BASELINE_PASS",
                    report["baseline_file_sha256"] == sha(baseline_path),
                    payload["environment"] == baseline["result"]["environment"],
                    report["machine"] == baseline["machine"],
                ]):
                    raise ValueError(f"referencia inconsistente: {host}/{name}")
            failed = {key: item for key, item in payload.get("checks", {}).items() if not item["passed"]}
            counts[report["status"]] += 1
            rows.append({
                "case": report["case"], "mutant": report["mutant"], "status": report["status"],
                "reason": report["reason"], "failed_contracts": failed,
                "wall_seconds": report["wall_seconds"], "returncode": report["returncode"],
                "evidence": f"{host}/{name}/run.json",
            })
            environments[report["case"]] = payload.get("environment")
            reports[host][name] = report
            inputs[f"{host}/{name}/run.json"] = sha(report_path)
        evaluable = counts["KILLED"] + counts["SURVIVED"]
        hosts[host] = {
            "runs": len(rows), "status_counts": dict(counts), "rows": rows,
            "detection": {"killed": counts["KILLED"], "non_equivalent_evaluable": evaluable, "fraction": counts["KILLED"] / evaluable if evaluable else None},
            "environments": environments,
        }
    comparisons = {}
    for name in sorted(expected):
        war, guerra = reports["war"][name], reports["guerra"][name]
        war_checks, guerra_checks = war["result"].get("checks", {}), guerra["result"].get("checks", {})
        deltas = {
            key: abs(war_checks[key]["actual"] - guerra_checks[key]["actual"])
            for key in war_checks.keys() & guerra_checks.keys()
            if isinstance(war_checks[key]["actual"], (int, float)) and isinstance(guerra_checks[key]["actual"], (int, float))
        }
        comparisons[name] = {
            "same_status": war["status"] == guerra["status"], "war_status": war["status"], "guerra_status": guerra["status"],
            "check_actual_absolute_differences": deltas,
            "maximum_absolute_difference_of_recorded_checks": max(deltas.values(), default=None),
        }
    return {
        "schema_version": 1, "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "aggregator_source_sha256": sha(Path(__file__).resolve()),
        "runner_source_sha256": sha(source), "contract_sha256": sha(contract),
        "total_runs": sum(host["runs"] for host in hosts.values()),
        "verified_artifact_hashes": verified_artifacts, "hosts": hosts,
        "cross_host": comparisons, "all_classifications_match": all(item["same_status"] for item in comparisons.values()),
        "input_run_sha256": inputs,
        "limitations": [
            "Reproducibilidad del mismo código, no independencia algorítmica",
            "No certifica Euler 3D, Navier-Stokes ni una teoría general",
            "La comparación entre hosts reporta diferencias; no usa una tolerancia retrospectiva para proclamar exactitud",
            "EQUIVALENT se justifica por roll de N posiciones; SURVIVED no implica equivalencia",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("la salida ya existe; conservar evidencia anterior")
    repository = Path(__file__).resolve().parent.parent
    skill = repository / "skills" / "escenarios-verificables"
    report = summarize(args.root, skill / "scripts" / "run_scenario.py", skill / "references" / "contratos-1d.md")
    assert report["total_runs"] == 2 * len(CASES) * len(MUTANTS)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"total_runs": report["total_runs"], "verified_artifact_hashes": report["verified_artifact_hashes"], "all_classifications_match": report["all_classifications_match"], "counts": {key: value["status_counts"] for key, value in report["hosts"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
