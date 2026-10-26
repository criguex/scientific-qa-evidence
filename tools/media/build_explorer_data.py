import glob
import hashlib
import json
import os
import re

import numpy as np
from PIL import Image

ROOT = os.environ.get("NPZ_ROOT", os.path.expanduser("~/Downloads/codex-2026-10-20-npz"))
OUT = os.environ.get("EXPLORER_OUT", os.path.join(os.getcwd(), "explorer-out"))
W_LO, W_HI = 0.5, 14.0
STRIDE = 2


def sig(a, n=6):
    a = np.asarray(a, dtype=np.float64)
    return [float(f"{v:.{n}g}") for v in a.ravel()] if a.ndim else float(f"{a:.{n}g}")


def digest(d):
    return hashlib.md5(b"".join(d[k].tobytes() for k in sorted(d.files))).hexdigest()


def to_byte(w):
    s = np.log1p(np.asarray(w, np.float64) / W_LO) / np.log1p(W_HI / W_LO)
    return np.clip(np.round(s * 255), 0, 255).astype(np.uint8)


def fluid():
    base = os.path.join(ROOT, "fluid-3d")
    runs = {
        "n32_dt001": "fluid_temporal_v2/remote/n32-dt001-T4/fields.npz",
        "n32_dt0005": "fluid_temporal_v2/remote/n32-dt0005-T4/fields.npz",
        "n64": "simulation_results_n64/fields.npz",
    }
    out = {"runs": {}}
    os.makedirs(os.path.join(OUT, "slices"), exist_ok=True)
    for key, rel in runs.items():
        d = np.load(os.path.join(base, rel))
        w = d["omega_magnitude"]
        flat = w.reshape(w.shape[0], w.shape[1], -1).astype(np.float64)
        out["times"] = sig(d["times"], 4)
        out["nus"] = sig(d["viscosities"])
        out["runs"][key] = {
            "n": int(d["n"]),
            "enst": [sig(v) for v in 0.5 * (flat ** 2).mean(axis=2)],
            "wmax": [sig(v) for v in flat.max(axis=2)],
        }
        if key == "n32_dt0005":
            continue
        n = int(d["n"])
        tag = "n32" if n == 32 else "n64"
        views = {
            "z0": w[:, ::STRIDE, :, :, 0],
            "zpi2": w[:, ::STRIDE, :, :, n // 4],
            "mip": w[:, ::STRIDE].max(axis=4),
        }
        for view, arr in views.items():
            for c in range(arr.shape[0]):
                frames = to_byte(arr[c]).transpose(0, 2, 1)[:, ::-1, :]
                sheet = frames.reshape(-1, n)
                Image.fromarray(sheet, mode="L").save(
                    os.path.join(OUT, "slices", f"{tag}_{view}_nu{c}.png"), optimize=True)
    legacy = np.load(os.path.join(base, "simulation_results/fields.npz"))
    dt001 = np.load(os.path.join(base, runs["n32_dt001"]))
    out["legacy_equals_dt001"] = digest(legacy) == digest(dt001)
    a = np.load(os.path.join(base, runs["n32_dt001"]))["omega_magnitude"].astype(np.float64)
    b = np.load(os.path.join(base, runs["n32_dt0005"]))["omega_magnitude"].astype(np.float64)
    out["dt_max_diff"] = [float(np.abs(a[c] - b[c]).max()) for c in range(2)]
    out["slice_times"] = sig(d["times"][::STRIDE], 4)
    return out


def pde():
    base = os.path.join(ROOT, "scenarios-v2", "scenarios_v2")
    cases = []
    for f in sorted(glob.glob(os.path.join(base, "guerra", "*", "fields.npz"))):
        name = f.split(os.sep)[-2]
        eq, variant = name.split("_", 1)
        d = np.load(f)
        twin = f.replace(os.sep + "guerra" + os.sep, os.sep + "war" + os.sep)
        identical = os.path.exists(twin) and digest(d) == digest(np.load(twin))
        num, ex = d["n64"].astype(np.float64), d["n64_exact"].astype(np.float64)
        err = np.abs(num - ex)
        res = {}
        for k in ("n32", "n64_half", "n64", "n128"):
            if k in d.files:
                res[k] = float(np.abs(d[k].astype(np.float64) - d[k + "_exact"]).max())
        cases.append({
            "eq": eq,
            "variant": variant,
            "identical_war": bool(identical),
            "x": sig(d["n64_x"], 5),
            "num": [sig(r) for r in num],
            "exact": [sig(r) for r in ex],
            "err": [sig(r, 3) for r in err],
            "err_max": float(err.max()),
            "res": res,
        })
    return cases


def ode():
    base = os.path.join(ROOT, "ode-v3", "ode_v3")
    cases = []
    pat = re.compile(r"((?:osc|rxn)\d\d)[/_](.+)$")
    seen = {}
    for f in sorted(glob.glob(os.path.join(base, "**", "fields.npz"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(f), base)
        group = rel.split(os.sep)[0]
        leaf = rel.split(os.sep, 1)[1]
        m = pat.search(leaf.replace(os.sep, "/"))
        model, variant = m.group(1), m.group(2)
        check = re.match(r".*check_(\d\d)_", leaf)
        d = np.load(f)
        nres = sum(1 for k in d.files if k.startswith("times_"))
        errs = [float(np.abs(d[f"states_{i}"] - d[f"oracle_{i}"]).max()) for i in range(nres)]
        k = nres - 1
        t, s, o = d[f"times_{k}"], d[f"states_{k}"], d[f"oracle_{k}"]
        step = max(1, (len(t) - 1) // 160)
        e = np.abs(s - o).max(axis=1)
        h = digest(d)
        cases.append({
            "group": group,
            "path": rel.replace(os.sep, "/"),
            "model": model,
            "variant": variant,
            "check": check.group(1) if check else None,
            "steps": [int(len(d[f"times_{i}"]) - 1) for i in range(nres)],
            "errs": errs,
            "t": sig(t[::step], 4),
            "num": [sig(s[::step, j]) for j in range(s.shape[1])],
            "oracle": [sig(o[::step, j]) for j in range(o.shape[1])],
            "err": sig(e[::step], 3),
            "hash": h[:10],
        })
        seen.setdefault((model, variant), []).append(group)
    return cases


def main():
    data = {"fluid": fluid(), "pde": pde(), "ode": ode()}
    with open(os.path.join(OUT, "data.json"), "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
    print(len(data["pde"]), "pde", len(data["ode"]), "ode",
          "legacy==dt001", data["fluid"]["legacy_equals_dt001"], "dtdiff", data["fluid"]["dt_max_diff"])


if __name__ == "__main__":
    main()
