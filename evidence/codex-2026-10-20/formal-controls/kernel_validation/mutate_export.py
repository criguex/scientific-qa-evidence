#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def load_export(path):
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise ValueError(f"invalid NDJSON at line {line_number}: {error}") from error
    if not records or records[0].get("meta", {}).get("format", {}).get("version") != "3.1.0":
        raise ValueError("expected lean4export NDJSON format 3.1.0")
    return records


def name_strings(records):
    parts = {}
    for record in records:
        if "in" not in record:
            continue
        node = record.get("str")
        if isinstance(node, dict) and isinstance(node.get("str"), str):
            parts[node.get("pre", 0)] = parts.get(node.get("pre", 0), "")
            parent = parts[node["pre"]]
            parts[record["in"]] = f"{parent}.{node['str']}" if parent else node["str"]
        elif isinstance(node, str):
            parts[record["in"]] = node
        elif "num" in record and record["num"].get("pre") in parts:
            parent = parts[record["num"]["pre"]]
            parts[record["in"]] = f"{parent}.{record['num']['i']}"
    return parts


def mutate(records, target_name="target", wrong_name="wrong"):
    names = name_strings(records)
    declarations = {}
    expr_ids = set()
    for index, record in enumerate(records):
        theorem = record.get("thm")
        if theorem:
            label = names.get(theorem.get("name"))
            if label in (target_name, wrong_name):
                if label in declarations:
                    raise ValueError(f"duplicate theorem: {label}")
                declarations[label] = (index, theorem)
        if "ie" in record:
            expr_ids.add(record["ie"])

    if set(declarations) != {target_name, wrong_name}:
        raise ValueError(f"expected theorem declarations {target_name!r} and {wrong_name!r}")
    target_index, target = declarations[target_name]
    _, wrong = declarations[wrong_name]
    if target["type"] == wrong["type"]:
        raise ValueError("fixture types unexpectedly equal; mutation would not test typechecking")
    if target["value"] not in expr_ids or wrong["value"] not in expr_ids:
        raise ValueError("theorem value references a missing expression")
    if target["value"] == wrong["value"]:
        raise ValueError("fixture values unexpectedly equal")
    if target.get("all") != [target["name"]]:
        raise ValueError("target dependency closure differs from the expected standalone fixture")

    normalized = json.loads(json.dumps(records))
    target_record = normalized.pop(target_index)
    normalized.append(target_record)
    changed = json.loads(json.dumps(normalized))
    if changed[-1].get("thm", {}).get("name") != target["name"]:
        raise AssertionError("target theorem was not moved to the end")
    prior_expr_ids = {record["ie"] for record in changed[:-1] if "ie" in record}
    if target["type"] not in prior_expr_ids or wrong["value"] not in prior_expr_ids:
        raise ValueError("target references an expression not declared before the theorem")
    changed[-1]["thm"]["value"] = wrong["value"]
    changed_target = changed[-1]["thm"]
    if changed_target["type"] != target["type"] or changed_target["all"] != target["all"]:
        raise AssertionError("mutation changed the theorem statement or dependency closure")
    return normalized, changed, {"target_type": target["type"], "original_value": target["value"], "replacement_value": wrong["value"], "wrong_type": wrong["type"]}


def main():
    parser = argparse.ArgumentParser(description="Create a type-mismatched Lean export fixture.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--baseline-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists() or args.baseline_output.exists():
        parser.error("an output already exists; refusing to overwrite evidence")
    records = load_export(args.input)
    baseline, mutated, details = mutate(records)
    payloads = {
        args.baseline_output: baseline,
        args.output: mutated,
    }
    for path, value in payloads.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(record, separators=(",", ":"), ensure_ascii=False) + "\n" for record in value), encoding="utf-8")
    print(json.dumps({"result": "MUTATED_TYPE_MISMATCH", "baseline_records": len(baseline), "mutant_records": len(mutated), **details}, sort_keys=True))


if __name__ == "__main__":
    main()
