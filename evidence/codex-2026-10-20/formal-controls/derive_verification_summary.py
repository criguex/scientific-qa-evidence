import argparse
import collections
import datetime
import hashlib
import json
import re
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("--evidence", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
root = args.evidence
raw_path = root / "resultados_5070" / "summary.json"
pairs = json.loads(raw_path.read_text(encoding="utf-8"), object_pairs_hook=list)
counts = collections.Counter(key for key, value in pairs)
duplicates = sorted(key for key, count in counts.items() if count > 1)
assert duplicates == ["commit"]
commit_values = [value for key, value in pairs if key == "commit"]
commit_sha = next(value for value in commit_values if re.fullmatch(r"[0-9a-f]{40}", value))
commit_status = next(value for value in commit_values if value == "OK")
manifest = json.loads((root / "audit_static.json").read_text(encoding="utf-8"))
assert commit_sha == manifest["commit"]
raw = dict(pairs)
run_log = (root / "resultados_5070" / "run.log").read_text(encoding="utf-8")
axioms = (root / "resultados_5070" / "axioms.txt").read_text(encoding="utf-8")
mutant = (root / "resultados_5070" / "mutant_force_zero.log").read_text(encoding="utf-8")
assert "Build completed successfully (11424 jobs)." in run_log and raw["build"] == "OK"
expected_names = [
    "NavierStokes.Comparator.navier_stokes_breakdown_R3",
    "NavierStokes.Comparator.navier_stokes_breakdown_periodic",
    "Euler.euler_breakdown_R3",
    "Euler.exists_compact_smooth_euler_singularity",
]
expected_axioms = ["propext", "Classical.choice", "Quot.sound"]
theorems = {}
for name in expected_names:
    match = re.search(r"'" + re.escape(name) + r"' depends on axioms: \[([^\]]*)\]", axioms)
    assert match is not None
    found = [item.strip() for item in match.group(1).split(",")]
    assert found == expected_axioms and "sorryAx" not in found
    theorems[name] = found
assert "has 3 explicit field, but only 2 were provided" in mutant
assert "ComparatorBridge.toComparator f = 0" in mutant
assert raw["comparator_ns"] == raw["comparator_euler"] == "SKIPPED"
source_paths = [
    raw_path, root / "resultados_5070" / "run.log",
    root / "resultados_5070" / "axioms.txt",
    root / "resultados_5070" / "mutant_force_zero.log",
    root / "audit_static.json", root / "build_on_5070.sh",
]
result = {
    "kind": "derived_summary_from_preserved_raw_evidence_not_independent_kernel",
    "derived_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "finished_utc": raw["finished_utc"],
    "commit_sha": commit_sha,
    "commit_status": commit_status,
    "raw_duplicate_keys": duplicates,
    "raw_commit_values_preserved": commit_values,
    "raw_summary_unchanged": True,
    "build": "OK",
    "build_seconds": int(raw["build_seconds"]),
    "build_used_mathlib_cache": True,
    "theorem_axioms": theorems,
    "criteria": {
        "NS-06": "CLOSED_BUILD_OK",
        "NS-07": "CLOSED_TWO_NS_STANDARD_AXIOMS_NO_SORRY",
        "EU-05": "CLOSED_EULER_SOLUTION_AND_TWO_THEOREMS_STANDARD_AXIOMS_NO_SORRY",
        "NS-09": "LIMITED_DETECTED_CONSTRUCTOR_SHAPE_AND_UNPROVIDED_ZERO_FORCE_FIELD",
        "NS-08": "OPEN_COMPARATORS_SKIPPED_NO_SECOND_KERNEL",
        "EU-06": "NOT_EXECUTED",
    },
    "mutation_interpretation": {
        "raw_status": raw["mutant_force_zero"],
        "observed": "constructor changes from two fields to three; existing proof lacks new zero-force field and leaves toComparator f = 0",
        "not_proven": ["force_is_essential", "proof_cannot_be_repaired", "unforced_theorem_is_false"],
    },
    "preflight_hash_count": len(manifest["sha256"]),
    "preflight_has_euler_files": any("Euler" in name for name in manifest["sha256"]),
    "limitations": [
        "Euler hashes recorded without prefixed external expected values",
        "Euler statement provenance limitation not resolved",
        "compiled formal theorem is not a conclusion from the fluid animation",
    ],
    "source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
}
assert result["preflight_hash_count"] == 8 and not result["preflight_has_euler_files"]
args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2, ensure_ascii=False))
