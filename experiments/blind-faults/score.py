"""Join blind results with the revealed key and compute the metrics. Run after reveal.

    python3 score.py results.json key.json > scoreboard.json

A faulty case counts as detected by a procedure iff that procedure did not accept it. A clean
case flagged by a procedure is a false alarm. Decision rules are frozen in DESIGN.md: no case
is dropped, and if F6 is not detected by both procedures the experiment is reported invalid.
"""

import json
import sys

FAULTY = {"F1", "F2", "F4", "F5", "F6"}


def main():
    results = json.load(open(sys.argv[1]))["cases"]
    key = json.load(open(sys.argv[2]))
    per_class = {}
    for case, cls in sorted(key.items()):
        r = results[case]
        bucket = per_class.setdefault(cls, {"n": 0, "baseline_detected": 0, "protocol_detected": 0,
                                            "baseline_false_alarm": 0, "protocol_false_alarm": 0, "cases": []})
        bucket["n"] += 1
        b_flagged = not r["baseline"]["accepted"]
        p_flagged = not r["protocol"]["accepted"]
        if cls in FAULTY:
            bucket["baseline_detected"] += b_flagged
            bucket["protocol_detected"] += p_flagged
        else:
            bucket["baseline_false_alarm"] += b_flagged
            bucket["protocol_false_alarm"] += p_flagged
        bucket["cases"].append({"case": case, "baseline_flagged": b_flagged, "protocol_flagged": p_flagged,
                                "protocol_flags": r["protocol"]["flags"]})

    f6 = per_class.get("F6", {})
    valid = f6.get("baseline_detected") == f6.get("n") and f6.get("protocol_detected") == f6.get("n")
    faulty_classes = [c for c in per_class if c in FAULTY]
    only_protocol = [c for c in faulty_classes
                     if per_class[c]["protocol_detected"] == per_class[c]["n"]
                     and per_class[c]["baseline_detected"] == 0]
    print(json.dumps({
        "valid": valid,
        "note": "valid is false unless F6 (positive control) is detected by both procedures",
        "per_class": per_class,
        "classes_only_protocol_detected": sorted(only_protocol),
        "baseline_false_alarms_on_clean": per_class.get("C", {}).get("baseline_false_alarm", 0),
        "protocol_false_alarms_on_clean": per_class.get("C", {}).get("protocol_false_alarm", 0),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
