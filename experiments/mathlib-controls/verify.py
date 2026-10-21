import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
LEAN = HERE / "lean"

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
SORRY = re.compile(r"declaration uses [`'‘’\"]?sorry")
CLASS = {"equivalence": "CHANGED_EQUIVALENT", "weaker": "CHANGED_WEAKER", "refutation": "CHANGED_FALSE"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_receipts(res=RES, lean=LEAN):
    receipts = {}
    for line in (res / "receipts.jsonl").read_text().splitlines():
        r = json.loads(line)
        folder = "comparator" if r["step"] == "comparator" else "second_route"
        r["stdout"] = (res / folder / f"{r['case']}.stdout.log").read_text()
        r["stderr"] = (res / folder / f"{r['case']}.stderr.log").read_text()
        assert sha256(res / folder / f"{r['case']}.stdout.log") == r["stdout_sha256"], f"stdout hash mismatch: {r['case']}"
        assert sha256(res / folder / f"{r['case']}.stderr.log") == r["stderr_sha256"], f"stderr hash mismatch: {r['case']}"
        for rel, digest in r["inputs"].items():
            assert sha256(lean / rel) == digest, f"input hash mismatch: {rel}"
        assert isinstance(r["exit_code"], int), f"missing exit code: {r['case']}"
        receipts[(r["step"], r["case"])] = r
    return receipts


def comparator_verdict(r):
    if r["exit_code"] == 0 and "Your solution is okay!" in r["stdout"]:
        return "ACCEPTED"
    if r["exit_code"] != 0 and "statement do not match" in r["stdout"] + r["stderr"]:
        return "REJECTED_STATEMENT"
    return "OTHER"


def route_ok(r, guarded):
    if r is None or r["exit_code"] != 0:
        return False
    text = r["stdout"] + r["stderr"]
    if re.search(r"(^|\s)error", text) or SORRY.search(text):
        return False
    return all(re.search(rf"guard: \S*\.{name} uses none", text) for name in guarded)


def classify(case, verdict, receipts):
    if verdict == "ACCEPTED":
        return "ACCEPTED_BY_CHECKER"
    if verdict != "REJECTED_STATEMENT" or case not in ROUTES:
        return "CHANGED_UNKNOWN"
    name, kind, guarded = ROUTES[case]
    if not route_ok(receipts.get(("second_route", name)), guarded):
        return "CHANGED_UNKNOWN"
    return CLASS[kind]


def evaluate(res=RES, lean=LEAN):
    receipts = load_receipts(res, lean)
    expected = json.loads((HERE / "expected.json").read_text())
    rows = []
    for c in expected["cases"]:
        verdict = comparator_verdict(receipts[("comparator", c["challenge"])])
        got = classify(c["id"], verdict, receipts)
        want = c["class"].split(",")[0].strip()
        rows.append({"id": c["id"], "comparator": verdict, "class": got, "expected": want, "match": got == want})
    cheat = receipts[("second_route", "PrimesReformCheat")]
    guard_ok = cheat["exit_code"] != 0 and "guard: QAControls.SecondRoute.primes_reform_equiv_cheat depends on Nat.exists_infinite_primes" in cheat["stdout"] + cheat["stderr"]
    dct = receipts[("second_route", "DCTReform")]
    signed_ok = route_ok(dct, []) and "theorem isolated_condition_not_integrable" in (lean / "QAControls/SecondRoute/DCTReform.lean").read_text()
    guard_built = receipts[("build", "Guard")]["exit_code"] == 0
    return rows, guard_ok, signed_ok, guard_built


def main():
    rows, guard_ok, signed_ok, guard_built = evaluate()
    for r in rows:
        print(f"{r['id']:16} {r['comparator']:19} {r['class']:22} {'OK' if r['match'] else 'MISMATCH (expected ' + r['expected'] + ')'}")
    print(f"guard built: {'OK' if guard_built else 'FAIL'}; cheat rejected by the guard: {'OK' if guard_ok else 'FAIL'}; signed-bound refutation: {'OK' if signed_ok else 'FAIL'}")
    assert all(r["match"] for r in rows) and guard_ok and signed_ok and guard_built
    print(f"PASS: {len(rows)} cases match the pre-registered classes; controls as registered. "
          "This checks the published records against their receipts; it does not rerun Lean.")


if __name__ == "__main__":
    main()
