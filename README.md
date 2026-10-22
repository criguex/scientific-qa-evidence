# Scientific QA Evidence

This repository contains an independent QA audit of the Lean 4 formalizations in [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler), which accompany “[Finite time blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf)” and “[Finite time blowup for the Euler equation](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf)” by OpenAI, plus a mutation-testing campaign on nine numerical models. The proofs belong to OpenAI. This repository proves nothing new, claims no Millennium Prize result and is not a mathematical review: it rebuilds the published artifacts, rechecks them with independent checkers, tests whether the checking pipeline catches errors, and publishes every step with hashes.

- [Read the seven-page summary (PDF)](docs/report/scientific-qa-evidence-report-v1.3.1.pdf)
- [Read every claim with its evidence and limits](CLAIMS.md)
- [Watch the evidence scenes](animations/index.html)
- [Help review the transcription of Clay's text](bridges/K0_REVIEW.md)
- [Leer en español](README.es.md)

By **Cristian Guerra**, QA Automation, Medellín, Colombia ([@criguex](https://github.com/criguex)).

## In one minute

OpenAI published Lean proofs that, for the Navier–Stokes equations, there are smooth starting data and forces for which no global smooth solution exists, and a finite-time singularity for the Euler equations. This repository checks those proofs the way a QA engineer would check any important release: rebuild them from source, recheck them with independent tools, try to make the checks fail on purpose, and keep every step reproducible.

Two results stand out:

1. **OpenAI's proofs check, every time and from scratch,** on five builds, two of them compiled entirely from source, with two independent proof checkers.
2. **A Lean proof that OpenAI's theorems imply the Clay Institute's own wording** of the two Navier–Stokes problems (C) and (D), with that wording transcribed literally into Lean. This holds only if the transcription is faithful, and **no independent person has checked that yet.** That check is the one review this project asks for.

Neither result is new mathematics, and nothing here claims a Millennium Prize result.

## What we found

**About OpenAI's proofs**

- They compile from OpenAI's pinned source and pass Comparator, the Lean tool that checks a submitted proof against a fixed challenge statement, with two independent proof checkers (Lean's own kernel and nanoda), on five builds; the last two were compiled from source with nothing prebuilt. A fresh replay of every proof step from an empty start agreed.
- The checked statement is exactly the published challenge: changing one symbol of it in six different ways made Comparator refuse every time, while a change to a comment only was accepted. The challenge text matches Google DeepMind's public formal statement of the problem.
- The checkers used include every Lean kernel soundness fix known in 2026, and a deliberately wrong proof is rejected.
- One build that looked clean had silently received seven prebuilt dependencies; its log did not show it, and only comparing file dates with the build start revealed it. A later build with caching disabled confirmed a fully local build.
- Not checked here: whether the Lean proof follows OpenAI's written paper, which [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) disputes.

**About the Clay Institute's wording**

- OpenAI's theorems are stated in DeepMind's formal style, not in Clay's words. We transcribed Clay's equations and the two problems into Lean, clause by clause, and proved in Lean that OpenAI's theorems imply them, for every viscosity, using only Lean's standard axioms.
- Clay's "smooth up to time zero" can be read in two ways; the implication holds under both.
- A control shows the transcription is not vacuous: the zero flow satisfies all its conditions for zero data, so "no solution exists" is a real statement.
- Open: whether the transcription is faithful to Clay's PDF, and, for the periodic problem (D) only, whether Clay's erratum on periodic pressure applies to solutions. Asked about the erratum, the Clay Institute's president said only that the periodic problems are posed on the torus.

**About the checking tools**

- Comparator compares statements by their exact form: it refused a reformulation that Lean considers identical by definition. So a refusal means only "the statement changed". Telling equivalent, weaker and false changes apart needed a separate proof each time, shown on three theorems Mathlib already proves.
- OpenAI's published procedure does not check that its logs match the record of what was run; a substituted log left its output unchanged, while a check against hashes recorded at run time caught it. This is standard practice in software supply-chain security ([in-toto](https://in-toto.io/), [SLSA](https://slsa.dev/provenance/v1)); here it is a case study, not a new technique.

**About the numerical models**

- On nine synthetic models, the tests flagged all 54 deliberately broken variants (51 distinct behaviours, since two broken variants give identical output), passed the 27 correct ones, and missed 3 deliberately tiny changes, identically on macOS and Linux.

**Our own mistakes, found and corrected in the open**

- A published claim of "no cache downloads" was false (seven prebuilt dependencies), two runs were mislabeled as the same build, and the numerical runner reported a valid reference when it had failed.
- The first version of the planted-fault experiment had evaluator defects; four review rounds found 17 issues, all fixed and kept with errata.
- A results verifier missed Lean's real `sorry` warning and accepted logs without exit codes; a release was first published on a failing build. Each was fixed, tested and recorded.

## Two things we are asking for

If you know Lean or the Navier–Stokes problem: **is [`bridges/ClayLiteral.lean`](bridges/ClayLiteral.lean) a faithful transcription of Clay's official problem statement?** The [review sheet](bridges/K0_REVIEW.md) lists 14 places to compare with the PDF, each with its page, equation and Lean line. They are points to check, not known defects: we found no concrete error. What helps most is a point-by-point answer (agree, object or unsure, with the citation and the argument), especially for (C); the sheet explains the format. Answers will be recorded there as received.

**An independent reproduction.** Every run here was made by the author. If you can rebuild OpenAI's proofs from the fixed version and publish your commit, environment, commands, outputs, exit codes and axioms, the [reproduction guide](docs/INDEPENDENT_REPRODUCTION.md) has the exact steps and a report template. A result that differs from ours is just as useful.

## The method: QA with scientific rigour

The testing method used here follows the scientific method, and every element has a record in this repository:

| Element of the scientific method | How this study applies it |
| --- | --- |
| Hypotheses that can fail | Before each experiment the expected outcome was written down, for example "Comparator must refuse these six changes" |
| Pre-registration | The planted-fault benchmark, the Mathlib controls and the receipt check were published with their expected results before any run ([benchmark](experiments/blind-faults/SEED_COMMITMENT.md), [Mathlib](experiments/mathlib-controls/DESIGN.md), [receipts](experiments/receipt-check/DESIGN.md)) |
| Controls | A clean control, a comment-only control, a `sorry` positive control, a deliberately cheating proof for the dependency guard |
| Attempts at refutation | Statement mutants, planted faults, deliberately broken numerical code: changes that should make the checks fail |
| Reproducibility | Commands, versions, hashes and exit codes for every step; rerun from a fresh clone ([FROM_ZERO](evidence/FROM_ZERO.md)) and in a fifth full build ([B5](evidence/formal/b5/README.md)) |
| Reporting what fails | Where this study's own check misses a fault ([case 2](experiments/receipt-check/RESULTS2.md)), errata kept, corrections made in public |
| Outside review | Four review rounds on the benchmark, an outside reviewer's corrections applied, a review of the Clay transcription requested ([sheet](bridges/K0_REVIEW.md)) |

**How it complements Lean.** Lean checks that each proof step is valid. It does not check how the proof was built, whether the statement checked is the intended one, whether it matches the problem as Clay wrote it, or whether the published evidence is the evidence that was produced. This method covers those: it rebuilds from source, tests that the statement check reacts to changes, connects the formal statement to Clay's text, and binds the recorded evidence to what actually ran. Within this scope, anyone can repeat the checks from public records, and they found no defect: OpenAI's Lean proofs check, and they imply Clay's questions (C) and (D) as transcribed here. That is "no defect found in this scope", not a certification of the whole solution: OpenAI's development and its dependencies were not audited line by line, the Clay transcription still needs an expert, and outside review is there to catch what this study may have missed, not to make the result true by authority.

**What can be claimed.** A QA method applied with scientific rigour (registered hypotheses, controls, attempts at refutation, full reproducibility) to the audit of a high-profile mathematical result. **What cannot be claimed yet** is that the method detects more than other methods in general. That would need cases prepared by someone else, a fair comparison with established tools such as in-toto and SLSA on the same faults, more than one project, and an independent replication.

## Results at a glance

| Question | Result | Record |
| --- | --- | --- |
| Does it build from source? | Yes. Five builds; the last two (B4 and B5, `lake --no-cache build`) exit 0, 11,424 jobs, 1 h 29 min and 1 h 16 min, every dependency compiled locally. | [builds](evidence/formal/cd-validation/README.md#builds-used-by-each-run), [B5](evidence/formal/b5/README.md) |
| Do independent kernels accept it? | Yes. Comparator with nanoda and the Lean kernel accepted Navier–Stokes (C, D) and Euler in all five runs, one per build. | [revalidation](evidence/formal/cd-validation/README.md) |
| Does Comparator check the exact statement? | Yes. 6 of 6 statement mutants refused; comment-only control accepted. | [mutants](evidence/formal/cd-validation/mutants/) |
| Is the challenge the public statement? | The 18 declarations match after textual normalization; name resolution was not verified. | [provenance](evidence/formal/statement-provenance/README.md) |
| Are the checkers current? | The kernel source includes every 2026 kernel soundness fix; nanoda postdates its fix. | [kernel currency](evidence/formal/kernel-currency.md) |
| Do the checkers reject a wrong proof? | Yes. Lean reports a type mismatch; nanoda stops with an internal assertion, classified as a rejection from its pinned source (its raw status is still pending). | [kernel mutation](evidence/formal/kernel-mutation/) |
| Does the formal statement match Clay's text? | Of 16 clauses, 6 match directly, 9 match through standard facts, 1 needs a human decision. In Lean, OpenAI's theorems imply a literal rendering of Clay's (C) and (D); that rendering is not yet independently reviewed. | [risk review](evidence/formal/clay-lean-risk.md), [bridges](bridges/README.md) |
| Do the numerical tests catch bugs? | 27 PASS · 54 KILLED · 3 SURVIVED per host, identical on macOS arm64 and Linux x86_64. | [numerical](evidence/README.md) |
| Does the protocol catch what the baseline misses? | On planted faults in a deterministic benchmark, yes: four fault classes flagged by the protocol and passed by a simulated baseline. | [benchmark](experiments/blind-faults/v2/README.md) |
| Does a refusal mean the theorem is false? | No. On three Mathlib theorems, Comparator refused all 8 changed statements, including 4 equivalent ones (one definitionally equal); a separate Lean route classified each one as equivalent, weaker or false, all as pre-registered. | [Mathlib controls](experiments/mathlib-controls/RESULTS.md) |
| Does the published procedure check its own evidence? | No. On the same authentic files, a receipt naming a missing log and a stale log under the right name left its result unchanged (exit 0, `Your solution is okay!`); P6 caught the first, only a hash-bound check caught both; tools such as in-toto already record and check such hashes. | [receipt check](experiments/receipt-check/RESULTS.md), [case 2](experiments/receipt-check/RESULTS2.md) |

Every claim with its evidence, result and limitation is in [CLAIMS.md](CLAIMS.md).

## Verify it yourself

Python 3.9 or newer, no dependencies, about a minute:

```sh
git clone https://github.com/criguex/scientific-qa-evidence.git
cd scientific-qa-evidence
shasum -a 256 -c evidence/SHA256SUMS.txt                           # every curated file is the published one
python3 evidence/verify_numerical.py                               # saved runs intact and identical across hosts
(cd evidence/numerical/source && python3 -m unittest test_runner)  # reruns all 84 numerical variants
python3 evidence/test_consistency.py                               # README, CLAIMS and records agree
python3 experiments/mathlib-controls/verify.py                     # check Mathlib-control receipts, recompute classes
(cd experiments/receipt-check && python3 -m unittest test_results)  # recompute the receipt checks on the published bundles
```

The same checks, and the tests of every other script, run in [GitHub Actions](.github/workflows/verify.yml) on Ubuntu and macOS on every push. [REPRODUCE.md](REPRODUCE.md) gives the versions, the steps from a clean checkout, and which results are recomputed versus only verified by hash. The Lean builds need OpenAI's repository and a Linux host; their records are verified by hash here. A run of the Python checks, the Lean bridges and the Mathlib-control steps from a fresh clone (not the OpenAI build itself) is recorded in [FROM_ZERO.md](evidence/FROM_ZERO.md).

## Part A · Formal audit of (C), (D) and Euler

```mermaid
flowchart TB
    A[OpenAI's proofs<br/>pinned commit f9e8bc5] --> B[Five builds<br/>B4, B5: nothing prebuilt]
    B --> C[Comparator]
    C --> D[nanoda + Lean kernel<br/>accept in all runs]
    A --> E[Statement mutants<br/>6/6 refused]
    A --> F[leanchecker --fresh<br/>replay OK]
    A --> G[Statement provenance<br/>matches DeepMind]
```

Comparator checks that the submitted solution proves exactly the theorem stated in the challenge file, using only the permitted axioms (`propext`, `Quot.sound`, `Classical.choice`). The first run (2026-10-20) is in [`evidence/formal/comparator/`](evidence/formal/comparator/README.md). The revalidation of 2026-10-21 added three more runs, statement mutants and a fresh replay. All 18 checks finished: none produced an unexpected result, and one could not run. A fifth build, B5, repeated the full build from source for release v1.3.0, and Comparator accepted both challenges again ([B5 record](evidence/formal/b5/README.md)).

<table>
<tr><td valign="top"><a href="animations/rerun.html"><b>Rebuild, check again</b></a> · <a href="docs/media/rerun.mp4">▶ MP4</a><br><a href="animations/rerun.html"><img src="docs/assets/rerun-preview.gif" width="380" alt="Comparator runs on four builds, all accepted"></a></td><td valign="top"><a href="animations/mutants.html"><b>Change the statement; it must be refused</b></a> · <a href="docs/media/mutants.mp4">▶ MP4</a><br><a href="animations/mutants.html"><img src="docs/assets/mutants-preview.gif" width="380" alt="Six statement mutants refused and a comment-only control accepted"></a></td></tr>
<tr><td valign="top"><a href="animations/replay.html"><b>Replay every step from an empty start</b></a> · <a href="docs/media/replay.mp4">▶ MP4</a><br><a href="animations/replay.html"><img src="docs/assets/replay-preview.gif" width="380" alt="Fresh kernel replay and which kernel implementations examined the proofs"></a></td><td valign="top"><a href="animations/provenance.html"><b>Where the statement comes from</b></a> · <a href="docs/media/provenance.mp4">▶ MP4</a><br><a href="animations/provenance.html"><img src="docs/assets/provenance-preview.gif" width="380" alt="OpenAI's challenge text matches DeepMind's public statement"></a></td></tr>
</table>

- **Rebuild, check again.** Four builds: the 2026-10-20 record (B1), an audit build whose Mathlib came from the prebuilt cache (B2), a fresh build (B3), and a full `lake --no-cache build` (B4) with every dependency compiled locally. Comparator accepted both challenges on each; a fifth build, B5, came later and is not in this scene. B3 had silently received 7 small dependencies as prebuilt [Reservoir](https://reservoir.lean-lang.org) archives, which is why B4 exists. The Lean toolchain and checker binaries were reused.
- **Change the statement; it must be refused.** OpenAI's proof is never touched. Six one-symbol edits to the challenge were all refused with `Challenge and solution theorem statement do not match`; a comment-only control was accepted. A refused mutant says nothing about whether the mutated statement is true, and the `f = 0` mutants say nothing about (A) or (B).
- **Replay every step from an empty start.** `leanchecker --fresh` accepted both solutions. It reuses Lean's kernel, so it is not a third implementation. `lean4lean` could not be built for Lean 4.34 and never examined the proofs.
- **Where the statement comes from.** The 18 declarations match after textual normalization; name resolution was not verified. The remaining differences with Google DeepMind's Formal Conjectures file are the import, the namespace, notation copied in with the same definition, and (A)/(B) left out.

**Against Clay's text.** (C) and (D) say "there exist data for which no solution exists", so the formal version could only be easier if it allowed data Clay forbids or demanded more of solutions than Clay does. Of 16 clauses, 6 match directly, 9 match through standard analysis facts, and 1 needs a human decision: Clay's erratum asks for periodic pressure "in Eqn (8)", the data list, while the formalization requires it of solutions in (D). See the [risk review](evidence/formal/clay-lean-risk.md) and Part D.

## Part B · Numerical mutation testing

Mutation testing asks whether a test suite notices when the code is deliberately broken. The contract and its tolerance (10⁻⁶) were frozen before any run ([`CONTRACT.md`](evidence/numerical/source/CONTRACT.md)), and every model has an independent oracle that shares no solver code with the implementation under test. The nine models are RC circuit, Newton cooling, second-order chemical kinetics, Beer–Lambert attenuation, logistic response, Snell refraction, thin lens, acoustic interface and Fechner response.

Each host recorded **27 PASS, 54 KILLED and 3 SURVIVED** over the same **84 paired variants**, not 168 distinct ones; the maximum scaled difference between hosts is 1.11 × 10⁻¹⁶. The 54 KILLED are cases, not behaviors: two acoustic mutants give identical outputs, leaving 51 distinct killed behaviors. The three survivors are a deliberately tiny RC change, kept visible on purpose. All models and inputs are synthetic; none of this is an empirical measurement.

## Part C · What the protocol adds

**Research question.** Can ordinary software-QA techniques (a frozen contract, an independent oracle, deliberate mutations and repeated runs) give an outside reader verifiable confidence in a machine-checked proof and in scientific code, without trusting the original authors' setup?

| Element | Numerical code | Formal proof pipeline |
| --- | --- | --- |
| Contract, frozen first | [`CONTRACT.md`](evidence/numerical/source/CONTRACT.md), tolerance 10⁻⁶ | The official challenge statement and the permitted axioms |
| Independent oracle | A separately coded solution per model | Comparator with two kernels, plus a `leanchecker --fresh` replay |
| Deliberate mutation | Two known bugs per model, plus one near-threshold change | A wrong proof value and six statement mutants with a control |
| Repetition | The same 84 variants on two hosts | Comparator on five builds |
| Specification check | The contract itself | Statement provenance, the Clay risk review and the Lean bridges (Part D) |

### Findings in this case

Compared with the verification procedure in OpenAI's README, the protocol produced eight findings that procedure does not show, three of them corrected defects in this study's own work ([FINDINGS.md](FINDINGS.md)).

### Blind-fault benchmark

An experiment planted faults in controlled cases, assigned by a committed seed and pre-registered (v1). After review it is presented as a deterministic regression benchmark: with the corrected v2 evaluator, written after that review, the protocol's checks flag four fault classes that a simulated baseline passes, both flag the positive control, and the clean case passes both. The first run is kept with errata, and four review rounds found 17 issues in the experiment itself ([results and errata](experiments/blind-faults/RESULTS.md), [corrected benchmark](experiments/blind-faults/v2/README.md)).

<a href="animations/experiment.html"><img src="docs/assets/experiment-preview.gif" width="380" alt="Planted faults flagged by the baseline and by the protocol, and four review rounds"></a><br><a href="docs/media/experiment.mp4">▶ MP4 1080p</a>

### Case study: integrity controls on authentic records

The benchmark's case C/F5 was moved from synthetic records to real ones. On a copy of a from-source build tree, OpenAI's published procedure (`lake exe cache get`, `lake build`, `lake exe comparator ComparatorChallenges/NavierStokes.json`) was recorded step by step, and then run again on a clean bundle and on one whose receipt names a log that does not exist.

| Variant | OpenAI's published procedure | Check P6 |
| --- | --- | --- |
| Clean | exit 0, `Your solution is okay!` | exit 0, no flag |
| Receipt names `comparator-run.log` | exit 0, output byte-identical to the clean run | exit 1, `P6:receipt-log-missing-comparator-run.log` |
| Stale log from another run under the right name (case 2) | exit 0, output byte-identical to the missing-log run | **passes: P6 only checks that the log exists**; a check against the hash recorded when the step ran flags it |

**In this experiment, P6 detects a traceability inconsistency that does not change Comparator's result:** the published procedure, run on the same files, exited 0 with the same output, because it does not by itself check that a receipt corresponds to the log it references. Byte-identical means: in case 1, the clean and missing-log runs; in case 2, the missing-log and stale-log runs, which also match case 1. Case 2's clean run has 13 extra `Built …` lines, because its first Comparator call in a fresh copy also built the Comparator executable. It does not mean Comparator accepted a false proof, since the proof was the same and accepted in both. **Limit of the hash check:** it detects a change relative to a trusted reference value, here the hash recorded when the step ran; it does not authenticate where a log came from if someone can replace both the file and that recorded value. Case 2 shows the limit of P6: a stale log under the right name passes it, and only binding each receipt to the hash recorded when the step ran catches it. Both cases were pre-registered, with commands, versions, outputs and exit codes ([case 1](experiments/receipt-check/RESULTS.md), [case 2](experiments/receipt-check/RESULTS2.md), [status and amendments](experiments/receipt-check/STATUS.md)).

**Not a new technique.** Binding each step's command, inputs and outputs to recorded hashes is established practice in software supply-chain security: [in-toto](https://in-toto.io/) records, for every step, the command, the hashes of its input and output files, its return value and its standard output and error, signs them and verifies them against a layout, and [SLSA provenance](https://slsa.dev/provenance/v1) records how a build was made and from which hashed dependencies. Both faults tested here are of the kind in-toto already detects. This is therefore a **case study of integrity controls for Lean evidence**; a fair comparison with in-toto or SLSA has not been done, and any added value in integration, Lean-specific diagnostics or ease of use would still have to be shown.

### Mathlib controls: "the statement changed" is not "the theorem is false"

A statement checker answers one question: is the submitted theorem exactly the challenge? To see what its answers mean, three theorems Mathlib already proves were each given the correct statement, equivalent reformulations and deliberate errors, with the expected outcome registered before any run. Every refused case then got a **second route** in plain Lean: an equivalence proof, a proof that it is weaker (both directions), or a refutation.

| Theorem | Statement tried | Comparator | Second route in Lean | Class |
| --- | --- | --- | --- | --- |
| Primes | `∀ n, ∃ p, n < p ∧ p.Prime` | ✅ accepted | — | accepted by the checker |
| | `n + 1 ≤ p` instead of `n < p` | ❌ refused | `Iff.rfl`: the same definition | equivalent |
| | `n ≤ p` instead of `n < p` | ❌ refused | equivalence for every predicate `P`, not just primes | equivalent |
| | `∀ n ≤ 100, …` (checking examples) | ❌ refused | full ⇒ bounded; bounded ⇏ full (take `P p := p = 101`) | weaker |
| | `∃ p, ∀ n, n < p ∧ p.Prime` (quantifiers swapped) | ❌ refused | refuted: take n = p | false |
| Cauchy–Schwarz | `abs ⟪x, y⟫ ≤ ‖x‖ * ‖y‖` | ✅ accepted | — | accepted by the checker |
| | `⟪x, y⟫ ^ 2 ≤ ‖x‖ ^ 2 * ‖y‖ ^ 2` | ❌ refused | `abs a ≤ bc ↔ a² ≤ b²c²` when b, c ≥ 0 | equivalent |
| | `<` instead of `≤` | ❌ refused | refuted with x = y = 1 | false |
| Dominated convergence | Mathlib's hypotheses | ✅ accepted | — | accepted by the checker |
| | `Integrable bound` as "measurable and ∫⁻ ofReal bound < ∞" | ❌ refused | equivalent only because domination forces bound ≥ 0 | equivalent |
| | domination removed | ❌ refused | refuted: (n+1) on (0, 1/(n+1)) tends to 0, every integral is 1 | false |

**What it shows.** A refusal only means "the statement changed": Comparator refused all eight changes, even `n + 1 ≤ p`, which Lean treats as identical to `n < p` by definition. An acceptance is equality as Comparator checks it, not a proof of anything else. Telling equivalent, weaker and false apart took a separate proof each time.

**The guard.** Any two true statements are trivially "equivalent", so an equivalence counts only if its proof does not use the theorem under test. A Lean command walks every transitive dependency of the proof:

```text
guard: QAControls.SecondRoute.primes_reform_equiv uses none of the theorems under test (1485 constants checked)
error: guard: QAControls.SecondRoute.primes_reform_equiv_cheat depends on Nat.exists_infinite_primes
```

<a href="animations/controls.html"><img src="docs/assets/controls-preview.gif" width="380" alt="Eleven Mathlib cases: Comparator verdicts, second-route classes and the guard"></a><br><a href="docs/media/controls.mp4">▶ MP4 1080p</a>

The second line is a deliberately cheating proof, rejected as registered. All 11 cases and both controls came out as pre-registered. Every step has a receipt (command, input hashes, output hashes, exit code), and `python3 experiments/mathlib-controls/verify.py` checks the records against them and recomputes every class; that checks the records, it does not rerun Lean ([design](experiments/mathlib-controls/DESIGN.md), [results](experiments/mathlib-controls/RESULTS.md)). Cases prepared by someone else are still needed ([how to contribute](experiments/mathlib-controls/HOLDOUT.md)).

### Prior work

Mutation analysis (DeMillo, Lipton and Sayward, 1978), specification mutation (1985, 2000), mutation analysis of Coq verification projects (mCoq, 2019), mutation analysis of benchmark checkers (2026), the de Bruijn criterion, [Comparator](https://github.com/leanprover/comparator) and Google DeepMind's [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures). The contribution is the combination and its application to the verification pipeline itself; methodological novelty is not claimed ([RELATED_WORK.md](RELATED_WORK.md)).

## Part D · From OpenAI's theorem to Clay's text

### In plain words

Clay's problem (C) asks for this: show that, for some smooth, fast-decaying starting velocity and force, the Navier–Stokes equations have no smooth solution with bounded energy for all time. OpenAI's Lean theorem says the same thing in DeepMind's formal language. The two texts could differ in small ways, and a difference in the wrong direction would make OpenAI's version easier than Clay's.

So, for each condition in Clay's text, we proved one direction in Lean: the data OpenAI uses satisfy Clay's conditions, and anything Clay would accept as a solution is also a solution in OpenAI's sense. Then the argument closes: if Clay's problem had a solution for OpenAI's data, it would be a solution of OpenAI's problem, which OpenAI's theorem rules out. Lean checks every step. What Lean cannot check is whether our Lean transcription of Clay's words is faithful, and that is the review asked for above.


OpenAI proves a formal statement written in Google DeepMind's style. Does it say what Clay's text says? To get Clay's (C) and (D) from it, one direction per clause is enough: OpenAI's data must satisfy Clay's conditions, and any Clay solution must be a formal solution. Then, if a Clay solution existed, it would be a formal one, which OpenAI's theorem rules out.

### What is proved

Clay's equations (1)–(11), (C), (D) and the erratum are written literally in Lean, in coordinates and with one-sided time derivatives, in [`bridges/ClayLiteral.lean`](bridges/ClayLiteral.lean). Then [`bridges/Bridges.lean`](bridges/Bridges.lean) proves, from OpenAI's theorems, with no hypotheses:

```lean
theorem k1_C          (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltC ν               -- Clay's (C)
theorem k1_D          (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltD_withErratum ν   -- Clay's (D)
theorem k1_C_oneSided (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltC_oneSided ν      -- (C), other reading of C^∞ at t = 0
theorem k1_D_oneSided (ν : ℝ) (hν : 0 < ν) : ClayLiteral.AltD_withErratum_oneSided ν
```

All four use only `propext`, `Classical.choice` and `Quot.sound`. A control proves that the zero solution meets every Clay solution condition, so "no solution exists" is not vacuously true.

<a href="animations/bridges.html"><img src="docs/assets/bridges-preview.gif" width="380" alt="Bridge rows from OpenAI's theorem to Clay's text and the four K1 theorems"></a><br><a href="docs/media/bridges.mp4">▶ MP4 1080p</a>

### How each clause is bridged

| Clay's text (as in `ClayLiteral`) | OpenAI's formal version | Lean bridge |
| --- | --- | --- |
| u° smooth, `div u° = 0`, decay (4) | OpenAI's witness has u₀ = 0 | `d1_zero`, `d2_zero`, `d3_zero` |
| f smooth on ℝ³ × [0, ∞), in either reading at t = 0 | OpenAI's force is smooth on all of ℝ × ℝ³, so it is its own extension | `witness_C`, `witness_D` |
| decay (5) and (9) of every mixed partial ∂x^α ∂t^m f | a bound on the norm of the m-th derivative | `d5`, `d7`: a partial is that derivative applied to unit vectors (`clay_bound`) |
| equation (1) in coordinates, with Σⱼ uⱼ∂ⱼuᵢ and Σₖ ∂ₖ² | the vector equation with Mathlib's `Δ` and `gradient` | `s1` |
| (2): Σᵢ ∂uᵢ/∂xᵢ = 0 | trace of the Jacobian = 0 | `s2` |
| (3) initial condition | the same | `s3` |
| (6), (11): u, p ∈ C^∞(ℝ³ × [0, ∞)) | `ContDiffOn` on the closed half-space | `s4` |
| (7): Lebesgue ∫ abs(u)² dx < C | `MemLp 2` and a bound on the Bochner integral | `s5` |
| (8), (10), erratum: periodicity | `IsOnePeriodic` | `d6`, `s6`, `s7_formal_side` |

Every row with its status is in [clay-lean-bridges.md](evidence/formal/clay-lean-bridges.md); the build receipt is in [`bridges/README.md`](bridges/README.md).

### What remains

- **Fidelity of `ClayLiteral`.** The result is only as faithful as the literal rendering, which nobody independent has reviewed against the PDF. In particular, `SmoothOneSided` is defined directly as Mathlib's `ContDiffOn` on the closed half-space; its name does not show that this is the smoothness Clay means, and that correspondence is itself a review point. The 14 points to check, smoothness at t = 0 first, are in [`bridges/K0_REVIEW.md`](bridges/K0_REVIEW.md).
- **Periodic pressure, (D) only.** K1 for (D) reads Clay's erratum as a condition on solutions; (C) does not use it. Asked about it, CMI's president replied on 2026-10-22 that he must avoid interpreting the official statements beyond the official account, and said only that (B) and (D) are problems in the periodic (toral) setting. That does not settle the erratum reading, so it stays open; it is not an endorsement of this reading, the formalization or any solution ([record](evidence/formal/clay-correspondence.md)).
- **No mathematician has reviewed any of this.**

## Animations

Thirteen evidence scenes and one illustrative scene, each offline as an interactive HTML page, a GIF preview and a 1080p MP4. Open the [gallery](animations/index.html), or read the [animation guide](animations/README.md) for equations, parameters and source traces.

<table>
<tr><td valign="top"><a href="animations/rc.html">RC · doubled time constant</a> · <a href="docs/media/rc.mp4">▶ MP4</a><br><img src="docs/assets/rc-mutation.gif" width="360" alt="RC baseline and mutation comparison"></td><td valign="top"><a href="animations/chemistry.html">Chemistry · doubled reaction rate</a> · <a href="docs/media/chemistry.mp4">▶ MP4</a><br><img src="docs/assets/chemistry-preview.gif" width="360" alt="Second-order concentration comparison at fixed volume"></td></tr>
<tr><td valign="top"><a href="animations/cooling.html">Cooling · halved rate constant</a> · <a href="docs/media/cooling.mp4">▶ MP4</a><br><img src="docs/assets/cooling-preview.gif" width="360" alt="Cooling baseline and rate mutation comparison"></td><td valign="top"><a href="animations/snell.html">Snell · swapped refractive indices</a> · <a href="docs/media/snell.mp4">▶ MP4</a><br><img src="docs/assets/snell-preview.gif" width="360" alt="Refraction rays and incidence-angle sweep"></td></tr>
<tr><td valign="top"><a href="animations/campaign.html">Campaign · paired classifications</a> · <a href="docs/media/campaign.mp4">▶ MP4</a><br><img src="docs/assets/campaign-preview.gif" width="360" alt="Per-host mutation campaign classifications"></td><td valign="top"><a href="animations/formal.html">Formal · proof-value typecheck control</a> · <a href="docs/media/formal.mp4">▶ MP4</a><br><img src="docs/assets/formal-preview.gif" width="360" alt="Baseline proof value accepted and wrong-type mutation rejected"></td></tr>
<tr><td valign="top"><a href="animations/rerun.html">C/D · rebuild and recheck</a> · <a href="docs/media/rerun.mp4">▶ MP4</a><br><img src="docs/assets/rerun-preview.gif" width="360" alt="Comparator runs on four builds"></td><td valign="top"><a href="animations/mutants.html">C/D · statement mutants</a> · <a href="docs/media/mutants.mp4">▶ MP4</a><br><img src="docs/assets/mutants-preview.gif" width="360" alt="Statement mutants refused and control accepted"></td></tr>
<tr><td valign="top"><a href="animations/replay.html">C/D · fresh kernel replay</a> · <a href="docs/media/replay.mp4">▶ MP4</a><br><img src="docs/assets/replay-preview.gif" width="360" alt="Fresh kernel replay and kernel implementations"></td><td valign="top"><a href="animations/provenance.html">Statement provenance · OpenAI vs DeepMind</a> · <a href="docs/media/provenance.mp4">▶ MP4</a><br><img src="docs/assets/provenance-preview.gif" width="360" alt="Declarations matching in OpenAI's and DeepMind's statements"></td></tr>
<tr><td valign="top"><a href="animations/bridges.html">Clay ↔ Lean bridges · K1</a> · <a href="docs/media/bridges.mp4">▶ MP4</a><br><img src="docs/assets/bridges-preview.gif" width="360" alt="Bridge rows from OpenAI's theorem to Clay's text and the four K1 theorems"></td><td valign="top"><a href="animations/controls.html">Mathlib controls · refusal is not refutation</a> · <a href="docs/media/controls.mp4">▶ MP4</a><br><img src="docs/assets/controls-preview.gif" width="360" alt="Eleven Mathlib cases: Comparator verdicts and second-route classes"></td></tr>
<tr><td valign="top"><a href="animations/experiment.html">Blind-fault benchmark</a> · <a href="docs/media/experiment.mp4">▶ MP4</a><br><img src="docs/assets/experiment-preview.gif" width="360" alt="Planted faults flagged by baseline and protocol"></td><td valign="top"><a href="animations/flow.html">Illustrative only, not evidence · Taylor–Green flow</a> · <a href="docs/media/flow.mp4">▶ MP4</a><br><img src="docs/assets/flow-scene.gif" width="360" alt="Exact 2D Taylor–Green flow with decaying energy, illustrative only"></td></tr>
</table>

The Taylor–Green scene is visual context only: the exact analytic solution of a smooth, decaying 2D flow, not campaign data, not evidence of blowup and not OpenAI's construction.

## Known limitations

A QA report is only useful if it says what it did not test.

- **One host, reused tools.** All formal runs used one Linux host. Every build reused the installed Lean toolchain and the prebuilt Comparator, lean4export, nanoda and landrun binaries, whose hashes are [recorded](evidence/formal/cd-validation/README.md#reused-tools).
- **Two kernel implementations.** Only the Lean kernel and nanoda have examined the proofs. `leanchecker` reuses the Lean kernel, and `lean4lean` could not be built for Lean 4.34.
- **Known kernel bugs only.** The checkers are current with the known 2026 fixes, but in July 2026 a Lean bug and a separate nanoda bug let the same false proof through, so agreement between two kernels says nothing about unknown bugs.
- **Standalone Comparator.** The runs used the tool pinned at `19e111e`, not the later `lake check` of Lean v4.35.0.
- **Proof correspondence not tested.** Whether the Lean proof follows OpenAI's paper is out of scope; [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) argues it does not, without claiming any Lean theorem is false.
- **The Clay comparison is not reviewed.** The Lean implication is relative to this repository's literal rendering of Clay's text, which no independent person has checked, and it leaves (D) without the erratum on solutions open.
- **Statement mutants test statement equality**, not whether the proof would fail if it were wrong. There is one wrong-proof fixture, not a mutation campaign over OpenAI's proofs.
- **Numerical limits.** The 54 KILLED count cases, not 51 distinct killed behaviors; the mutants are coarse, so the detection threshold is not measured; all models are synthetic.
- **The benchmark uses planted faults** over recorded artifacts, not live Lean, and gives no real-world detection rate.
- **The Mathlib controls are small and author-designed:** 11 cases on three theorems, no held-out cases from someone else yet.

## How AI was used

The work was AI-assisted and human-directed. OpenAI Codex was the main coding agent at first, and Anthropic's Claude Code made the later audit, documentation and experiment changes. Each commit names the agent in a `Co-Authored-By` trailer. Cristian Guerra chose the questions, froze the contracts, decided what counts as evidence and is responsible for every claim. Details, including a mid-session change of the assistant's reported model, are in [AUTHORSHIP.md](AUTHORSHIP.md).

## Repository map

```text
README.md, README.es.md   this overview, in English and Spanish
CLAIMS.md                 every claim → evidence → result → limitation
FINDINGS.md               what the protocol found that the documented procedure does not show
RELATED_WORK.md           prior work and novelty assessment
REPRODUCE.md              versions, steps, recomputed vs hash-verified
AUTHORSHIP.md             authorship and AI disclosure
CITATION.cff, LICENSE_STATUS.md, CONTRIBUTING.md   how to cite, rights, contributions
evidence/
  formal/                 builds, Comparator runs, mutants, replays, provenance, kernel currency,
                          Clay fidelity and risk reviews, bridge table, CMI correspondence
    cd-validation/        the 2026-10-21 revalidation (builds B1–B4, runs 1–4, mutants, replays)
    b5/                   build B5 and run 5, for release v1.3.0
  numerical/              frozen contract, source and tests, 84-case runs for macOS and Linux
  FROM_ZERO.md            checks rerun from a fresh clone
  SHA256SUMS.txt          checksums for every curated file
experiments/
  blind-faults/           benchmark: committed seed and frozen v1, errata, corrected v2 evaluator
  mathlib-controls/       statement changed vs theorem false, on three Mathlib theorems
  receipt-check/          receipts vs artifacts on authentic records, two cases
bridges/                  Clay's text in Lean, the proof that OpenAI's theorems imply it, review sheet
animations/               thirteen evidence scenes and one illustrative scene, build and export scripts, tests
docs/                     GIF previews, MP4 videos, PDF summaries, review request
.github/workflows/        CI that runs every check on each push
```

## Credit, rights and status

- **Original proofs:** OpenAI, [openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler) at `f9e8bc5` (Apache-2.0), with the papers [Finite time blowup for Navier–Stokes](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf) and [for the Euler equation](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf).
- **Problem statement:** C. L. Fefferman, [Existence and smoothness of the Navier–Stokes equation](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), Clay Mathematics Institute. **Challenge statement:** Google DeepMind, [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) at `8bf45ed` (Apache-2.0).
- **Tools, at the revisions used:** [Lean 4](https://github.com/leanprover/lean4) v4.34.0-rc2 (`6a10ac8`), [Mathlib](https://github.com/leanprover-community/mathlib4) (`85e3a25`), [Comparator](https://github.com/leanprover/comparator) (`19e111e`), [lean4export](https://github.com/leanprover/lean4export) (`cacf989`), [nanoda](https://github.com/ammkrn/nanoda_lib) (`9d6964f`), all Apache-2.0, and [landrun](https://github.com/Zouuup/landrun) (`ec104f6`, MIT). Each revision is checked to exist in its repository; binary hashes are in [`receipts/`](evidence/formal/cd-validation/receipts/).
- **Related analysis:** Bastounis, Circelli and Hansen, [arXiv:2610.08144](https://arxiv.org/abs/2610.08144); the rest of the prior work is in [RELATED_WORK.md](RELATED_WORK.md).
- **This QA study:** Cristian Guerra. To cite it, use [CITATION.cff](CITATION.cff).
- **Rights:** publication is authorized, but no open-source license is granted. See [LICENSE_STATUS.md](LICENSE_STATUS.md).
- **Status:** latest release [v1.3.2](https://github.com/criguex/scientific-qa-evidence/releases/tag/v1.3.2), which fixes the state after outside review: the claim scoped to "no defect found in this scope", an [independent reproduction guide](docs/INDEPENDENT_REPRODUCTION.md), the [Clay review sheet](bridges/K0_REVIEW.md) with page, equation and line citations, and three closed tooling findings. It adds no mathematical validation. Earlier: v1.3.1 (receipt check on authentic records, CMI correspondence) and v1.3.0 (Lean bridges to Clay's text, Mathlib controls, build B5). The seven-page PDF summarizes v1.3.1.

No theorem discovery, scientific certification, empirical validation or proof about a real-world system is claimed.
