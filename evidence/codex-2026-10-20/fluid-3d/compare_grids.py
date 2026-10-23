import argparse
import datetime
import hashlib
import json
import socket
from pathlib import Path

import numpy as np


def read(directory):
    summary = json.loads((directory / "simulation_summary.json").read_text(encoding="utf-8"))
    actual = hashlib.sha256((directory / "fields.npz").read_bytes()).hexdigest()
    if actual != summary["artifact_sha256"]["fields.npz"]:
        raise ValueError(f"hash fields.npz incorrecto: {directory}")
    fields = np.load(directory / "fields.npz", allow_pickle=False)
    return summary, fields


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--coarse", type=Path, required=True)
    parser.add_argument("--fine", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    coarse, coarse_fields = read(args.coarse)
    fine, fine_fields = read(args.fine)
    for key in ("dt", "T", "viscosities", "forcing", "domain", "initial", "method"):
        if coarse["parameters"][key] != fine["parameters"][key]:
            raise ValueError(f"parámetro incompatible: {key}")
    n_coarse = coarse["parameters"]["n"]
    n_fine = fine["parameters"]["n"]
    if n_fine != 2 * n_coarse:
        raise ValueError("se espera una malla fina con el doble de puntos por eje")
    assert np.allclose(
        coarse_fields["initial_velocity"],
        fine_fields["initial_velocity"][:, ::2, ::2, ::2],
        atol=1e-14, rtol=0,
    )
    results = {}
    for index, label in enumerate(("Euler", "NavierStokes")):
        value = coarse_fields["final_velocity"][index]
        reference = fine_fields["final_velocity"][index, :, ::2, ::2, ::2]
        assert reference.shape == value.shape
        rms_reference = float(np.sqrt(np.mean(reference ** 2)))
        difference = float(np.sqrt(np.mean((value - reference) ** 2)))
        if rms_reference == 0:
            raise ValueError("referencia de norma cero")
        diagnostics_key = "euler_final" if index == 0 else "ns_final"
        results[label] = {
            "rms_velocity_difference": difference,
            "reference_velocity_rms": rms_reference,
            "relative_rms_velocity_difference": difference / rms_reference,
            "coarse_final": coarse["diagnostics"][diagnostics_key],
            "fine_final": fine["diagnostics"][diagnostics_key],
        }
    report = {
        "scope": "SENSIBILIDAD ESPACIAL ENTRE DOS MALLAS; NO CERTIFICADO DE CONVERGENCIA",
        "host": socket.gethostname(),
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "grids": [n_coarse, n_fine],
        "dt": coarse["parameters"]["dt"], "T": coarse["parameters"]["T"],
        "comparison": "Velocidad final de la malla fina muestreada en puntos coincidentes, sin filtrado adicional.",
        "interpretation": "Diferencia observada, no error contra una solución continua exacta. No se asigna PASS espacial.",
        "coarse_source_sha256": coarse["source_sha256"],
        "fine_source_sha256": fine["source_sha256"],
        "coarse_fields_sha256": coarse["artifact_sha256"]["fields.npz"],
        "fine_fields_sha256": fine["artifact_sha256"]["fields.npz"],
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
