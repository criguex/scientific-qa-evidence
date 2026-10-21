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
    "validation": "validation-preview.gif",
}
FRAMES = 120
FPS = 15
DURATION = 20


def export(page, animation_id, destination):
    page.goto((ANIMATIONS / f"{animation_id}.html").as_uri())
    page.evaluate("cancelAnimationFrame(raf)")
    with tempfile.TemporaryDirectory() as frames:
        for index in range(FRAMES):
            page.evaluate(f"renderAt({DURATION * index / (FRAMES - 1)})")
            data = page.evaluate("document.getElementById('scene').toDataURL('image/png')")
            Path(frames, f"f{index:03d}.png").write_bytes(base64.b64decode(data.split(",", 1)[1]))
        palette = "split[a][b];[a]palettegen=max_colors=256:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{frames}/f%03d.png", "-vf", palette, "-loop", "0", str(destination)], check=True)


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
