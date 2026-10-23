#!/usr/bin/env python3
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import socket
import subprocess
import time
from pathlib import Path

try:
    from .mutate_export import load_export
except ImportError:
    from mutate_export import load_export


AXIOMS = ["propext", "Classical.choice", "Quot.sound"]


def nanoda_config(export_path):
    return {"export_file_path": str(export_path), "use_stdin": False, "permitted_axioms": AXIOMS, "unpermitted_axiom_hard_error": True, "num_threads": 1, "nat_extension": True, "string_extension": True, "print_success_message": True, "print_axioms": True, "pp_to_stdout": True}


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def verify_pair(baseline, mutant):
    if len(baseline) != len(mutant) or not baseline:
        raise ValueError("baseline/mutant record counts differ")
    baseline_target = baseline[-1].get("thm")
    mutant_target = mutant[-1].get("thm")
    if not baseline_target or not mutant_target or baseline_target.get("name") != mutant_target.get("name"):
        raise ValueError("target theorem is not the final record in both exports")
    if baseline_target.get("type") != mutant_target.get("type") or baseline_target.get("all") != mutant_target.get("all"):
        raise ValueError("mutation changed theorem statement or dependency closure")
    candidate = json.loads(json.dumps(baseline))
    candidate[-1]["thm"]["value"] = mutant_target.get("value")
    if candidate != mutant:
        raise ValueError("baseline and mutant differ beyond target.thm.value")
    defined_exprs = {record["ie"] for record in mutant[:-1] if "ie" in record}
    if mutant_target.get("type") not in defined_exprs or mutant_target.get("value") not in defined_exprs:
        raise ValueError("target type or proof expression is not declared before target")
    if baseline_target.get("value") == mutant_target.get("value"):
        raise ValueError("baseline and mutant proof values are equal")
    return {"target_type_expr_id": baseline_target["type"], "baseline_value_expr_id": baseline_target["value"], "mutant_value_expr_id": mutant_target["value"]}


def classify_lean(returncode, stdout, stderr, timed_out=False):
    if timed_out:
        return "TIMEOUT_INCONCLUSIVE"
    if returncode == 0 and "LEAN_KERNEL_ACCEPT" in stdout:
        return "ACCEPT"
    if returncode == 2 and "LEAN_KERNEL_REJECT:" in stderr and "(kernel) declaration type mismatch" in stderr:
        return "KERNEL_TYPE_MISMATCH_REJECT"
    if returncode == 2 and "LEAN_KERNEL_REJECT:" in stderr:
        return "REPLAY_REJECTION_UNCLASSIFIED"
    if returncode == 3 or "EXPORT_PARSE_REJECT:" in stderr:
        return "EXPORT_PARSE_FAILURE"
    return "INFRA_OR_HARNESS_FAILURE"


def classify_nanoda(returncode, output, timed_out=False):
    if timed_out:
        return "TIMEOUT_INCONCLUSIVE"
    if returncode == 0 and re.search(r"(?m)^Checked [0-9]+ declarations with no errors$", output):
        return "ACCEPT"
    if returncode != 0:
        return "NONZERO_UNCLASSIFIED"
    return "SUCCESS_MARKER_MISSING"


def execute(label, command, cwd, raw_dir, environment):
    started = utc_now()
    before = time.monotonic()
    (raw_dir / f"{label}.command.json").write_text(json.dumps(command, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    try:
        result = subprocess.run(command, cwd=cwd, env=environment, text=True, encoding="utf-8", errors="replace", capture_output=True, check=False, timeout=120)
        stdout, stderr, returncode = result.stdout, result.stderr, result.returncode
        launch_error = None
    except subprocess.TimeoutExpired as error:
        stdout = error.stdout.decode("utf-8", errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode("utf-8", errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
        returncode = 124
        launch_error = "TimeoutExpired"
    except OSError as error:
        stdout, stderr, returncode = "", str(error), 127
        launch_error = type(error).__name__
    elapsed = time.monotonic() - before
    finished = utc_now()
    (raw_dir / f"{label}.stdout.log").write_text(stdout, encoding="utf-8")
    (raw_dir / f"{label}.stderr.log").write_text(stderr, encoding="utf-8")
    return {"label": label, "command": command, "started_utc": started, "finished_utc": finished, "duration_seconds": round(elapsed, 6), "returncode": returncode, "launch_error": launch_error, "stdout_sha256": sha256(raw_dir / f"{label}.stdout.log"), "stderr_sha256": sha256(raw_dir / f"{label}.stderr.log"), "command_sha256": sha256(raw_dir / f"{label}.command.json")}


def main():
    parser = argparse.ArgumentParser(description="Run real Lean and nanoda kernel controls on a baseline/mutant NDJSON pair.")
    parser.add_argument("--formal-repo", required=True, type=Path)
    parser.add_argument("--lake", required=True, type=Path)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--nanoda", required=True, type=Path)
    parser.add_argument("--fixture-source", required=True, type=Path)
    parser.add_argument("--replay-harness", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--mutant", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    paths = [args.formal_repo, args.lake, args.lean, args.nanoda, args.fixture_source, args.replay_harness, args.baseline, args.mutant]
    if any(not path.exists() for path in paths):
        parser.error("one or more input paths do not exist")
    if not os.access(args.lake, os.X_OK) or not os.access(args.lean, os.X_OK) or not os.access(args.nanoda, os.X_OK):
        parser.error("lake, lean, and nanoda must be executable files")
    baseline_records = load_export(args.baseline)
    mutant_records = load_export(args.mutant)
    mutation = verify_pair(baseline_records, mutant_records)
    args.output_dir.mkdir(mode=0o700, parents=True, exist_ok=False)
    raw_dir = args.output_dir / "raw"
    public_dir = args.output_dir / "public"
    raw_dir.mkdir(mode=0o700)
    public_dir.mkdir(mode=0o755)

    actual_paths = {"<FORMAL_REPO>": str(args.formal_repo.resolve()), "<LAKE>": str(args.lake.resolve()), "<LEAN>": str(args.lean.resolve()), "<NANODA>": str(args.nanoda.resolve()), "<FIXTURE_SOURCE>": str(args.fixture_source.resolve()), "<HARNESS>": str(args.replay_harness.resolve()), "<BASELINE>": str(args.baseline.resolve()), "<MUTANT>": str(args.mutant.resolve()), "<OUTPUT>": str(args.output_dir.resolve())}
    def scrub(value):
        text = str(value).replace(socket.gethostname(), "<HOST>")
        for token, path in sorted(actual_paths.items(), key=lambda item: len(item[1]), reverse=True):
            text = text.replace(path, token)
        text = re.sub(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", "<IP>", text)
        text = re.sub(r"/(?:home|Users)/[^/\s]+", "/<USER>", text)
        text = re.sub(r"user-\d+\.slice|user@\d+\.service", "<USER_SLICE>", text)
        return text

    entries = []
    environment = os.environ.copy()
    environment.pop("LEAN_PATH", None)
    for case, export_path in (("baseline", args.baseline.resolve()), ("mutant", args.mutant.resolve())):
        lean_label = f"lean_{case}"
        lean_command = [str(args.lake.resolve()), "env", str(args.lean.resolve()), "--run", str(args.replay_harness.resolve()), str(export_path)]
        entry = execute(lean_label, lean_command, str(args.formal_repo.resolve()), raw_dir, environment)
        lean_stdout = (raw_dir / f"{lean_label}.stdout.log").read_text(encoding="utf-8")
        lean_stderr = (raw_dir / f"{lean_label}.stderr.log").read_text(encoding="utf-8")
        entry.update({"kernel": "Lean", "case": case, "export_sha256": sha256(export_path), "classification": classify_lean(entry["returncode"], lean_stdout, lean_stderr, entry["launch_error"] == "TimeoutExpired")})
        entries.append(entry)

        config_path = raw_dir / f"nanoda_{case}.config.json"
        config = nanoda_config(export_path)
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        public_config = dict(config)
        public_config["export_file_path"] = "<BASELINE>" if case == "baseline" else "<MUTANT>"
        (public_dir / f"nanoda_{case}.config.json").write_text(json.dumps(public_config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        nanoda_label = f"nanoda_{case}"
        nanoda_command = [str(args.nanoda.resolve()), str(config_path)]
        entry = execute(nanoda_label, nanoda_command, str(args.formal_repo.resolve()), raw_dir, environment)
        output_text = (raw_dir / f"{nanoda_label}.stdout.log").read_text(encoding="utf-8") + (raw_dir / f"{nanoda_label}.stderr.log").read_text(encoding="utf-8")
        entry.update({"kernel": "nanoda", "case": case, "export_sha256": sha256(export_path), "config_sha256": sha256(config_path), "classification": classify_nanoda(entry["returncode"], output_text, entry["launch_error"] == "TimeoutExpired")})
        entries.append(entry)

    tool_hashes = {"lake_sha256": sha256(args.lake), "lean_sha256": sha256(args.lean), "nanoda_sha256": sha256(args.nanoda)}
    code_hashes = {"fixture_source_sha256": sha256(args.fixture_source), "replay_harness_sha256": sha256(args.replay_harness), "runner_sha256": sha256(Path(__file__)), "mutator_sha256": sha256(Path(__file__).with_name("mutate_export.py"))}
    input_hashes = {"baseline_sha256": sha256(args.baseline), "mutant_sha256": sha256(args.mutant)}
    results = []
    for entry in entries:
        public_entry = dict(entry)
        public_entry["command"] = [scrub(arg) for arg in entry["command"]]
        results.append(public_entry)
        for suffix in ("stdout", "stderr"):
            source = raw_dir / f"{entry['label']}.{suffix}.log"
            (public_dir / source.name).write_text(scrub(source.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
        (public_dir / f"{entry['label']}.command.json").write_text(json.dumps(public_entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    collection_complete = len(entries) == 4
    summary = {"scope": "fixture-only kernel acceptance/replay controls; not universal validation", "started_utc": min(item["started_utc"] for item in entries), "finished_utc": max(item["finished_utc"] for item in entries), "collection_complete": collection_complete, "status": "COLLECTED_PENDING_CLASSIFICATION", "all_expected_responses": None, "mutation": mutation, "input_sha256": input_hashes, "tool_sha256": tool_hashes, "code_sha256": code_hashes, "runs": results}
    (public_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output_dir": scrub(args.output_dir.resolve()), "collection_complete": collection_complete, "status": summary["status"], "summary": scrub(public_dir / "summary.json"), "run_count": len(entries)}, ensure_ascii=False))
    return 0 if collection_complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
