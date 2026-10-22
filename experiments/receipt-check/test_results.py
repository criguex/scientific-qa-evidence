import difflib
import json
import unittest
from pathlib import Path

import check_p6

HERE = Path(__file__).resolve().parent
RES = HERE / "results"


def receipts():
    return [json.loads(line) for line in (RES / "receipts.jsonl").read_text().splitlines()]


class ReceiptCheck(unittest.TestCase):
    def test_variants_differ_only_in_one_receipt_row(self):
        for name in ("build.log", "cache_get.log", "comparator.log"):
            self.assertEqual((RES / "C" / name).read_bytes(), (RES / "F5" / name).read_bytes())
        diff = [line for line in difflib.unified_diff((RES / "C" / "receipt.tsv").read_text().splitlines(),
                                                      (RES / "F5" / "receipt.tsv").read_text().splitlines(), lineterm="", n=0)
                if line[:1] in "+-" and not line.startswith(("+++", "---"))]
        self.assertEqual(len(diff), 2)
        self.assertIn("comparator.log", diff[0])
        self.assertIn("comparator-run.log", diff[1])

    def test_published_procedure_passes_both_variants_identically(self):
        z = {r["variant"]: r for r in receipts() if r["step"] == "Z_comparator"}
        self.assertEqual(z["C"]["exit_code"], 0)
        self.assertEqual(z["F5"]["exit_code"], 0)
        self.assertEqual(z["C"]["log_sha256"], z["F5"]["log_sha256"])
        self.assertTrue((RES / "C.Z.log").read_text().rstrip().endswith("Your solution is okay!"))
        self.assertEqual((RES / "C.Z.log").read_bytes(), (RES / "F5.Z.log").read_bytes())

    def test_p6_recomputed_from_the_published_bundles(self):
        self.assertEqual(check_p6.p6_flags(RES / "C"), [])
        self.assertEqual(check_p6.p6_flags(RES / "F5"), ["P6:receipt-log-missing-comparator-run.log"])

    def test_recorded_x_matches_expectation(self):
        expected = json.loads((HERE / "expected.json").read_text())["variants"]
        x = {r["variant"]: r["exit_code"] for r in receipts() if r["step"] == "X_p6"}
        self.assertEqual(x, {"C": expected["C"]["X"]["exit"], "F5": expected["F5"]["X"]["exit"]})
        for v in ("C", "F5"):
            self.assertEqual(json.loads((RES / f"{v}.X.json").read_text())["p6_flags"], expected[v]["X"]["p6_flags"])


if __name__ == "__main__":
    unittest.main()


RES2 = HERE / "results2"


class SubstitutedLog(unittest.TestCase):
    def test_checks_recomputed_from_the_published_bundles(self):
        import check_hash
        self.assertEqual(check_p6.p6_flags(RES2 / "C"), [])
        self.assertEqual(check_hash.hash_flags(RES2 / "C"), [])
        self.assertEqual(check_p6.p6_flags(RES2 / "F7"), [])
        self.assertEqual(check_hash.hash_flags(RES2 / "F7"), ["H:log-hash-mismatch-comparator.log"])
        self.assertEqual(check_hash.hash_flags(RES2 / "F5"), ["H:log-missing-comparator-run.log"])

    def test_f7_changes_only_the_comparator_log(self):
        for name in ("build.log", "cache_get.log", "receipt.tsv"):
            self.assertEqual((RES2 / "C" / name).read_bytes(), (RES2 / "F7" / name).read_bytes())
        self.assertEqual((RES2 / "F7" / "comparator.log").read_bytes(),
                         (HERE.parents[1] / "evidence/formal/b5/comparator5_NavierStokes.stdout.log").read_bytes())

    def test_procedure_output_does_not_see_the_substitution(self):
        self.assertEqual((RES2 / "F5.Z.log").read_bytes(), (RES2 / "F7.Z.log").read_bytes())
        z = {r["variant"]: r["exit_code"] for r in map(json.loads, (RES2 / "receipts.jsonl").read_text().splitlines()) if r["step"] == "Z_comparator"}
        self.assertEqual(z, {"C": 0, "F5": 0, "F7": 0})

    def test_recorded_outcomes_match_registration(self):
        expected = json.loads((HERE / "expected2.json").read_text())["variants"]
        got = {(r["variant"], r["step"]): r["exit_code"] for r in map(json.loads, (RES2 / "receipts.jsonl").read_text().splitlines())}
        for v, e in expected.items():
            self.assertEqual(got[(v, "Z_comparator")], e["Z"]["exit"])
            self.assertEqual(got[(v, "X1_p6")], e["X1"]["exit"])
            self.assertEqual(got[(v, "X2_hash")], e["X2"]["exit"])


class HashCheckStandalone(unittest.TestCase):
    def bundle(self, receipt=None, drop=None):
        import shutil
        import tempfile
        d = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, d)
        shutil.copytree(RES2 / "C", d / "b")
        if drop:
            (d / "b" / drop).unlink()
        if receipt is not None:
            (d / "b" / "receipt.tsv").write_text(receipt)
        return d / "b"

    def flags(self, **kwargs):
        import check_hash
        return check_hash.hash_flags(self.bundle(**kwargs))

    def rows(self):
        return (RES2 / "C" / "receipt.tsv").read_text().splitlines()

    def test_empty_receipt_is_rejected(self):
        self.assertEqual(self.flags(receipt=""), ["H:receipt-header"])

    def test_header_only_receipt_reports_every_step_missing(self):
        self.assertEqual(self.flags(receipt=self.rows()[0] + "\n"),
                         ["H:step-missing-cache_get", "H:step-missing-build", "H:step-missing-comparator"])

    def test_missing_receipt_is_rejected(self):
        self.assertEqual(self.flags(drop="receipt.tsv"), ["H:receipt-missing"])

    def test_wrong_header_is_rejected(self):
        self.assertEqual(self.flags(receipt="\n".join(["a\tb\tc\td"] + self.rows()[1:]) + "\n"), ["H:receipt-header"])

    def test_malformed_row_is_reported(self):
        r = self.rows()
        self.assertEqual(self.flags(receipt="\n".join(r[:3] + ["comparator only three\tfields\there"]) + "\n"),
                         ["H:receipt-row-malformed-4", "H:step-missing-comparator"])

    def test_dropped_row_is_reported(self):
        r = self.rows()
        self.assertEqual(self.flags(receipt="\n".join(r[:3]) + "\n"), ["H:step-missing-comparator"])

    def test_duplicated_row_is_reported(self):
        r = self.rows()
        self.assertEqual(self.flags(receipt="\n".join(r + [r[3]]) + "\n"), ["H:step-duplicate-comparator"])

    def test_unexpected_step_is_reported(self):
        r = self.rows()
        self.assertEqual(self.flags(receipt="\n".join(r + ["extra\tx\tbuild.log\t0"]) + "\n"), ["H:step-unexpected-extra"])
