import unittest

import verify


def receipt(stdout="", stderr="", rc=0):
    return {"stdout": stdout, "stderr": stderr, "exit_code": rc}


class RouteOk(unittest.TestCase):
    def test_backtick_sorry_is_rejected(self):
        self.assertFalse(verify.route_ok(receipt(stdout="warning: X.lean:5:8: declaration uses `sorry`\n"), []))

    def test_quoted_sorry_is_rejected(self):
        self.assertFalse(verify.route_ok(receipt(stdout="warning: declaration uses 'sorry'\n"), []))

    def test_empty_log_with_exit_zero_is_accepted(self):
        self.assertTrue(verify.route_ok(receipt(), []))

    def test_empty_log_with_failing_exit_is_rejected(self):
        self.assertFalse(verify.route_ok(receipt(rc=1), []))

    def test_missing_receipt_is_rejected(self):
        self.assertFalse(verify.route_ok(None, []))

    def test_error_line_is_rejected(self):
        self.assertFalse(verify.route_ok(receipt(stdout="X.lean:3:0: error: unknown identifier\n"), []))

    def test_missing_guard_line_is_rejected(self):
        self.assertFalse(verify.route_ok(receipt(), ["cs_reform_equiv"]))

    def test_guard_line_is_accepted(self):
        line = "info: guard: QAControls.SecondRoute.cs_reform_equiv uses none of the theorems under test (1 constants checked)\n"
        self.assertTrue(verify.route_ok(receipt(stdout=line), ["cs_reform_equiv"]))


class Records(unittest.TestCase):
    def test_published_records_pass(self):
        rows, guard_ok, signed_ok, guard_built = verify.evaluate()
        self.assertTrue(all(r["match"] for r in rows) and guard_ok and signed_ok and guard_built)

    def test_tampered_log_is_detected(self):
        import shutil, tempfile
        with tempfile.TemporaryDirectory() as d:
            res = verify.Path(d) / "results"
            shutil.copytree(verify.RES, res)
            p = res / "second_route" / "PrimesSwap.stdout.log"
            p.write_text(p.read_text() + " ")
            with self.assertRaises(AssertionError):
                verify.load_receipts(res, verify.LEAN)

    def test_tampered_input_is_detected(self):
        import shutil, tempfile
        with tempfile.TemporaryDirectory() as d:
            lean = verify.Path(d) / "lean"
            shutil.copytree(verify.LEAN, lean)
            p = lean / "QAControls" / "SecondRoute" / "PrimesSwap.lean"
            p.write_text(p.read_text() + "\n")
            with self.assertRaises(AssertionError):
                verify.load_receipts(verify.RES, lean)


if __name__ == "__main__":
    unittest.main()
