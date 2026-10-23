import os

for name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[name] = "1"

import argparse
import csv
import datetime
import hashlib
import json
import math
import platform
import socket
import subprocess
import sys
import time
import traceback
from pathlib import Path


CASES = ("heat", "advection", "wave")
MUTANTS = ("baseline", "sign", "coefficient", "frozen", "boundary_zero", "equivalent_periodic_shift", "tiny_coefficient")
PARAMETERS = {
    "heat": {"coefficient": 0.13, "equation": "u_t = kappa u_xx"},
    "advection": {"coefficient": 1.3, "equation": "u_t = -c u_x"},
    "wave": {"coefficient": 0.8, "equation": "u_t = v; v_t = c^2 u_xx"},
}
CHANGES = {
    "baseline": "operador sin cambios",
    "sign": "invertir signo de difusión, transporte o aceleración de onda",
    "coefficient": "multiplicar por 1.25 el coeficiente del RHS; en onda solo c^2 del segundo campo",
    "frozen": "anular todos los campos del RHS",
    "boundary_zero": "sustituir por cero los vecinos que cruzan los bordes",
    "equivalent_periodic_shift": "aplicar roll de exactamente N nodos al estado antes del operador",
    "tiny_coefficient": "multiplicar por 1.000001 el coeficiente del RHS; en onda solo c^2",
}


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def environment_fingerprint():
    import numpy as np

    return {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "python_executable": str(Path(sys.executable).resolve()),
        "numpy_version": np.__version__,
        "numpy_location": str(Path(np.__file__).resolve()),
        "machine_architecture": platform.machine(),
        "byteorder": sys.byteorder,
        "dtype": "float64",
    }


def baseline_metadata_matches(data, case, source_hash, contract_hash, environment):
    return all([
        data.get("status") == "BASELINE_PASS",
        data.get("mutant") == "baseline",
        data.get("case") == case,
        data.get("source_sha256") == source_hash,
        data.get("contract_sha256") == contract_hash,
        data.get("machine", {}).get("hostname") == socket.gethostname(),
        bool(environment),
        data.get("result", {}).get("environment") == environment,
        data.get("result", {}).get("completed") is True,
        data.get("result", {}).get("all_contracts_passed") is True,
    ])


def validate_baseline(path, case, source_hash, contract_hash, environment):
    if path is None:
        return False, "no se proporcionó referencia"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not baseline_metadata_matches(data, case, source_hash, contract_hash, environment):
            return False, "referencia, fuente, contrato, host o fingerprint de entorno no coinciden"
        artifacts = data.get("artifact_sha256", {})
        required = {"worker_result.json", "stdout.log", "stderr.log", "returncode.txt", "fields.npz", "metrics.csv"}
        if not required.issubset(artifacts):
            return False, "faltan hashes de artefactos obligatorios en la referencia"
        for name, expected in artifacts.items():
            artifact = path.parent / name
            if Path(name).name != name or artifact.resolve().parent != path.parent.resolve() or sha(artifact) != expected:
                return False, f"artefacto de referencia alterado o inválido: {name}"
        worker_result = json.loads((path.parent / "worker_result.json").read_text(encoding="utf-8"))
        if worker_result != data["result"]:
            return False, "el resultado de referencia no coincide con su artefacto original"
        return True, "misma fuente, contrato, host y entorno; artefactos verificados"
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return False, "referencia ilegible o mal formada"


def classify(mutant, baseline_valid, returncode, result, timed_out=False):
    if timed_out:
        return "INCONCLUSIVE", "timeout sin diagnóstico causal"
    if returncode != 0 or not isinstance(result, dict) or result.get("failure_kind") == "infrastructure":
        return "INFRA_FAIL", "fallo de proceso, dependencia, artefacto o runner"
    if mutant == "baseline":
        return ("BASELINE_PASS", "referencia satisface el contrato") if result.get("all_contracts_passed") else ("INCONCLUSIVE", "referencia no satisface el contrato")
    if not baseline_valid:
        return "INCONCLUSIVE", "no hay referencia válida del mismo caso, fuente, contrato, host y entorno"
    if result.get("failure_kind") == "numerical":
        return "KILLED", "se infringió finitud durante la integración del operador mutado"
    if not result.get("completed"):
        return "INCONCLUSIVE", "ejecución incompleta sin evidencia causal suficiente"
    if not result.get("all_contracts_passed"):
        return "KILLED", "el mutante ejecutado viola el contrato numérico"
    if mutant == "equivalent_periodic_shift":
        return "EQUIVALENT", "roll por N posiciones es la identidad en esta malla periódica discreta"
    return "SURVIVED", "el contrato no detectó el cambio; no implica equivalencia"


def self_check():
    passed = {"completed": True, "all_contracts_passed": True}
    failed = {"completed": True, "all_contracts_passed": False}
    samples = [
        ("sign", True, 0, failed, False, "KILLED"),
        ("sign", False, 0, failed, False, "INCONCLUSIVE"),
        ("tiny_coefficient", True, 0, passed, False, "SURVIVED"),
        ("equivalent_periodic_shift", True, 0, passed, False, "EQUIVALENT"),
        ("sign", True, 1, failed, False, "INFRA_FAIL"),
        ("sign", True, 0, passed, True, "INCONCLUSIVE"),
        ("sign", True, 0, {"failure_kind": "numerical"}, False, "KILLED"),
        ("baseline", True, 0, failed, False, "INCONCLUSIVE"),
    ]
    for mutant, baseline, code, payload, timeout, expected in samples:
        assert classify(mutant, baseline, code, payload, timeout)[0] == expected
    environment = {"python_version": "test", "numpy_version": "test", "python_executable": "/fixture/python"}
    reference = {
        "status": "BASELINE_PASS", "mutant": "baseline", "case": "heat",
        "source_sha256": "source", "contract_sha256": "contract",
        "machine": {"hostname": socket.gethostname()},
        "result": {"environment": environment, "completed": True, "all_contracts_passed": True},
    }
    assert baseline_metadata_matches(reference, "heat", "source", "contract", environment)
    assert not baseline_metadata_matches(reference, "heat", "source", "contract", {**environment, "numpy_version": "different"})
    assert not baseline_metadata_matches(reference, "heat", "source", "contract", {**environment, "python_executable": "/other/python"})
    assert not baseline_metadata_matches({**reference, "mutant": "sign"}, "heat", "source", "contract", environment)
    print(json.dumps({"classification_self_checks": len(samples), "baseline_fingerprint_self_checks": 4, "passed": True}))


def worker(args):
    import numpy as np

    coefficient = PARAMETERS[args.case]["coefficient"]
    final_time = 0.7
    endpoints = {}
    rows = []
    checks = {}

    def oracle(x, t):
        if args.case == "heat":
            return np.array([1 + 0.5 * np.exp(-coefficient * t) * np.sin(x) + 0.2 * np.exp(-4 * coefficient * t) * np.cos(2 * x)])
        if args.case == "advection":
            return np.array([0.2 + np.sin(x - coefficient * t) + 0.25 * np.cos(2 * (x - coefficient * t))])
        c = coefficient
        return np.array([
            np.sin(x) * np.cos(c * t) + 0.25 * np.cos(2 * x) * np.cos(2 * c * t) + (0.3 / c) * np.cos(x) * np.sin(c * t),
            -c * np.sin(x) * np.sin(c * t) - 0.5 * c * np.cos(2 * x) * np.sin(2 * c * t) + 0.3 * np.cos(x) * np.cos(c * t),
        ])

    def integrate(n, half_step=False):
        x = 2 * np.pi * np.arange(n) / n
        dx = 2 * np.pi / n
        dt_max = 0.2 * dx * dx / coefficient if args.case == "heat" else 0.2 * dx / abs(coefficient)
        steps = math.ceil(final_time / dt_max) * (2 if half_step else 1)
        dt = final_time / steps
        state = oracle(x, 0)
        original_mean = state.mean(axis=1)
        factor = {"sign": -1, "coefficient": 1.25, "tiny_coefficient": 1.000001}.get(args.mutant, 1)

        def rhs(value):
            if args.mutant == "frozen":
                return np.zeros_like(value)
            if args.mutant == "equivalent_periodic_shift":
                value = np.roll(value, n, axis=-1)
            field = value[0]
            left, right = np.roll(field, 1), np.roll(field, -1)
            if args.mutant == "boundary_zero":
                left[0], right[-1] = 0, 0
            lap = (right - 2 * field + left) / (dx * dx)
            if args.case == "heat":
                return np.array([coefficient * factor * lap])
            if args.case == "advection":
                return np.array([-coefficient * factor * (right - left) / (2 * dx)])
            return np.array([value[1], coefficient * coefficient * factor * lap])

        def invariant(value):
            if args.case == "heat":
                return float(np.var(value[0]))
            if args.case == "advection":
                return float(np.mean(value[0] ** 2))
            forward = (np.roll(value[0], -1) - value[0]) / dx
            return float(0.5 * np.mean(value[1] ** 2 + coefficient * coefficient * forward ** 2))

        invariant_initial = invariant(state)
        previous = invariant_initial
        max_increase, max_relative_drift, max_mean_drift = 0.0, 0.0, 0.0
        for step in range(steps + 1):
            t = step * dt
            current = invariant(state)
            max_increase = max(max_increase, current - previous)
            max_relative_drift = max(max_relative_drift, abs(current - invariant_initial) / invariant_initial)
            max_mean_drift = max(max_mean_drift, float(np.max(np.abs(state.mean(axis=1) - original_mean))))
            error = float(np.sqrt(np.mean((state - oracle(x, t)) ** 2)))
            rows.append({"n": n, "half_step": half_step, "dt": dt, "t": t, "rms_error": error, "invariant": current, "mean_drift": max_mean_drift})
            previous = current
            if step == steps:
                break
            k1 = rhs(state)
            k2 = rhs(state + 0.5 * dt * k1)
            k3 = rhs(state + 0.5 * dt * k2)
            k4 = rhs(state + dt * k3)
            state = state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            if not np.isfinite(state).all():
                raise FloatingPointError("estado no finito tras paso RK4")
        key = f"n{n}" + ("_half" if half_step else "")
        endpoints[key] = state
        endpoints[f"{key}_exact"] = oracle(x, final_time)
        endpoints[f"{key}_x"] = x
        return {
            "n": n, "dt": dt, "steps": steps, "rms_error": error,
            "mean_drift_max": max_mean_drift,
            "invariant_relative_drift_max": max_relative_drift,
            "invariant_increase_max": max_increase,
        }

    def check(name, actual, threshold, accepted):
        checks[name] = {"actual": actual, "criterion": threshold, "passed": bool(accepted)}

    with np.errstate(over="raise", invalid="raise", divide="raise"):
        resolutions = [32, 64, 128] if args.mutant == "baseline" else [64]
        runs = [integrate(n) for n in resolutions]
        for item in runs:
            n = item["n"]
            check(f"mean_n{n}", item["mean_drift_max"], "< 1e-10", item["mean_drift_max"] < 1e-10)
            if args.case == "heat":
                check(f"variance_monotone_n{n}", item["invariant_increase_max"], "<= 1e-12", item["invariant_increase_max"] <= 1e-12)
            else:
                check(f"discrete_invariant_n{n}", item["invariant_relative_drift_max"], "< 1e-7", item["invariant_relative_drift_max"] < 1e-7)
        if args.mutant == "baseline":
            errors = [item["rms_error"] for item in runs]
            check("oracle_n128", errors[-1], "< 1e-3", errors[-1] < 1e-3)
            for index in range(2):
                order = math.log2(errors[index] / errors[index + 1])
                check(f"spatial_order_{resolutions[index]}_{resolutions[index + 1]}", order, "1.7 <= p <= 2.3", 1.7 <= order <= 2.3)
            half = integrate(64, True)
            delta = float(np.sqrt(np.mean((endpoints["n64"] - endpoints["n64_half"]) ** 2)))
            check("temporal_consistency", delta, "< 1e-6 and < .02 * E64", delta < 1e-6 and delta < 0.02 * errors[1])
            runs.append(half)
        else:
            check("oracle_n64", runs[0]["rms_error"], "< .005", runs[0]["rms_error"] < 0.005)
    np.savez_compressed(args.output / "fields.npz", **endpoints)
    with (args.output / "metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    versions = {"python": platform.python_version(), "numpy": np.__version__}
    if not args.no_plot:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        versions["matplotlib"] = matplotlib.__version__
        key = f"n{max(resolutions)}"
        observed, exact, x = endpoints[key], endpoints[f"{key}_exact"], endpoints[f"{key}_x"]
        fig, axes = plt.subplots(len(observed), 2, figsize=(12, 3.5 * len(observed)), squeeze=False)
        for component in range(len(observed)):
            axes[component, 0].plot(x, exact[component], label="Oráculo analítico", color="#12605c")
            axes[component, 0].plot(x, observed[component], "--", label="Aproximación", color="#ba7205")
            axes[component, 0].set_title("u" if component == 0 else "v")
            axes[component, 0].legend()
            axes[component, 1].plot(x, observed[component] - exact[component], color="#ba7205")
            axes[component, 1].set_title("Error firmado respecto al oráculo")
            for axis in axes[component]:
                axis.set_xlabel("x")
                axis.grid(alpha=0.2)
        fig.suptitle(f"{args.case} · {args.mutant} · N={max(resolutions)} · T=0.7")
        fig.tight_layout()
        fig.savefig(args.output / "comparison.png", dpi=150)
        plt.close(fig)
    return {"completed": True, "all_contracts_passed": all(item["passed"] for item in checks.values()), "checks": checks, "runs": runs, "versions": versions, "all_values_finite": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=CASES)
    parser.add_argument("--mutant", choices=MUTANTS, default="baseline")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.self_check:
        self_check()
        return 0
    if args.case is None or args.output is None:
        parser.error("--case y --output son obligatorios")
    args.output = args.output.resolve()
    if args.worker:
        environment = None
        try:
            environment = environment_fingerprint()
            payload = worker(args)
        except FloatingPointError as error:
            payload = {"completed": False, "all_contracts_passed": False, "failure_kind": "numerical", "error": str(error)}
            traceback.print_exc()
        except Exception as error:
            traceback.print_exc()
            payload = {"completed": False, "failure_kind": "infrastructure", "error_type": type(error).__name__, "error": str(error)}
        payload["environment"] = environment
        (args.output / "worker_result.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return 10 if payload.get("failure_kind") == "infrastructure" else 0
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout debe ser finito y positivo")
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("la carpeta de salida no está vacía; conserva la evidencia anterior")
    args.output.mkdir(parents=True, exist_ok=True)
    started_utc, started_ns = utc(), time.perf_counter_ns()
    source_hash = sha(__file__)
    contract_path = Path(__file__).resolve().parent.parent / "references" / "contratos-1d.md"
    contract_hash = sha(contract_path)
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", "--case", args.case, "--mutant", args.mutant, "--output", str(args.output)]
    if args.no_plot:
        command.append("--no-plot")
    timed_out, result = False, None
    try:
        execution = subprocess.run(command, capture_output=True, timeout=args.timeout, check=False)
        stdout, stderr, returncode = execution.stdout, execution.stderr, execution.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, returncode, timed_out = error.stdout or b"", error.stderr or b"", None, True
    except OSError as error:
        stdout, stderr, returncode = b"", str(error).encode("utf-8"), -1
    (args.output / "stdout.log").write_bytes(stdout)
    (args.output / "stderr.log").write_bytes(stderr)
    (args.output / "returncode.txt").write_text(str(returncode) + "\n", encoding="utf-8")
    result_path = args.output / "worker_result.json"
    if result_path.exists():
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except ValueError:
            result = None
    baseline_valid, baseline_reason = validate_baseline(
        args.baseline, args.case, source_hash, contract_hash,
        result.get("environment") if isinstance(result, dict) else None,
    )
    status, reason = classify(args.mutant, baseline_valid, returncode, result, timed_out)
    finished_ns = time.perf_counter_ns()
    report = {
        "schema_version": 1, "case": args.case, "mutant": args.mutant,
        "status": status, "reason": reason, "operator_change": CHANGES[args.mutant],
        "started_utc": started_utc, "finished_utc": utc(),
        "monotonic_start_ns": started_ns, "monotonic_finish_ns": finished_ns,
        "wall_seconds": (finished_ns - started_ns) / 1e9,
        "source_sha256": source_hash, "contract_sha256": contract_hash,
        "machine": {"hostname": socket.gethostname(), "platform": platform.platform(), "processor": platform.processor(), "logical_cpus": os.cpu_count()},
        "parameters": {**PARAMETERS[args.case], "T": 0.7, "domain": "periodic [0,2*pi)", "seed": 0, "randomness_used": False, "threads_requested": 1, "compute_device": "CPU"},
        "command": command, "returncode": returncode, "timeout_seconds": args.timeout,
        "baseline_valid": baseline_valid,
        "baseline_validation_reason": baseline_reason,
        "baseline_file_sha256": sha(args.baseline) if args.baseline and args.baseline.exists() else None,
        "result": result,
        "limitations": ["contrato de calibración 1D; no prueba de una teoría general", "invariantes no sustituyen precisión", "SURVIVED no significa equivalencia"],
        "artifact_sha256": {path.name: sha(path) for path in sorted(args.output.iterdir()) if path.is_file()},
    }
    (args.output / "run.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"case": args.case, "mutant": args.mutant, "status": status, "reason": reason, "output": str(args.output)}, ensure_ascii=False))
    return 2 if status == "INFRA_FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
