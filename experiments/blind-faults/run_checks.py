"""Run both procedures over every case directory, blind to key.json.

    python3 run_checks.py cases > results.json

Reads only the case artifacts, never key.json. Records, per case, whether the baseline and
the protocol accepted it and which checks each raised.
"""

import json
import sys
from pathlib import Path

import protocol_lib as P


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "cases")
    results = {}
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():
            continue
        case = P.read_case(directory)
        b_accept, b_flags = P.baseline(case)
        p_accept, p_flags = P.protocol(case)
        results[directory.name] = {
            "baseline": {"accepted": b_accept, "flags": b_flags},
            "protocol": {"accepted": p_accept, "flags": p_flags},
        }
    print(json.dumps({"schema": 1, "cases": results}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
