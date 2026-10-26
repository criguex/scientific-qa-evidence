# Cómo generé los videos y el explorador

Guardo aquí los tres scripts con los que hice el material visual de la página, para que cualquiera pueda volver a generarlo. Ninguno toca la evidencia ni cambia la huella de `verificar.py`. Los escribí con ayuda de asistentes de IA, bajo mi dirección.

Necesitan Python 3.9+, numpy, matplotlib y Pillow; los videos, además, `ffmpeg`.

## Los datos de entrada

- **Arrays NPZ de las corridas del 20 de octubre:** `codex-2026-10-20-npz.tar`, adjunto a la [release v1.3.3](https://github.com/criguex/scientific-qa-evidence/releases/tag/v1.3.3). Descomprímelo; queda la carpeta `codex-2026-10-20-npz/`.
- **Evidencia de la recompilación de Lean del 23 de octubre:** descomprime `evidence/lean-cloud-2026-10-23/evidencia_Lean_completa_20261023.zip` en cualquier carpeta.

## Los scripts

| Script | Qué genera | Cómo correrlo |
|---|---|---|
| `render_fluid_video.py` | Video 3D de la vorticidad de Taylor–Green, sin viscosidad frente a con viscosidad (`site/media/taylor_green_vorticidad_64.mp4` y `_32.mp4`) | `RENDER_SRC=.../codex-2026-10-20-npz/fluid-3d/simulation_results_n64/fields.npz python3 render_fluid_video.py` (para 32³, usa `simulation_results/fields.npz`). Tarda unos 10 minutos. |
| `build_explorer_data.py` | `data.json` y los cortes `slices/*.png` del explorador (`site/fluido/`) | `NPZ_ROOT=.../codex-2026-10-20-npz EXPLORER_OUT=salida python3 build_explorer_data.py` |
| `render_lean_video.py` | Video de la recompilación de Lean, 609 de 609 piezas (`site/media/reproduccion_lean_609.mp4`) | `LEAN_EVIDENCE=.../carpeta-del-zip python3 render_lean_video.py` |

Los videos se guardan en la carpeta desde donde corres el comando; `RENDER_OUT` cambia el nombre del archivo. El 26 de octubre comprobé que `build_explorer_data.py` produce un `data.json` idéntico, byte a byte, al publicado en `site/fluido/`.

Los videos son ilustrativos. La simulación sin viscosidad muestra falta de resolución, no una explosión: el pico de vorticidad pasa de 7,2 con 32³ a 13,7 con 64³.
