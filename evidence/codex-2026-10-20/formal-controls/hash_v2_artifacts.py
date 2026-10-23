import argparse
import hashlib
import json
from pathlib import Path


ROOTS = (
    "skills/escenarios-verificables",
    "evidence/scenarios_v2",
    "evidence/images_gpt",
    "evidence/voice_preview_v2",
    "evidence/fluid_temporal_v2",
    "simulation/analytic_render",
)
FILES = (
    "README.md",
    "PLAN_VALIDACION_V2.md",
    "NS08_PROPUESTA_NO_EJECUTADA.md",
    "INFORME_ESCENARIOS_V2.md",
    "simulation/render_analytic_scenarios.py",
    "controls/summarize_scenarios.py",
    "controls/hash_v2_artifacts.py",
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repository = Path(__file__).resolve().parent.parent
    output = args.output.resolve()
    if output.name == "SHA256SUMS.txt":
        parser.error("el manifiesto V1 SHA256SUMS.txt no se modifica")
    if output.exists():
        parser.error("la salida ya existe; elegir un manifiesto V2 nuevo")
    if not output.is_relative_to(repository):
        parser.error("el manifiesto debe guardarse dentro del repositorio")
    for filename in ("render_summary.json", "TRES_ESCENARIOS_ANALITICOS_5070.mp4", "PORTADA_TRES_ESCENARIOS.png"):
        if not (repository / "simulation" / "analytic_render" / filename).is_file():
            parser.error(f"falta un artefacto final requerido: {filename}")
    render_directory = repository / "simulation" / "analytic_render"
    render = json.loads((render_directory / "render_summary.json").read_text(encoding="utf-8"))
    renderer_hash = hashlib.sha256((repository / "simulation" / "render_analytic_scenarios.py").read_bytes()).hexdigest()
    if renderer_hash != render["source_sha256"]:
        parser.error("la fuente del renderer no coincide con el render registrado")
    for name, expected in render["artifact_sha256"].items():
        relative = Path(name.replace("\\", "/"))
        artifact = render_directory / relative
        if relative.is_absolute() or ".." in relative.parts or not artifact.is_file() or hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
            parser.error(f"artefacto de render ausente o alterado: {name}")
    paths = {repository / name for name in FILES}
    for name in ROOTS:
        directory = repository / name
        if not directory.is_dir():
            parser.error(f"falta la entrega requerida: {name}")
        paths.update(path for path in directory.rglob("*") if path.is_file() and "__pycache__" not in path.parts and path.name != ".DS_Store")
    if any(not path.is_file() or path.is_symlink() for path in paths):
        parser.error("falta una fuente o hay enlaces simbólicos; revisar antes de congelar")
    rows = []
    for path in sorted(paths):
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{checksum}  {path.relative_to(repository).as_posix()}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{len(rows)} archivos V2 registrados en {output.name}; {len(render['artifact_sha256'])} hashes originales de render verificados; manifiesto V1 intacto")


if __name__ == "__main__":
    main()
