> English translation of [README.md](README.md). If they differ, the original prevails.

# How I generated the videos and the explorer

Here I keep the three scripts I used to make the page's visual material, so that anyone can regenerate it. None of them touches the evidence or changes the `verificar.py` fingerprint. I wrote them with help from AI assistants, under my direction.

They need Python 3.9+, numpy, matplotlib and Pillow; the videos also need `ffmpeg`.

## The input data

- **NPZ arrays from the October 20 runs:** `codex-2026-10-20-npz.tar`, attached to [release v1.3.3](https://github.com/criguex/scientific-qa-evidence/releases/tag/v1.3.3). Unzip it; you get the `codex-2026-10-20-npz/` folder.
- **Evidence from the October 23 Lean rebuild:** unzip `evidence/lean-cloud-2026-10-23/evidencia_Lean_completa_20261023.zip` into any folder.

## The scripts

| Script | What it generates | How to run it |
|---|---|---|
| `render_fluid_video.py` | 3D video of Taylor–Green vorticity, without viscosity versus with viscosity (`site/media/taylor_green_vorticidad_64.mp4` and `_32.mp4`) | `RENDER_SRC=.../codex-2026-10-20-npz/fluid-3d/simulation_results_n64/fields.npz python3 render_fluid_video.py` (for 32³, use `simulation_results/fields.npz`). Takes about 10 minutes. |
| `build_explorer_data.py` | `data.json` and the `slices/*.png` cuts for the explorer (`site/fluido/`) | `NPZ_ROOT=.../codex-2026-10-20-npz EXPLORER_OUT=output python3 build_explorer_data.py` |
| `render_lean_video.py` | Video of the Lean rebuild, 609 of 609 pieces (`site/media/reproduccion_lean_609.mp4`) | `LEAN_EVIDENCE=.../zip-folder python3 render_lean_video.py` |

The videos are saved in the folder from which you run the command; `RENDER_OUT` changes the file name. On October 26 I checked that `build_explorer_data.py` produces a `data.json` identical, byte for byte, to the one published in `site/fluido/`.

The videos are illustrative. The simulation without viscosity shows a lack of resolution, not a blow-up: the vorticity peak goes from 7.2 at 32³ to 13.7 at 64³.
