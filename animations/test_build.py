import hashlib
import tempfile
import unittest
from pathlib import Path

import build


class AnimationPackageTests(unittest.TestCase):
    def test_source_hashes_match_allowlisted_inputs(self):
        package = build.load_package()
        for entry in package["source_hashes"].values():
            path = build.ROOT / entry["path"]
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(entry["sha256"], digest)

    def test_campaign_counts_are_paired_per_host(self):
        campaign = build.load_package()["animations"]["campaign"]
        self.assertEqual(campaign["per_host"]["variant_evaluations"], 84)
        self.assertEqual(campaign["per_host"]["classification_counts"], {"PASS": 27, "KILLED": 54, "SURVIVED": 3})
        self.assertTrue(campaign["paired_variant_records"])
        self.assertEqual(len(campaign["per_host"]["hosts"]), 2)

    def test_control_outcomes_and_observation_data_are_source_derived(self):
        animations = build.load_package()["animations"]
        self.assertEqual(animations["rc"]["baseline"]["status"], "PASS")
        self.assertEqual(animations["rc"]["mutation"]["status"], "KILLED")
        for actual, expected in zip(animations["chemistry"]["baseline"]["recorded_rk4_mol_l"], [0.8, 0.6, 0.48, 0.4]):
            self.assertAlmostEqual(actual, expected, places=8)
        self.assertEqual(animations["cooling"]["mutation"]["invariants"], "ok")
        self.assertEqual(animations["snell"]["mutation"]["status"], "KILLED")
        self.assertEqual(animations["formal"]["nanoda_mutant_raw"], "COLLECTED_PENDING_CLASSIFICATION")
        self.assertEqual(animations["formal"]["nanoda_mutant_derived"], "TYPECHECK_ASSERTION_REJECT_DERIVED")

    def test_standalone_outputs_are_offline_accessible_and_deterministic(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            build.generate(Path(first))
            build.generate(Path(second))
            for animation_id in build.PAGES:
                filename = f"{animation_id}.html"
                content = (Path(first) / filename).read_text(encoding="utf-8")
                self.assertIn('lang="en"', content)
                self.assertIn("window.renderAt=renderAt", content)
                self.assertIn("How to read this animation", content)
                self.assertIn(build.AUTHOR, content)
                self.assertNotIn("media/animations/", content)
                self.assertNotIn("<script src=", content.lower())
                self.assertNotIn("<link rel=\"stylesheet\" href=", content.lower())
                self.assertEqual(content, (Path(second) / filename).read_text(encoding="utf-8"))
            self.assertEqual((Path(first) / "manifest.json").read_bytes(), (Path(second) / "manifest.json").read_bytes())

    def test_gallery_has_single_embed_scene_specific_note_and_download_targets(self):
        with tempfile.TemporaryDirectory() as output:
            build.generate(Path(output))
            gallery = (Path(output) / "index.html").read_text(encoding="utf-8")
            self.assertEqual(gallery.count("<iframe"), 1)
            self.assertIn("id=\"active-note\"", gallery)
            self.assertIn("../docs/assets/flow-preview.gif", gallery)
            self.assertNotIn("media/animations/", gallery)
            for animation_id in build.PAGES:
                self.assertIn(f'data-id="{animation_id}"', gallery)

    def test_validation_verdicts_are_known_and_records_are_private(self):
        validation = build.load_package()["animations"]["validation"]
        allowed = {"PENDING", "ACCEPTED", "CONTROL_ACCEPTED", "CONTROL_FAILED", "KILLED", "SURVIVED", "REJECTED", "OK", "FAILED"}
        for check in validation["checks"]:
            self.assertTrue(check["verdict"] in allowed or check["verdict"].startswith(("INVALID", "KILLED_BUT", "FAILED", "TARBALL")), check)
            self.assertIn(check["expected"], build.EXPECTED_VERDICTS)
        control = next(check for check in validation["checks"] if check["id"] == "mutant_control_comment")
        self.assertEqual(control["expected"], "accept")
        record_dir = build.ROOT / "evidence/formal/cd-validation"
        for path in record_dir.rglob("*"):
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.assertNotRegex(text, r"/home/|/Users/|\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.")


if __name__ == "__main__":
    unittest.main()
