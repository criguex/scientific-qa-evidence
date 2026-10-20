import json
import tempfile
import unittest
from pathlib import Path

import prepare_media


class PrepareMediaTests(unittest.TestCase):
    def make_source(self, root, language="en"):
        settings = prepare_media.LANGUAGE_SETTINGS[language]
        document = json.loads(settings["script"].read_text(encoding="utf-8"))
        records = []
        for chapter in document["chapters"]:
            directory = root / language / chapter["id"]
            directory.mkdir(parents=True)
            (directory / settings["audio"]).write_bytes(b"a" * 1200)
            (directory / "captions.json").write_text(json.dumps([
                {"text": "Aligned caption.", "startMs": 0, "endMs": 900}
            ]), encoding="utf-8")
            records.append({
                "id": chapter["id"],
                "language": language,
                "duration_seconds": 2.0,
                "clip_end_seconds": 1.0,
            })
        (root / "postprocess_summary.json").write_text(json.dumps({
            "status": "postprocessing_complete_no_new_provider_calls",
            "language": language,
            "processed": records,
        }), encoding="utf-8")

    def test_exports_media_timing_and_offset_long_subtitles(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            video_public = root / "video-public"
            public = video_public / "english"
            manifest_path = root / "src" / "generatedMedia.json"
            source.mkdir()
            self.make_source(source)
            manifest_path.parent.mkdir()
            manifest_path.write_text('{"status":"pending"}\n', encoding="utf-8")

            result = prepare_media.prepare(source, public, manifest_path)

            self.assertEqual(result["status"], "ready")
            self.assertEqual(result["long_duration_in_frames"], 300)
            self.assertEqual(result["chapters"][1]["from_frame"], 60)
            self.assertTrue((video_public / "english" / "audio" / "01_method.mp3").is_file())
            self.assertEqual(result["chapters"][0]["audio"], "english/audio/01_method.mp3")
            long_srt = (public / "subtitles" / "EN-long.srt").read_text(encoding="utf-8")
            self.assertIn("00:00:02,000 --> 00:00:02,900", long_srt)
            short_vtt = (public / "subtitles" / "EN-01_method-short.vtt").read_text(encoding="utf-8")
            self.assertTrue(short_vtt.startswith("WEBVTT\n\n1\n"))
            with self.assertRaises(FileExistsError):
                prepare_media.prepare(source, public, manifest_path)

    def test_unsafe_ids_fail_before_copying(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            self.make_source(source)
            script = json.loads(prepare_media.SCRIPT_PATH.read_text(encoding="utf-8"))
            script["chapters"][0]["id"] = "../outside"
            script_path = root / "bad-narration.json"
            script_path.write_text(json.dumps(script), encoding="utf-8")
            with self.assertRaises(ValueError):
                prepare_media.prepare(source, root / "public", root / "generatedMedia.json", script_path)
            self.assertFalse((root / "public").exists())

    def test_spanish_media_uses_own_audio_tree_and_caption_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            public = root / "video-public" / "spanish"
            manifest_path = root / "src" / "generatedSpanishMedia.json"
            source.mkdir()
            self.make_source(source, "es")
            manifest_path.parent.mkdir()
            manifest_path.write_text('{"status":"pending"}\n', encoding="utf-8")

            result = prepare_media.prepare(
                source, public, manifest_path, prepare_media.SPANISH_SCRIPT_PATH, "es"
            )

            self.assertEqual(result["language"], "es")
            self.assertEqual(result["tempo"], 1.25)
            self.assertEqual(result["chapters"][0]["audio"], "spanish/audio/01_method.mp3")
            self.assertTrue((public / "audio" / "01_method.mp3").is_file())
            self.assertTrue((public / "subtitles" / "ES-long.vtt").is_file())
            short = (public / "subtitles" / "ES-01_method-short.srt").read_text(encoding="utf-8")
            self.assertIn("Aligned caption.", short)
            with self.assertRaises(FileExistsError):
                prepare_media.prepare(
                    source, public, manifest_path, prepare_media.SPANISH_SCRIPT_PATH, "es"
                )


if __name__ == "__main__":
    unittest.main()
