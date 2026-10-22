import base64
import subprocess
import sys
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

ANIMATIONS = Path(__file__).resolve().parent
ASSETS = ANIMATIONS.parent / "docs" / "assets"
OUTPUTS = {
    "rc": "rc-mutation.gif",
    "chemistry": "chemistry-preview.gif",
    "cooling": "cooling-preview.gif",
    "snell": "snell-preview.gif",
    "campaign": "campaign-preview.gif",
    "formal": "formal-preview.gif",
    "rerun": "rerun-preview.gif",
    "mutants": "mutants-preview.gif",
    "replay": "replay-preview.gif",
    "provenance": "provenance-preview.gif",
    "experiment": "experiment-preview.gif",
    "bridges": "bridges-preview.gif",
    "controls": "controls-preview.gif",
    "flow": "flow-scene.gif",
}
FRAMES = 120
FPS = 15
DURATION = 20
REALTIME = {"rerun", "mutants", "replay", "provenance", "experiment", "bridges", "controls", "flow"}
REALTIME_FPS = 10
LIGHT = {"flow": "scale=720:-1:flags=lanczos,format=rgb24,"}


def export(page, animation_id, destination):
    page.goto((ANIMATIONS / f"{animation_id}.html").as_uri())
    page.evaluate("cancelAnimationFrame(raf)")
    frame_count, fps = (DURATION * REALTIME_FPS, REALTIME_FPS) if animation_id in REALTIME else (FRAMES, FPS)
    with tempfile.TemporaryDirectory() as frames:
        for index in range(frame_count):
            page.evaluate(f"renderAt({DURATION * index / (frame_count - 1)})")
            data = page.evaluate("document.getElementById('scene').toDataURL('image/png')")
            Path(frames, f"f{index:03d}.png").write_bytes(base64.b64decode(data.split(",", 1)[1]))
        colors = 128 if animation_id in LIGHT else 256
        palette = LIGHT.get(animation_id, "") + f"split[a][b];[a]palettegen=max_colors={colors}:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(fps), "-i", f"{frames}/f%03d.png", "-vf", palette, "-loop", "0", str(destination)], check=True)


def main(ids):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1400})
        for animation_id in ids:
            export(page, animation_id, ASSETS / OUTPUTS[animation_id])
            print(ASSETS / OUTPUTS[animation_id])
        browser.close()


if __name__ == "__main__":
    main(sys.argv[1:] or list(OUTPUTS))
