#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import sys
from pathlib import Path
from typing import Any


FPS = 30
SCRIPT_PATH = Path(__file__).with_name("narration.json")
SPANISH_SCRIPT_PATH = Path(__file__).with_name("narration.es.json")
LANGUAGE_SETTINGS = {
    "en": {"script": SCRIPT_PATH, "tag": "EN", "directory": "english", "audio": "audio_1.20x.mp3", "tempo": 1.2},
    "es": {"script": SPANISH_SCRIPT_PATH, "tag": "ES", "directory": "spanish", "audio": "audio_1.25x.mp3", "tempo": 1.25},
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_id(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value) is not None


def subtitle_stamp(milliseconds: int, decimal: str) -> str:
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}{decimal}{millis:03}"


def subtitle_text(captions: list[dict[str, Any]], offset_ms: int = 0, decimal: str = ",") -> str:
    blocks = []
    for index, caption in enumerate(captions, start=1):
        start = int(caption["startMs"]) + offset_ms
        end = int(caption["endMs"]) + offset_ms
        if start < 0 or end <= start or not isinstance(caption.get("text"), str) or not caption["text"].strip():
            raise ValueError("Caption times or text are invalid.")
        blocks.append(f"{index}\n{subtitle_stamp(start, decimal)} --> {subtitle_stamp(end, decimal)}\n{caption['text']}\n")
    return "\n".join(blocks)


def cue_offset(frame: int) -> int:
    return round(frame * 1000 / FPS)


def prepare(source: Path, public: Path, manifest_path: Path, script_path: Path | None = None, language: str = "en") -> dict[str, Any]:
    settings = LANGUAGE_SETTINGS.get(language)
    if settings is None:
        raise ValueError("Language must be 'en' or 'es'.")
    script_path = script_path or settings["script"]
    narration = load_json(script_path)
    chapters = narration.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != 5:
        raise ValueError("Narration must contain exactly five chapters.")
    ids = [chapter.get("id") for chapter in chapters if isinstance(chapter, dict)]
    if len(ids) != len(chapters) or any(not safe_id(chapter_id) for chapter_id in ids) or len(set(ids)) != 5:
        raise ValueError("Chapter IDs must be unique, safe path components.")
    chapter_text = [chapter.get(language) for chapter in chapters]
    other_language = "es" if language == "en" else "en"
    if any(other_language in chapter or not isinstance(text, dict) for chapter, text in zip(chapters, chapter_text)):
        raise ValueError(f"{language.upper()} release narration must contain only {language.upper()} chapter text.")

    postprocess = load_json(source / "postprocess_summary.json")
    processed = postprocess.get("processed")
    if postprocess.get("status") != "postprocessing_complete_no_new_provider_calls" or not isinstance(processed, list):
        raise ValueError("A complete post-processing summary is required.")
    if postprocess.get("language", "en") != language:
        raise ValueError("Post-processing language does not match the selected release language.")
    by_id = {item.get("id"): item for item in processed if isinstance(item, dict) and item.get("language", language) == language}
    if len(by_id) != len(processed) or set(by_id) != set(ids):
        raise ValueError(f"Post-processing summary must contain each {language.upper()} chapter exactly once.")

    records = []
    for chapter in chapters:
        chapter_id = chapter["id"]
        item = by_id[chapter_id]
        duration = float(item["duration_seconds"])
        clip_end = float(item["clip_end_seconds"])
        if not math.isfinite(duration) or not math.isfinite(clip_end) or duration <= 0 or clip_end <= 0 or clip_end > duration:
            raise ValueError(f"Invalid audio duration or clip boundary for {chapter_id}.")
        directory = source / language / chapter_id
        audio = directory / settings["audio"]
        captions_path = directory / "captions.json"
        if not audio.is_file() or audio.stat().st_size < 1000 or not captions_path.is_file():
            raise FileNotFoundError(f"Processed audio and captions are required for {chapter_id}.")
        captions = load_json(captions_path)
        if not isinstance(captions, list) or not captions:
            raise ValueError(f"Non-empty aligned captions are required for {chapter_id}.")
        for caption in captions:
            if not isinstance(caption, dict) or not isinstance(caption.get("startMs"), int) or not isinstance(caption.get("endMs"), int):
                raise ValueError(f"Invalid aligned caption in {chapter_id}.")
            if caption["startMs"] < 0 or caption["endMs"] <= caption["startMs"] or caption["endMs"] > math.ceil(duration * 1000) + 100:
                raise ValueError(f"Caption falls outside the audio duration in {chapter_id}.")
        records.append({
            "id": chapter_id,
            "title": chapter[language]["title"],
            "audio_source": audio,
            "captions": captions,
            "duration_seconds": duration,
            "clip_end_seconds": clip_end,
            "duration_in_frames": math.ceil(duration * FPS),
            "clip_end_frame": math.ceil(clip_end * FPS),
        })

    audio_dir = public / "audio"
    subtitle_dir = public / "subtitles"
    planned = [audio_dir / f"{record['id']}.mp3" for record in records]
    planned.extend([subtitle_dir / f"{settings['tag']}-long.srt", subtitle_dir / f"{settings['tag']}-long.vtt"])
    for record in records:
        planned.extend([
            subtitle_dir / f"{settings['tag']}-{record['id']}-short.srt",
            subtitle_dir / f"{settings['tag']}-{record['id']}-short.vtt",
        ])
    if any(path.exists() for path in planned):
        raise FileExistsError("A destination media file already exists; refusing overwrite.")
    if manifest_path.exists():
        existing = load_json(manifest_path)
        if existing.get("status") != "pending":
            raise FileExistsError("A ready media manifest already exists; refusing overwrite.")

    audio_dir.mkdir(parents=True, exist_ok=True)
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    offset_frames = 0
    long_captions = []
    manifest_chapters = []
    for record in records:
        shutil.copyfile(record["audio_source"], audio_dir / f"{record['id']}.mp3")
        frame_offset = offset_frames
        offset_ms = cue_offset(frame_offset)
        long_captions.extend({**caption, "startMs": caption["startMs"] + offset_ms, "endMs": caption["endMs"] + offset_ms} for caption in record["captions"])
        short = []
        for caption in record["captions"]:
            if caption["startMs"] >= record["clip_end_seconds"] * 1000:
                break
            short.append({**caption, "endMs": min(caption["endMs"], math.ceil(record["clip_end_seconds"] * 1000))})
        srt_path = subtitle_dir / f"{settings['tag']}-{record['id']}-short.srt"
        vtt_path = subtitle_dir / f"{settings['tag']}-{record['id']}-short.vtt"
        srt_path.write_text(subtitle_text(short), encoding="utf-8")
        vtt_path.write_text("WEBVTT\n\n" + subtitle_text(short, decimal="."), encoding="utf-8")
        manifest_chapters.append({
            "id": record["id"],
            "title": record["title"],
            "audio": f"{settings['directory']}/audio/{record['id']}.mp3",
            "duration_seconds": record["duration_seconds"],
            "clip_end_seconds": record["clip_end_seconds"],
            "duration_in_frames": record["duration_in_frames"],
            "clip_end_frame": record["clip_end_frame"],
            "from_frame": frame_offset,
            "captions": record["captions"],
        })
        offset_frames += record["duration_in_frames"]

    (subtitle_dir / f"{settings['tag']}-long.srt").write_text(subtitle_text(long_captions), encoding="utf-8")
    (subtitle_dir / f"{settings['tag']}-long.vtt").write_text("WEBVTT\n\n" + subtitle_text(long_captions, decimal="."), encoding="utf-8")
    manifest = {
        "status": "ready",
        "language": language,
        "tempo": settings["tempo"],
        "fps": FPS,
        "width": 1920,
        "height": 1080,
        "long_duration_in_frames": offset_frames,
        "chapters": manifest_chapters,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Copy language-specific audio and derive aligned subtitle assets.")
    parser.add_argument("--source", type=Path, required=True, help="Post-processed TTS output directory")
    parser.add_argument("--public", type=Path, required=True, help="Release video public directory")
    parser.add_argument("--manifest", type=Path, required=True, help="Generated media manifest path")
    parser.add_argument("--language", choices=tuple(LANGUAGE_SETTINGS), default="en")
    parser.add_argument("--script", type=Path)
    arguments = parser.parse_args(argv)
    try:
        manifest = prepare(arguments.source, arguments.public, arguments.manifest, arguments.script, arguments.language)
        print(json.dumps({"status": manifest["status"], "language": manifest["language"], "chapters": len(manifest["chapters"]), "long_duration_in_frames": manifest["long_duration_in_frames"]}))
        return 0
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
