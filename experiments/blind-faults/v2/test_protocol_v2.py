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


if __name__ == "__main__":
    unittest.main()
