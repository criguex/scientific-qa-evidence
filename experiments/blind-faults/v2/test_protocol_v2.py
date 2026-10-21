import json
import unittest

import protocol_lib_v2 as V2


class CleanAndControlTests(unittest.TestCase):
    def test_clean_passes_both(self):
        case = V2.clean_case()
        self.assertEqual(V2.baseline(case), (True, []))
        self.assertEqual(V2.protocol(case), (True, []))

    def test_sorry_is_caught_by_both(self):
        case = V2.clean_case()
        case["axioms.txt"] = "'demo_breakdown' depends on axioms: [propext, sorryAx]\n"
        self.assertFalse(V2.baseline(case)[0])
        self.assertFalse(V2.protocol(case)[0])


class AbsentEvidenceTests(unittest.TestCase):
    def test_each_missing_artifact_is_flagged_not_crashed(self):
        for name in V2.REQUIRED:
            case = V2.clean_case()
            del case[name]
            b_ok, b_flags = V2.baseline(case)
            p_ok, p_flags = V2.protocol(case)
            self.assertFalse(b_ok, f"baseline accepted without {name}")
            self.assertFalse(p_ok, f"protocol accepted without {name}")
            self.assertIn(f"B:missing:{name}", b_flags)

    def test_receipt_naming_absent_log_is_flagged(self):
        case = V2.clean_case()
        del case["comparator.log"]
        self.assertIn("P6:receipt-log-missing-comparator.log", V2.protocol(case)[1])


class IncompleteEvidenceTests(unittest.TestCase):
    def test_empty_axioms_report_fails_closed(self):
        case = V2.clean_case()
        case["axioms.txt"] = ""
        self.assertFalse(V2.baseline(case)[0])

    def test_truncated_axioms_report_fails_closed(self):
        case = V2.clean_case()
        case["axioms.txt"] = "'demo_breakdown' depends on axioms:\n"
        self.assertIn("B:axioms-incomplete", V2.baseline(case)[1])

    def test_truncated_numeric_summary_fails_closed(self):
        case = V2.clean_case()
        case["numeric_summary.json"] = '{"collection_complete": tr'
        self.assertIn("B:numeric-summary-unparseable", V2.baseline(case)[1])

    def test_summary_without_completion_flag_fails_closed(self):
        case = V2.clean_case()
        case["numeric_summary.json"] = json.dumps({"oracle_valid": True})
        self.assertIn("B:numeric-incomplete", V2.baseline(case)[1])

    def test_build_log_without_success_line_fails(self):
        case = V2.clean_case()
        case["build.log"] = "✔ [1/3] Built Demo.Core\n"
        self.assertIn("B:build-failed", V2.baseline(case)[1])

    def test_malformed_receipt_and_olean_rows_are_flagged(self):
        case = V2.clean_case()
        case["receipt.tsv"] += "broken-row\n"
        case["oleans.tsv"] += "Demo\tthree\tzero\n"
        flags = V2.protocol(case)[1]
        self.assertIn("P6:receipt-unparseable", flags)
        self.assertIn("P1:oleans-unparseable", flags)


class ReviewRound2Tests(unittest.TestCase):
    """Regression tests for the three defects reported in the second review."""

    def test_non_object_summary_is_rejected_not_crashed(self):
        for value in ("[]", "42", '"text"', "null"):
            case = V2.clean_case()
            case["numeric_summary.json"] = value
            b_ok, b_flags = V2.baseline(case)
            p_ok, _ = V2.protocol(case)
            self.assertFalse(b_ok, value)
            self.assertFalse(p_ok, value)
            self.assertIn("B:numeric-summary-not-object", b_flags, value)

    def test_header_only_tables_are_rejected(self):
        case = V2.clean_case()
        case["receipt.tsv"] = "step\tcommand\tlog\texit\n"
        case["oleans.tsv"] = "package\ttotal\tolder_than_build_start\n"
        accepted, flags = V2.protocol(case)
        self.assertFalse(accepted)
        self.assertIn("P6:receipt-no-rows", flags)
        self.assertIn("P1:oleans-no-rows", flags)

    def test_wrong_headers_are_rejected(self):
        case = V2.clean_case()
        case["receipt.tsv"] = case["receipt.tsv"].replace("step\tcommand", "stage\tcommand")
        self.assertIn("P6:receipt-bad-header", V2.protocol(case)[1])

    def test_nonzero_receipt_exit_codes_are_rejected(self):
        case = V2.clean_case()
        case["receipt.tsv"] = case["receipt.tsv"].replace("\t0\n", "\t1\n")
        accepted, flags = V2.protocol(case)
        self.assertFalse(accepted)
        self.assertIn("P6:receipt-exit-build-1", flags)
        self.assertIn("P6:receipt-exit-comparator-1", flags)

    def test_receipts_must_cover_build_and_comparator(self):
        case = V2.clean_case()
        case["receipt.tsv"] = "step\tcommand\tlog\texit\nbuild\tlake build\tbuild.log\t0\n"
        self.assertIn("P6:receipt-step-missing-comparator", V2.protocol(case)[1])


class Round4SemanticTests(unittest.TestCase):
    """Round 4: false accepts and false alarms found by the assistant's semantic review."""

    def assertRejected(self, case):
        self.assertFalse(V2.protocol(case)[0], V2.protocol(case))

    def assertAccepted(self, case):
        self.assertEqual(V2.protocol(case), (True, []))

    def test_every_axioms_line_is_checked(self):
        case = V2.clean_case()
        case["axioms.txt"] += "'other_thm' depends on axioms: [propext, sorryAx]\n"
        self.assertRejected(case)

    def test_axioms_must_cover_the_proved_theorem(self):
        case = V2.clean_case()
        case["axioms.txt"] = "'unrelated' depends on axioms: [propext]\n"
        self.assertIn("B:axioms-missing-for-demo_breakdown", V2.baseline(case)[1])

    def test_comparator_failure_beside_ok_line_is_rejected(self):
        case = V2.clean_case()
        case["comparator.log"] += "uncaught exception: Challenge and solution theorem statement do not match\n"
        self.assertRejected(case)

    def test_build_error_beside_success_line_is_rejected(self):
        case = V2.clean_case()
        case["build.log"] = "error: Foo.lean:3:1: unknown identifier\n" + case["build.log"]
        self.assertRejected(case)

    def test_invalid_oracle_is_rejected_even_if_complete(self):
        case = V2.clean_case()
        case["numeric_summary.json"] = json.dumps({"collection_complete": True, "oracle_valid": False, "export_errors": []})
        self.assertRejected(case)

    def test_bom_and_crlf_do_not_change_the_verdict(self):
        case = V2.clean_case()
        case = {k: "\ufeff" + v.replace("\n", "\r\n") for k, v in case.items()}
        self.assertAccepted(case)

    def test_comment_in_statement_is_not_a_difference(self):
        case = V2.clean_case()
        case["solution_statement.lean"] = "-- the challenge statement\n" + case["solution_statement.lean"]
        self.assertAccepted(case)

    def test_statement_change_still_detected_after_comment_stripping(self):
        case = V2.inject(V2.clean_case(), "F2")
        case["solution_statement.lean"] = "/- note -/\n" + case["solution_statement.lean"]
        self.assertIn("P2:statement-differs-from-reference", V2.protocol(case)[1])


if __name__ == "__main__":
    unittest.main()
