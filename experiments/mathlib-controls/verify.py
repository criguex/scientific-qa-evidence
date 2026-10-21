import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"

ROUTES = {
    "primes/defeq": ("PrimesDefeq", "equivalence", ["primes_defeq_equiv"]),
    "primes/reform": ("PrimesReform", "equivalence", ["primes_reform_equiv"]),
    "primes/bounded": ("PrimesBounded", "weaker", ["bounded_of_full", "bounded_not_imp_full"]),
    "primes/swap": ("PrimesSwap", "refutation", []),
    "cs/reform": ("CSReform", "equivalence", ["cs_reform_equiv"]),
    "cs/strict": ("CSStrict", "refutation", []),
    "dct/reform": ("DCTReform", "equivalence", ["dct_reform_equiv"]),
    "dct/nodom": ("DCTNoDom", "refutation", []),
}


def comparator_verdicts():
    rows = [line.split("\t") for line in (RES / "summary.tsv").read_text().splitlines() if line.strip()]
    return {r[0]: r[1] for r in rows}


def route_ok(log_name, guarded):
    text = (RES / "second_route" / f"{log_name}.log").read_text()
    if re.search(r"error", text) or "declaration uses 'sorry'" in text:
        return False
    return all(re.search(rf"guard: \S*{name} uses none", text) for name in guarded)


def classify(case, verdict):
    if verdict == "ACCEPTED":
        return "ACCEPTED_BY_CHECKER"
    if verdict != "REJECTED_STATEMENT" or case not in ROUTES:
        return "CHANGED_UNKNOWN"
    log_name, kind, guarded = ROUTES[case]
    if not route_ok(log_name, guarded):
        return "CHANGED_UNKNOWN"
    return {"equivalence": "CHANGED_EQUIVALENT", "weaker": "CHANGED_WEAKER", "refutation": "CHANGED_FALSE"}[kind]


def main():
    expected = json.loads((HERE / "expected.json").read_text())
    verdicts = comparator_verdicts()
    out = []
    for c in expected["cases"]:
        got = classify(c["id"], verdicts[c["challenge"]])
        want = c["class"].split(",")[0].strip()
        out.append({"id": c["id"], "comparator": verdicts[c["challenge"]], "class": got, "expected": want, "match": got == want})
    cheat = (RES / "second_route" / "PrimesReformCheat.log").read_text()
    guard_ok = "guard: QAControls.SecondRoute.primes_reform_equiv_cheat depends on Nat.exists_infinite_primes" in cheat
    signed = "isolated_condition_not_integrable" in (HERE / "lean/QAControls/SecondRoute/DCTReform.lean").read_text() and route_ok("DCTReform", [])
    for row in out:
        print(f"{row['id']:16} {row['comparator']:19} {row['class']:22} {'OK' if row['match'] else 'MISMATCH (expected ' + row['expected'] + ')'}")
    print(f"guard control (cheat rejected): {'OK' if guard_ok else 'FAIL'}")
    print(f"signed-bound control (refutation builds): {'OK' if signed else 'FAIL'}")
    assert all(r["match"] for r in out) and guard_ok and signed
    (RES / "classification.json").write_text(json.dumps({"cases": out, "guard_control": guard_ok, "signed_bound_control": signed}, indent=2) + "\n")
    print(f"PASS: {len(out)} cases match the pre-registered classes; both controls behave as registered")


if __name__ == "__main__":
    main()
