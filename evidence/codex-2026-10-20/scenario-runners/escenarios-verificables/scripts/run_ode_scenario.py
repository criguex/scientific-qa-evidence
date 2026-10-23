import os

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import argparse
import csv
import datetime
import hashlib
import importlib.util
import json
import math
import platform
import socket
import subprocess
import sys
import time
import traceback
from pathlib import Path


SHARED_SHA = "cc9259992eee682d9ebb7c368e0cb91454b3f777d4b41ae3a87baf72e19094b9"
SCENARIOS = {"oscillator": {}, "reaction": {}}
for index, (zeta, omega, x0, v0) in enumerate(
    [(z, w, x, v) for z in (0.0, 0.35, 1.0, 1.8) for w, x, v in ((0.8, 0.7, -0.2), (1.7, -0.4, 0.9))]
    + [(0.0, 0.0, 0.4, 0.3)], 1
):
    SCENARIOS["oscillator"][f"osc{index:02}"] = {"omega": omega, "zeta": zeta, "x0": x0, "v0": v0}
for index, (kf, kr, a0, b0) in enumerate(
    [(0, 0, 1, 0), (0, 0, 0.3, 0.7), (0.4, 0, 1, 0), (0, 0.6, 0, 1),
     (0.2, 0.3, 1, 0), (0.7, 0.1, 0.2, 0.8), (2, 3, 0.4, 0.6),
     (0.3, 0.7, 0.7, 0.3), (0.2, 0.3, 0, 0)], 1
):
    SCENARIOS["reaction"][f"rxn{index:02}"] = {"kf": float(kf), "kr": float(kr), "A0": float(a0), "B0": float(b0)}
MUTANTS = {
    "oscillator": ("baseline", "spring_sign", "damping_sign", "spring_coefficient", "frozen"),
    "reaction": ("baseline", "reverse_sign", "forward_coefficient", "mass_leak", "frozen"),
}
CHANGES = {
    "baseline": "sin cambios",
    "spring_sign": "cambiar -omega^2*x por +omega^2*x en la aceleración",
    "damping_sign": "cambiar -2*zeta*omega*v por +2*zeta*omega*v",
    "spring_coefficient": "multiplicar por 1.25 solo el término -omega^2*x",
    "reverse_sign": "cambiar +kr*B por -kr*B en A' y -kr*B por +kr*B en B'",
    "forward_coefficient": "multiplicar kf por 1.25 en ambas ecuaciones",
    "mass_leak": "omitir -kr*B solo en B'",
    "frozen": "anular ambos campos del RHS",
}


def load_shared():
    path = Path(__file__).with_name("run_scenario.py")
    if hashlib.sha256(path.read_bytes()).hexdigest() != SHARED_SHA:
        raise RuntimeError("hash del helper V2 distinto; no reutilizar una dependencia modificada")
    spec = importlib.util.spec_from_file_location("verified_scenario_v2", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_parameters(case, parameters):
    if not all(math.isfinite(value) for value in parameters.values()):
        raise ValueError("todos los parámetros deben ser finitos")
    if case == "oscillator":
        if parameters["omega"] < 0 or parameters["zeta"] < 0:
            raise ValueError("omega y zeta deben ser no negativos")
        if parameters["omega"] == 0 and parameters["zeta"] != 0:
            raise ValueError("el caso libre omega=0 se define aquí con zeta=0")
    elif any(value < 0 for value in parameters.values()):
        raise ValueError("tasas y concentraciones iniciales deben ser no negativas")


def initial(case, p):
    import numpy as np

    return np.array([p["x0"], p["v0"]] if case == "oscillator" else [p["A0"], p["B0"]], dtype=np.float64)


def oracle(case, p, t):
    import numpy as np

    t = np.asarray(t, dtype=np.float64)
    if case == "reaction":
        total, q = p["A0"] + p["B0"], p["kf"] + p["kr"]
        if q == 0:
            return np.stack([np.full_like(t, p["A0"]), np.full_like(t, p["B0"])], axis=-1)
        equilibrium = p["kr"] * total / q
        a = equilibrium + (p["A0"] - equilibrium) * np.exp(-q * t)
        return np.stack([a, total - a], axis=-1)
    w, z, x0, v0 = p["omega"], p["zeta"], p["x0"], p["v0"]
    if w == 0:
        return np.stack([x0 + v0 * t, np.full_like(t, v0)], axis=-1)
    alpha = z * w
    if z < 1:
        beta = w * np.sqrt(1 - z * z)
        decay, cosine, sine = np.exp(-alpha * t), np.cos(beta * t), np.sin(beta * t)
        x = decay * (x0 * cosine + (v0 + alpha * x0) * sine / beta)
        v = decay * (v0 * cosine - (alpha * v0 + w * w * x0) * sine / beta)
    elif z == 1:
        d = v0 + w * x0
        x = np.exp(-w * t) * (x0 + d * t)
        v = np.exp(-w * t) * (v0 - w * d * t)
    else:
        beta = w * np.sqrt(z * z - 1)
        plus, minus = -alpha + beta, -alpha - beta
        cplus, cminus = (v0 - minus * x0) / (plus - minus), (plus * x0 - v0) / (plus - minus)
        x = cplus * np.exp(plus * t) + cminus * np.exp(minus * t)
        v = plus * cplus * np.exp(plus * t) + minus * cminus * np.exp(minus * t)
    return np.stack([x, v], axis=-1)


def rhs(case, p, mutant, state):
    import numpy as np

    if mutant == "frozen":
        return np.zeros_like(state)
    if case == "oscillator":
        spring = -p["omega"] ** 2 * state[0]
        damping = -2 * p["zeta"] * p["omega"] * state[1]
        if mutant == "spring_sign":
            spring *= -1
        elif mutant == "spring_coefficient":
            spring *= 1.25
        elif mutant == "damping_sign":
            damping *= -1
        return np.array([state[1], spring + damping])
    forward = p["kf"] * state[0] * (1.25 if mutant == "forward_coefficient" else 1)
    reverse = p["kr"] * state[1]
    if mutant == "reverse_sign":
        return np.array([-forward - reverse, forward + reverse])
    return np.array([-forward + reverse, forward if mutant == "mass_leak" else forward - reverse])


def equivalence_reason(case, p, mutant):
    if case == "oscillator":
        if mutant in ("spring_sign", "spring_coefficient") and p["omega"] == 0:
            return "omega=0: el término de resorte es cero para todos los estados"
        if mutant == "damping_sign" and p["zeta"] * p["omega"] == 0:
            return "zeta*omega=0: el término de amortiguamiento es cero para todos los estados"
    else:
        if mutant in ("reverse_sign", "mass_leak") and p["kr"] == 0:
            return "kr=0: los términos inversos modificados son cero para todos los estados"
        if mutant == "forward_coefficient" and p["kf"] == 0:
            return "kf=0: el término directo modificado es cero para todos los estados"
        if mutant == "frozen" and p["kf"] == p["kr"] == 0:
            return "kf=kr=0: el operador original es cero para todos los estados"
    return None


def configuration_matches(reference, case, scenario, parameters):
    return all([
        reference.get("case") == case,
        reference.get("scenario") == scenario,
        reference.get("parameters") == parameters,
        reference.get("dependencies", {}).get("run_scenario.py") == SHARED_SHA,
    ])


def observed_order(coarse, fine):
    return None if min(coarse, fine) <= 1e-12 else math.log2(coarse / fine)


def self_check(shared):
    import numpy as np

    shared.self_check()
    tested = 0
    for case, scenarios in SCENARIOS.items():
        for p in scenarios.values():
            validate_parameters(case, p)
            assert np.max(np.abs(oracle(case, p, 0) - initial(case, p))) < 1e-12
            derivative = (oracle(case, p, 1e-6) - oracle(case, p, -1e-6)) / 2e-6
            assert np.max(np.abs(derivative - rhs(case, p, "baseline", initial(case, p)))) < 1e-7
            tested += 2
    for case, p in (
        ("oscillator", {"omega": -1, "zeta": 0, "x0": 1, "v0": 0}),
        ("oscillator", {"omega": 0, "zeta": 1, "x0": 1, "v0": 0}),
        ("oscillator", {"omega": 1, "zeta": -0.1, "x0": 1, "v0": 0}),
        ("oscillator", {"omega": 1, "zeta": 0, "x0": math.nan, "v0": 0}),
        ("reaction", {"kf": -1, "kr": 0, "A0": 1, "B0": 0}),
        ("reaction", {"kf": 1, "kr": 0, "A0": -1, "B0": 0}),
        ("reaction", {"kf": 1, "kr": math.inf, "A0": 1, "B0": 0}),
    ):
        try:
            validate_parameters(case, p)
        except ValueError:
            tested += 1
        else:
            raise AssertionError("se aceptó un parámetro inválido")
    assert observed_order(1e-9, 1e-9 / 16) == 4
    assert observed_order(0, 0) is None
    assert observed_order(1e-11, 1e-13) is None
    assert equivalence_reason("oscillator", SCENARIOS["oscillator"]["osc09"], "spring_sign")
    assert not equivalence_reason("oscillator", SCENARIOS["oscillator"]["osc09"], "frozen")
    assert not equivalence_reason("reaction", SCENARIOS["reaction"]["rxn08"], "frozen")
    assert not equivalence_reason("reaction", SCENARIOS["reaction"]["rxn09"], "frozen")
    parameters = {"omega": 0.8, "zeta": 0}
    reference = {"case": "oscillator", "scenario": "osc01", "parameters": parameters, "dependencies": {"run_scenario.py": SHARED_SHA}}
    assert configuration_matches(reference, "oscillator", "osc01", parameters)
    assert not configuration_matches(reference, "oscillator", "osc02", parameters)
    assert not configuration_matches(reference, "oscillator", "osc01", {**parameters, "omega": 1.7})
    print(json.dumps({"ode_self_checks": tested + 10, "scenarios": 18, "passed": True}))


def worker(args):
    import numpy as np

    p = SCENARIOS[args.case][args.scenario]
    validate_parameters(args.case, p)
    checks, rows, arrays, runs = {}, [], {}, []
    stepsizes = (0.05, 0.025, 0.0125) if args.mutant == "baseline" else (0.0125,)

    def check(name, value, criterion, passed, status=None):
        checks[name] = {"actual": value, "criterion": criterion, "passed": bool(passed)}
        if status:
            checks[name]["status"] = status

    with np.errstate(over="raise", invalid="raise", divide="raise"):
        for run_index, dt in enumerate(stepsizes):
            steps = round(4 / dt)
            times = np.arange(steps + 1) * dt
            states = np.empty((steps + 1, 2))
            states[0] = initial(args.case, p)
            for step in range(steps):
                state = states[step]
                k1 = rhs(args.case, p, args.mutant, state)
                k2 = rhs(args.case, p, args.mutant, state + dt * k1 / 2)
                k3 = rhs(args.case, p, args.mutant, state + dt * k2 / 2)
                k4 = rhs(args.case, p, args.mutant, state + dt * k3)
                states[step + 1] = state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
                if not np.isfinite(states[step + 1]).all():
                    raise FloatingPointError(f"estado no finito en paso {step + 1}")
            exact = oracle(args.case, p, times)
            errors = np.sqrt(np.mean((states - exact) ** 2, axis=1))
            stride = round(0.05 / dt)
            maximum = float(np.max(errors[::stride]))
            suffix = f"h{dt:g}"
            if args.case == "oscillator":
                invariant = 0.5 * (states[:, 1] ** 2 + p["omega"] ** 2 * states[:, 0] ** 2)
                if p["zeta"] == 0:
                    absolute_drift = float(np.max(np.abs(invariant - invariant[0])))
                    if invariant[0] == 0:
                        check(f"zero_energy_absolute_drift_{suffix}", absolute_drift, "<= 1e-12", absolute_drift <= 1e-12)
                    else:
                        drift = absolute_drift / float(invariant[0])
                        check(f"energy_relative_drift_{suffix}", drift, "<= 1e-6", drift <= 1e-6)
                else:
                    increase = float(np.max(np.diff(invariant)))
                    check(f"energy_increase_{suffix}", increase, "<= 1e-12", increase <= 1e-12)
            else:
                total = p["A0"] + p["B0"]
                invariant = states.sum(axis=1)
                drift = float(np.max(np.abs(invariant - total)))
                minimum, maximum_state = float(np.min(states)), float(np.max(states))
                check(f"mass_drift_{suffix}", drift, "<= 1e-12", drift <= 1e-12)
                check(f"nonnegative_{suffix}", minimum, ">= -1e-12", minimum >= -1e-12)
                check(f"bounded_{suffix}", maximum_state, "<= initial_total + 1e-12", maximum_state <= total + 1e-12)
            for index, t in enumerate(times):
                rows.append({"dt": dt, "t": float(t), "state_0": float(states[index, 0]), "state_1": float(states[index, 1]), "oracle_0": float(exact[index, 0]), "oracle_1": float(exact[index, 1]), "rms_error": float(errors[index]), "common_time": index % stride == 0, "invariant": float(invariant[index])})
            arrays[f"times_{run_index}"] = times
            arrays[f"states_{run_index}"] = states
            arrays[f"oracle_{run_index}"] = exact
            runs.append({"dt": dt, "steps": steps, "common_sample_count": len(errors[::stride]), "maximum_rms_error_common_times": maximum})
        check("oracle_fine", runs[-1]["maximum_rms_error_common_times"], "< 1e-6", runs[-1]["maximum_rms_error_common_times"] < 1e-6)
        if args.mutant == "baseline":
            for index in range(2):
                order = observed_order(runs[index]["maximum_rms_error_common_times"], runs[index + 1]["maximum_rms_error_common_times"])
                check(f"order_pair_{index}", order, "3.6 <= p <= 4.4 if both errors > 1e-12", order is None or 3.6 <= order <= 4.4, "ROUND_OFF_LIMITED" if order is None else "MEASURED")
    np.savez_compressed(args.output / "fields.npz", **arrays)
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
        labels = ("x", "v") if args.case == "oscillator" else ("A", "B")
        fig, axes = plt.subplots(2, 2, figsize=(12, 6.5), facecolor="#091728")
        color = "#86E7C8" if args.mutant == "baseline" else "#FFC675"
        for index, label in enumerate(labels):
            for axis in axes[index]:
                axis.set_facecolor("#11273A")
                axis.tick_params(colors="#B4C5D2")
                axis.grid(alpha=0.15)
                axis.set_xlabel("t (adimensional)", color="#B4C5D2")
            axes[index, 0].plot(times, exact[:, index], "--", color="#F1F7F7", label="Oráculo")
            axes[index, 0].plot(times, states[:, index], color=color, label=args.mutant)
            axes[index, 0].set_title(label, color="#F1F7F7")
            axes[index, 0].legend(facecolor="#11273A", labelcolor="#F1F7F7")
            axes[index, 1].plot(times, states[:, index] - exact[:, index], color=color)
            axes[index, 1].set_title(f"Error firmado de {label}", color="#F1F7F7")
        fig.suptitle(f"{args.case} · {args.scenario} · {args.mutant} · dt = {dt:g}", color="#F1F7F7")
        fig.tight_layout()
        fig.savefig(args.output / "comparison.png", dpi=120, facecolor=fig.get_facecolor())
        plt.close(fig)
    equilibrium = bool(np.all(rhs(args.case, p, "baseline", initial(args.case, p)) == 0))
    return {"completed": True, "all_contracts_passed": all(item["passed"] for item in checks.values()), "checks": checks, "runs": runs, "versions": versions, "all_values_finite": True, "initial_state_is_exact_equilibrium": equilibrium, "equivalence_reason": equivalence_reason(args.case, p, args.mutant)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=SCENARIOS)
    parser.add_argument("--scenario")
    parser.add_argument("--mutant", default="baseline")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--timeout", type=float, default=120)
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--list-scenarios", action="store_true")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.list_scenarios:
        print(json.dumps(SCENARIOS, indent=2))
        return 0
    if args.self_check:
        self_check(load_shared())
        return 0
    if args.case is None or args.scenario not in SCENARIOS[args.case] or args.output is None:
        parser.error("se requieren --case, --scenario válido y --output")
    if args.mutant not in MUTANTS[args.case]:
        parser.error(f"mutantes de {args.case}: {MUTANTS[args.case]}")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout debe ser finito y positivo")
    args.output = args.output.resolve()
    if args.worker:
        environment = None
        try:
            shared = load_shared()
            environment = shared.environment_fingerprint()
            payload = worker(args)
        except FloatingPointError as error:
            payload = {"completed": False, "all_contracts_passed": False, "failure_kind": "numerical", "error": str(error)}
            traceback.print_exc()
        except Exception as error:
            payload = {"completed": False, "failure_kind": "infrastructure", "error_type": type(error).__name__, "error": str(error)}
            traceback.print_exc()
        payload["environment"] = environment
        (args.output / "worker_result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return 10 if payload.get("failure_kind") == "infrastructure" else 0
    if args.output.exists() and any(args.output.iterdir()):
        parser.error("la salida no está vacía; conservar la evidencia")
    args.output.mkdir(parents=True, exist_ok=True)
    started_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    started_ns = time.perf_counter_ns()
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    contract = Path(__file__).resolve().parent.parent / "references" / "contratos-ode-v3.md"
    contract_hash = hashlib.sha256(contract.read_bytes()).hexdigest() if contract.is_file() else None
    parameters = {
        **SCENARIOS[args.case][args.scenario], "T": 4.0, "units": "adimensionales",
        "equation": "x'=v; v'=-omega^2*x-2*zeta*omega*v" if args.case == "oscillator" else "A'=-kf*A+kr*B; B'=kf*A-kr*B",
        "method": "RK4", "baseline_dt": [0.05, 0.025, 0.0125], "mutant_dt": 0.0125,
        "common_sample_interval": 0.05, "seed": 0, "randomness_used": False,
        "threads_requested": 1, "compute_device": "CPU",
    }
    command = [sys.executable, str(Path(__file__).resolve()), "--worker", "--case", args.case, "--scenario", args.scenario, "--mutant", args.mutant, "--output", str(args.output)]
    if args.no_plot:
        command.append("--no-plot")
    timed_out, shared, result = False, None, None
    try:
        if contract_hash is None:
            raise FileNotFoundError("falta el contrato ODE V3")
        shared = load_shared()
        execution = subprocess.run(command, capture_output=True, timeout=args.timeout, check=False)
        stdout, stderr, returncode = execution.stdout, execution.stderr, execution.returncode
    except subprocess.TimeoutExpired as error:
        stdout, stderr, returncode, timed_out = error.stdout or b"", error.stderr or b"", None, True
    except Exception:
        stdout, stderr, returncode = b"", traceback.format_exc().encode("utf-8"), -1
    (args.output / "stdout.log").write_bytes(stdout)
    (args.output / "stderr.log").write_bytes(stderr)
    (args.output / "returncode.txt").write_text(str(returncode) + "\n", encoding="utf-8")
    result_path = args.output / "worker_result.json"
    if result_path.exists():
        try:
            result = json.loads(result_path.read_text(encoding="utf-8"))
        except ValueError:
            pass
    baseline_valid, baseline_reason = False, "no se proporcionó referencia válida"
    if shared:
        baseline_valid, baseline_reason = shared.validate_baseline(args.baseline, args.case, source_hash, contract_hash, result.get("environment") if isinstance(result, dict) else None)
        if baseline_valid:
            reference = json.loads(args.baseline.read_text(encoding="utf-8"))
            baseline_valid = configuration_matches(reference, args.case, args.scenario, parameters)
            if not baseline_valid:
                baseline_reason = "configuración, parámetros o dependencia auxiliar distintos"
        status, reason = shared.classify(args.mutant, baseline_valid, returncode, result, timed_out)
        if status == "SURVIVED" and result.get("equivalence_reason"):
            status, reason = "EQUIVALENT", result["equivalence_reason"]
        elif status == "SURVIVED" and result.get("initial_state_is_exact_equilibrium"):
            reason += "; dato inicial de equilibrio: cobertura limitada de trayectorias"
    else:
        status, reason = "INFRA_FAIL", "dependencia auxiliar ausente o hash incorrecto"
    finished_ns = time.perf_counter_ns()
    report = {
        "schema_version": 3, "case": args.case, "scenario": args.scenario, "mutant": args.mutant,
        "status": status, "reason": reason, "operator_change": CHANGES[args.mutant],
        "started_utc": started_utc, "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "monotonic_start_ns": started_ns, "monotonic_finish_ns": finished_ns,
        "wall_seconds": (finished_ns - started_ns) / 1e9,
        "source_sha256": source_hash, "contract_sha256": contract_hash,
        "dependencies": {"run_scenario.py": SHARED_SHA},
        "machine": {"hostname": socket.gethostname(), "platform": platform.platform(), "processor": platform.processor(), "logical_cpus": os.cpu_count()},
        "parameters": parameters, "command": command, "returncode": returncode, "timeout_seconds": args.timeout,
        "baseline_valid": baseline_valid, "baseline_validation_reason": baseline_reason,
        "baseline_file_sha256": hashlib.sha256(args.baseline.read_bytes()).hexdigest() if args.baseline and args.baseline.is_file() else None,
        "result": result,
        "limitations": ["Modelos ODE estipulados, no validación experimental de física o química reales", "Equilibrio inicial puede no excitar un operador incorrecto", "ROUND_OFF_LIMITED no acredita orden cuatro", "Un fallo de infraestructura no recibe crédito de detección"],
        "artifact_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(args.output.iterdir()) if path.is_file()},
    }
    (args.output / "run.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"case": args.case, "scenario": args.scenario, "mutant": args.mutant, "status": status, "reason": reason, "output": str(args.output)}, ensure_ascii=False))
    return 2 if status == "INFRA_FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
