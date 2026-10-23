import os

for variable in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[variable] = "1"

import argparse
import csv
import datetime
import hashlib
import json
import platform
import socket
import time
from pathlib import Path

import numpy as np


AXES = (-3, -2, -1)


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class SpectralFlow:
    def __init__(self, n):
        if n < 12 or n % 2:
            raise ValueError("n debe ser par y al menos 12")
        self.n = n
        line = np.arange(n, dtype=np.float64) * (2 * np.pi / n)
        self.x, self.y, self.z = np.meshgrid(line, line, line, indexing="ij")
        waves = np.fft.fftfreq(n, d=1 / n)
        self.k = np.array(np.meshgrid(waves, waves, waves, indexing="ij"))
        self.k2 = np.sum(self.k * self.k, axis=0)
        self.inverse_k2 = np.zeros_like(self.k2)
        np.divide(1, self.k2, out=self.inverse_k2, where=self.k2 != 0)
        self.mask = np.all(np.abs(self.k) < n / 3, axis=0)

    def transform(self, values):
        return np.fft.fftn(values, axes=AXES)

    def physical(self, spectral):
        return np.fft.ifftn(spectral, axes=AXES).real

    def project(self, spectral):
        dot = np.sum(self.k * spectral, axis=0)
        return (spectral - self.k * (dot * self.inverse_k2)) * self.mask

    def curl(self, spectral):
        kx, ky, kz = self.k
        ux, uy, uz = spectral
        return self.physical(1j * np.array([
            ky * uz - kz * uy,
            kz * ux - kx * uz,
            kx * uy - ky * ux,
        ]))

    def initial(self):
        x, y, z = self.x, self.y, self.z
        return np.array([
            np.sin(x) * np.cos(y) * np.cos(z),
            -np.cos(x) * np.sin(y) * np.cos(z),
            np.zeros_like(x),
        ])

    def rhs(self, spectral, viscosity):
        spectral = self.project(spectral)
        velocity = self.physical(spectral)
        omega = self.curl(spectral)
        ux, uy, uz = velocity
        wx, wy, wz = omega
        rotational = np.array([
            uy * wz - uz * wy,
            uz * wx - ux * wz,
            ux * wy - uy * wx,
        ])
        return self.project(self.transform(rotational)) - viscosity * self.k2 * spectral

    def step(self, spectral, viscosity, dt):
        k1 = self.rhs(spectral, viscosity)
        k2 = self.rhs(spectral + 0.5 * dt * k1, viscosity)
        k3 = self.rhs(spectral + 0.5 * dt * k2, viscosity)
        k4 = self.rhs(spectral + dt * k3, viscosity)
        return self.project(spectral + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6)

    def diagnostics(self, spectral, dt):
        velocity = self.physical(spectral)
        omega = self.curl(spectral)
        magnitude = np.sqrt(np.sum(omega * omega, axis=0))
        divergence = self.physical(1j * np.sum(self.k * spectral, axis=0))
        energy = 0.5 * np.mean(np.sum(velocity * velocity, axis=0))
        enstrophy = 0.5 * np.mean(magnitude * magnitude)
        cutoff = self.n / 3
        high = np.any(np.abs(self.k) >= 0.8 * cutoff, axis=0) & self.mask
        spectral_energy = np.sum(np.abs(spectral) ** 2, axis=0)
        tail = np.sum(spectral_energy[high]) / max(np.sum(spectral_energy), 1e-300)
        return {
            "energy": float(energy),
            "enstrophy": float(enstrophy),
            "omega_max": float(np.max(magnitude)),
            "divergence_linf": float(np.max(np.abs(divergence))),
            "cfl": float(dt * np.max(np.sum(np.abs(velocity), axis=0)) / (2 * np.pi / self.n)),
            "spectral_tail_fraction": float(tail),
        }, magnitude


def integrate(flow, initial, viscosity, dt, end):
    steps = round(end / dt)
    if abs(steps * dt - end) > 1e-12:
        raise ValueError("T debe ser un múltiplo entero de dt")
    spectral = flow.project(flow.transform(initial))
    for _ in range(steps):
        spectral = flow.step(spectral, viscosity, dt)
    return flow.physical(spectral)


def acceptable(divergence, euler_drift, ns_increase):
    return divergence < 1e-10 and euler_drift < 1e-5 and ns_increase <= 1e-12


def self_test():
    flow = SpectralFlow(16)
    results = {}

    def check(name, value, threshold):
        passed = bool(np.isfinite(value) and value < threshold)
        results[name] = {"value": float(value), "threshold_exclusive": threshold, "passed": passed}

    initial = flow.initial()
    spectral = flow.project(flow.transform(initial))
    initial_metrics, _ = flow.diagnostics(spectral, 0.01)
    check("taylor_green_energy_initial", abs(initial_metrics["energy"] - 0.125), 1e-13)
    check("taylor_green_enstrophy_initial", abs(initial_metrics["enstrophy"] - 0.375), 1e-13)
    exact_tg_rhs = np.array([
        -0.25 * np.sin(flow.x) * np.cos(flow.x) * np.cos(2 * flow.z),
        -0.25 * np.sin(flow.y) * np.cos(flow.y) * np.cos(2 * flow.z),
        0.125 * (np.cos(2 * flow.x) + np.cos(2 * flow.y)) * np.sin(2 * flow.z),
    ])
    for label, viscosity in (("euler", 0.0), ("ns", 0.04)):
        expected = exact_tg_rhs - 3 * viscosity * initial
        check(
            f"taylor_green_closed_form_rhs_{label}",
            np.max(np.abs(flow.physical(flow.rhs(spectral, viscosity)) - expected)),
            1e-12,
        )
    gradient = np.array([-np.sin(flow.x), np.zeros_like(flow.x), np.zeros_like(flow.x)])
    check("leray_rejects_gradient", np.max(np.abs(flow.physical(flow.project(flow.transform(gradient))))), 1e-12)
    shear = np.array([np.sin(flow.y), np.zeros_like(flow.x), np.zeros_like(flow.x)])
    shear_hat = flow.transform(shear)
    expected_curl = np.array([np.zeros_like(flow.x), np.zeros_like(flow.x), -np.cos(flow.y)])
    check("curl_matches_analytic_shear", np.max(np.abs(flow.curl(shear_hat) - expected_curl)), 1e-12)
    check("shear_euler_rhs_zero", np.max(np.abs(flow.rhs(shear_hat, 0))), 1e-10)
    check("shear_viscous_rhs", np.max(np.abs(flow.physical(flow.rhs(shear_hat, 0.04)) + 0.04 * shear)), 1e-12)
    for label, viscosity in (("euler", 0.0), ("ns", 0.04)):
        actual = integrate(flow, shear, viscosity, 0.02, 1.0)
        exact = shear * np.exp(-viscosity)
        check(f"analytic_shear_{label}_t1", np.max(np.abs(actual - exact)), 1e-10)

    velocity = flow.physical(spectral)
    advective = np.zeros_like(velocity)
    for axis in range(3):
        derivative = flow.physical(1j * flow.k[axis] * spectral)
        advective -= velocity[axis] * derivative
    convective_rhs = flow.project(flow.transform(advective))
    check("rotational_vs_convective_rhs", np.max(np.abs(flow.rhs(spectral, 0) - convective_rhs)), 1e-10)
    negative = {
        "reject_large_divergence": not acceptable(1e-4, 0, 0),
        "reject_euler_energy_drift": not acceptable(0, 1e-3, 0),
        "reject_ns_energy_growth": not acceptable(0, 0, 1e-3),
        "reject_wrong_viscous_sign": bool(np.max(np.abs(shear * np.exp(0.04) - shear * np.exp(-0.04))) > 1e-3),
        "reject_reversed_nonlinearity": bool(np.max(np.abs(-exact_tg_rhs - exact_tg_rhs)) > 1e-3),
    }
    for name, passed in negative.items():
        results[name] = {"passed": bool(passed), "kind": "negative_control"}
    convergence = {}
    for label, viscosity in (("euler", 0.0), ("ns", 0.04)):
        values = [integrate(flow, initial, viscosity, dt, 1.0) for dt in (0.04, 0.02, 0.01)]
        differences = [
            float(np.sqrt(np.mean((values[0] - values[1]) ** 2))),
            float(np.sqrt(np.mean((values[1] - values[2]) ** 2))),
        ]
        ratio = differences[0] / differences[1] if differences[1] > 0 else None
        resolved = differences[1] > 1e-12
        passed = bool(resolved and ratio is not None and ratio >= 8)
        convergence[label] = {
            "n": 16, "T": 1.0, "dt": [0.04, 0.02, 0.01],
            "successive_rms_differences": differences,
            "ratio": ratio, "above_noise_floor": resolved,
            "expected_ratio_rk4": 16, "minimum_ratio": 8, "passed": passed,
            "scope": "refinamiento temporal a malla fija; no convergencia espacial",
        }
        results[f"time_refinement_{label}"] = convergence[label]
    return {
        "tests": results,
        "all_tests_passed": all(item["passed"] for item in results.values()),
    }


def simulate(output, n, dt, end, controls):
    started = utc()
    clock_start = time.perf_counter()
    flow = SpectralFlow(n)
    steps = round(end / dt)
    if abs(steps * dt - end) > 1e-12 or steps < 1:
        raise ValueError("T debe ser positivo y múltiplo de dt")
    interval = round(0.02 / dt)
    if interval < 1 or abs(interval * dt - 0.02) > 1e-12:
        raise ValueError("dt debe dividir el intervalo de guardado 0.02")
    initial = flow.initial()
    states = [flow.project(flow.transform(initial)) for _ in range(2)]
    viscosities = (0.0, 0.04)
    labels = ("Euler", "NavierStokes")
    snapshots = [[], []]
    rows = []
    times = []
    for step in range(steps + 1):
        t = step * dt
        if step % interval == 0 or step == steps:
            times.append(t)
            for index, (state, label) in enumerate(zip(states, labels)):
                metric, magnitude = flow.diagnostics(state, dt)
                if not all(np.isfinite(value) for value in metric.values()):
                    raise FloatingPointError(f"métrica no finita: {label}, t={t}")
                rows.append({"t": t, "model": label, **metric})
                snapshots[index].append(magnitude.astype(np.float32))
            if step % max(1, steps // 10) == 0:
                print(f"simulation step={step}/{steps} t={t:.2f}", flush=True)
        if step < steps:
            states = [flow.step(state, viscosity, dt) for state, viscosity in zip(states, viscosities)]
    with (output / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    np.savez_compressed(
        output / "fields.npz",
        times=np.array(times), omega_magnitude=np.array(snapshots),
        initial_velocity=initial,
        final_velocity=np.array([flow.physical(state) for state in states]),
        viscosities=np.array(viscosities), n=np.array(n),
    )
    euler = [row for row in rows if row["model"] == "Euler"]
    ns = [row for row in rows if row["model"] == "NavierStokes"]
    divergence = max(row["divergence_linf"] for row in rows)
    euler_drift = max(abs(row["energy"] / euler[0]["energy"] - 1) for row in euler)
    ns_increase = float(max(np.diff([row["energy"] for row in ns])))
    all_passed = bool(controls["all_tests_passed"] and acceptable(divergence, euler_drift, ns_increase))
    summary = {
        "scope": "SIMULACION NUMERICA ILUSTRATIVA; NO PRUEBA DE EXPLOSION NI DE LOS TEOREMAS LEAN",
        "started_utc": started, "finished_utc": utc(),
        "wall_seconds": time.perf_counter() - clock_start,
        "machine": {"hostname": socket.gethostname(), "platform": platform.platform()},
        "versions": {"python": platform.python_version(), "numpy": np.__version__},
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parameters": {
            "n": n, "dt": dt, "T": end, "save_dt": 0.02,
            "viscosities": list(viscosities), "forcing": 0,
            "domain": "periodic [0, 2*pi]^3",
            "initial": "(sin(x)cos(y)cos(z), -cos(x)sin(y)cos(z), 0)",
            "method": "Fourier rotational pseudospectral; Leray; RK4; strict 2/3 mask each stage",
            "compute_dtype": "float64/complex128",
            "visualization_storage_dtype": "float32 vorticity magnitude; float64 endpoint velocity",
            "threads_requested": 1, "compute_device": "CPU",
        },
        "controls": controls,
        "diagnostics": {
            "divergence_linf_max": divergence,
            "euler_energy_relative_drift_max": euler_drift,
            "ns_energy_increase_max": ns_increase,
            "cfl_max": max(row["cfl"] for row in rows),
            "euler_spectral_tail_fraction_max": max(row["spectral_tail_fraction"] for row in euler),
            "ns_spectral_tail_fraction_max": max(row["spectral_tail_fraction"] for row in ns),
            "euler_initial": euler[0], "euler_final": euler[-1],
            "ns_initial": ns[0], "ns_final": ns[-1],
            "snapshot_count_per_model": len(times),
        },
        "all_numerical_checks_passed": all_passed,
        "limits": [
            "No convergencia espacial medida.",
            f"Malla {n}^3 ilustrativa; las escalas cercanas al corte espectral pueden no resolverse.",
            "Dominio periodico y dato Taylor-Green: diferentes de datos compactos en R3.",
            "Tiempo finito muestreado no prueba regularidad global ni singularidad.",
        ],
    }
    for name in ("fields.npz", "metrics.csv"):
        summary.setdefault("artifact_sha256", {})[name] = hashlib.sha256((output / name).read_bytes()).hexdigest()
    (output / "simulation_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"all_numerical_checks_passed": all_passed, "diagnostics": summary["diagnostics"]}, indent=2), flush=True)
    return 0 if all_passed else 1


def main():
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--self-test", action="store_true")
    action.add_argument("--simulate", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--dt", type=float, default=0.01)
    parser.add_argument("--T", type=float, default=4.0)
    args = parser.parse_args()
    if args.dt <= 0 or args.T <= 0:
        parser.error("dt y T deben ser positivos")
    args.output.mkdir(parents=True, exist_ok=True)
    controls = self_test()
    (args.output / "numerical_controls.json").write_text(
        json.dumps(controls, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({"self_tests_passed": controls["all_tests_passed"]}), flush=True)
    if not controls["all_tests_passed"]:
        return 1
    if args.self_test:
        return 0
    return simulate(args.output, args.n, args.dt, args.T, controls)


if __name__ == "__main__":
    raise SystemExit(main())
