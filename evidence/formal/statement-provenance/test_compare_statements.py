import unittest

from compare_statements import compare


class CompareStatementsTests(unittest.TestCase):
    def test_comments_and_whitespace_do_not_count(self):
        reference = "/-- doc -/\ntheorem t (nu : ℝ) (h : nu > 0) :\n    True := by\n  sorry\n"
        candidate = "-- note\ntheorem t (nu : ℝ)   (h : nu > 0) : True := by sorry\n"
        result = compare(reference, candidate)
        self.assertEqual(result["only_in_reference"], [])
        self.assertEqual(result["only_in_candidate"], [])

    def test_a_changed_hypothesis_is_reported(self):
        result = compare("theorem t (h : nu > 0) : True := by sorry\n", "theorem t (h : nu ≥ 0) : True := by sorry\n")
        self.assertEqual(result["only_in_reference"], ["theorem t (h : nu > 0) : True := by sorry"])
        self.assertEqual(result["only_in_candidate"], ["theorem t (h : nu ≥ 0) : True := by sorry"])


if __name__ == "__main__":
    unittest.main()
