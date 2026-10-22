import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDED = HERE / "results" / "receipts.jsonl"


def recorded_hashes(path=RECORDED):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
    return {r["step"]: r["log_sha256"] for r in rows if r["variant"] == "bundle"}


HEADER = "step\tcommand\tlog\texit"


def hash_flags(bundle, recorded=None):
    recorded = recorded if recorded is not None else recorded_hashes()
    receipt = Path(bundle) / "receipt.tsv"
    if not receipt.is_file():
        return ["H:receipt-missing"]
    lines = receipt.read_text().splitlines()
    if not lines or lines[0] != HEADER:
        return ["H:receipt-header"]
    flags = []
    seen = []
    for number, line in enumerate(lines[1:], start=2):
        fields = line.split("\t")
        if len(fields) != 4:
            flags.append(f"H:receipt-row-malformed-{number}")
            continue
        step, _, log, exit_code = fields
        if step in seen:
            flags.append(f"H:step-duplicate-{step}")
        seen.append(step)
        if step not in recorded:
            flags.append(f"H:step-unexpected-{step}")
            continue
        path = Path(bundle) / log
        if not path.is_file():
            flags.append(f"H:log-missing-{log}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != recorded[step]:
            flags.append(f"H:log-hash-mismatch-{log}")
        if exit_code != "0":
            flags.append(f"H:exit-{step}-{exit_code}")
    flags += [f"H:step-missing-{step}" for step in recorded if step not in seen]
    return flags

if __name__ == "__main__":
    flags = hash_flags(sys.argv[1])
    print(json.dumps({"hash_flags": flags}))
    sys.exit(1 if flags else 0)
