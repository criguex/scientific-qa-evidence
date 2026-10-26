import os
import sys
import subprocess
import multiprocessing as mp

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import colormaps

SRC = os.environ.get("RENDER_SRC", os.path.expanduser("~/Downloads/codex-2026-10-20-npz/fluid-3d/simulation_results_n64/fields.npz"))
WORK = os.environ.get("RENDER_WORK", os.path.join(os.getcwd(), ".render_work"))
OUT = os.environ.get("RENDER_OUT", os.path.join(os.getcwd(), "taylor_green_vorticidad_64.mp4"))

FPS = 30
SUB = 3
HOLD_START = 45
HOLD_END = 60
PANEL = 560
DEPTH = 220
EXT = 1.78
ELEV = np.deg2rad(24)
AZ0 = np.deg2rad(35)
W_LO, W_HI = 0.5, 14.0
S0 = 0.13
DENSITY = 7.0
BG = np.array([13, 17, 23]) / 255.0
CMAP = colormaps["inferno"]
LUT = CMAP(np.linspace(0, 1, 1024))[:, :3].astype(np.float32)
C_EULER = "#ff8a3d"
C_NS = "#4cc9f0"

_vol = None
_meta = None


def to_s(w):
    return np.log1p(np.asarray(w) / W_LO) / np.log1p(W_HI / W_LO)


def view_matrix(az, el):
    ca, sa = np.cos(az), np.sin(az)
    ce, se = np.cos(el), np.sin(el)
    rz = np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]])
    base = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    rx = np.array([[1, 0, 0], [0, ce, -se], [0, se, ce]])
    return rx @ base @ rz


def sample(flat, q, n):
    f = np.floor(q)
    t = (q - f).astype(np.float32)
    i0 = f.astype(np.int64) % n
    i1 = (i0 + 1) % n
    x0, y0, z0 = i0[:, 0], i0[:, 1], i0[:, 2]
    x1, y1, z1 = i1[:, 0], i1[:, 1], i1[:, 2]
    tx, ty, tz = t[:, 0], t[:, 1], t[:, 2]
    nn = n * n

    def g(a, b, c):
        return flat[a * nn + b * n + c]

    c00 = g(x0, y0, z0) * (1 - tx) + g(x1, y0, z0) * tx
    c10 = g(x0, y1, z0) * (1 - tx) + g(x1, y1, z0) * tx
    c01 = g(x0, y0, z1) * (1 - tx) + g(x1, y0, z1) * tx
    c11 = g(x0, y1, z1) * (1 - tx) + g(x1, y1, z1) * tx
    c0 = c00 * (1 - ty) + c10 * ty
    c1 = c01 * (1 - ty) + c11 * ty
    return c0 * (1 - tz) + c1 * tz


def render_volume(vol, az):
    n = vol.shape[0]
    flat = vol.ravel()
    v = view_matrix(az, ELEV)
    lin = np.linspace(-EXT, EXT, PANEL, dtype=np.float64)
    sx, sy = np.meshgrid(lin, lin[::-1])
    a = sx.reshape(-1, 1) * v[0] + sy.reshape(-1, 1) * v[1]
    color = np.zeros((a.shape[0], 3), np.float32)
    trans = np.ones(a.shape[0], np.float32)
    ds = 2 * EXT / DEPTH
    for sz in np.linspace(EXT, -EXT, DEPTH):
        p = a + sz * v[2]
        inside = np.all(np.abs(p) <= 1.0, axis=1) & (trans > 0.004)
        if not inside.any():
            continue
        idx = np.nonzero(inside)[0]
        q = (p[idx] + 1.0) * (n / 2.0)
        w = sample(flat, q, n)
        s = np.clip(to_s(w), 0, 1).astype(np.float32)
        tf = np.clip((s - S0) / (1 - S0), 0, 1) ** 1.3
        alpha = 1 - np.exp(-DENSITY * tf * ds)
        rgb = LUT[(s * (len(LUT) - 1)).astype(np.int64)] * 1.6
        tr = trans[idx]
        color[idx] += (tr * alpha)[:, None] * rgb
        trans[idx] = tr * (1 - alpha)
    img = color + trans[:, None] * BG
    return np.clip(img, 0, 1).reshape(PANEL, PANEL, 3)


def cube_edges(az):
    v = view_matrix(az, ELEV)
    corners = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
    cam = corners @ v.T
    edges = []
    for i in range(8):
        for j in range(i + 1, 8):
            if np.sum(np.abs(corners[i] - corners[j])) == 2:
                depth = (cam[i, 2] + cam[j, 2]) / 2
                edges.append((cam[[i, j], 0], cam[[i, j], 1], depth))
    return edges


def frame_plan(nt):
    steps = (nt - 1) * SUB + 1
    tpos = np.concatenate([np.zeros(HOLD_START), np.arange(steps) / SUB, np.full(HOLD_END, nt - 1.0)])
    total = len(tpos)
    az = AZ0 + 2 * np.pi * np.arange(total) / total
    return tpos, az


def prepare():
    os.makedirs(WORK, exist_ok=True)
    d = np.load(SRC)
    omega = d["omega_magnitude"].astype(np.float32)
    np.save(os.path.join(WORK, "omega.npy"), omega)
    flat = omega.reshape(omega.shape[0], omega.shape[1], -1)
    np.savez(
        os.path.join(WORK, "meta.npz"),
        times=d["times"],
        nus=d["viscosities"],
        enst=0.5 * (flat.astype(np.float64) ** 2).mean(axis=2),
        wmax=flat.max(axis=2),
    )


def init_worker():
    global _vol, _meta
    _vol = np.load(os.path.join(WORK, "omega.npy"), mmap_mode="r")
    m = np.load(os.path.join(WORK, "meta.npz"))
    _meta = {k: m[k] for k in m.files}


def volume_at(case, tp):
    nt = _vol.shape[1]
    i = int(np.floor(tp))
    f = tp - i
    if i >= nt - 1:
        return np.asarray(_vol[case, nt - 1])
    return (1 - f) * np.asarray(_vol[case, i]) + f * np.asarray(_vol[case, i + 1])


def interp(series, tp):
    return np.interp(tp, np.arange(len(series)), series)


def draw_panel(fig, rect, img, az, label, sub, accent):
    ax = fig.add_axes(rect)
    ax.imshow(img, extent=(-EXT, EXT, -EXT, EXT), interpolation="bilinear")
    for xs, ys, depth in cube_edges(az):
        ax.plot(xs, ys, color="#c9d1d9", lw=0.8, alpha=0.55 if depth > -0.2 else 0.18)
    ax.set_xlim(-EXT, EXT)
    ax.set_ylim(-EXT, EXT)
    ax.axis("off")
    fig.text(rect[0] + rect[2] / 2, rect[1] + rect[3] + 0.028, label, ha="center", va="bottom",
             color=accent, fontsize=21, fontweight="bold")
    fig.text(rect[0] + rect[2] / 2, rect[1] + rect[3] + 0.006, sub, ha="center", va="bottom",
             color="#8b949e", fontsize=14)


def draw_chart(fig, rect, times, series, tp, title, ylabel):
    ax = fig.add_axes(rect)
    ax.set_facecolor("#0d1117")
    t_now = interp(times, tp)
    for s, c, lab in zip(series, (C_EULER, C_NS), ("ν = 0", "ν = 0.04")):
        ax.plot(times, s, color=c, lw=1.2, alpha=0.25)
        k = int(np.floor(tp)) + 1
        ax.plot(np.append(times[:k], t_now), np.append(s[:k], interp(s, tp)), color=c, lw=2.4, label=lab)
        ax.plot([t_now], [interp(s, tp)], "o", color=c, ms=7, mec="white", mew=1.2)
    ax.axvline(t_now, color="#c9d1d9", lw=0.8, alpha=0.4)
    ax.set_xlim(times[0], times[-1])
    ax.set_title(title, color="#e6edf3", fontsize=15, loc="left", pad=8)
    ax.set_xlabel("tiempo t", color="#8b949e", fontsize=12)
    ax.set_ylabel(ylabel, color="#8b949e", fontsize=12)
    ax.tick_params(colors="#8b949e", labelsize=11)
    for sp in ax.spines.values():
        sp.set_color("#30363d")
    ax.grid(color="#21262d", lw=0.8)
    ax.legend(loc="upper left", frameon=False, labelcolor="#c9d1d9", fontsize=12)


def render_frame(args):
    k, tp, az = args
    path = os.path.join(WORK, "frames", f"f{k:05d}.png")
    if os.path.exists(path):
        return k
    times, nus, enst, wmax = _meta["times"], _meta["nus"], _meta["enst"], _meta["wmax"]
    imgs = [render_volume(volume_at(c, tp), az) for c in range(2)]
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100, facecolor="#0d1117")
    fig.text(0.04, 0.945, "Vórtice de Taylor–Green en 3D · magnitud de la vorticidad |ω|",
             color="#e6edf3", fontsize=28, fontweight="bold", va="center")
    fig.text(0.04, 0.902, "Mismo estado inicial, dos fluidos: sin viscosidad (Euler) frente a viscoso (Navier–Stokes, Re = 25)",
             color="#8b949e", fontsize=16, va="center")
    pw, ph = 0.290, 0.515
    draw_panel(fig, [0.040, 0.290, pw, ph], imgs[0], az, "ν = 0  ·  Euler", "sin viscosidad", C_EULER)
    draw_panel(fig, [0.350, 0.290, pw, ph], imgs[1], az, f"ν = {nus[1]:g}  ·  Navier–Stokes", "con viscosidad", C_NS)
    t_now = interp(times, tp)
    fig.text(0.700, 0.800, f"t = {t_now:4.2f}", color="#e6edf3", fontsize=40, fontweight="bold",
             family="DejaVu Sans Mono", va="center")
    rows = [("ν = 0", C_EULER, 0), (f"ν = {nus[1]:g}", C_NS, 1)]
    y = 0.715
    fig.text(0.700, y + 0.035, "pico |ω|", color="#8b949e", fontsize=13, va="center")
    fig.text(0.800, y + 0.035, "enstrofía", color="#8b949e", fontsize=13, va="center")
    for lab, col, c in rows:
        fig.text(0.640, y, lab, color=col, fontsize=17, fontweight="bold", va="center")
        fig.text(0.700, y, f"{interp(wmax[c], tp):6.2f}", color="#e6edf3", fontsize=19,
                 family="DejaVu Sans Mono", va="center")
        fig.text(0.800, y, f"{interp(enst[c], tp):6.3f}", color="#e6edf3", fontsize=19,
                 family="DejaVu Sans Mono", va="center")
        y -= 0.05
    cax = fig.add_axes([0.700, 0.535, 0.24, 0.022])
    ticks = np.array([0.5, 1, 2, 4, 8, 14])
    grad = np.linspace(0, 1, 512)[None, :]
    cax.imshow(grad, aspect="auto", cmap=CMAP, extent=(0, 1, 0, 1))
    cax.set_xticks(to_s(ticks))
    cax.set_xticklabels([f"{t:g}" for t in ticks])
    cax.set_yticks([])
    cax.tick_params(colors="#8b949e", labelsize=11)
    for sp in cax.spines.values():
        sp.set_color("#30363d")
    fig.text(0.700, 0.572, "|ω|  (escala logarítmica, misma en ambos)", color="#8b949e", fontsize=12, va="center")
    notes = [
        f"Malla periódica {_vol.shape[2]}³ en [0, 2π)³ · 201 instantes, t ∈ [0, 4]",
        "u₀ = (sin x cos y cos z, −cos x sin y cos z, 0)",
        "Con ν = 0 el pico depende de la malla",
        "(32³: 7.2 · 64³: 13.7): es falta de resolución,",
        "no evidencia de explosión.",
    ]
    for i, line in enumerate(notes):
        fig.text(0.640, 0.465 - i * 0.032, line, color="#8b949e", fontsize=13, va="center")
    draw_chart(fig, [0.075, 0.07, 0.36, 0.17], times, enst, tp, "Enstrofía  ½⟨|ω|²⟩", "")
    draw_chart(fig, [0.545, 0.07, 0.36, 0.17], times, wmax, tp, "Pico de vorticidad  max |ω|", "")
    fig.savefig(path, facecolor=fig.get_facecolor())
    plt.close(fig)
    return k


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    if not os.path.exists(os.path.join(WORK, "omega.npy")):
        prepare()
    os.makedirs(os.path.join(WORK, "frames"), exist_ok=True)
    nt = np.load(os.path.join(WORK, "meta.npz"))["times"].shape[0]
    tpos, az = frame_plan(nt)
    jobs = [(k, float(tpos[k]), float(az[k])) for k in range(len(tpos))]
    if only is not None:
        jobs = [jobs[int(x)] for x in only.split(",")]
    with mp.Pool(max(1, os.cpu_count() - 1), initializer=init_worker) as pool:
        for i, _ in enumerate(pool.imap_unordered(render_frame, jobs), 1):
            if i % 25 == 0 or i == len(jobs):
                print(f"{i}/{len(jobs)}", flush=True)
    if only is not None:
        return
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
        "-i", os.path.join(WORK, "frames", "f%05d.png"),
        "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", OUT,
    ], check=True)
    print(OUT)


if __name__ == "__main__":
    main()
