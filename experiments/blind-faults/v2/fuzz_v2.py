"""Round 3: deterministic robustness fuzzing of evaluator v2.

    python3 fuzz_v2.py            # report
    python3 -m unittest fuzz_v2   # CI: fails if any input crashes the evaluator

Invariant: baseline() and protocol() are total functions. For any mutation of any
artifact they must return a verdict, never raise. The seed is fixed so the run is
reproducible.
"""

import random
import unittest

import protocol_lib_v2 as V2

SEED = 20261021
ROUNDS = 400


def mutations(text, rng):
    lines = text.splitlines(keepends=True)
    yield text[: rng.randrange(len(text) + 1)]                       # truncate
    yield text + "".join(chr(rng.randrange(1, 0x2FFF)) for _ in range(rng.randrange(1, 40)))
    yield text.replace("\n", "\r\n")                                  # CRLF
    yield "﻿" + text                                             # BOM
    yield text.replace("\t", " ")                                     # tabs to spaces
    yield "".join(rng.sample(lines, len(lines))) if lines else text   # shuffle lines
    yield "".join(lines + lines)                                      # duplicate
    yield "".join(l for l in lines if rng.random() < 0.5)             # drop lines
    yield "".join(rng.choice(["\x00", "\t", "\n", "[", "]", ",", '"', "{", "}", "0", "-1", "9" * 30])
                  for _ in range(rng.randrange(0, 60)))               # garbage
    yield rng.choice(["[]", "{}", "null", "0", '""', "[[]]", '{"collection_complete": []}',
                      '{"export_errors": 5, "collection_complete": true}'])


def fuzz(seed=SEED, rounds=ROUNDS):
    rng = random.Random(seed)
    crashes = []
    tried = 0
    for _ in range(rounds):
        base = V2.inject(V2.clean_case(), rng.choice(["C", "F1", "F2", "F4", "F5", "F6"]))
        name = rng.choice(sorted(base))
        for mutated in mutations(base[name], rng):
            case = dict(base)
            case[name] = mutated
            for fn in (V2.baseline, V2.protocol):
                tried += 1
                try:
                    accepted, flags = fn(case)
                    assert isinstance(accepted, bool) and isinstance(flags, list)
                except Exception as exc:
                    crashes.append((fn.__name__, name, type(exc).__name__, repr(mutated[:60])))
    return tried, crashes


class FuzzTests(unittest.TestCase):
    def test_evaluator_never_crashes(self):
        tried, crashes = fuzz()
        self.assertEqual(crashes, [], f"{len(crashes)} crashes in {tried} evaluations, e.g. {crashes[:3]}")


if __name__ == "__main__":
    tried, crashes = fuzz()
    print(f"evaluations: {tried}  crashes: {len(crashes)}")
    seen = set()
    for fn, name, exc, sample in crashes:
        if (fn, name, exc) not in seen:
            seen.add((fn, name, exc))
            print(f"  {fn} on {name}: {exc}  e.g. {sample}")
