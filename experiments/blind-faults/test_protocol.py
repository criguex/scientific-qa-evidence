import unittest

import protocol_lib as P


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.base = P.clean_case()

    def test_clean_passes_both(self):
        self.assertEqual(P.baseline(self.base), (True, []))
        self.assertEqual(P.protocol(self.base), (True, []))

    def test_positive_control_f6_caught_by_both(self):
        faulty = P.inject(self.base, "F6")
        self.assertFalse(P.baseline(faulty)[0])
        self.assertFalse(P.protocol(faulty)[0])

    def test_f1_f2_f4_f5_pass_baseline_but_protocol_flags(self):
        for fault in ("F1", "F2", "F4", "F5"):
            faulty = P.inject(self.base, fault)
            self.assertTrue(P.baseline(faulty)[0], f"{fault}: baseline should accept")
            accepted, flags = P.protocol(faulty)
            self.assertFalse(accepted, f"{fault}: protocol should flag")
            self.assertTrue(flags, f"{fault}: protocol should name a check")

    def test_each_fault_changes_exactly_one_artifact(self):
        for fault in ("F1", "F2", "F4", "F5", "F6"):
            faulty = P.inject(self.base, fault)
            changed = [k for k in self.base if self.base[k] != faulty.get(k)]
            self.assertEqual(len(changed), 1, f"{fault} changed {changed}")

    def test_clean_injection_is_identity(self):
        self.assertEqual(P.inject(self.base, "C"), self.base)


if __name__ == "__main__":
    unittest.main()
