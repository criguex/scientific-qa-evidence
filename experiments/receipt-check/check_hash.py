import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RECORDED = HERE / "results" / "receipts.jsonl"


def recorded_hashes(path=RECORDED):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines()]
    return {r["step"]: r["log_sha256"] for r in rows if r["variant"] == "bundle"}


def hash_flags(bundle, recorded=None):
    recorded = recorded if recorded is not None else recorded_hashes()
    lines = (Path(bundle) / "receipt.tsv").read_text().splitlines()
    flags = []
    for line in lines[1:]:
        step, _, log, exit_code = line.split("\t")
        path = Path(bundle) / log
        if not path.is_file():
            flags.append(f"H:log-missing-{log}")
        elif hashlib.sha256(path.read_bytes()).hexdigest() != recorded.get(step):
            flags.append(f"H:log-hash-mismatch-{log}")
        if exit_code != "0":
            flags.append(f"H:exit-{step}-{exit_code}")
    return flags


if __name__ == "__main__":
    flags = hash_flags(sys.argv[1])
    print(json.dumps({"hash_flags": flags}))
    sys.exit(1 if flags else 0)
