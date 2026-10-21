"""Deterministic regression benchmark for evaluator v2.

    python3 run_benchmark_v2.py > benchmark_v2.json

One case per class is enough: the evaluator is deterministic, so repeated instances of a
class give the same verdict. Also records wall-clock time per procedure, which v1 planned
but did not measure.
"""

import json
import time

import protocol_lib_v2 as V2


def timed(fn, case, repeats=2000):
    start = time.perf_counter()
    for _ in range(repeats):
        result = fn(case)
    return result, (time.perf_counter() - start) / repeats


def main():
    rows = {}
    for cls in ["C", "F1", "F2", "F4", "F5", "F6"]:
        case = V2.inject(V2.clean_case(), cls)
        (b_ok, b_flags), b_t = timed(V2.baseline, case)
        (p_ok, p_flags), p_t = timed(V2.protocol, case)
        rows[cls] = {"fault": V2.FAULTS.get(cls, "none (clean)"),
                     "baseline": {"flagged": not b_ok, "flags": b_flags, "seconds_per_case": b_t},
                     "protocol": {"flagged": not p_ok, "flags": p_flags, "seconds_per_case": p_t}}
    print(json.dumps({"evaluator": "v2", "kind": "deterministic regression benchmark", "classes": rows}, indent=2))


if __name__ == "__main__":
    main()
