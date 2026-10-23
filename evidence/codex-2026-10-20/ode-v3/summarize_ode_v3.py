import argparse
import collections
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path


RUNNER_SHA = "f118929e692f90ff86cc9bda0f1e3a5288abd0191dceaae432eafaf0c00db9a8"
CONTRACT_SHA = "cee74957ddab6f5fa196d06840cfa642f5c08c15eb7b70540eb7e56c9bf5ed06"
HELPER_SHA = "cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9"
GROUPS = {
    "war_main": ("war/results", "main", "oscillator", tuple(f"osc{i:02}" for i in range(1, 10))),
    "guerra_main": ("guerra/raw/results", "main", "reaction", tuple(f"rxn{i:02}" for i in range(1, 10))),
    "war_cross": ("war/results_cross_reaction", "cross", "reaction", ("rxn07", "rxn08", "rxn09")),
    "guerra_cross": ("guerra/cross/results_cross_oscillator", "cross", "oscillator", ("osc06", "osc08", "osc09")),
    "independent_review": ("independent_review/raw", "review", None, None),
}
STATES = {"BASELINE_PASS", "KILLED", "SURVIVED", "EQUIVALENT", "INFRA_FAIL", "INCONCLUSIVE"}
FIXTURE = "osc05_altered_parameters"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def missing_npz_dirs(root):
    return [run.parent for run in root.rglob("run.json") if not (run.parent / "fields.npz").is_file()]


def load_module(path):
    spec = importlib.util.spec_from_file_location("frozen_ode", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_report(path, report, module):
    require(report["source_sha256"] == RUNNER_SHA, f"fuente distinta: {path}")
    require(report["contract_sha256"] == CONTRACT_SHA, f"contrato distinto: {path}")
    require(report["dependencies"] == {"run_scenario.py": HELPER_SHA}, f"helper distinto: {path}")
    require(report["status"] in STATES and report["returncode"] == 0, f"estado o salida inesperada: {path}")
    require(report["case"] in module.SCENARIOS, f"familia desconocida: {path}")
    require(report["mutant"] in module.MUTANTS[report["case"]], f"mutante desconocido: {path}")
    parameters = module.SCENARIOS[report["case"]][report["scenario"]]
    require(all(report["parameters"][key] == value for key, value in parameters.items()), f"parámetros alterados: {path}")
    require(report["monotonic_finish_ns"] >= report["monotonic_start_ns"], f"reloj invertido: {path}")
    required = {"fields.npz", "metrics.csv", "worker_result.json", "stdout.log", "stderr.log", "returncode.txt"}
    require(required.issubset(report["artifact_sha256"]), f"faltan artefactos: {path}")
    for filename, expected in report["artifact_sha256"].items():
        require(Path(filename).name == filename and sha(path.parent / filename) == expected, f"hash alterado: {path}/{filename}")
    require(read(path.parent / "worker_result.json") == report["result"], f"resultado crudo distinto: {path}")
    require((path.parent / "returncode.txt").read_text().strip() == "0", f"salida cruda distinta: {path}")
    result = report["result"]
    require(result["completed"] and result["all_values_finite"], f"ejecución no terminada: {path}")
    require(result["all_contracts_passed"] == all(item["passed"] for item in result["checks"].values()), f"contratos incoherentes: {path}")
    return len(report["artifact_sha256"])


def summarize(root, repository):
    skill = repository / "skills" / "escenarios-verificables"
    source, contract, helper = skill / "scripts/run_ode_scenario.py", skill / "references/contratos-ode-v3.md", skill / "scripts/run_scenario.py"
    require((sha(source), sha(contract), sha(helper)) == (RUNNER_SHA, CONTRACT_SHA, HELPER_SHA), "fuentes locales distintas de las congeladas")
    module = load_module(source)
    shared = module.load_shared()
    groups, report_manifest, all_reports, fixture_manifest = {}, {}, {}, {}
    artifact_count = 0
    for group_name, (relative, category, case, scenarios) in GROUPS.items():
        reports = {}
        for path in sorted((root / relative).rglob("run.json")):
            report = read(path)
            key = path.relative_to(root).as_posix()
            report_manifest[key] = sha(path)
            if group_name == "independent_review" and path.parent.name == FIXTURE:
                fixture_manifest[key] = {
                    "sha256": sha(path), "not_an_execution": True,
                    "alteration": "copia de osc05_baseline; omega de 0.8 a 0.81 solo en run.json",
                    "raw_artifacts_verified": 0,
                }
                for filename, expected in report["artifact_sha256"].items():
                    require(Path(filename).name == filename and sha(path.parent / filename) == expected, f"fixture alterado fuera del cambio declarado: {path}")
                    fixture_manifest[key]["raw_artifacts_verified"] += 1
                require(report["parameters"]["omega"] == 0.81, "falta alteración declarada del fixture")
                continue
            artifact_count += verify_report(path, report, module)
            reports[key] = (path, report)
            all_reports[key] = report
        if category != "review":
            expected = {(case, scenario, mutant) for scenario in scenarios for mutant in module.MUTANTS[case]}
            actual = [(r["case"], r["scenario"], r["mutant"]) for _, r in reports.values()]
            require(len(actual) == len(expected) and set(actual) == expected, f"matriz incompleta o duplicada: {group_name}")
        else:
            require(len(reports) == 30, "la revisión local debe tener 30 ejecuciones, sin contar el fixture")
        hash_index = {sha(path): report for path, report in reports.values()}
        counts, rows = collections.Counter(), []
        for key, (path, report) in reports.items():
            result = report["result"]
            if report["mutant"] != "baseline" and report["status"] in {"KILLED", "SURVIVED", "EQUIVALENT"}:
                baseline = hash_index.get(report["baseline_file_sha256"])
                require(baseline is not None and baseline["status"] == "BASELINE_PASS", f"referencia ausente: {path}")
                require(report["baseline_valid"] and module.configuration_matches(baseline, report["case"], report["scenario"], report["parameters"]), f"referencia incompatible: {path}")
                require(baseline["machine"] == report["machine"] and baseline["result"]["environment"] == result["environment"], f"entorno de referencia distinto: {path}")
            status, _ = shared.classify(report["mutant"], report["baseline_valid"], report["returncode"], result)
            if status == "SURVIVED" and result.get("equivalence_reason"):
                status = "EQUIVALENT"
                expected_equivalence = module.equivalence_reason(report["case"], module.SCENARIOS[report["case"]][report["scenario"]], report["mutant"])
                require(expected_equivalence == result["equivalence_reason"], f"equivalencia sin fundamento: {path}")
            require(status == report["status"], f"clasificación no reproducida: {path}")
            counts[status] += 1
            rows.append({
                "case": report["case"], "scenario": report["scenario"], "mutant": report["mutant"],
                "status": status, "reason": report["reason"], "evidence": key,
                "oracle_fine": result["checks"]["oracle_fine"]["actual"],
                "failed_checks": {k: v for k, v in result["checks"].items() if not v["passed"]},
                "wall_seconds": report["wall_seconds"],
            })
        groups[group_name] = {"category": category, "runs": len(rows), "status_counts": dict(counts), "rows": rows}
    categories = {}
    for category in ("main", "cross", "review"):
        counts = collections.Counter()
        for group in groups.values():
            if group["category"] == category:
                counts.update(group["status_counts"])
        categories[category] = {"runs": sum(counts.values()), "status_counts": dict(counts)}
    require([categories[k]["runs"] for k in ("main", "cross", "review")] == [90, 30, 30], "partición incorrecta")
    cross = read(root / "cross_host_comparison.json")
    require(cross["paired_runs"] == 30 and len(cross["rows"]) == 30, "comparación cruzada incompleta")
    lookup = {(r["case"], r["scenario"], r["mutant"], r["machine"]["hostname"].lower()): report_manifest[key] for key, r in all_reports.items() if not key.startswith("independent_review/")}
    for row in cross["rows"]:
        identity = row["case"], row["scenario"], row["mutant"]
        for host in ("war", "guerra"):
            require(lookup[(*identity, host)] == row[f"{host}_report_sha256"], f"comparación enlazada a otra evidencia: {identity}")
    main = categories["main"]["status_counts"]
    return {
        "schema_version": 3, "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "aggregator_sha256": sha(Path(__file__)), "runner_sha256": RUNNER_SHA, "contract_sha256": CONTRACT_SHA, "helper_sha256": HELPER_SHA,
        "model_families": 2, "distinct_parameter_scenarios": 18,
        "actual_cli_runs": 150, "verified_artifact_hashes_actual_runs": artifact_count,
        "copied_fixtures_not_runs": fixture_manifest, "input_run_sha256": report_manifest,
        "categories": categories, "groups": groups,
        "main_detection": {
            "killed": main["KILLED"], "non_equivalent_evaluable": main["KILLED"] + main["SURVIVED"],
            "fraction": main["KILLED"] / (main["KILLED"] + main["SURVIVED"]),
            "denominator_unit": "pares configuración-mutante; no probabilidad de verdad",
        },
        "cross_host_evidence_sha256": sha(root / "cross_host_comparison.json"),
        "cross_host_recorded_result": {k: cross[k] for k in ("paired_runs", "matched_statuses", "all_arrays_exactly_equal", "maximum_absolute_difference")},
        "cross_host_note": "Este agregador verifica los enlaces por hash; la comparación numérica de arrays está documentada por separado.",
        "limitations": [
            "Verificación interna reproducible, no certificación externa ni acreditación",
            "Dos modelos estipulados, no validación experimental de materiales ni sustancias",
            "Dos hosts con el mismo código comprueban reproducibilidad, no independencia algorítmica",
            "El fixture de parámetros alterados no es una ejecución adicional",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("usar un archivo nuevo para preservar evidencia")
    missing_npz = missing_npz_dirs(args.root)
    if missing_npz:
        parser.error(
            "el resumen V3 requiere el bundle opcional con fields.npz; "
            f"faltan datos en {len(missing_npz)} directorios. Descargue y verifique el paquete privado antes de reintentar"
        )
    report = summarize(args.root, Path(__file__).resolve().parent.parent)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("actual_cli_runs", "verified_artifact_hashes_actual_runs", "categories", "main_detection")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
