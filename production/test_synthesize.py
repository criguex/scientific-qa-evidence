import base64
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import synthesize


class SynthesizeTests(unittest.TestCase):
    def test_script_limits_and_tts_settings(self):
        calls = synthesize.load_script()
        self.assertEqual(len(calls), 5)
        self.assertTrue(all(call["language"] == "en" for call in calls))
        self.assertLessEqual(sum(len(call["text"]) for call in calls), synthesize.MAX_CHARACTERS)
        payload = synthesize.payload_for(calls[0]["text"])
        self.assertEqual(payload["model_id"], "eleven_multilingual_v2")
        self.assertEqual(payload["voice_settings"]["speed"], 1.0)
        self.assertNotIn("language_code", payload)

    def test_spanish_script_is_separate_and_uses_125_tempo(self):
        calls = synthesize.load_script(language="es")
        self.assertEqual(len(calls), 5)
        self.assertTrue(all(call["language"] == "es" for call in calls))
        self.assertLessEqual(sum(len(call["text"]) for call in calls), synthesize.MAX_CHARACTERS)
        self.assertTrue(all(len(call["text"]) <= 5_000 for call in calls))
        self.assertEqual(synthesize.LANGUAGE_SETTINGS["en"]["tempo"], 1.2)
        self.assertEqual(synthesize.LANGUAGE_SETTINGS["es"]["tempo"], 1.25)
        self.assertEqual(synthesize.filter_for("en"), synthesize.POSTPROCESS_FILTER)
        self.assertEqual(synthesize.filter_for("es"), "atempo=1.25,loudnorm=I=-16:TP=-1.5:LRA=11")

    def test_spanish_schema_is_rejected_before_output_or_provider_when_mislabeled(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = json.loads(synthesize.SPANISH_SCRIPT_PATH.read_text(encoding="utf-8"))
            document["chapters"][0]["en"] = {"title": "Wrong language", "clip_text": "Text", "long_extra": "More text"}
            script = root / "mixed-language.json"
            script.write_text(json.dumps(document), encoding="utf-8")
            output = root / "no-output"
            with patch.object(synthesize, "request_once") as request:
                with self.assertRaises(ValueError):
                    synthesize.run_generation(output, "mock-key", script, "es")
            self.assertFalse(output.exists())
            request.assert_not_called()

    def test_dry_run_does_not_make_network_request(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "not-created"
            with patch.object(synthesize.urllib.request, "urlopen", side_effect=AssertionError("network called")):
                self.assertEqual(synthesize.main(["--dry-run", "--out", str(output)]), 0)
            self.assertFalse(output.exists())

    def test_key_file_must_contain_only_expected_assignment(self):
        with tempfile.TemporaryDirectory() as directory:
            key_file = Path(directory) / "key.env"
            key_file.write_text("GV_ELEVENLABS_API_KEY='secret-value'\n", encoding="utf-8")
            self.assertEqual(synthesize.load_key(None, key_file), "secret-value")
            key_file.write_text("GV_ELEVENLABS_API_KEY=x\nOTHER=value\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                synthesize.load_key(None, key_file)

    def test_alignment_generates_scaled_captions_and_clip_boundary(self):
        text = "One two three four five six seven eight nine. Clip ends here."
        alignment = {
            "characters": list(text),
            "character_start_times_seconds": [index * 0.1 for index in range(len(text))],
            "character_end_times_seconds": [(index + 1) * 0.1 for index in range(len(text))],
        }
        captions, clip_end = synthesize.captions_from_alignment(alignment, "One two", tempo=1.2)
        self.assertEqual(captions[0]["text"], "One two three four five six seven eight")
        self.assertEqual(captions[0]["startMs"], 0)
        self.assertAlmostEqual(clip_end, alignment["character_end_times_seconds"][6] / 1.2, places=5)
        self.assertIsNone(captions[0]["confidence"])
        self.assertIn("--> ", synthesize.to_srt(captions))

    def test_existing_output_refuses_generation_without_calling_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "existing"
            output.mkdir()
            with patch.object(synthesize, "request_once", side_effect=AssertionError("provider called")):
                with self.assertRaises(FileExistsError):
                    synthesize.run_generation(output, "not-a-real-key")

    def test_invalid_chapter_ids_and_fields_refuse_before_output_or_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = json.loads(synthesize.SCRIPT_PATH.read_text(encoding="utf-8"))
            cases = {
                "duplicate": lambda doc: doc["chapters"][1].update(id=doc["chapters"][0]["id"]),
                "traversal": lambda doc: doc["chapters"][0].update(id="../../escape"),
                "absolute": lambda doc: doc["chapters"][0].update(id=str(root / "escape")),
                "drive-relative": lambda doc: doc["chapters"][0].update(id="C:escape"),
                "missing-field": lambda doc: doc["chapters"][0]["en"].update(clip_text=None),
                "spanish-content": lambda doc: doc["chapters"][0].update(es={"title": "No"}),
            }
            with patch.object(synthesize, "request_once") as request:
                for name, mutate in cases.items():
                    document = json.loads(json.dumps(original))
                    mutate(document)
                    script = root / f"{name}.json"
                    output = root / f"output-{name}"
                    script.write_text(json.dumps(document), encoding="utf-8")
                    with self.subTest(case=name), self.assertRaises(ValueError):
                        synthesize.run_generation(output, "mock-key", script)
                    self.assertFalse(output.exists())
                    self.assertFalse((root / "escape").exists())
            request.assert_not_called()

    def test_paid_audio_and_metadata_survive_missing_alignment_without_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "generated"
            encoded_audio = base64.b64encode(b"a" * 1100).decode("ascii")
            metadata = {"duration_seconds": 0.01, "request_id": "mock-request", "character_cost": "123", "http_status": 200}
            with patch.object(synthesize, "request_once", return_value=({"audio_base64": encoded_audio}, metadata)) as request:
                with self.assertRaisesRegex(ValueError, "alignment"):
                    synthesize.run_generation(output, "mock-key")
            request.assert_called_once()
            call = synthesize.load_script()[0]
            chapter_dir = output / call["language"] / call["id"]
            self.assertEqual(json.loads((chapter_dir / "response_raw.json").read_text(encoding="utf-8"))["audio_base64"], encoded_audio)
            self.assertEqual((chapter_dir / "audio_raw.mp3").read_bytes(), b"a" * 1100)
            manifest = json.loads((chapter_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["provider_request_id"], "mock-request")
            self.assertEqual(manifest["character_cost"], "123")
            self.assertEqual(manifest["status"], "response_error_no_retry")
            self.assertFalse((chapter_dir / "alignment_raw.json").exists())

    def test_invalid_base64_keeps_raw_paid_response_and_metadata_without_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "generated"
            response = {"audio_base64": "not-base64!", "alignment": {"characters": []}}
            metadata = {"duration_seconds": 0.01, "request_id": "mock-invalid", "character_cost": "123", "http_status": 200}
            with patch.object(synthesize, "request_once", return_value=(response, metadata)) as request:
                with self.assertRaises(ValueError):
                    synthesize.run_generation(output, "mock-key")
            request.assert_called_once()
            call = synthesize.load_script()[0]
            chapter_dir = output / call["language"] / call["id"]
            self.assertEqual(json.loads((chapter_dir / "response_raw.json").read_text(encoding="utf-8")), response)
            manifest = json.loads((chapter_dir / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["provider_request_id"], "mock-invalid")
            self.assertEqual(manifest["character_cost"], "123")
            self.assertEqual(manifest["status"], "response_error_no_retry")
            self.assertFalse((chapter_dir / "audio_raw.mp3").exists())

    def test_generation_saves_each_response_before_next_call(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "fresh-output"
            calls_seen = []

            def fake_request(text, key, timeout=120):
                index = len(calls_seen)
                if index:
                    previous = synthesize.load_script()[index - 1]
                    self.assertTrue((output / previous["language"] / previous["id"] / "manifest.json").is_file())
                calls_seen.append(text)
                return {
                    "audio_base64": base64.b64encode(b"a" * 1100).decode("ascii"),
                    "alignment": {
                        "characters": list(text),
                        "character_start_times_seconds": [i * 0.01 for i in range(len(text))],
                        "character_end_times_seconds": [(i + 1) * 0.01 for i in range(len(text))],
                    },
                }, {"duration_seconds": 0.01, "request_id": f"fake-{index}", "character_cost": None, "http_status": 200}

            with patch.object(synthesize, "request_once", side_effect=fake_request):
                result = synthesize.run_generation(output, "mock-key")
            self.assertEqual(len(calls_seen), 5)
            self.assertEqual(result["requests"], 5)
            self.assertEqual(result["language"], "en")
            self.assertTrue((output / "summary.json").is_file())
            for manifest in output.glob("*/*/manifest.json"):
                self.assertNotIn("mock-key", manifest.read_text(encoding="utf-8"))

    def test_spanish_generation_writes_five_responses_to_separate_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "spanish-output"
            responses = []

            def fake_request(text, key, timeout=120):
                responses.append(text)
                return {
                    "audio_base64": base64.b64encode(b"s" * 1100).decode("ascii"),
                    "alignment": {
                        "characters": list(text),
                        "character_start_times_seconds": [i * 0.01 for i in range(len(text))],
                        "character_end_times_seconds": [(i + 1) * 0.01 for i in range(len(text))],
                    },
                }, {"duration_seconds": 0.01, "request_id": "mock-es", "character_cost": None, "http_status": 200}

            with patch.object(synthesize, "request_once", side_effect=fake_request):
                result = synthesize.run_generation(output, "mock-key", language="es")

            self.assertEqual(result["requests"], 5)
            self.assertEqual(result["language"], "es")
            self.assertEqual(len(responses), 5)
            self.assertTrue((output / "es" / "01_method" / "audio_raw.mp3").is_file())
            self.assertTrue((output / "summary.json").is_file())

    def test_postprocess_uses_mocked_ffmpeg_and_never_calls_provider(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "generated"
            output.mkdir()
            synthesize.atomic_json(output / "summary.json", {"status": "all_raw_responses_saved"})
            for call in synthesize.load_script():
                chapter_dir = output / call["language"] / call["id"]
                chapter_dir.mkdir(parents=True)
                (chapter_dir / "audio_raw.mp3").write_bytes(b"raw")
                alignment = {
                    "characters": list(call["text"]),
                    "character_start_times_seconds": [i * 0.01 for i in range(len(call["text"]))],
                    "character_end_times_seconds": [(i + 1) * 0.01 for i in range(len(call["text"]))],
                }
                synthesize.atomic_json(chapter_dir / "alignment_raw.json", alignment)
                synthesize.atomic_json(chapter_dir / "manifest.json", {"status": "generated_raw; postprocess_pending"})

            def fake_subprocess(command, **kwargs):
                self.assertIn("timeout", kwargs)
                if command[0] == "ffmpeg":
                    Path(command[-1]).write_bytes(b"processed")
                    return type("Result", (), {"stdout": ""})()
                return type("Result", (), {"stdout": '{"format":{"duration":"12.5"}}'})()

            with patch.object(synthesize.subprocess, "run", side_effect=fake_subprocess) as mock_run:
                with patch.object(synthesize, "request_once", side_effect=AssertionError("provider called")):
                    result = synthesize.run_postprocess(output)
            self.assertEqual(result["status"], "postprocessing_complete_no_new_provider_calls")
            self.assertEqual(len(mock_run.call_args_list), 10)
            self.assertEqual(mock_run.call_args_list[0].args[0][7], "atempo=1.2,loudnorm=I=-16:TP=-1.5:LRA=11")
            first_chapter = synthesize.load_script()[0]
            captions = json.loads((output / first_chapter["language"] / first_chapter["id"] / "captions.json").read_text(encoding="utf-8"))
            self.assertTrue(captions)
            self.assertTrue(all(caption["endMs"] >= caption["startMs"] for caption in captions))

    def test_spanish_postprocess_uses_125_tempo_and_separate_audio_name(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "generated"
            output.mkdir()
            synthesize.atomic_json(output / "summary.json", {"status": "all_raw_responses_saved", "language": "es"})
            for call in synthesize.load_script(language="es"):
                chapter_dir = output / "es" / call["id"]
                chapter_dir.mkdir(parents=True)
                (chapter_dir / "audio_raw.mp3").write_bytes(b"raw")
                alignment = {
                    "characters": list(call["text"]),
                    "character_start_times_seconds": [i * 0.01 for i in range(len(call["text"]))],
                    "character_end_times_seconds": [(i + 1) * 0.01 for i in range(len(call["text"]))],
                }
                synthesize.atomic_json(chapter_dir / "alignment_raw.json", alignment)
                synthesize.atomic_json(chapter_dir / "manifest.json", {"status": "generated_raw; postprocess_pending"})

            def fake_subprocess(command, **kwargs):
                if command[0] == "ffmpeg":
                    Path(command[-1]).write_bytes(b"processed")
                    self.assertEqual(command[7], "atempo=1.25,loudnorm=I=-16:TP=-1.5:LRA=11")
                    return type("Result", (), {"stdout": ""})()
                return type("Result", (), {"stdout": '{"format":{"duration":"12.5"}}'})()

            with patch.object(synthesize.subprocess, "run", side_effect=fake_subprocess) as mock_run:
                with patch.object(synthesize, "request_once", side_effect=AssertionError("provider called")):
                    result = synthesize.run_postprocess(output, language="es")
            self.assertEqual(result["language"], "es")
            self.assertEqual(result["tempo"], 1.25)
            self.assertTrue((output / "es" / "01_method" / "audio_1.25x.mp3").is_file())
            self.assertFalse((output / "es" / "01_method" / "audio_1.20x.mp3").exists())
            self.assertEqual(len(mock_run.call_args_list), 10)


if __name__ == "__main__":
    unittest.main()
