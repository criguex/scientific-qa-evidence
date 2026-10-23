#!/usr/bin/env python3
"""Read-only integrity and paired-result checks for this public evidence bundle."""

import csv
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_manifest(directory, manifest_name):
    manifest = directory / manifest_name
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        path = directory / relative.strip()
        assert path.is_file(), f"missing manifest entry: {path}"
        assert sha256(path) == expected, f"hash mismatch: {path}"


def verify_campaign(name):
    directory = ROOT / name
    summary_path = directory / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    expected_summary_hash = (directory / "summary.json.sha256").read_text().split()[0]
    assert sha256(summary_path) == expected_summary_hash, f"summary hash mismatch: {name}"
    assert summary["collection_complete"] is True
    assert summary["all_expected_responses"] is None
    assert summary["variant_evaluations"] == 84
    assert summary["process_invocations"] == 1
    assert summary["counts"] == {"KILLED": 54, "PASS": 27, "SURVIVED": 3}
    assert len(summary["artifact_sha256"]) == 85
    for relative, expected in summary["artifact_sha256"].items():
        assert sha256(directory / relative) == expected, f"artifact hash mismatch: {name}/{relative}"
    with (directory / "observations.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 756, f"unexpected CSV row count: {name}: {len(rows)}"
    cases = {}
    for path in sorted(directory.glob("case_*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        cases[(record["case_id"], record["variant"])] = record
    assert len(cases) == 84
    return summary, cases, rows


def verify_clean_build03():
    directory = ROOT / "clean_build03"
    verify_manifest(directory, "public_manifest.sha256")
    manifest_paths = {
        line.split(maxsplit=1)[1].strip()
        for line in (directory / "public_manifest.sha256").read_text(encoding="utf-8").splitlines()
    }
    actual_paths = {path.name for path in directory.iterdir() if path.is_file() and path.name != "public_manifest.sha256"}
    assert manifest_paths == actual_paths
    summary = json.loads((directory / "summary.json").read_text(encoding="utf-8"))
    assert summary["phase"] == "complete"
    assert summary["status"] == "PASS" and summary["passed"] is True
    assert summary["exit_code"] == summary["build_exit_code"] == 0
    assert summary["build_complete_evidence_present"] is True
    assert summary["source_inventory_sha256"] == "95bb21c93e834581e1400e31e33a9fb7943db2f64f11425b034f97b9b52e95fc"
    assert (directory / "build.exit_code.txt").read_text().strip() == "0"
    assert summary["duration_seconds"] == 2496
    assert (directory / "build.time.txt").read_text(encoding="utf-8").startswith("elapsed_seconds=2448.86")
    assert "Build completed successfully (11424 jobs)." in (directory / "build.stdout.log").read_text(encoding="utf-8")
    inventory = directory / "source_inventory.sha256"
    assert sha256(inventory) == summary["source_inventory_sha256"]
    assert len(inventory.read_text(encoding="utf-8").splitlines()) == 2669
    assert "LEAN_NUM_THREADS=6" in (directory / "command.txt").read_text(encoding="utf-8")
    assert "AF_INET=EPERM" in (directory / "preflight.network.txt").read_text(encoding="utf-8")
    assert "AF_UNIX=EPERM" in (directory / "preflight.network.txt").read_text(encoding="utf-8")
    assert summary["network_scope"].endswith("no acredita sandbox hermética")


def main():
    for dirname, manifest in (
        ("kernel01", "public_manifest.sha256"),
        ("kernel02", "public_manifest.sha256"),
        ("kernel_fixture_v2", "public_manifest.sha256"),
        ("periodic05", "public_manifest.sha256"),
    ):
        verify_manifest(ROOT / dirname, manifest)
    verify_clean_build03()

    source = ROOT / "multidomain_source_v2.tar.gz"
    assert sha256(source) == "8a98368e7ac53aeb3fedb777ba13073afe42f03b9204d0cfec77120a1f218f99"
    mac_summary, mac, mac_rows = verify_campaign("multidomain_mac")
    war_summary, war, war_rows = verify_campaign("multidomain_war")
    assert set(mac) == set(war)
    finite_pairs = null_pairs = 0
    maximum_scaled_delta = 0.0
    for case_id in sorted(mac):
        left, right = mac[case_id], war[case_id]
        assert (left["status"], left["params"]) == (right["status"], right["params"]), case_id
        assert left["values"].keys() == right["values"].keys(), case_id
    row_key = lambda row: tuple(row[key] for key in (
        "case_id", "variant", "resolution", "fraction", "component"
    ))
    mac_by_row = {row_key(row): row for row in mac_rows}
    war_by_row = {row_key(row): row for row in war_rows}
    assert mac_by_row.keys() == war_by_row.keys()
    scales = {(case_id, variant): float(case["scale"])
              for (case_id, variant), case in mac.items()}
    for key, left_row in mac_by_row.items():
        right_row = war_by_row[key]
        a, b = left_row["value"], right_row["value"]
        if not a or not b:
            assert not a and not b, key
            null_pairs += 1
        else:
            finite_pairs += 1
            maximum_scaled_delta = max(
                maximum_scaled_delta,
                abs(float(a) - float(b)) / scales[(key[0], key[1])],
            )
    assert finite_pairs == 738 and null_pairs == 18
    assert maximum_scaled_delta <= 1.1102230246251566e-16
    assert mac_summary["source_sha256"] == war_summary["source_sha256"]
    print(
        "Evidence integrity PASS: manifests, clean03 build, 2 campaign summaries, 170 case artifacts, "
        "2 CSVs (756 rows each), 738 finite pairs, 18 null pairs; "
        f"max scaled cross-host delta={maximum_scaled_delta:.17g}."
    )


if __name__ == "__main__":
    main()
