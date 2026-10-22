import hashlib
import json
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "blind-faults" / "v2" / "protocol_lib_v2.py"
sys.path.insert(0, str(LIB.parent))
import protocol_lib_v2 as protocol_lib


def p6_flags(directory):
    _, flags = protocol_lib.protocol(protocol_lib.read_case(directory))
    return [flag for flag in flags if flag.startswith("P6:")]


if __name__ == "__main__":
    flags = p6_flags(sys.argv[1])
    print(json.dumps({"protocol_lib_v2_sha256": hashlib.sha256(LIB.read_bytes()).hexdigest(), "p6_flags": flags}))
    sys.exit(1 if flags else 0)
