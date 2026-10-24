#!/usr/bin/env python3
"""Un solo comando para repetir las comprobaciones del repositorio en cualquier computador.

Uso: python verificar.py   (en Mac o Linux puede ser python3 verificar.py)
Necesita Python 3.9 o más reciente y nada más. Funciona en Windows, macOS y Linux.
"""

import datetime
import hashlib
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SUMS = ROOT / "evidence" / "SHA256SUMS.txt"
REPORT = ROOT / "mi_resultado.txt"
FORM = "https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_sums():
    bad, total = [], 0
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line[:64], line[64:].lstrip(" *")
        total += 1
        path = ROOT / rel
        if not path.is_file():
            bad.append(f"falta: {rel}")
        elif sha256(path) != expected:
            bad.append(f"distinto: {rel}")
    detail = f"{total} archivos revisados"
    if bad:
        hint = ""
        if any(b.startswith("distinto") for b in bad) and os.name == "nt":
            hint = ("\nEn Windows esto suele pasar cuando git cambia los finales de línea. "
                    "Descarga el ZIP desde GitHub o clona con: git clone -c core.autocrlf=false ...")
        return False, detail + f", {len(bad)} con problemas:\n" + "\n".join(bad[:20]) + hint
    return True, detail


def run(argv, cwd):
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, *argv], cwd=ROOT / cwd, env=env, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", timeout=900)
    out = (p.stdout + p.stderr).strip().splitlines()
    return p.returncode == 0, "\n".join(out[-15:])


STEPS = [
    ("Archivos intactos (SHA-256)", check_sums),
    ("Corridas numéricas guardadas, iguales entre Mac y Linux", lambda: run(["evidence/verify_numerical.py"], ".")),
    ("Volver a correr las 84 variantes numéricas", lambda: run(["-m", "unittest", "test_runner"], "evidence/numerical/source")),
    ("README, CLAIMS y registros dicen lo mismo", lambda: run(["evidence/test_consistency.py"], ".")),
    ("Recibos de los controles Mathlib", lambda: run(["verify.py"], "experiments/mathlib-controls")),
    ("Comprobación de recibos en los paquetes publicados", lambda: run(["-m", "unittest", "test_results"], "experiments/receipt-check")),
]


def fingerprint(version, results):
    text = version + "|" + "|".join(f"{name}={'OK' if ok else 'FALLA'}" for name, ok, _, _ in results)
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12].upper()
    return f"{h[:4]}-{h[4:8]}-{h[8:]}"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.version_info < (3, 9):
        print("Se necesita Python 3.9 o más reciente. Tienes", platform.python_version())
        return 2
    if not SUMS.is_file():
        print("No encuentro evidence/SHA256SUMS.txt. Ejecuta el comando dentro de la carpeta del repositorio.")
        return 2
    version = sha256(SUMS)[:12]
    print()
    print("Verificación de scientific-qa-evidence")
    print(f"Versión de los datos: {version}   Sistema: {platform.system()} {platform.machine()}   Python {platform.python_version()}")
    print()
    results = []
    for i, (name, fn) in enumerate(STEPS, 1):
        print(f"  {i}/{len(STEPS)}  {name} ...", end="", flush=True)
        start = time.time()
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        secs = time.time() - start
        results.append((name, ok, secs, detail))
        print(f"\r  {i}/{len(STEPS)}  [{'OK' if ok else 'FALLA'}]  {name}  ({secs:.1f} s)")
        if not ok:
            for line in detail.splitlines():
                print("            " + line)
    passed = sum(ok for _, ok, _, _ in results)
    code = fingerprint(version, results)
    print()
    if passed == len(STEPS):
        print(f"Resultado: las {len(STEPS)} comprobaciones salieron OK en tu computador.")
    else:
        print(f"Resultado: {len(STEPS) - passed} de {len(STEPS)} comprobaciones FALLARON. Ese dato también es valioso: repórtalo.")
    print(f"Tu huella: {code}")
    print("Si otra persona con la misma versión obtiene la misma huella, a los dos les dio exactamente lo mismo.")
    lines = [
        "scientific-qa-evidence · verificar.py",
        f"fecha (UTC): {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}",
        f"sistema: {platform.platform()} · {platform.machine()}",
        f"python: {platform.python_version()} ({platform.python_implementation()})",
        f"versión de los datos: {version}",
        f"huella: {code}",
        "",
    ]
    for name, ok, secs, detail in results:
        lines.append(f"[{'OK' if ok else 'FALLA'}] {name} ({secs:.1f} s)")
        if not ok:
            lines += ["    " + d for d in detail.splitlines()]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print()
    print(f"Guardé el detalle en {REPORT.name}. Para contarnos tu resultado (igual o distinto):")
    print(f"  {FORM}")
    print()
    return 0 if passed == len(STEPS) else 1


if __name__ == "__main__":
    sys.exit(main())
