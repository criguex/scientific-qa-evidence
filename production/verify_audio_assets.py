#!/usr/bin/env python3

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def sha256(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1_048_576), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    trace = json.loads((ROOT / "production" / "audio-assets.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "video" / "src" / "generatedMedia.json").read_text(encoding="utf-8"))
    narration = ROOT / "production" / "narration.json"
    if sha256(narration) != trace["narration_sha256"]:
        raise ValueError("Narration hash does not match the audio trace.")
    if trace["provider_speed"] != 1.0 or trace["offline_tempo"] != 1.2 or manifest.get("status") != "ready":
        raise ValueError("Provider/offline speed or generated media status is unexpected.")
    manifest_chapters = {chapter["id"]: chapter for chapter in manifest["chapters"]}
    if len(trace["chapters"]) != 5 or manifest_chapters.keys() != {item["id"] for item in trace["chapters"]}:
        raise ValueError("Audio trace and generated manifest chapter sets differ.")
    for item in trace["chapters"]:
        audio = ROOT / item["file"]
        chapter = manifest_chapters[item["id"]]
        if not audio.is_file() or sha256(audio) != item["processed_audio_sha256"]:
            raise ValueError(f"Processed audio hash mismatch: {item['id']}")
        if chapter["audio"] != f"english/audio/{item['id']}.mp3":
            raise ValueError(f"Audio path mismatch: {item['id']}")
        if abs(chapter["duration_in_frames"] / manifest["fps"] - item["duration_seconds"]) > 1 / manifest["fps"]:
            raise ValueError(f"Audio timing mismatch: {item['id']}")
        if abs(chapter["clip_end_frame"] / manifest["fps"] - item["short_clip_end_seconds"]) > 1 / manifest["fps"]:
            raise ValueError(f"Short clip boundary mismatch: {item['id']}")
    print("PASS: frozen narration, five processed audio hashes, durations, and short clip boundaries match the generated media manifest.")


if __name__ == "__main__":
    main()
