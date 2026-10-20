#!/usr/bin/env python3

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "numerical" / "paired"
EXPECTED_SUMMARY_HASHES = {
    "macos-arm64": "d45fe458dd10c1c5053cb7ba49796b84a2fd178e7627b46fa74c5e71eb95e0ec",
    "linux-x86_64": "867ce78201e211a587dcec4a6c89900963d54b92b6b5f6d78a73c52f84954b17",
}


def digest(path):
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1_048_576), b""):
            hasher.update(block)
    return hasher.hexdigest()


def campaign(host):
    folder = ROOT / host
    summary_path = folder / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    expected_summary_hash = (folder / "summary.json.sha256").read_text(encoding="utf-8").split()[0]
    if expected_summary_hash != EXPECTED_SUMMARY_HASHES[host] or digest(summary_path) != expected_summary_hash:
        raise ValueError(f"Summary hash mismatch: {host}")
    if summary.get("collection_complete") is not True or summary.get("variant_evaluations") != 84:
        raise ValueError(f"Incomplete campaign summary: {host}")
    if summary.get("counts") != {"KILLED": 54, "PASS": 27, "SURVIVED": 3}:
        raise ValueError(f"Unexpected mutation counts: {host}")
    artifact_hashes = summary.get("artifact_sha256", {})
    if len(artifact_hashes) != 85:
        raise ValueError(f"Unexpected artifact manifest size: {host}")
    for relative, expected in artifact_hashes.items():
        path = folder / relative
        if not path.is_file() or digest(path) != expected:
            raise ValueError(f"Artifact hash mismatch: {host}/{relative}")
    records = {}
    for path in sorted(folder.glob("case_*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        records[(record["case_id"], record["variant"])] = record
    if len(records) != 84:
        raise ValueError(f"Expected 84 unique case/variant records for {host}")
    with (folder / "observations.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 756:
        raise ValueError(f"Expected 756 observation rows for {host}")
    return summary, records, rows


def main():
    mac_summary, mac, mac_rows = campaign("macos-arm64")
    linux_summary, linux, linux_rows = campaign("linux-x86_64")
    if mac_summary["source_sha256"] != linux_summary["source_sha256"] or mac.keys() != linux.keys():
        raise ValueError("The paired runs do not share source and case identifiers.")
    for key in mac:
        left, right = mac[key], linux[key]
        if (left["status"], left["params"], left["values"].keys()) != (right["status"], right["params"], right["values"].keys()):
            raise ValueError(f"Paired result mismatch: {key}")
    row_key = lambda row: tuple(row[name] for name in ("case_id", "variant", "resolution", "fraction", "component"))
    mac_by_key = {row_key(row): row for row in mac_rows}
    linux_by_key = {row_key(row): row for row in linux_rows}
    if mac_by_key.keys() != linux_by_key.keys():
        raise ValueError("Paired observation keys differ.")
    scales = {(case_id, variant): float(record["scale"]) for (case_id, variant), record in mac.items()}
    finite = null = 0
    max_scaled_delta = 0.0
    for key, left in mac_by_key.items():
        right = linux_by_key[key]
        if not left["value"] or not right["value"]:
            if left["value"] or right["value"]:
                raise ValueError(f"Null/non-null mismatch: {key}")
            null += 1
        else:
            finite += 1
            max_scaled_delta = max(max_scaled_delta, abs(float(left["value"]) - float(right["value"])) / scales[(key[0], key[1])])
    if finite != 738 or null != 18 or max_scaled_delta > 1.1102230246251566e-16:
        raise ValueError("Paired numerical comparison does not match the recorded derived summary.")
    print(f"PASS: 2 summaries, 168 case records, 2 x 756 observation rows, {finite} finite pairs, {null} null pairs; max scaled delta {max_scaled_delta:.17g}.")


if __name__ == "__main__":
    main()
