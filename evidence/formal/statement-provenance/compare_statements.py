#!/usr/bin/env python3

import argparse
import difflib
import hashlib
import json
import re
from pathlib import Path

NAME = re.compile(r"(?:noncomputable\s+)?(?:theorem|structure|def|lemma)\s+(\S+)")
DECLARATION = re.compile(r"(?<!noncomputable)\n(?=(?:noncomputable\s+)?(?:theorem|structure|def|lemma|local notation|notation|open|namespace|variable|end|import)\b)")


def declarations(text):
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    text = re.sub(r"@\[[^\]]*\]", "", text)
    return [re.sub(r"\s+", " ", part).strip() for part in DECLARATION.split(text) if part.strip()]


def compare(reference_text, candidate_text):
    reference = declarations(reference_text)
    candidate = declarations(candidate_text)
    shared = [line for line in reference if line in candidate]
    return {
        "identical_declarations": len(shared),
        "identical_names": [match.group(1) for match in map(NAME.match, shared) if match],
        "only_in_reference": [line for line in reference if line not in candidate],
        "only_in_candidate": [line for line in candidate if line not in reference],
        "unified_diff": list(difflib.unified_diff(reference, candidate, "reference", "candidate", lineterm="", n=0)),
    }


def main():
    parser = argparse.ArgumentParser(description="Compare two Lean statement files declaration by declaration, ignoring comments, attributes and whitespace.")
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    arguments = parser.parse_args()
    reference_bytes = arguments.reference.read_bytes()
    candidate_bytes = arguments.candidate.read_bytes()
    result = compare(reference_bytes.decode("utf-8"), candidate_bytes.decode("utf-8"))
    result["reference_sha256"] = hashlib.sha256(reference_bytes).hexdigest()
    result["candidate_sha256"] = hashlib.sha256(candidate_bytes).hexdigest()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
