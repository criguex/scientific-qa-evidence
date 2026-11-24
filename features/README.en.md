> English translation of [README.md](README.md). If they differ, the original prevails.

# Gherkin scenarios

Each `.feature` file is a user story from the audit, written in Gherkin in Spanish (`# language: es`): **Dado** (Given) the context, **Cuando** (When) the action, and **Entonces** (Then) the result that can be measured.

| File | Story | Criteria met |
| --- | --- | --- |
| [01-compilacion.feature](01-compilacion.feature) | US-1 · The proofs build | 3 of 3 |
| [02-verificadores.feature](02-verificadores.feature) | US-2 · Other checkers agree | 3 of 4 |
| [03-trampas-al-enunciado.feature](03-trampas-al-enunciado.feature) | US-3 · The statement lets no trap through | 4 of 4 |
| [04-pregunta-de-clay.feature](04-pregunta-de-clay.feature) | US-4 · It is Clay's question | 2 of 4 |
| [05-reproducible.feature](05-reproducible.feature) | US-5 · Someone else repeats it without me | 2 of 4 |
| [06-trazabilidad.feature](06-trazabilidad.feature) | US-6 · The evidence is traceable | 5 of 5 |

**How to read the tags.** `@HU-n` is the story, `@CA-n.m` the acceptance criterion, `@cumple` a criterion the evidence supports, and `@pendiente` one that does not yet. Pending scenarios end with a comment that says why.

**What these are and are not.** These scenarios describe the checks that have already been run and point to their evidence. They are not automated tests: the Lean builds take more than an hour and run separately. What does run on every push is in [`verificar.py`](../verificar.py) and in the [CI](../.github/workflows/verify.yml).

The full explanation, with test cases, executions, defects and the traceability matrix, is in [docs/METODOLOGIA.md](../docs/METODOLOGIA.md) ([English](../docs/METHODOLOGY.md)). The interactive version, with the scenarios also translated into English, is at [criguex.github.io/scientific-qa-evidence/metodologia](https://criguex.github.io/scientific-qa-evidence/metodologia/).
