import math
import csv
import io
import json
import contextlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

import runner
import sut
import oracles
from suite import CASES, OBSERVATION_FRACTIONS, TOLERANCE


class ContractTests(unittest.TestCase):
    def test_invalid_baseline_blocks_mutant_kill(self):
        self.assertEqual(runner.classify_variant(False, "BASELINE_INVALID", False, 1.0), "BLOCKED_BASELINE")

    def test_nan_never_passes(self):
        self.assertEqual(runner.classify_variant(True, "PASS", True, math.nan), "BASELINE_INVALID")
        self.assertEqual(runner.classify_variant(False, "PASS", True, math.nan), "KILLED")

    def test_mutations_change_rhs_or_conservation_at_multiple_points(self):
        for case_id, mutant in (("rc_01", "rhs_sign"), ("chemical_second_order_01", "rhs_sign"), ("acoustic_interface_01", "pressure_boundary_sign")):
            case = next(c for c in CASES if c["case_id"] == case_id)
            baseline = sut.evaluate(case, "baseline", 64)
            changed = sut.evaluate(case, mutant, 64)
            self.assertEqual(len(baseline), len(changed))
            self.assertGreater(sum(abs(a-b) for a, b in zip(baseline, changed)), 1e-8)
            self.assertGreater(sum(abs(a-b) for a, b in zip(baseline[:2], changed[:2])), 1e-8)
        acoustic = next(c for c in CASES if c["case_id"] == "acoustic_interface_01")
        mutated_pressure = sut.evaluate(acoustic, "pressure_boundary_sign", 64)[-2:]
        p = acoustic["params"]
        energy = (mutated_pressure[0] / p["pi"]) ** 2 + (p["z1"] / p["z2"]) * (mutated_pressure[1] / p["pi"]) ** 2
        self.assertGreater(abs(energy - 1), 1e-6)

    def test_tiny_rc_calibration_is_allowed_to_survive(self):
        case = next(c for c in CASES if c["case_id"] == "rc_01")
        perturbed = sut.evaluate(case, "tau_tiny", 256)
        import oracles
        expected = oracles.evaluate(case, 256)
        error = max(abs(a-b) for a, b in zip(perturbed, expected)) / case["scale"]
        self.assertLessEqual(error, TOLERANCE)
        self.assertEqual(runner.classify_variant(False, "PASS", True, error), "SURVIVED")

    def test_independent_oracles_agree_at_multiple_observations(self):
        for case in CASES:
            resolutions = (64, 128, 256) if case["model"] in runner.REFINED_MODELS else (1,)
            for steps in resolutions:
                actual = sut.evaluate(case, "baseline", steps)
                expected = oracles.evaluate(case, steps)
                error = max(abs(a-b) for a, b in zip(actual, expected)) / case["scale"]
                self.assertLessEqual(error, TOLERANCE, case["case_id"])
                valid, reason = runner.invariants(case, actual)
                self.assertTrue(valid, f"{case['case_id']}: {reason}")
                self.assertEqual(runner.classify_variant(True, "PASS", valid, error), "PASS", case["case_id"])

    def test_existing_output_directory_is_refused(self):
        with tempfile.TemporaryDirectory() as parent:
            marker = Path(parent) / "keep.txt"
            marker.write_text("evidence stays", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                runner.main(["--out", parent])
            self.assertEqual(marker.read_text(encoding="utf-8"), "evidence stays")

    def test_run_variant_pass_and_nan_serialization(self):
        case = next(c for c in CASES if c["case_id"] == "rc_01")
        good = runner.run_variant(case, "baseline")
        self.assertEqual(good["status"], "PASS")
        self.assertEqual(good["return_code"], 0)
        with patch.object(sut, "evaluate", return_value=[math.nan] * 4):
            bad = runner.run_variant(case, "baseline")
        self.assertEqual(bad["status"], "BASELINE_INVALID")
        self.assertTrue(bad["non_finite_observed"])
        self.assertIsNone(bad["values"]["256"][0])
        json.dumps(bad, allow_nan=False)

    def test_oracle_nonfinite_after_first_entry_is_inconclusive(self):
        case = next(c for c in CASES if c["case_id"] == "rc_01")
        with patch.object(oracles, "evaluate", return_value=[0.0, math.nan, 0.0, 0.0]):
            result = runner.run_variant(case, "baseline")
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertFalse(result["oracle_valid"])

    def test_full_runner_csv_preserves_every_json_value_and_component(self):
        with tempfile.TemporaryDirectory() as parent:
            out = Path(parent) / "evidence"
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(runner.main(["--out", str(out)]), 0)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["variant_evaluations"], 84)
            expected = {}
            for file_path in sorted(out.glob("case_*.json")):
                result = json.loads(file_path.read_text(encoding="utf-8"))
                base_case_id = result["case_id"].removesuffix("_tiny")
                case = next(item for item in CASES if item["case_id"] == base_case_id)
                for resolution, values in result["values"].items():
                    step_count = 1 if resolution == "N/A" else int(resolution)
                    reference = oracles.evaluate(case, step_count)
                    for i, value in enumerate(values):
                        point = i // 2 if result["model"] == "acoustic_interface" else i
                        fraction = str(OBSERVATION_FRACTIONS[point])
                        component = ("reflected_pressure" if i % 2 == 0 else "transmitted_pressure") if result["model"] == "acoustic_interface" else "scalar"
                        key = (result["case_id"], result["model"], result["variant"], resolution, fraction, component)
                        point_error = abs(value - reference[i]) / result["scale"] if value is not None and math.isfinite(value) and math.isfinite(reference[i]) else None
                        expected[key] = (value, reference[i] if math.isfinite(reference[i]) else None, result["normalized_error"].get(resolution), point_error)
            with (out / "observations.csv").open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 756)
            self.assertEqual(len(rows), len(expected))
            observed = {}
            for row in rows:
                key = (row["case_id"], row["model"], row["variant"], row["resolution"], row["fraction"], row["component"])
                observed[key] = (
                    float(row["value"]) if row["value"] else None,
                    float(row["oracle"]) if row["oracle"] else None,
                    float(row["max_normalized_error"]) if row["max_normalized_error"] else None,
                    float(row["point_normalized_error"]) if row["point_normalized_error"] else None,
                )
            self.assertEqual(set(observed), set(expected))
            for key, (value, reference, max_error, point_error) in expected.items():
                self.assertEqual(observed[key][0] is None, value is None)
                if value is not None:
                    self.assertAlmostEqual(observed[key][0], value, places=12)
                if reference is None:
                    self.assertIsNone(observed[key][1])
                else:
                    self.assertAlmostEqual(observed[key][1], reference, places=12)
                if max_error is None:
                    self.assertIsNone(observed[key][2])
                else:
                    self.assertAlmostEqual(observed[key][2], max_error, places=12)
                if point_error is None:
                    self.assertIsNone(observed[key][3])
                else:
                    self.assertAlmostEqual(observed[key][3], point_error, places=12)
            acoustic_rows = [row for row in rows if row["model"] == "acoustic_interface"]
            self.assertEqual(len(acoustic_rows), 3 * 3 * 8)
            self.assertEqual(sum(row["component"] == "reflected_pressure" for row in acoustic_rows), 3 * 3 * 4)


if __name__ == "__main__":
    unittest.main()
