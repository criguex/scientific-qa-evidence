# Scientific QA Evidence

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23925749.svg)](https://doi.org/10.5281/zenodo.23925749) [![verify](https://github.com/criguex/scientific-qa-evidence/actions/workflows/verify.yml/badge.svg)](https://github.com/criguex/scientific-qa-evidence/actions/workflows/verify.yml)

**An independent software-QA audit of OpenAI's Lean proofs about the Navier–Stokes and Euler equations.** The mathematics is OpenAI's. This repository checks it and makes the checking repeatable by anyone.

[Public page](https://criguex.github.io/scientific-qa-evidence/) · [Leer en español](README.es.md) · [Glossary](docs/GLOSSARY.md) · [Every claim with its evidence](CLAIMS.md) · [Full write-up](docs/DETAILS.md)

By **Cristian Guerra Gómez**, software QA engineer, Medellín, Colombia · [ORCID 0009-0001-7189-5214](https://orcid.org/0009-0001-7189-5214) · [@criguex](https://github.com/criguex)

## In one minute

In 2026 OpenAI published proofs, checked by the Lean proof assistant, that the Navier–Stokes equations **with an external force** can break down: there are smooth starting data and forces for which no smooth solution exists for all time. In the Clay Mathematics Institute's official problem these are alternatives (C) and (D). OpenAI also proved a finite-time singularity for the Euler equations.

I am a software tester, not a mathematician. I checked those proofs the way I would check an important software release:

- rebuild them from a fixed version and check them again with independent tools;
- change the statement on purpose, to confirm that the checks notice;
- write the Clay Institute's own wording in Lean and prove that OpenAI's theorems imply it;
- record every command, version, hash and exit code, including my own mistakes.

**Result: no defect found in this scope.** That is not a certification. Two things are still missing: an expert review of my Lean transcription of Clay's text, and a rebuild of the Lean proofs by someone other than me.

**What this is not.** It is not new mathematics and not a solution of the Millennium Prize problem: the problem without external force, Clay's (A) and (B), remains open. Nobody with mathematical training has reviewed this work yet.

## Check it yourself in five minutes

1. Install [Python](https://www.python.org/downloads/) 3.9 or newer.
2. [Download this repository as a ZIP](https://github.com/criguex/scientific-qa-evidence/archive/refs/heads/main.zip) and unzip it.
3. Open a terminal in that folder and run:

   ```sh
   python verificar.py
   ```

   On Mac or Linux it may be `python3 verificar.py`. In under a minute it runs six checks, prints OK or FALLA (fail) for each one and gives a short **fingerprint**. If your fingerprint matches someone else's for the same data version, you both got exactly the same result. Its messages are in Spanish.

   Reference for the current data version (`c8edd482375d`): fingerprint **`5292-A47D-AFA5`**, the same on my Mac and on GitHub's Ubuntu, macOS and Windows runners.

4. Tell me what you got, same or different, with the [reproduction form](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml). So far there are 4 reports from 3 people, all of whom know me ([reports](evidence/reproductions/README.md)). A different result is just as useful.

The same checks run on every push in [GitHub Actions](.github/workflows/verify.yml). The commands one by one, the versions, and which results are recomputed versus only verified by hash are in [docs/REPRODUCE.md](docs/REPRODUCE.md).

## What was checked

| Question | Answer | Record |
| --- | --- | --- |
| Do OpenAI's proofs build? | Yes. Five builds from OpenAI's pinned commit `f9e8bc5`; the last two (`lake --no-cache build`) compiled every Lean dependency locally, while the Lean toolchain and the checker binaries were reused. A later cloud rebuild on 2026-10-23 (609 of 609 modules, exit 0) used the Mathlib cache. | [builds](evidence/formal/cd-validation/README.md), [cloud rebuild](evidence/lean-cloud-2026-10-23/README.md) |
| Do independent checkers accept them? | Yes. Comparator, with Lean's kernel and the separate checker nanoda, accepted Navier–Stokes (C), (D) and Euler on all five builds. All 18 checks finished. | [revalidation](evidence/formal/cd-validation/README.md) |
| Is the checked statement the published one? | Yes. Six one-symbol changes to the statement were all refused, and a comment-only change was accepted. The 18 declarations match after textual normalization; name resolution was not verified. | [mutants](evidence/formal/cd-validation/mutants/), [provenance](evidence/formal/statement-provenance/README.md) |
| Does it match the Clay Institute's text? | Of 16 clauses, 6 match directly, 9 match through standard facts and 1 needs a human decision. In Lean, OpenAI's theorems imply my literal transcription of Clay's (C) and (D); nobody independent has reviewed that transcription. | [risk review](evidence/formal/clay-lean-risk.md), [bridges](bridges/README.md) |
| What does a refusal by the checker mean? | Only "the statement changed", not "the theorem is false". Shown on three theorems that Mathlib already proves. | [Mathlib controls](experiments/mathlib-controls/RESULTS.md) |
| Does the published procedure check its own logs? | No. A swapped log left its result unchanged, and a check against hashes recorded at run time caught it. This is standard supply-chain practice (in-toto, SLSA), shown here as a case study. | [receipt check](experiments/receipt-check/RESULTS.md) |
| Do the numerical tests catch bugs? | On nine synthetic models: 27 PASS · 54 KILLED · 3 SURVIVED per host, identical on macOS and Linux. The 54 killed variants are 51 distinct killed behaviors, and the 3 survivors are tiny changes kept visible on purpose. All models are synthetic; none of this is an empirical measurement. | [numerical evidence](evidence/README.md) |

My own mistakes, found and corrected in the open, are in the [full write-up](docs/DETAILS.md#what-we-found) and in [FINDINGS.md](FINDINGS.md). [CLAIMS.md](CLAIMS.md) gives each claim with its evidence and its limitation.

## What I am asking for

1. **A review of my transcription of Clay's text.** If you know Lean or the Navier–Stokes problem: is [`bridges/ClayLiteral.lean`](bridges/ClayLiteral.lean) faithful to Clay's official statement? The [review sheet](bridges/K0_REVIEW.md) lists 14 points to compare with the PDF, each with its page, equation and Lean line. Two doubts matter most: what "smooth" means at time zero, and whether the erratum on periodic pressure applies to solutions in (D).
2. **An independent rebuild of the Lean proofs.** Every Lean run so far was made by me or by tools under my direction. The [reproduction guide](docs/INDEPENDENT_REPRODUCTION.md) has the exact steps and a report template.
3. **A run of `verificar.py` on your computer**, reported with the form above. A report from Linux by a person is still missing.

## Main limitations

- **Not reviewed by a mathematician.** The link to Clay's text depends on a transcription that nobody independent has checked.
- **Not independent.** All Lean builds ran on infrastructure I chose (one Linux host and one cloud container operated by an AI agent), and the reproduction reports so far come from people I know.
- **Two kernel implementations only.** Lean's kernel and nanoda examined the proofs; agreement between two checkers says nothing about bugs nobody knows yet.
- **Out of scope:** whether the Lean proof follows OpenAI's written paper, which [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) disputes.
- **Small, synthetic numerical tests** with coarse mutants, so no real-world detection rate.

The complete list is in the [full write-up](docs/DETAILS.md#known-limitations).

## Learn more

| If you want to… | Read |
| --- | --- |
| Understand a term (Comparator, nanoda, mutant, fingerprint…) | [Glossary](docs/GLOSSARY.md) |
| See the whole study: method, parts A–D, animations, every limitation | [Full write-up](docs/DETAILS.md) |
| Check one claim against its evidence | [CLAIMS.md](CLAIMS.md) |
| Review the Lean transcription of Clay's text | [bridges/K0_REVIEW.md](bridges/K0_REVIEW.md) |
| Rebuild the Lean proofs yourself | [docs/INDEPENDENT_REPRODUCTION.md](docs/INDEPENDENT_REPRODUCTION.md) |
| Watch the evidence scenes | [animations](animations/index.html) |
| Know how AI was used | [docs/AUTHORSHIP.md](docs/AUTHORSHIP.md) |
| Find any file | [Documentation map](docs/README.md) |

## Cite, license and credit

- **Cite:** Guerra Gómez, C. *Scientific QA Evidence*. Zenodo. [doi:10.5281/zenodo.23925749](https://doi.org/10.5281/zenodo.23925749) (all versions; see [CITATION.cff](CITATION.cff)).
- **License:** code under [Apache-2.0](LICENSE); text, data and media under [CC BY 4.0](LICENSE-CC-BY-4.0.txt). You may reuse it with credit ([details](LICENSE_STATUS.md)).
- **Original proofs:** OpenAI, [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at `f9e8bc5` (Apache-2.0). **Problem statement:** C. L. Fefferman, [Existence and smoothness of the Navier–Stokes equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), Clay Mathematics Institute. **Challenge statement:** Google DeepMind, [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures). The tools and their versions are in the [full write-up](docs/DETAILS.md#credit-rights-and-status).
- **AI use:** I did this work with AI assistants (OpenAI Codex and Anthropic Claude Code) under my direction. I chose the questions, decided what counts as evidence and am responsible for every claim ([details](docs/AUTHORSHIP.md)).
- **Releases:** [all releases](https://github.com/criguex/scientific-qa-evidence/releases), each one archived on Zenodo.
