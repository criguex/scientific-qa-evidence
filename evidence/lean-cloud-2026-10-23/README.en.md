> English translation of [README.md](README.md). If they differ, the original prevails.

# Rebuilding OpenAI's proofs in a cloud container (Oct 23, 2026)

With help from an AI assistant and under my direction, I rebuilt OpenAI's Lean proofs in a cloud Linux container, separate from my own computer. In this folder I keep the complete evidence of that run, the same evidence I sent to OpenAI support (case 17914950).

## Result

| Step | Result |
|---|---|
| `lake build +NavierStokes.ComparatorSolution:olean` | exit code 0 at 21:53:04 UTC; 609 of 609 `NavierStokes` modules in the import chain ([end of the log](build-tail.log)) |
| Axioms of `navier_stokes_breakdown_R3` and `navier_stokes_breakdown_periodic` | `propext`, `Classical.choice`, `Quot.sound`; no `sorryAx` |
| `ClayLiteral`, `Bridges` and `Audit` on three pinned versions of this repository (c5f4f55, 059a53c, ac195f7) | 9 of 9 steps with exit code 0, the last at 21:58:36 UTC ([summary](final-verification-summary.json)) |

Versions: Lean v4.34.0-rc2, a single process (`LEAN_NUM_THREADS=1`), OpenAI `NavierStokesAndEuler` at f9e8bc5b38b6e212696e8a30e3e91517af887bbd.

## Limits

- **It is not a build from scratch:** the official Mathlib dependency cache was used. The full no-cache builds are B4 and B5, in [evidence/formal](../formal/).
- **It is not independent:** I operated it with help from an AI assistant and under my direction. It is still pending for someone else to rebuild it ([guide](../../docs/INDEPENDENT_REPRODUCTION.md)).
- **The audit prints declarations and axioms;** it is not a check with a second kernel.
- **Version c5f4f55 keeps explicit bridge hypotheses.** 059a53c and ac195f7 do not have them and require positive viscosity. Branch D concludes `AltD_withErratum`.
- **There was an interruption:** the run that started at 20:55 UTC lost tracking after 281 modules. It was logged as interrupted, with an unknown exit status, and was resumed at 21:19:24 UTC without overwriting logs. The detail is in `LEEME_RESULTADO.txt`.

## How to check the package

```sh
shasum -a 256 evidencia_Lean_completa_20261023.zip
# 639cdab5f067d3e421132c9495962755408d30baf78d1455f4deeb41be27b080
```

The zip contains 242 files: commands, pinned sources, logs, receipts with input and output hashes, and the event chains of each run. Start with [`LEEME_RESULTADO.txt`](LEEME_RESULTADO.txt). A matching hash proves the file is the same one that was sent, not who made it.

---

**In English.** With help from an AI assistant and under my direction, I rebuilt OpenAI's Lean proofs in a cloud Linux container on 2026-10-23. `ComparatorSolution` built with exit code 0 (609/609 modules). The two headline theorems use only `propext`, `Classical.choice` and `Quot.sound`. The Clay transcription, bridges and axiom audit passed in three pinned versions of this repository (9/9). I used the official Mathlib cache, so this is not an independent reproduction.
