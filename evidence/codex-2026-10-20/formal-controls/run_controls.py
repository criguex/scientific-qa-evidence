import argparse
import datetime
import hashlib
import json
import platform
import re
import socket
import subprocess
from pathlib import Path


COMMIT = "f9e8bc5b38b6e212696e8a30e3e91517af887bbd"
LEAN = Path("<WSL_HOME>/.elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/lean")
FILES = {
    "lean-toolchain",
    "lakefile.toml",
    "lake-manifest.json",
    "formalization.yaml",
    "ComparatorChallenges/NavierStokes.lean",
    "ComparatorChallenges/NavierStokes.json",
    "NavierStokes/ComparatorDefinitions.lean",
    "NavierStokes/ComparatorSolution.lean",
}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(command, cwd):
    try:
        result = subprocess.run(
            [str(item) for item in command],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )
        return {
            "command": [str(item) for item in command],
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {
            "command": [str(item) for item in command],
            "returncode": None,
            "stdout": "",
            "stderr": str(error),
            "infrastructure_error": type(error).__name__,
        }


def classify(name, result):
    text = result["stdout"] + result["stderr"]
    if name == "positive":
        return result["returncode"] == 0 and (
            "'control_true' does not depend on any axioms" in text
        )
    if name == "negative":
        return result["returncode"] not in (0, None) and (
            "error:" in text
            and ("trivial" in text or "assumption" in text)
            and "failed" in text
            and "False" in text
        )
    if name == "sorry":
        return result["returncode"] == 0 and bool(
            re.search(r"'control_sorry' depends on axioms:\s*\[sorryAx\]", text)
        )
    raise ValueError(name)


def self_check():
    assert classify("positive", {
        "returncode": 0,
        "stdout": "'control_true' does not depend on any axioms",
        "stderr": "",
    })
    assert classify("negative", {
        "returncode": 1,
        "stdout": "error: tactic 'trivial' failed\n⊢ False",
        "stderr": "",
    })
    assert not classify("negative", {
        "returncode": 137, "stdout": "", "stderr": "Killed",
    })
    assert not classify("negative", {
        "returncode": None, "stdout": "", "stderr": "TimeoutExpired",
    })
    assert classify("negative", {
        "returncode": 1,
        "stdout": "negative.lean:1:36: error: Tactic `assumption` failed\n\n⊢ False\n",
        "stderr": "",
    })
    assert classify("sorry", {
        "returncode": 0,
        "stdout": "'control_sorry' depends on axioms: [sorryAx]",
        "stderr": "",
    })
    assert not classify("sorry", {
        "returncode": 0,
        "stdout": "warning: declaration uses 'sorry'",
        "stderr": "",
    })
    assert digest(b"abc") != digest(b"abd")


def main():
    parser = argparse.ArgumentParser(
        description="Controles del verificador; no verifican los teoremas NS/Euler."
    )
    parser.add_argument("repo", type=Path)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("outputdir", type=Path)
    args = parser.parse_args()
    self_check()
    repo = args.repo.resolve(strict=True)
    manifest_path = args.manifest.resolve(strict=True)
    outputdir = args.outputdir.resolve()
    if outputdir == repo or repo in outputdir.parents:
        parser.error("outputdir debe estar fuera del repositorio auditado")
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    expected_hashes = manifest.get("sha256", {})
    if set(expected_hashes) != FILES or any(
        not isinstance(value, str)
        or re.fullmatch(r"[0-9a-f]{64}", value) is None
        for value in expected_hashes.values()
    ):
        parser.error("manifiesto debe contener los ocho hashes SHA256 esperados")
    outputdir.mkdir(parents=True, exist_ok=True)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = {
        "scope": "CONTROLES DEL VERIFICADOR; NO SON UNA PRUEBA DE NS NI EULER",
        "started_utc": started,
        "machine": {
            "hostname": socket.gethostname(),
            "platform": platform.platform(),
            "python": platform.python_version(),
        },
        "repo": str(repo),
        "manifest": str(manifest_path),
        "manifest_sha256": digest(manifest_bytes),
        "lean_binary": str(LEAN),
        "self_check_passed": True,
        "controls": {},
        "all_controls_passed": False,
    }
    controls = report["controls"]
    controls["manifest_commit"] = {
        "expected": COMMIT,
        "actual": manifest.get("commit"),
        "passed": manifest.get("commit") == COMMIT,
    }
    commit_result = run(["git", "-C", repo, "rev-parse", "HEAD"], outputdir)
    controls["commit"] = {
        "expected": COMMIT,
        "actual": commit_result["stdout"].strip(),
        "execution": commit_result,
        "passed": commit_result["returncode"] == 0
        and commit_result["stdout"].strip() == COMMIT,
    }
    hashes = {}
    for filename, expected in expected_hashes.items():
        path = (repo / filename).resolve()
        if repo not in path.parents:
            raise ValueError(f"archivo fuera del repositorio: {filename}")
        try:
            actual = digest(path.read_bytes())
            hashes[filename] = {
                "expected": expected, "actual": actual, "passed": actual == expected
            }
        except OSError as error:
            hashes[filename] = {
                "expected": expected, "actual": None,
                "passed": False, "error": str(error),
            }
    controls["hashes"] = {
        "files": hashes,
        "expected_count": 8,
        "actual_count": len(hashes),
        "passed": len(hashes) == 8 and all(v["passed"] for v in hashes.values()),
    }
    try:
        original = (repo / "lean-toolchain").read_bytes()
        mutated = bytearray(original)
        mutated[0] ^= 1
        mutation_hash = digest(mutated)
        expected_hash = expected_hashes["lean-toolchain"]
        (outputdir / "hash_original.bin").write_bytes(original)
        (outputdir / "hash_mutated.bin").write_bytes(mutated)
        (outputdir / "hash_original.sha256").write_text(
            expected_hash + "  hash_original.bin\n", encoding="utf-8"
        )
        (outputdir / "hash_mutated.sha256").write_text(
            expected_hash + "  hash_mutated.bin\n", encoding="utf-8"
        )
        original_check = run(
            ["sha256sum", "-c", "hash_original.sha256"], outputdir
        )
        mutated_check = run(
            ["sha256sum", "-c", "hash_mutated.sha256"], outputdir
        )
        controls["hash_mutation"] = {
            "expected": "rechazar contenido con exactamente un byte modificado",
            "method": "XOR 1 del primer byte en memoria; copias y sha256sum -c fuera del repo",
            "original_sha256": digest(original),
            "mutated_sha256": mutation_hash,
            "changed_bytes": sum(a != b for a, b in zip(original, mutated)),
            "original_check": original_check,
            "mutated_check": mutated_check,
            "passed": digest(original) == expected_hash
            and mutation_hash != expected_hash
            and len(original) == len(mutated)
            and sum(a != b for a, b in zip(original, mutated)) == 1
            and original_check["returncode"] == 0
            and "hash_original.bin: OK" in original_check["stdout"]
            and mutated_check["returncode"] == 1
            and "hash_mutated.bin: FAILED" in mutated_check["stdout"],
        }
    except (OSError, IndexError) as error:
        controls["hash_mutation"] = {"passed": False, "error": str(error)}
    version = run([LEAN, "--version"], outputdir)
    controls["toolchain"] = {
        "expected": "Lean 4.34.0-rc2; commit 6a10ac8c22beadecabdbb0919c2b50214762f91d",
        "execution": version,
        "passed": version["returncode"] == 0
        and "4.34.0-rc2" in version["stdout"]
        and "6a10ac8c22beadecabdbb0919c2b50214762f91d" in version["stdout"],
    }
    expectations = {
        "positive": "exit 0; control_true no depende de axiomas",
        "negative": "exit no cero por error lógico de trivial ante False",
        "sorry": "exit 0 y #print axioms revela sorryAx",
    }
    for name, expected in expectations.items():
        fixture = Path(__file__).resolve().parent / f"{name}.lean"
        result = run([LEAN, fixture], outputdir)
        for stream in ("stdout", "stderr"):
            (outputdir / f"{name}.{stream}.log").write_text(
                result[stream], encoding="utf-8"
            )
        controls[name] = {
            "expected": expected,
            "fixture_sha256": digest(fixture.read_bytes()),
            "execution": result,
            "passed": classify(name, result),
        }
    report["all_controls_passed"] = all(
        item["passed"] for item in controls.values()
    )
    report["finished_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    target = outputdir / "controls_summary.json"
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "summary": str(target),
        "all_controls_passed": report["all_controls_passed"],
        "scope": report["scope"],
    }, ensure_ascii=False))
    return 0 if report["all_controls_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
