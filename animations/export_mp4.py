import base64
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

ANIMATIONS = Path(__file__).resolve().parent
OUT = ANIMATIONS.parent / "docs" / "media"
IDS = sys.argv[1:] or ["rc", "chemistry", "cooling", "snell", "campaign", "formal", "rerun", "mutants", "replay", "provenance"]
FPS, DURATION = 30, 20
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1400})
    for animation_id in IDS:
        started = time.time()
        page.goto((ANIMATIONS / f"{animation_id}.html").as_uri())
        page.evaluate("cancelAnimationFrame(raf)")
        target = OUT / f"{animation_id}.mp4"
        encoder = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-",
                                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(target)],
                                   stdin=subprocess.PIPE)
        frames = FPS * DURATION
        for index in range(frames + 1):
            page.evaluate(f"renderAt({DURATION * index / frames})")
            data = page.evaluate("document.getElementById('scene').toDataURL('image/png')")
            encoder.stdin.write(base64.b64decode(data.split(",", 1)[1]))
        encoder.stdin.close()
        encoder.wait()
        print(f"{target} {target.stat().st_size / 1e6:.1f} MB {time.time() - started:.0f}s", flush=True)
    browser.close()
