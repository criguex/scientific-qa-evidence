import unittest

try:
    from .mutate_export import mutate
    from .run_kernel_controls import classify_lean, classify_nanoda, nanoda_config
except ImportError:
    from mutate_export import mutate
    from run_kernel_controls import classify_lean, classify_nanoda, nanoda_config


class MutateExportTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            {"meta": {"format": {"version": "3.1.0"}}},
            {"in": 1, "str": {"pre": 0, "str": "target"}},
            {"in": 2, "str": {"pre": 0, "str": "wrong"}},
            {"ie": 10, "sort": 0},
            {"ie": 11, "sort": 1},
            {"thm": {"all": [1], "levelParams": [], "name": 1, "type": 10, "value": 10}},
            {"thm": {"all": [2], "levelParams": [], "name": 2, "type": 11, "value": 11}},
        ]

    def test_normalizes_target_after_referenced_expression(self):
        baseline, mutant, _ = mutate(self.records)
        self.assertEqual(baseline[-1]["thm"]["name"], 1)
        prior_exprs = {record["ie"] for record in mutant[:-1] if "ie" in record}
        self.assertIn(mutant[-1]["thm"]["value"], prior_exprs)

    def test_pair_differs_only_in_target_value(self):
        baseline, mutant, _ = mutate(self.records)
        differences = []
        for index, (left, right) in enumerate(zip(baseline, mutant)):
            if left != right:
                differences.append(index)
                self.assertEqual(set(left), set(right))
                self.assertEqual(set(left["thm"]) - {"value"}, set(right["thm"]) - {"value"})
                self.assertEqual(index, len(baseline) - 1)
        self.assertEqual(len(differences), 1)
        self.assertNotEqual(baseline[-1]["thm"]["value"], mutant[-1]["thm"]["value"])

    def test_lean_rejection_requires_kernel_type_mismatch_marker(self):
        self.assertEqual(classify_lean(2, "", "LEAN_KERNEL_REJECT: parser failed"), "REPLAY_REJECTION_UNCLASSIFIED")
        self.assertEqual(classify_lean(2, "", "LEAN_KERNEL_REJECT: (kernel) declaration type mismatch"), "KERNEL_TYPE_MISMATCH_REJECT")
        self.assertEqual(classify_lean(3, "", "EXPORT_PARSE_REJECT: Expr not found"), "EXPORT_PARSE_FAILURE")

    def test_nanoda_acceptance_requires_exact_success_line(self):
        self.assertEqual(classify_nanoda(0, "Checked 2 declarations with no errors"), "ACCEPT")
        self.assertEqual(classify_nanoda(0, "Checked 2 declarations with no typechecker errors, 1 pretty printer error"), "SUCCESS_MARKER_MISSING")
        self.assertEqual(classify_nanoda(1, "assertion failed"), "NONZERO_UNCLASSIFIED")

    def test_nanoda_config_prints_axioms_without_weakening_the_allowlist(self):
        config = nanoda_config("baseline.ndjson")
        self.assertTrue(config["print_axioms"])
        self.assertTrue(config["pp_to_stdout"])
        self.assertTrue(config["unpermitted_axiom_hard_error"])
        self.assertEqual(config["permitted_axioms"], ["propext", "Classical.choice", "Quot.sound"])
        self.assertEqual(config["num_threads"], 1)


if __name__ == "__main__":
    unittest.main()
