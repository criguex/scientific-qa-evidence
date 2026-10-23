import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


FILES = (
    "README.md",
    "INFORME_FISICA_QUIMICA_V3.md",
    "controls/summarize_ode_v3.py",
    "controls/hash_v3_artifacts.py",
    "simulation/render_ode_contacts.py",
    "skills/escenarios-verificables/SKILL.md",
    "skills/escenarios-verificables/agents/openai.yaml",
    "skills/escenarios-verificables/references/contratos-1d.md",
    "skills/escenarios-verificables/references/contratos-ode-v3.md",
    "skills/escenarios-verificables/scripts/run_ode_scenario.py",
    "skills/escenarios-verificables/scripts/run_scenario.py",
    ".gitattributes",
    ".gitignore",
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = Path(__file__).resolve().parent.parent
    output = args.output.resolve()
    if output.name in {"SHA256SUMS.txt", "SHA256SUMS_V2.txt"} or output.exists():
        parser.error("no sobrescribir manifiestos anteriores; elegir un archivo V3 nuevo")
    if not output.is_relative_to(repository):
        parser.error("guardar el manifiesto dentro del repositorio")
    aggregator_path = repository / "controls/summarize_ode_v3.py"
    spec = importlib.util.spec_from_file_location("ode_aggregator", aggregator_path)
    aggregator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(aggregator)
    evidence = repository / "evidence/ode_v3"
    verified = aggregator.summarize(evidence, repository)
    recorded = json.loads((evidence / "campaign_summary.json").read_text(encoding="utf-8"))
    for key in ("actual_cli_runs", "verified_artifact_hashes_actual_runs", "categories", "input_run_sha256", "copied_fixtures_not_runs"):
        if verified[key] != recorded[key]:
            parser.error(f"resumen no coincide con los datos: {key}")
    contacts_verified = 0
    renderer_hash = sha(repository / "simulation/render_ode_contacts.py")
    for family in ("physics", "chemistry"):
        directory = evidence / "contacts" / family
        summary = json.loads((directory / "contacts_summary.json").read_text(encoding="utf-8"))
        if summary["source_sha256"] != renderer_hash or summary["new_integration_performed"]:
            parser.error(f"procedencia de render incoherente: {family}")
        if len(summary["input_run_sha256"]) != 9:
            parser.error(f"faltan referencias gráficas: {family}")
        allowed_inputs = set(recorded["input_run_sha256"].values())
        if not set(summary["input_run_sha256"].values()).issubset(allowed_inputs):
            parser.error(f"el render usa referencias no incluidas: {family}")
        for filename, expected in summary["artifact_sha256"].items():
            if Path(filename).name != filename or sha(directory / filename) != expected:
                parser.error(f"artefacto gráfico alterado: {family}/{filename}")
            contacts_verified += 1
    paths = {repository / name for name in FILES}
    paths.update(path for path in evidence.rglob("*") if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store")
    if any(not path.is_file() or path.is_symlink() for path in paths):
        parser.error("fuente ausente o enlace simbólico; revisar antes de congelar")
    rows = [f"{sha(path)}  {path.relative_to(repository).as_posix()}" for path in sorted(paths)]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({
        "manifest": output.name, "files": len(rows),
        "actual_runs": verified["actual_cli_runs"],
        "raw_artifact_hashes_verified": verified["verified_artifact_hashes_actual_runs"],
        "contact_images_verified": contacts_verified,
        "prior_manifests_modified": False,
    }))


if __name__ == "__main__":
    main()
