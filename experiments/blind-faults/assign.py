"""Assign faults to cases using the committed secret seed. Run by the author.

    python3 assign.py --seed-file ~/semilla-experimento.txt --out cases

Reads the seed hex from the file, shuffles the 21 fault slots with it, writes one case
directory per slot (case-01 .. case-21) and key.json mapping case -> fault class.

The person running the checks does not read the seed file or key.json until results are
recorded. Blinding is guaranteed by the frozen hash of these scripts (FROZEN.md), published
before this script is run with the seed.
"""

import argparse
import hashlib
import json
import random
from pathlib import Path

import protocol_lib as P


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed-file", required=True)
    parser.add_argument("--out", default="cases")
    args = parser.parse_args()

    seed_bytes = Path(args.seed_file).expanduser().read_bytes()
    seed_hex = seed_bytes.decode("utf-8").strip()
    seed_sha = hashlib.sha256(seed_bytes).hexdigest()

    slots = []
    for cls in ("F1", "F2", "F4", "F5", "F6"):
        slots += [cls] * P.PER_CLASS
    slots += ["C"] * P.CLEAN
    assert len(slots) == 21, len(slots)

    random.Random(seed_hex).shuffle(slots)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    key = {}
    base = P.clean_case()
    for index, cls in enumerate(slots, 1):
        name = f"case-{index:02d}"
        P.write_case(out / name, P.inject(base, cls))
        key[name] = cls
    (Path("key.json")).write_text(json.dumps(key, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"seed_sha256": seed_sha, "cases": len(slots), "out": str(out),
                      "key": "key.json (keep private until results are recorded)"}, indent=2))


if __name__ == "__main__":
    main()
