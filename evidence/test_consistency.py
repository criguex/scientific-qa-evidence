import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
README_ES = (ROOT / "README.es.md").read_text(encoding="utf-8")
CLAIMS = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
DERIVED = json.loads((ROOT / "evidence/numerical/multidomain_derived.json").read_text(encoding="utf-8"))
RESULTS = json.loads((ROOT / "evidence/formal/cd-validation/results.json").read_text(encoding="utf-8"))
PROVENANCE = json.loads((ROOT / "evidence/formal/statement-provenance/result.json").read_text(encoding="utf-8"))
RISK = (ROOT / "evidence/formal/clay-lean-risk.md").read_text(encoding="utf-8")


class ConsistencyTests(unittest.TestCase):
    def test_numerical_counts_match_the_derived_record(self):
        counts = DERIVED["per_host"]["classification_counts"]
        for text in (README, README_ES, CLAIMS):
            for status in ("PASS", "KILLED", "SURVIVED"):
                self.assertIn(f"{counts[status]} {status}", text)
        self.assertIn("51 distinct killed behaviors", README)
        self.assertIn("51 comportamientos eliminados distintos", README_ES)
        self.assertIn("51 distinct killed behaviors", CLAIMS)

    def test_synthetic_models_are_not_presented_as_experiments(self):
        self.assertIn("not physical experiments", CLAIMS)
        self.assertIn("none of this is an empirical measurement", README)

    def test_revalidation_check_count_matches_results(self):
        total = len(RESULTS["checks"])
        done = sum(check["verdict"] != "PENDING" for check in RESULTS["checks"])
        if RESULTS["state"] == "complete":
            self.assertIn(f"All {total} checks finished", README)
            self.assertIn(f"Terminaron las {total} pruebas", README_ES)
        else:
            self.assertIn(f"{done} of {total} checks have finished", README)
            self.assertIn(f"Terminaron {done} de {total} pruebas", README_ES)
        cd_readme = (ROOT / "evidence/formal/cd-validation/README.md").read_text(encoding="utf-8")
        self.assertIn(f"of {total} checks recorded", cd_readme)

    def test_statement_scope_is_textual(self):
        named = len(PROVENANCE["identical_names"])
        english = f"The {named} declarations match after textual normalization; name resolution was not verified."
        for text in (README, CLAIMS, (ROOT / "evidence/formal/statement-provenance/README.md").read_text(encoding="utf-8")):
            self.assertIn(english, text)
        self.assertIn(f"Las {named} declaraciones coinciden tras normalización textual; la resolución de nombres no se verificó.", README_ES)

    def test_risk_counts_match_the_review(self):
        rows, direct, standard, attention = map(int, re.search(r"\*\*Count:\*\* (\d+) rows\. (\d+) direct, (\d+) equal by a standard fact, (\d+) needing attention", RISK).groups())
        self.assertEqual(direct + standard + attention, rows)
        self.assertIn(f"{rows} clauses: {direct} direct, {standard} via named standard facts, {attention} needing a human decision", CLAIMS)
        self.assertIn(f"Of {rows} clauses, {direct} match directly, {standard} match", README)

    def test_no_placeholders_remain(self):
        for text in (README, README_ES, CLAIMS):
            self.assertNotRegex(text, r"\b(?:B4_RESULT|RUNS)_[A-Z]{2}\b")


if __name__ == "__main__":
    unittest.main()
