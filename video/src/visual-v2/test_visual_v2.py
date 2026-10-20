import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MEDIA = json.loads((ROOT / "video/src/generatedMedia.json").read_text(encoding="utf-8"))
SPANISH_MEDIA = json.loads((ROOT / "video/src/generatedSpanishMedia.json").read_text(encoding="utf-8"))
PLAN = json.loads((ROOT / "video/src/visual-v2/publication.json").read_text(encoding="utf-8"))
STORY = (ROOT / "video/src/visual-v2/Story.tsx").read_text(encoding="utf-8")
REGISTRATIONS = (ROOT / "video/src/visual-v2/Root.tsx").read_text(encoding="utf-8")


class VisualV2Tests(unittest.TestCase):
    def test_long_timeline_uses_exact_full_chapter_boundaries(self):
        self.assertEqual(MEDIA["fps"], 30)
        self.assertEqual(MEDIA["long_duration_in_frames"], 13246)
        cursor = 0
        for chapter in MEDIA["chapters"]:
            self.assertEqual(chapter["from_frame"], cursor)
            self.assertGreater(chapter["duration_in_frames"], chapter["clip_end_frame"])
            self.assertGreater(chapter["captions"][-1]["endMs"], 0)
            cursor += chapter["duration_in_frames"]
        self.assertEqual(cursor, MEDIA["long_duration_in_frames"])
        self.assertIn('id="EN-V2-Long"', REGISTRATIONS)

    def test_youtube_and_tiktok_plan_contains_exactly_five_aligned_short_openings(self):
        youtube_shorts = PLAN["youtube"]["shorts"]
        tiktok_ids = PLAN["tiktok"]["shorts_composition_ids"]
        self.assertEqual(len(youtube_shorts), 5)
        self.assertEqual(PLAN["tiktok"]["short_count"], 5)
        self.assertEqual(tiktok_ids, [item["composition_id"] for item in youtube_shorts])
        for index, item in enumerate(youtube_shorts):
            chapter = MEDIA["chapters"][index]
            self.assertIn(chapter["id"].split("_")[0], item["render_path"])
            self.assertIn(item["composition_id"], REGISTRATIONS)
            self.assertIn(f"durationInFrames={{media.chapters[{index}].clip_end_frame}}", REGISTRATIONS)
        self.assertEqual(PLAN["youtube"]["long_video"]["status"], "render_pending")
        self.assertEqual(PLAN["supersedes"]["status"], "rejected_static_text_draft")
        self.assertFalse(PLAN["supersedes"]["upload_allowed"])

    def test_story_uses_saved_audio_and_alignment_without_second_speed_change(self):
        self.assertIn("<Audio src={staticFile(chapter.audio)}", STORY)
        self.assertIn("startMs", STORY)
        self.assertIn("endMs", STORY)
        self.assertNotIn("playbackRate", STORY)
        self.assertIn("<CaptionOverlay", STORY)
        self.assertIn("timeOverrideSeconds={sceneTime}", STORY)

    def test_required_scientific_beats_are_present_with_cautious_scope(self):
        for claim in [
            "Nine synthetic models",
            "4.751",
            "3.884",
            "64 steps",
            "128 steps",
            "256 steps",
            "propext",
            "Classical.choice",
            "Quot.sound",
            "417.56 s",
            "654.43 s",
            "738 finite",
            "18 non-finite",
            "1.11 × 10⁻¹⁶",
            "11,424 jobs",
            "1.3023 × 10⁻⁵",
            "7.24 × 10⁻⁷",
            "4.27 × 10⁻⁸",
            "NOT CAMPAIGN EVIDENCE",
            "OpenAI",
        ]:
            self.assertIn(claim, STORY)
        self.assertNotIn("Nine model families", STORY)
        self.assertIn("Cristian Guerra", STORY)
        self.assertIn("Medellín", STORY)

    def test_narrative_beats_change_frequently_throughout_each_chapter(self):
        section = STORY.split("const beats: Beat[][] = [", 1)[1].split("\n];", 1)[0]
        chapters = re.split(r"\n  \],\n  \[", section)
        self.assertEqual(len(chapters), 5)
        for chapter in chapters:
            seconds = [int(value) for value in re.findall(r"\{ at: (\d+),", chapter)]
            self.assertGreaterEqual(len(seconds), 10)
            intervals = [right - left for left, right in zip(seconds, seconds[1:])]
            self.assertLessEqual(max(intervals), 12)

    def test_visuals_preserve_the_claimed_vector_and_error_scale(self):
        torus = STORY.split("const TorusDiagram", 1)[1].split("const ODEBars", 1)[0]
        bars = STORY.split("const ODEBars", 1)[1].split("const PhaseGraphic", 1)[0]
        self.assertIn("parallel equal-length constant-velocity arrows", torus)
        self.assertIn("((frame * 2.4) % 316)", torus)
        self.assertNotIn("rotate(", torus)
        self.assertIn("Bar length proportional to absolute error", bars)
        self.assertIn("item.value / values[0].value * 100", bars)
        self.assertIn("Math.max(2,", bars)
        self.assertNotIn("Math.sqrt", bars)

    def test_video_and_portrait_layout_keep_content_inside_safe_frame(self):
        stage = STORY.split("const StageArt", 1)[1].split("const StoryVisual", 1)[0]
        visual = STORY.split("const StoryVisual", 1)[1].split("const CaptionOverlay", 1)[0]
        captions = STORY.split("const CaptionOverlay", 1)[1].split("const ChapterSegment", 1)[0]
        self.assertIn('objectFit="contain"', stage)
        self.assertIn('width: "100%", height: vertical ? 211 : 187', stage)
        self.assertIn("TWO-PANEL FLOW CLIP · FULL FRAME", stage)
        self.assertIn("top: 42, left: 54, right: 54, display: \"grid\"", visual)
        self.assertIn("top: 145, left: 54, right: 54", visual)
        self.assertIn('fontFamily: "Inter, Avenir Next, Arial, sans-serif"', captions)
        self.assertIn('fontFamily: "inherit"', captions)
        self.assertIn("minWidth: 0, maxWidth: \"100%\", overflowWrap: \"anywhere\"", visual)

    def test_final_chapter_points_to_the_live_public_repository(self):
        self.assertIn("The public repository links source, records and reproducible checks", STORY)
        self.assertNotIn("publication remains a separate review decision", STORY)

    def test_spanish_exports_use_spanish_audio_and_actual_caption_timing(self):
        self.assertEqual(SPANISH_MEDIA["status"], "ready")
        self.assertEqual(SPANISH_MEDIA["language"], "es")
        self.assertEqual(SPANISH_MEDIA["fps"], 30)
        self.assertEqual(len(SPANISH_MEDIA["chapters"]), 5)
        self.assertIn('id="ES-V2-Long"', REGISTRATIONS)
        self.assertIn('language="es"', REGISTRATIONS)
        self.assertEqual(len(PLAN["youtube"]["spanish"]["shorts"]), 5)
        self.assertEqual(PLAN["youtube"]["spanish"]["long_video"]["composition_id"], "ES-V2-Long")
        for index, item in enumerate(PLAN["youtube"]["spanish"]["shorts"]):
            self.assertIn(item["composition_id"], REGISTRATIONS)
            self.assertIn(f"durationInFrames={{spanishMedia.chapters[{index}].clip_end_frame}}", REGISTRATIONS)
        self.assertIn('const cue = spanishMedia.chapters[chapterIndex].captions.find((caption) => caption.text.includes(anchor))', STORY)
        spanish_beat_source = STORY.split("const spanishBeats", 1)[1].split("const getSpanishBeats", 1)[0]
        beat_chapters = re.split(r"\n  \],\n  \[", spanish_beat_source)
        self.assertEqual(len(beat_chapters), 5)
        for beat_source, chapter in zip(beat_chapters, SPANISH_MEDIA["chapters"]):
            anchors = re.findall(r'anchor: "([^"]+)"', beat_source)
            self.assertGreaterEqual(len(anchors), 10)
            start_times = []
            for anchor in anchors:
                cue = next((item for item in chapter["captions"] if anchor in item["text"]), None)
                self.assertIsNotNone(cue, (chapter["id"], anchor))
                start_times.append(cue["startMs"] / 1000)
            self.assertEqual(start_times, sorted(start_times), chapter["id"])
            self.assertLessEqual(max(right - left for left, right in zip(start_times, start_times[1:])), 12, chapter["id"])
        cursor = 0
        for chapter in SPANISH_MEDIA["chapters"]:
            self.assertEqual(chapter["from_frame"], cursor)
            self.assertGreater(chapter["duration_in_frames"], chapter["clip_end_frame"])
            self.assertTrue((ROOT / "video/public" / chapter["audio"]).is_file())
            cursor += chapter["duration_in_frames"]
        self.assertEqual(cursor, SPANISH_MEDIA["long_duration_in_frames"])
        for phrase in ["¿Qué puede demostrar una prueba?", "Nueve modelos sintéticos", "Control periódico independiente", "Registros pareados, no 168 casos", "Una ruta de evidencia revisable"]:
            self.assertIn(phrase, STORY)


if __name__ == "__main__":
    unittest.main()
