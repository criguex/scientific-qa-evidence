"""Evaluator v2 for the blind-fault benchmark. v1 (../protocol_lib.py) stays frozen.

Fixes three defects found in v1 after its results were published:
1. Incomplete evidence failed open: an empty or truncated axioms report was accepted.
2. Absent evidence crashed: a missing artifact raised KeyError instead of a verdict.
3. P6 assumed comparator.log existed; no case contained it, so receipts pointing to a
   missing log passed.

v2 fails closed: a required artifact that is missing or unparseable is a flag, in both
procedures, and receipts are checked against the files actually present.
"""

import json
import re
from pathlib import Path

PERMITTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
REQUIRED = ["build.log", "comparator.log", "oleans.tsv", "solution_statement.lean",
            "reference.lean", "axioms.txt", "receipt.tsv", "numeric_summary.json"]
AXIOMS_LINE = re.compile(r"depends on axioms: \[([^\]]*)\]\s*$", re.M)


def clean_case():
    """Clean template, now including the comparator.log that the receipts name."""
    return {
        "build.log": "✔ [1/3] Built Demo.Core\n✔ [2/3] Built Demo.Solution\n"
                     "Build completed successfully (3 jobs).\n",
        "comparator.log": "Running Lean default kernel on solution.\n"
                          "Lean default kernel accepts the solution\nYour solution is okay!\n",
        "oleans.tsv": "package\ttotal\tolder_than_build_start\nDemo\t3\t0\nmathlib\t2\t0\n",
        "solution_statement.lean": "theorem demo_breakdown (nu : Real) (h : nu > 0) :\n"
                                   "    Exists u, Breakdown u := by sorry\n",
        "reference.lean": "theorem demo_breakdown (nu : Real) (h : nu > 0) :\n"
                          "    Exists u, Breakdown u := by sorry\n",
        "axioms.txt": "'demo_breakdown' depends on axioms: [propext, Classical.choice, Quot.sound]\n",
        "receipt.tsv": "step\tcommand\tlog\texit\nbuild\tlake build\tbuild.log\t0\n"
                       "comparator\tlake env comparator demo.json\tcomparator.log\t0\n",
        "numeric_summary.json": json.dumps({"collection_complete": True, "oracle_valid": True,
                                            "export_errors": []}, indent=2) + "\n",
    }


def _missing(case):
    return [f"missing:{name}" for name in REQUIRED if name not in case or not case[name].strip()]


def _axioms_flags(text, prefix):
    match = AXIOMS_LINE.search(text or "")
    if not match:
        return [f"{prefix}:axioms-incomplete"]
    used = {a.strip() for a in match.group(1).split(",") if a.strip()}
    return [] if used <= PERMITTED_AXIOMS else [f"{prefix}:axioms"]


RECEIPT_HEADER = "step\tcommand\tlog\texit"
OLEANS_HEADER = "package\ttotal\tolder_than_build_start"
REQUIRED_STEPS = {"build", "comparator"}


def _summary(case):
    try:
        value = json.loads(case.get("numeric_summary.json", ""))
    except ValueError:
        return {}, ["numeric-summary-unparseable"]
    if not isinstance(value, dict):
        return {}, ["numeric-summary-not-object"]
    return value, []


def _rows(text, header, label):
    lines = [line for line in (text or "").splitlines() if line.strip()]
    if not lines or lines[0] != header:
        return [], [f"{label}-bad-header"]
    if len(lines) == 1:
        return [], [f"{label}-no-rows"]
    return [line.split("\t") for line in lines[1:]], []


def baseline(case):
    """Documented procedure, failing closed on missing or incomplete evidence."""
    flags = [f"B:{m}" for m in _missing(case)]
    if "Build completed successfully" not in case.get("build.log", ""):
        flags.append("B:build-failed")
    if "Your solution is okay!" not in case.get("comparator.log", ""):
        flags.append("B:comparator-not-ok")
    flags += _axioms_flags(case.get("axioms.txt"), "B")
    summary, errors = _summary(case)
    flags += [f"B:{e}" for e in errors]
    if summary.get("collection_complete") is not True:
        flags.append("B:numeric-incomplete")
    return (not flags, sorted(set(flags)))


def _norm(src):
    return [" ".join(line.split()) for line in (src or "").splitlines() if line.strip()]


def protocol(case):
    _, flags = baseline(case)
    flags = list(flags)
    olean_rows, errors = _rows(case.get("oleans.tsv"), OLEANS_HEADER, "P1:oleans")
    flags += errors
    for parts in olean_rows:
        if len(parts) != 3 or not parts[2].isdigit():
            flags.append("P1:oleans-unparseable")
        elif int(parts[2]) > 0:
            flags.append(f"P1:prebuilt-{parts[0]}")
    if _norm(case.get("solution_statement.lean")) != _norm(case.get("reference.lean")):
        flags.append("P2:statement-differs-from-reference")
    summary, _ = _summary(case)
    if summary.get("export_errors") and summary.get("collection_complete"):
        flags.append("P5:oracle-failure-hidden")
    present = set(case)
    receipt_rows, errors = _rows(case.get("receipt.tsv"), RECEIPT_HEADER, "P6:receipt")
    flags += errors
    steps = set()
    for parts in receipt_rows:
        if len(parts) != 4:
            flags.append("P6:receipt-unparseable")
            continue
        step, _, log, exit_code = parts
        steps.add(step)
        if log not in present:
            flags.append(f"P6:receipt-log-missing-{log}")
        if exit_code != "0":
            flags.append(f"P6:receipt-exit-{step}-{exit_code}")
    if receipt_rows:
        for step in sorted(REQUIRED_STEPS - steps):
            flags.append(f"P6:receipt-step-missing-{step}")
    return (not flags, sorted(set(flags)))


def read_case(directory):
    directory = Path(directory)
    return {p.name: p.read_text(encoding="utf-8") for p in sorted(directory.iterdir()) if p.is_file()}


FAULTS = {
    "F1": "a dependency arrived prebuilt (pre-dated .olean files); the build log is clean",
    "F2": "the solution statement differs textually from the pinned reference",
    "F4": "the oracle failed but the harness reports a complete run",
    "F5": "a receipt names a log the build did not write",
    "F6": "positive control: the solution depends on sorry",
}


def inject(case, fault):
    c = dict(case)
    if fault == "C":
        return c
    if fault == "F1":
        c["oleans.tsv"] += "batteries\t190\t190\n"
    elif fault == "F2":
        c["solution_statement.lean"] = c["solution_statement.lean"].replace("nu > 0", "nu >= 0")
    elif fault == "F4":
        c["numeric_summary.json"] = json.dumps({"collection_complete": True, "oracle_valid": True,
                                                "export_errors": [{"case_id": "rc_001", "exception": "oracle:ValueError"}]}, indent=2) + "\n"
    elif fault == "F5":
        c["receipt.tsv"] = c["receipt.tsv"].replace("\tbuild.log\t", "\tother-build.log\t")
    elif fault == "F6":
        c["axioms.txt"] = "'demo_breakdown' depends on axioms: [propext, Classical.choice, Quot.sound, sorryAx]\n"
    else:
        raise ValueError(fault)
    return c
