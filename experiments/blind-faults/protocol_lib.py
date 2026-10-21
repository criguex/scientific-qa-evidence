"""Shared fixtures, fault injectors and the two procedures for the blind-fault experiment.

A case is a directory of recorded artifacts of the kind the real protocol reads: a Lean
build log, an artifact-timestamp table, a solution statement and its pinned reference, an
axioms report, run receipts, and a numerical-harness summary. The experiment models the
protocol's checks over these artifacts; it does not re-run Lean. The live Lean, Comparator
and kernel runs are in the main study under evidence/formal/. Disclosed in DESIGN.md.

Blinding is guaranteed by freezing these scripts (hash in FROZEN.md) before the seed is
used, not by hiding cases: the checks are fixed and deterministic.
"""

import json
from pathlib import Path

PERMITTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CLASSES = ["F1", "F2", "F4", "F5", "F6", "C"]
PER_CLASS = 3
CLEAN = 6


def clean_case():
    """A clean case: every artifact well-formed, both procedures should accept."""
    return {
        "build.log": "info: mathlib: checking out revision ...\n"
                     "✔ [1/3] Built Demo.Core\n✔ [2/3] Built Demo.Solution\n"
                     "Build completed successfully (3 jobs).\n",
        "oleans.tsv": "package\ttotal\tolder_than_build_start\n"
                      "Demo\t3\t0\nmathlib\t2\t0\n",
        "solution_statement.lean": "theorem demo_breakdown (nu : Real) (h : nu > 0) :\n"
                                   "    Exists u, Breakdown u := by sorry\n",
        "reference.lean": "theorem demo_breakdown (nu : Real) (h : nu > 0) :\n"
                          "    Exists u, Breakdown u := by sorry\n",
        "axioms.txt": "'demo_breakdown' depends on axioms: [propext, Classical.choice, Quot.sound]\n",
        "receipt.tsv": "step\tcommand\tlog\texit\n"
                       "build\tlake build\tbuild.log\t0\n"
                       "comparator\tlake env comparator demo.json\tcomparator.log\t0\n",
        "numeric_summary.json": json.dumps({
            "collection_complete": True, "counts": {"PASS": 27, "KILLED": 54, "SURVIVED": 3},
            "oracle_valid": True, "export_errors": [],
        }, indent=2) + "\n",
    }


def inject(case, fault):
    """Return a copy of a clean case with one fault planted. Clean cases use fault 'C'."""
    c = dict(case)
    if fault == "C":
        return c
    if fault == "F1":
        # A dependency arrived prebuilt: its oleans predate the build start, but the log is clean.
        c["oleans.tsv"] = ("package\ttotal\tolder_than_build_start\n"
                           "Demo\t3\t0\nmathlib\t2\t0\nbatteries\t190\t190\n")
    elif fault == "F2":
        # The challenge statement was weakened; the solution proves the weaker claim.
        # ">= 0" instead of "> 0" admits more data, so "no solution" is easier. Reference unchanged.
        c["solution_statement.lean"] = ("theorem demo_breakdown (nu : Real) (h : nu >= 0) :\n"
                                        "    Exists u, Breakdown u := by sorry\n")
    elif fault == "F4":
        # The oracle raised an exception but the harness reported the case as passing.
        c["numeric_summary.json"] = json.dumps({
            "collection_complete": True, "counts": {"PASS": 27, "KILLED": 54, "SURVIVED": 3},
            "oracle_valid": True, "export_errors": [{"case_id": "rc_001", "exception": "oracle:ValueError"}],
        }, indent=2) + "\n"
    elif fault == "F5":
        # A receipt names a log that is not the one the build actually wrote.
        c["receipt.tsv"] = ("step\tcommand\tlog\texit\n"
                            "build\tlake build\tother-build.log\t0\n"
                            "comparator\tlake env comparator demo.json\tcomparator.log\t0\n")
    elif fault == "F6":
        # Positive control: the solution still depends on sorry.
        c["axioms.txt"] = "'demo_breakdown' depends on axioms: [propext, Classical.choice, Quot.sound, sorryAx]\n"
    else:
        raise ValueError(f"unknown fault {fault}")
    return c


# --- The two procedures. Each returns (accepted: bool, flags: list[str]). ---

def _axioms_ok(text):
    inside = text.split("[", 1)[1].rsplit("]", 1)[0] if "[" in text else ""
    used = {a.strip() for a in inside.split(",") if a.strip()}
    return used <= PERMITTED_AXIOMS


def baseline(case):
    """Procedure B: OpenAI's documented procedure, modeled over the artifacts.

    Accept iff the build succeeded, the solution uses only permitted axioms, and the
    numerical summary is complete. This is what `lake build` + Comparator + the suite report.
    """
    flags = []
    if "Build completed successfully" not in case["build.log"]:
        flags.append("B:build-failed")
    if not _axioms_ok(case["axioms.txt"]):
        flags.append("B:axioms")
    if not json.loads(case["numeric_summary.json"]).get("collection_complete"):
        flags.append("B:numeric-incomplete")
    return (not flags, flags)


def _norm(src):
    return [" ".join(line.split()) for line in src.splitlines() if line.strip()]


def protocol(case):
    """Procedure P: the baseline plus the protocol's own checks P1, P2, P5, P6."""
    accepted_b, flags = baseline(case)
    flags = list(flags)
    # P1: artifact check — a package built locally must have no pre-dated oleans.
    for row in case["oleans.tsv"].splitlines()[1:]:
        name, total, older = row.split("\t")
        if int(older) > 0:
            flags.append(f"P1:prebuilt-{name}")
    # P2: statement provenance — the proved statement must match the pinned reference.
    if _norm(case["solution_statement.lean"]) != _norm(case["reference.lean"]):
        flags.append("P2:statement-mismatch")
    # P5: harness integrity — a recorded oracle failure must not coexist with a complete run.
    summ = json.loads(case["numeric_summary.json"])
    if summ.get("export_errors") and summ.get("collection_complete"):
        flags.append("P5:oracle-failure-hidden")
    # P6: receipts — every receipt's log must be present as an artifact.
    logs = {name for name in case if name.endswith(".log")} | {"build.log", "comparator.log"}
    for row in case["receipt.tsv"].splitlines()[1:]:
        log = row.split("\t")[2]
        if log not in logs:
            flags.append(f"P6:receipt-log-{log}")
    return (not flags, flags)


def write_case(directory, case):
    directory.mkdir(parents=True, exist_ok=True)
    for name, content in case.items():
        (directory / name).write_text(content, encoding="utf-8")


def read_case(directory):
    directory = Path(directory)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(directory.iterdir()) if p.is_file()}


def _demo():
    base = clean_case()
    assert baseline(base) == (True, []), "clean must pass baseline"
    assert protocol(base) == (True, []), "clean must pass protocol"
    expect = {
        "F1": ("baseline-accepts", "protocol-flags"),
        "F2": ("baseline-accepts", "protocol-flags"),
        "F4": ("baseline-accepts", "protocol-flags"),
        "F5": ("baseline-accepts", "protocol-flags"),
        "F6": ("baseline-flags", "protocol-flags"),
    }
    for fault, (b_expect, _) in expect.items():
        faulty = inject(base, fault)
        b_acc, _ = baseline(faulty)
        p_acc, p_flags = protocol(faulty)
        if b_expect == "baseline-accepts":
            assert b_acc, f"{fault}: baseline should accept"
        else:
            assert not b_acc, f"{fault}: baseline should flag"
        assert not p_acc, f"{fault}: protocol should flag, got {p_flags}"
    print("protocol_lib self-check: OK")


if __name__ == "__main__":
    _demo()
