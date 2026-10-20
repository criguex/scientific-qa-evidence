#!/usr/bin/env python3
"""Generate the approved narration once, then post-process it without new API calls."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VOICE_ID = "WbPw2BEKJmkwDvOBt9Z9"
MODEL_ID = "eleven_multilingual_v2"
SPEED = 1.0
MAX_REQUESTS = 5
MAX_CHARACTERS = 11_000
TEMPO = 1.2
POSTPROCESS_FILTER = "atempo=1.2,loudnorm=I=-16:TP=-1.5:LRA=11"
SCRIPT_PATH = Path(__file__).with_name("narration.json")
SPANISH_SCRIPT_PATH = Path(__file__).with_name("narration.es.json")
LANGUAGE_SETTINGS = {
    "en": {"tempo": 1.2, "audio_name": "audio_1.20x.mp3"},
    "es": {"tempo": 1.25, "audio_name": "audio_1.25x.mp3"},
}


def script_path_for(language: str) -> Path:
    if language == "en":
        return SCRIPT_PATH
    if language == "es":
        return SPANISH_SCRIPT_PATH
    raise ValueError("Language must be 'en' or 'es'.")


def filter_for(language: str) -> str:
    settings = LANGUAGE_SETTINGS.get(language)
    if settings is None:
        raise ValueError("Language must be 'en' or 'es'.")
    return f"atempo={settings['tempo']:g},loudnorm=I=-16:TP=-1.5:LRA=11"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def payload_for(text: str) -> dict[str, Any]:
    return {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.1,
            "use_speaker_boost": True,
            "speed": SPEED,
        },
    }


def load_script(path: Path | None = None, language: str = "en") -> list[dict[str, Any]]:
    if language not in LANGUAGE_SETTINGS:
        raise ValueError("Language must be 'en' or 'es'.")
    path = path or script_path_for(language)
    document = json.loads(path.read_text(encoding="utf-8"))
    chapters = document.get("chapters")
    if not isinstance(chapters, list) or len(chapters) != 5:
        raise ValueError("The narration must contain exactly five chapters.")
    chapter_ids = [chapter.get("id") for chapter in chapters if isinstance(chapter, dict)]
    if len(chapter_ids) != len(chapters) or any(
        not isinstance(chapter_id, str)
        or not chapter_id
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", chapter_id)
        or chapter_id in {".", ".."}
        or Path(chapter_id).is_absolute()
        or "/" in chapter_id
        or "\\" in chapter_id
        or "\x00" in chapter_id
        for chapter_id in chapter_ids
    ):
        raise ValueError("Each chapter ID must be a safe single path component.")
    if len(set(chapter_ids)) != len(chapter_ids):
        raise ValueError("Chapter IDs must be unique.")
    calls: list[dict[str, Any]] = []
    for chapter in chapters:
        other_language = "es" if language == "en" else "en"
        if other_language in chapter:
            raise ValueError(f"{language.upper()} release scripts must contain only {language.upper()} chapter text.")
        entry = chapter.get(language)
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(field), str) or not entry[field]
            for field in ("title", "clip_text", "long_extra")
        ):
            raise ValueError(f"Chapter {chapter['id']} is missing required {language.upper()} text fields.")
        clip = entry["clip_text"]
        text = f"{clip} {entry['long_extra']}"
        if not text.startswith(clip + " "):
            raise ValueError(f"Invalid excerpt boundary for {chapter['id']} {language.upper()}.")
        calls.append({"id": chapter["id"], "language": language, "title": entry["title"], "clip_text": clip, "text": text})
    characters = sum(len(call["text"]) for call in calls)
    if len(calls) > MAX_REQUESTS:
        raise ValueError("Narration exceeds the five-request limit.")
    if characters > MAX_CHARACTERS:
        raise ValueError("Narration exceeds the 11,000-character limit.")
    if any(len(call["text"]) > 5_000 for call in calls):
        raise ValueError("A chapter exceeds the provider's 5,000-character request cap.")
    return calls


def load_key(env_value: str | None, dotenv_path: Path | None) -> str:
    if env_value:
        return env_value.strip()
    if dotenv_path is None:
        raise ValueError("Set GV_ELEVENLABS_API_KEY or pass an explicit key file.")
    key_values: list[str] = []
    other_assignments: list[str] = []
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].strip()
        name, separator, value = line.partition("=")
        if not separator:
            raise ValueError("Key file must contain only the configured key assignment.")
        if name.strip() != "GV_ELEVENLABS_API_KEY":
            other_assignments.append(name.strip())
            continue
        tokens = shlex.split(value, comments=True)
        key_values.append(tokens[0] if tokens else "")
    if other_assignments or len(key_values) != 1 or not key_values[0]:
        raise ValueError("Key file must contain exactly one GV_ELEVENLABS_API_KEY assignment.")
    return key_values[0]


def request_once(text: str, key: str, timeout: int = 120) -> tuple[dict[str, Any], dict[str, Any]]:
    body = json.dumps(payload_for(text), ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps?output_format=mp3_44100_128",
        data=body,
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    started = time.monotonic()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        result = json.load(response)
        metadata = {
            "request_id": response.headers.get("request-id"),
            "character_cost": response.headers.get("character-cost"),
            "http_status": response.status,
        }
    return result, {**metadata, "duration_seconds": round(time.monotonic() - started, 3)}


def atomic_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_generation(out_dir: Path, key: str, script_path: Path | None = None, language: str = "en") -> dict[str, Any]:
    calls = load_script(script_path, language)
    if out_dir.exists():
        raise FileExistsError("Output path already exists; refusing duplicate paid requests.")
    out_dir.mkdir(parents=True)
    results: list[dict[str, Any]] = []
    for index, call in enumerate(calls, start=1):
        chapter_dir = out_dir / call["language"] / call["id"]
        chapter_dir.mkdir(parents=True)
        request_data = payload_for(call["text"])
        atomic_json(chapter_dir / "request.json", request_data)
        record: dict[str, Any] = {
            "id": call["id"],
            "language": call["language"],
            "request_started_utc": utc_now(),
            "request_characters": len(call["text"]),
            "request_sha256": hashlib.sha256(call["text"].encode("utf-8")).hexdigest(),
            "voice_id": VOICE_ID,
            "model_id": MODEL_ID,
            "speed": SPEED,
            "status": "pending",
        }
        try:
            response, metadata = request_once(call["text"], key)
            record.update({
                "status": "response_received; processing_pending",
                "response_saved_utc": utc_now(),
                "duration_seconds": metadata["duration_seconds"],
                "provider_request_id": metadata["request_id"],
                "character_cost": metadata["character_cost"],
                "http_status": metadata["http_status"],
            })
            atomic_json(chapter_dir / "response_raw.json", response)
            atomic_json(chapter_dir / "manifest.json", record)
            audio = base64.b64decode(response["audio_base64"], validate=True)
            if len(audio) < 1_000:
                raise ValueError("Unexpectedly small audio response; inspect saved request before any retry.")
            (chapter_dir / "audio_raw.mp3").write_bytes(audio)
            alignment = response.get("alignment") or response.get("normalized_alignment")
            if not isinstance(alignment, dict):
                raise ValueError("Provider response did not include character alignment.")
            atomic_json(chapter_dir / "alignment_raw.json", alignment)
            record.update({
                "status": "generated_raw; postprocess_pending",
                "audio_bytes": len(audio),
                "audio_sha256": hashlib.sha256(audio).hexdigest(),
                "alignment_sha256": hashlib.sha256(json.dumps(alignment, ensure_ascii=False, sort_keys=True).encode()).hexdigest(),
            })
            atomic_json(chapter_dir / "manifest.json", record)
            results.append(record)
            print(json.dumps({"saved": index, "of": len(calls), "id": call["id"], "status": record["status"]}))
        except urllib.error.HTTPError as error:
            record.update({"status": "http_error_no_retry", "http_status": error.code, "response_saved_utc": utc_now()})
            atomic_json(chapter_dir / "manifest.json", record)
            raise RuntimeError(f"Provider returned HTTP {error.code}; stopped without retry.") from None
        except (urllib.error.URLError, TimeoutError) as error:
            record.update({"status": "network_error_no_retry", "error_type": type(error).__name__, "response_saved_utc": utc_now()})
            atomic_json(chapter_dir / "manifest.json", record)
            raise RuntimeError("Network request failed; stopped without retry.") from None
        except Exception as error:
            record.update({"status": "response_error_no_retry", "error_type": type(error).__name__, "response_saved_utc": utc_now()})
            atomic_json(chapter_dir / "manifest.json", record)
            raise
    summary = {"status": "all_raw_responses_saved", "language": calls[0]["language"], "requests": len(results), "generated_utc": utc_now(), "results": results}
    atomic_json(out_dir / "summary.json", summary)
    return summary


def captions_from_alignment(alignment: dict[str, Any], clip_text: str, tempo: float = TEMPO) -> tuple[list[dict[str, Any]], float]:
    chars = alignment["characters"]
    starts = alignment.get("character_start_times_seconds") or alignment.get("character_start_times")
    ends = alignment.get("character_end_times_seconds") or alignment.get("character_end_times")
    if not (len(chars) == len(starts) == len(ends)) or len(chars) < len(clip_text):
        raise ValueError("Alignment character arrays do not match the submitted narration.")
    clip_end = float(ends[len(clip_text) - 1]) / tempo
    aligned_text = "".join(chars)
    if not aligned_text.startswith(clip_text):
        raise ValueError("Alignment text does not preserve the submitted clip prefix.")
    words = list(re.finditer(r"\S+", aligned_text))
    groups: list[dict[str, Any]] = []
    current: list[Any] = []
    for word in words:
        current.append(word)
        if len(current) >= 8 or word.group().endswith((".", "!", "?", ";", ":")):
            first, last = current[0], current[-1]
            groups.append({
                "text": aligned_text[first.start():last.end()],
                "start": float(starts[first.start()]) / tempo,
                "end": float(ends[last.end() - 1]) / tempo,
            })
            current = []
    if current:
        first, last = current[0], current[-1]
        groups.append({
            "text": aligned_text[first.start():last.end()],
            "start": float(starts[first.start()]) / tempo,
            "end": float(ends[last.end() - 1]) / tempo,
        })
    captions = [{
        "text": group["text"],
        "startMs": round(group["start"] * 1000),
        "endMs": round(group["end"] * 1000),
        "timestampMs": round(group["start"] * 1000),
        "confidence": None,
    } for group in groups]
    return captions, clip_end


def to_srt(captions: list[dict[str, Any]]) -> str:
    def stamp(ms: int) -> str:
        hours, rem = divmod(ms, 3_600_000)
        minutes, rem = divmod(rem, 60_000)
        seconds, millis = divmod(rem, 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{millis:03}"

    chunks = []
    for index, caption in enumerate(captions, start=1):
        chunks.append(f"{index}\n{stamp(caption['startMs'])} --> {stamp(caption['endMs'])}\n{caption['text']}\n")
    return "\n".join(chunks)


def run_postprocess(out_dir: Path, script_path: Path | None = None, language: str = "en") -> dict[str, Any]:
    if not out_dir.is_dir():
        raise FileNotFoundError("Generated output directory does not exist.")
    chapters = load_script(script_path, language)
    settings = LANGUAGE_SETTINGS[language]
    tempo = settings["tempo"]
    filter_value = filter_for(language)
    if not (out_dir / "summary.json").is_file():
        raise FileNotFoundError("Generation summary is missing; refusing post-processing.")
    generation_summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    if generation_summary.get("status") != "all_raw_responses_saved" or generation_summary.get("language", "en") != language:
        raise ValueError("Generation summary status or language does not match the selected release.")
    for chapter in chapters:
        directory = out_dir / chapter["language"] / chapter["id"]
        if not (directory / "audio_raw.mp3").is_file() or not (directory / "alignment_raw.json").is_file():
            raise FileNotFoundError("A raw response or alignment is missing; refusing post-processing.")
        if any((directory / name).exists() for name in (settings["audio_name"], "captions.json", "captions.srt")):
            raise FileExistsError("Post-processed output already exists; refusing overwrite.")
    processed: list[dict[str, Any]] = []
    for chapter in chapters:
        directory = out_dir / chapter["language"] / chapter["id"]
        raw_audio = directory / "audio_raw.mp3"
        final_audio = directory / settings["audio_name"]
        if not raw_audio.is_file() or final_audio.exists():
            raise FileExistsError("Missing raw audio or post-processed output already exists.")
        subprocess.run([
            "ffmpeg", "-nostdin", "-v", "error", "-i", str(raw_audio),
            "-filter:a", filter_value, "-ar", "44100", "-c:a", "libmp3lame", "-q:a", "2", str(final_audio),
        ], check=True, capture_output=True, text=True, timeout=300)
        probe = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(final_audio),
        ], check=True, capture_output=True, text=True, timeout=30)
        duration = float(json.loads(probe.stdout)["format"]["duration"])
        alignment = json.loads((directory / "alignment_raw.json").read_text(encoding="utf-8"))
        captions, clip_end = captions_from_alignment(alignment, chapter["clip_text"], tempo)
        atomic_json(directory / "captions.json", captions)
        (directory / "captions.srt").write_text(to_srt(captions), encoding="utf-8")
        manifest_path = directory / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        final_bytes = final_audio.read_bytes()
        manifest.update({
            "status": "postprocessed",
            "postprocess_utc": utc_now(),
            "language": language,
            "tempo": tempo,
            "postprocess_filter": filter_value,
            "sample_rate_hz": 44100,
            "final_duration_seconds": duration,
            "clip_end_seconds": clip_end,
            "final_audio_bytes": len(final_bytes),
            "final_audio_sha256": hashlib.sha256(final_bytes).hexdigest(),
            "captions_sha256": hashlib.sha256((directory / "captions.json").read_bytes()).hexdigest(),
        })
        atomic_json(manifest_path, manifest)
        processed.append({"id": chapter["id"], "language": chapter["language"], "duration_seconds": duration, "clip_end_seconds": clip_end})
    summary = {"status": "postprocessing_complete_no_new_provider_calls", "language": language, "tempo": tempo, "processed": processed, "timestamp_utc": utc_now()}
    atomic_json(out_dir / "postprocess_summary.json", summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--generate", action="store_true")
    mode.add_argument("--postprocess", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--key-file", type=Path)
    parser.add_argument("--language", choices=tuple(LANGUAGE_SETTINGS), default="en")
    parser.add_argument("--script", type=Path)
    args = parser.parse_args(argv)
    script_path = args.script or script_path_for(args.language)
    try:
        if args.dry_run:
            calls = load_script(script_path, args.language)
            print(json.dumps({"status": "dry_run_only", "language": args.language, "requests": len(calls), "characters": sum(len(c["text"]) for c in calls), "voice_id": VOICE_ID, "model_id": MODEL_ID, "speed": SPEED, "tempo": LANGUAGE_SETTINGS[args.language]["tempo"], "no_network": True}))
            return 0
        if args.generate:
            key = load_key(os.environ.get("GV_ELEVENLABS_API_KEY"), args.key_file)
            result = run_generation(args.out, key, script_path, args.language)
        else:
            result = run_postprocess(args.out, script_path, args.language)
        print(json.dumps({"status": result["status"], "requests": result.get("requests"), "processed": len(result.get("processed", []))}))
        return 0
    except Exception as error:
        print(json.dumps({"status": "failed", "error_type": type(error).__name__}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
