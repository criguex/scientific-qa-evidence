import json
import math
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import oracles
import runner
import sut
from suite import CASES

SAVED = Path(__file__).resolve().parents[1] / "paired" / "macos-arm64"


def raise_runtime_error(*args, **kwargs):
    raise RuntimeError("forced")


class RunnerExceptionTests(unittest.TestCase):
    def test_oracle_exception_marks_oracle_invalid(self):
        with mock.patch.object(oracles, "evaluate", raise_runtime_error):
            result = runner.run_variant(CASES[0], "baseline")
        self.assertFalse(result["oracle_valid"])
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertEqual(result["return_code"], 1)
        self.assertEqual(result["invariants"]["exception"], "oracle:RuntimeError")

    def test_sut_exception_keeps_oracle_valid(self):
        with mock.patch.object(sut, "evaluate", raise_runtime_error):
            result = runner.run_variant(CASES[0], "baseline")
        self.assertTrue(result["oracle_valid"])
        self.assertEqual(result["status"], "INCONCLUSIVE")
        self.assertEqual(result["invariants"]["exception"], "sut:RuntimeError")

    def test_mutant_exception_is_inconclusive_not_killed(self):
        with mock.patch.object(sut, "evaluate", raise_runtime_error):
            result = runner.run_variant(CASES[0], "tau_double", baseline_status="PASS")
        self.assertEqual(result["status"], "INCONCLUSIVE")


class RunnerRegressionTests(unittest.TestCase):
    def test_rerun_reproduces_saved_campaign(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "rerun"
            with mock.patch("builtins.print"):
                self.assertEqual(runner.main(["--out", str(out)]), 0)
            summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["counts"], {"KILLED": 54, "PASS": 27, "SURVIVED": 3})
            for saved_path in sorted(SAVED.glob("case_*.json")):
                saved = json.loads(saved_path.read_text(encoding="utf-8"))
                fresh = json.loads((out / saved_path.name).read_text(encoding="utf-8"))
                for key in ("case_id", "variant", "status", "oracle_valid", "invariants"):
                    self.assertEqual(fresh[key], saved[key], f"{saved_path.name} {key}")
                for resolution, values in saved["values"].items():
                    for old, new in zip(values, fresh["values"][resolution]):
                        if old is None:
                            self.assertIsNone(new)
                        else:
                            self.assertLessEqual(abs(old - new), 1e-12 * max(1.0, abs(old)), saved_path.name)


if __name__ == "__main__":
    unittest.main()
