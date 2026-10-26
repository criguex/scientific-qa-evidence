import json
import multiprocessing as mp
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

EVID = os.environ.get("LEAN_EVIDENCE", os.path.expanduser("~/lean-evidence"))
WORK = os.environ.get("RENDER_WORK", os.path.join(os.getcwd(), ".frames_lean"))
OUT = os.environ.get("RENDER_OUT", os.path.join(os.getcwd(), "reproduccion_lean_609.mp4"))

FPS = 30
INTRO = 60
BUILD = 450
PAUSE = 60
BRIDGES = 150
FINAL = 240
BG = "#0d1117"
INK = "#e6edf3"
MUTED = "#8b949e"
DIM = "#4b5563"
OK = "#3fb950"
WARN = "#d29922"
ACC = "#4cc9f0"
PANEL = "#131820"
LINE = "#262e39"
MONO = "DejaVu Sans Mono"
COL = timedelta(hours=-5)

PAT = re.compile(r"Built (NavierStokes\.\S+) \((?:(\d+)m\s*)?([\d.]+)(ms|s)\)")


def utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def parse(path):
    mods = []
    for line in open(path, encoding="utf-8"):
        m = PAT.search(line)
        if m:
            sec = float(m.group(3)) / (1000 if m.group(4) == "ms" else 1) + 60 * int(m.group(2) or 0)
            mods.append((m.group(1).replace("NavierStokes.", ""), sec))
    return mods


def timeline(mods, start, end):
    total = sum(s for _, s in mods)
    acc, out = 0.0, []
    for name, s in mods:
        acc += s
        out.append((name, s, start + (end - start) * (acc / total)))
    return out


def load():
    seg1 = timeline(parse(os.path.join(EVID, "logs/20g_openai_target_serial.stdout.log")),
                    utc("2026-10-23T20:55:16Z"), utc("2026-10-23T21:15:03Z"))
    seg2 = timeline(parse(os.path.join(EVID, "logs/22h_openai_target_serial.stdout.log")),
                    utc("2026-10-23T21:19:24Z"), utc("2026-10-23T21:53:04Z"))
    summ = json.load(open(os.path.join(EVID, "receipts/25-final-verification-summary.json")))
    stages = sorted(summ["results"], key=lambda r: r["finished_utc"])
    stages = [r for r in stages if re.match(r"23h_[0-9a-f]{7}_", r["stage"])]
    return seg1, seg2, stages, summ


def hhmm(t):
    return (t + COL).strftime("%H:%M:%S")


def base_fig():
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor=BG)
    fig.text(0.04, 0.935, "Las demostraciones de OpenAI, compiladas y verificadas otra vez",
             color=INK, fontsize=30, fontweight="bold", va="center")
    fig.text(0.04, 0.885, "Reproducción en un contenedor Linux en la nube, ejecutada por un asistente de IA · 23 de octubre de 2026",
             color=MUTED, fontsize=17, va="center")
    return fig


def terminal(fig, lines, title):
    ax = fig.add_axes([0.04, 0.12, 0.50, 0.70])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.015",
                                facecolor=PANEL, edgecolor=LINE, lw=1.2))
    ax.text(0.03, 0.955, title, color=MUTED, fontsize=13, family=MONO, va="center")
    n = len(lines)
    for i, (txt, color) in enumerate(lines):
        y = 0.89 - i * (0.84 / 15)
        alpha = 0.35 + 0.65 * (i + 1) / n if n else 1
        ax.text(0.03, y, txt, color=color, fontsize=16, family=MONO, va="center", alpha=alpha)


def build_frame(k, seg1, seg2):
    allm = seg1 + seg2
    n1 = len(seg1)
    if k < BUILD // 2:
        done = round(n1 * (k + 1) / (BUILD // 2))
        paused = False
    elif k < BUILD // 2 + PAUSE:
        done, paused = n1, True
    else:
        kk = k - BUILD // 2 - PAUSE
        done = n1 + round(len(seg2) * (kk + 1) / (BUILD - BUILD // 2))
        paused = False
    done = max(1, min(done, len(allm)))
    fig = base_fig()
    lines = []
    for i in range(max(0, done - (13 if paused else 14)), done):
        name, s, _ = allm[i]
        lines.append((f"✔ {i + 1:3d}/609  {name[:34]:<34} {s:5.1f} s", OK if i == done - 1 else INK))
    if paused:
        lines.append(("■ seguimiento perdido · 281 piezas guardadas", WARN))
    terminal(fig, lines, "lake build  ·  registro de compilación (resumido)")
    x0 = 0.60
    fig.text(x0, 0.76, "piezas verificadas", color=MUTED, fontsize=18, va="center")
    fig.text(x0, 0.665, f"{done}", color=INK, fontsize=96, fontweight="bold", va="center", family=MONO)
    fig.text(x0 + 0.155, 0.645, "/ 609", color=MUTED, fontsize=40, va="center", family=MONO)
    bar = fig.add_axes([x0, 0.555, 0.34, 0.025])
    bar.set_xlim(0, 609)
    bar.set_ylim(0, 1)
    bar.axis("off")
    bar.add_patch(FancyBboxPatch((0, 0), 609, 1, boxstyle="round,pad=0,rounding_size=0.4", facecolor=LINE, lw=0))
    bar.add_patch(FancyBboxPatch((0, 0), done, 1, boxstyle="round,pad=0,rounding_size=0.4",
                                 facecolor=WARN if paused else ACC, lw=0))
    t = allm[done - 1][2]
    fig.text(x0, 0.49, f"hora en Colombia  {hhmm(t)}", color=INK, fontsize=20, family=MONO, va="center")
    notes = [
        "Cada pieza es un archivo de la demostración.",
        "Lean la compila y comprueba cada paso lógico;",
        "si un paso fallara, la compilación se detiene.",
    ]
    if paused:
        notes = [
            "La sesión perdió el seguimiento a las 16:15.",
            "No se borró nada: se guardaron las 281 piezas,",
            "se verificó la copia y se reanudó a las 16:19.",
        ]
    for i, s in enumerate(notes):
        fig.text(x0, 0.40 - i * 0.05, s, color=WARN if paused else MUTED, fontsize=19, va="center")
    fig.text(0.04, 0.06, "Lean v4.34.0-rc2 · OpenAI NavierStokesAndEuler @ f9e8bc5 · un solo proceso · caché oficial de Mathlib",
             color=DIM, fontsize=13, va="center")
    return fig


def bridges_frame(k, seg2, stages):
    fig = base_fig()
    shown = min(len(stages), 1 + k * len(stages) // (BRIDGES - 30))
    lines = [(f"✔ 609/609  ComparatorSolution  código de salida 0", OK), ("", INK)]
    names = {"ClayLiteral": "enunciado oficial de Clay", "Bridges": "puente OpenAI → Clay", "Audit": "auditoría de axiomas"}
    for r in stages[:shown]:
        _, ver, step = r["stage"].split("_", 2)
        lines.append((f"✔ {ver}  {names.get(step, step):<26} código {r['exit_code']}", OK))
    terminal(fig, lines, "segunda parte  ·  conexión con el enunciado oficial")
    x0 = 0.60
    fig.text(x0, 0.76, "pasos adicionales", color=MUTED, fontsize=18, va="center")
    fig.text(x0, 0.665, f"{shown}", color=INK, fontsize=96, fontweight="bold", va="center", family=MONO)
    fig.text(x0 + 0.075, 0.645, f"/ {len(stages)}", color=MUTED, fontsize=40, va="center", family=MONO)
    for i, s in enumerate([
        "Tres versiones fijas de mis archivos: el enunciado",
        "del Instituto Clay escrito palabra por palabra,",
        "y el puente que lo conecta con OpenAI.",
    ]):
        fig.text(x0, 0.52 - i * 0.05, s, color=MUTED, fontsize=19, va="center")
    fig.text(x0, 0.36, f"último paso  {hhmm(utc(stages[min(shown, len(stages)) - 1]['finished_utc']))}",
             color=INK, fontsize=20, family=MONO, va="center")
    fig.text(0.04, 0.06, "Cada paso deja un recibo con comando, hashes de entrada y salida, y código de salida",
             color=DIM, fontsize=13, va="center")
    return fig


def final_frame(k):
    fig = base_fig()
    rows = [
        ("609 / 609", "piezas de la demostración compiladas y verificadas"),
        ("código 0", "la compilación terminó sin ningún error"),
        ("9 / 9", "pasos de conexión con el enunciado oficial"),
        ("3 axiomas", "los estándar de Lean; sin atajos «sorry»"),
    ]
    for i, (a, b) in enumerate(rows):
        y = 0.74 - i * 0.095
        fig.text(0.06, y, a, color=OK, fontsize=34, fontweight="bold", family=MONO, va="center")
        fig.text(0.30, y, b, color=INK, fontsize=22, va="center")
    if k >= 45:
        fig.text(0.06, 0.33, "Lo que esto NO es", color=WARN, fontsize=20, fontweight="bold", va="center")
        fig.text(0.06, 0.28, "No es revisión humana independiente, ni certificación, ni la solución del problema del milenio.",
                 color=MUTED, fontsize=18, va="center")
        fig.text(0.06, 0.24, "La matemática es de OpenAI. La versión clásica del problema, sin fuerza externa, sigue abierta.",
                 color=MUTED, fontsize=18, va="center")
    if k >= 105:
        fig.text(0.06, 0.15, "Falta lo más importante: que otras personas lo repitan en sus computadores.",
                 color=ACC, fontsize=22, fontweight="bold", va="center")
        fig.text(0.06, 0.10, "github.com/criguex/scientific-qa-evidence", color=INK, fontsize=22, family=MONO, va="center")
    return fig


_data = None


def init():
    global _data
    _data = load()


def render(k):
    path = os.path.join(WORK, f"f{k:05d}.png")
    seg1, seg2, stages, _ = _data
    if k < INTRO:
        fig = build_frame(0, seg1, seg2) if k >= 30 else base_fig()
        if k < 30:
            fig.text(0.04, 0.55, "¿Se puede repetir una demostración matemática como se repite una prueba de software?",
                     color=INK, fontsize=26, va="center")
            fig.text(0.04, 0.48, "Lo intenté con las demostraciones de OpenAI sobre Navier–Stokes.", color=MUTED, fontsize=22, va="center")
    elif k < INTRO + BUILD + PAUSE:
        fig = build_frame(k - INTRO, seg1, seg2)
    elif k < INTRO + BUILD + PAUSE + BRIDGES:
        fig = bridges_frame(k - INTRO - BUILD - PAUSE, seg2, stages)
    else:
        fig = final_frame(k - INTRO - BUILD - PAUSE - BRIDGES)
    fig.savefig(path, facecolor=BG)
    plt.close(fig)
    return k


def main():
    seg1, seg2, stages, summ = load()
    assert len(seg1) + len(seg2) == summ["base_modules_completed"] == 609, (len(seg1), len(seg2))
    assert summ["base_exit_code"] == 0 and all(r["exit_code"] == 0 for r in stages) and len(stages) == 9
    os.makedirs(WORK, exist_ok=True)
    total = INTRO + BUILD + PAUSE + BRIDGES + FINAL
    only = [int(x) for x in sys.argv[1].split(",")] if len(sys.argv) > 1 else range(total)
    with mp.Pool(max(1, os.cpu_count() - 1), initializer=init) as pool:
        list(pool.imap_unordered(render, only))
    if len(sys.argv) > 1:
        return
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(WORK, "f%05d.png"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT],
                   check=True)
    print(OUT, total / FPS, "s")


if __name__ == "__main__":
    main()
