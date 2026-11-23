# The audit step by step: stories, criteria and test cases

This page tells the audit the way a QA team tells it when it reviews a software release before it goes to production. There are user stories, acceptance criteria answered with **yes** or **no**, scenarios written in Gherkin, test cases, dated executions and, at the end, the defects found and what is missing.

Everything comes from the evidence already in this repository. Each criterion links the record that supports it. If a criterion cannot be answered with evidence, the answer is **no**, even if I believe it is yes.

**Interactive version, with visual examples:** [criguex.github.io/scientific-qa-evidence/methodology](https://criguex.github.io/scientific-qa-evidence/methodology/) · [en español](https://criguex.github.io/scientific-qa-evidence/metodologia/)

[Back to the README](../README.md) · [Spanish version of this page](METODOLOGIA.md) · [Gherkin scenarios](../features/) (in Spanish) · [Every claim with its evidence](../CLAIMS.md) · [Glossary](GLOSSARY.md)

## The words used here

| Word | What it is | Example in this audit |
| --- | --- | --- |
| User story (US) | What someone needs and why | "As a reviewer, I want the proofs to build, so that I know Lean checked every step" |
| Acceptance criterion (AC) | A yes-or-no question that decides whether the story is met | "Does it build from the pinned commit with exit code 0?" |
| Scenario (Gherkin) | The criterion written as **Given** (the context), **When** (the action) and **Then** (a result that can be measured) | Given commit `f9e8bc5`, when I build it, then it exits with code 0 |
| Test case (TC) | What is concretely done to answer the criterion | Build without cache and check that every `.olean` file is new |
| Execution | A real run of the case, with date, command and result | B4, 21 October 2026, 1 h 29 min, exit code 0 |
| Evidence | The record anyone can review | The log, the receipt with its hash, the results JSON |
| Defect | Something that did not do what it should | A build I believed clean had received prebuilt packages |

One important clarification: **the proof is OpenAI's**. Nothing new is proved here. What is tested is the evidence: whether it builds, whether the statement is the right one, whether it matches Clay's question and whether someone else can repeat it.

## The method, in seven steps

1. **Understand what is asked.** The need is written as a user story: who has it, what they want and why.
2. **Analyze before testing.** Ask "what could go wrong?" and rank the risks. For example, that the verified statement is not the official question, or that a build uses prebuilt pieces without saying so.
3. **Write the acceptance criteria.** Each risk becomes a yes-or-no question. If evidence cannot answer it, it is not a usable criterion.
4. **Write the scenarios in Gherkin.** Each criterion is written with Given, When and Then, in natural language, before anything runs.
5. **Design the test cases.** Each scenario becomes one or more concrete actions: build, run the checker, or change one symbol of the statement to see whether it notices.
6. **Run and keep the evidence.** Each run leaves its command, version, hash and exit code, failed runs included.
7. **Decide and report.** Each criterion ends as yes or no, with its evidence. Defects are recorded, my own included. What is missing is said plainly.

One rule runs through all of it: **the machine checks the computation, the traps check the machine, and a person checks the question.** Verifying (the machine) is not the same as validating (a person decides whether it was the right question).

## Summary: six stories, 24 criteria

| US | The question, in plain words | Criteria met | Scenarios |
| --- | --- | --- | --- |
| [US-1](#us-1--the-proofs-build) | Did Lean check every step of the proof? | **3 of 3** | [01-compilacion.feature](../features/01-compilacion.feature) |
| [US-2](#us-2--other-checkers-agree) | Do other checkers agree? | **3 of 4** | [02-verificadores.feature](../features/02-verificadores.feature) |
| [US-3](#us-3--the-statement-lets-no-trap-through) | Is the verified statement exactly the published one? | **4 of 4** | [03-trampas-al-enunciado.feature](../features/03-trampas-al-enunciado.feature) |
| [US-4](#us-4--it-is-clays-question) | Is it the Clay Institute's official question? | **2 of 4** | [04-pregunta-de-clay.feature](../features/04-pregunta-de-clay.feature) |
| [US-5](#us-5--someone-else-repeats-it-without-me) | Can someone else repeat it without me? | **2 of 4** | [05-reproducible.feature](../features/05-reproducible.feature) |
| [US-6](#us-6--the-evidence-is-traceable-and-the-tool-checks-itself) | Is the evidence reliable, and does the tool check itself? | **5 of 5** | [06-trazabilidad.feature](../features/06-trazabilidad.feature) |
| **Total** | | **19 of 24** | |

**Quick read.** What depends on machines and traps is met. What depends on other people is not yet: an expert still has to review the Clay transcription, and someone other than me has to rebuild in Lean. That is why this is not a certification.

---

## US-1 · The proofs build

> **As** a reviewer of the proof,
> **I want** the code OpenAI published to build from a pinned version,
> **so that** I know Lean checked every step and no step is left unproved.

**Why it matters.** In Lean, if a step of the proof is wrong, the program does not build. Building is the first test: if it fails, there is no point going on. The risk is that the build uses pieces someone else compiled earlier and nobody checked again.

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-1.1 | Does OpenAI's code at commit `f9e8bc5` build and exit with code 0? | **Yes** | [builds B1–B4](../evidence/formal/cd-validation/README.md), [B5](../evidence/formal/b5/), [cloud](../evidence/lean-cloud-2026-10-23/README.md) |
| AC-1.2 | Does it build with every Lean dependency compiled on the machine, without downloading prebuilt pieces? | **Yes** | [B4 and B5 without cache](../evidence/formal/cd-validation/README.md#b4--no-cache-build-2026-10-21) |
| AC-1.3 | Do the conclusions depend only on Lean's three standard axioms, with no pending steps (`sorry`)? | **Yes** | [axiom audit](../evidence/formal/b5/axioms.log) |

### Test cases and executions

| Case | What was done | Execution | Result |
| --- | --- | --- | --- |
| TC-1.1 | Build from the pinned commit, reusing dependency caches | B1 · 20 Oct · 11,424 jobs | Exit 0 |
| TC-1.1 | Build with the official Mathlib cache, as OpenAI instructs | B2 · 20 Oct | Exit 0 |
| TC-1.1 | Rebuild in a cloud container, operated by an AI agent under my direction | 23 Oct · Lean v4.34.0-rc2 | **609 of 609** modules, exit 0 |
| TC-1.2 | Compile Mathlib on the machine, with an empty cache | B3 · 21 Oct · 1 h 27 min | Exit 0, but **with a defect of mine**: 7 dependencies arrived prebuilt ([D-1](#defects-found)) |
| TC-1.2 | Build everything without cache (`lake --no-cache build`) and check that every `.olean` is newer than the start | B4 · 21 Oct · 1 h 29 min | Exit 0, no package downloaded |
| TC-1.2 | Repeat the no-cache build for release 1.3.0 | B5 · 21/22 Oct · 1 h 15 min 39 s | Exit 0, all 11,406 `.olean` files new |
| TC-1.3 | Ask Lean which axioms the final theorems depend on | B5 | Only `propext`, `Classical.choice` and `Quot.sound` |

**What it does not prove.** Every build reused the installed Lean toolchain and the checker binaries, and ran on machines I chose. Building shows the computation is done right, not that it is the right computation (that is US-3 and US-4).

---

## US-2 · Other checkers agree

> **As** a reviewer,
> **I want** separately written checkers to accept the same proof,
> **so that** I do not depend on a single program that might have a bug.

**Why it matters.** If the checker has a bug, it may accept something false. With two separately written checkers that risk drops, though it does not disappear.

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-2.1 | Does Comparator, with Lean's kernel, accept the (C), (D) and Euler solutions on every build? | **Yes** | [revalidation](../evidence/formal/cd-validation/README.md), [20 Oct record](../evidence/formal/comparator/README.md) |
| AC-2.2 | Does a second, separately written checker (nanoda) accept them too? | **Yes** | the same runs |
| AC-2.3 | Do the checkers used include every known kernel soundness fix? | **Yes** | [kernel currency](../evidence/formal/kernel-currency.md) |
| AC-2.4 | Did a third kernel implementation check them? | **No** | lean4lean did not build for Lean 4.34 ([receipt](../evidence/formal/cd-validation/receipts/lean4lean.txt)) |

### Test cases and executions

| Case | What was done | Execution | Result |
| --- | --- | --- | --- |
| TC-2.1 | Run Comparator on every build, for Navier–Stokes and for Euler | Runs 1 to 5, on B1 to B5 | All **18 checks** finished: `Your solution is okay!` and exit 0 in every one |
| TC-2.2 | Replay the kernel check from scratch (`leanchecker --fresh`) | On B2 · 19.6 and 22.5 min | Exit 0 for both solutions |
| TC-2.3 | Compare the kernel source used with the versions that fix the known 2026 bugs | Source review | Identical to v4.33.1, v4.34.0 and v4.34.1 |
| TC-2.4 | Attempt a third check with lean4lean | On B2 | Did not build: incompatible Lean version |

**What it does not prove.** Two agreeing checkers say nothing about a bug neither of them knows. The runs were on a single Linux machine.

---

## US-3 · The statement lets no trap through

> **As** a reviewer,
> **I want** to know that the checker compares the exact statement,
> **so that** I can be sure that what was proved is what was published and not an easier version.

**Why it matters.** "Passing" says little if the test lets anything through. So traps are set: change a single symbol of the statement and see whether the checker notices. In QA this is called **testing the test** (mutation testing).

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-3.1 | Does the checker reject every one-symbol change to the statement? | **Yes, 6 of 6** | [mutants](../evidence/formal/cd-validation/mutants/) |
| AC-3.2 | Does it accept a change that does not alter the meaning (a comment only)? | **Yes** | [control](../evidence/formal/cd-validation/mutants/control_comment.diff) |
| AC-3.3 | Does the challenge statement match the one Google DeepMind published? | **Yes** | [provenance](../evidence/formal/statement-provenance/README.md) |
| AC-3.4 | Do we know what a rejection means: "the statement changed", not "the theorem is false"? | **Yes** | [Mathlib controls](../experiments/mathlib-controls/RESULTS.md) |

### Test cases and executions

The six traps and the control ran on build B2. Each trap took 1.4 minutes (the control, 7 minutes):

| Case | The trap | Expected | Result |
| --- | --- | --- | --- |
| TC-3.1a | (C) without external force (`f = 0`) | Rejection | **Rejected** |
| TC-3.1b | (D) without external force (`f = 0`) | Rejection | **Rejected** |
| TC-3.1c | (C) with periodic data instead of data on ℝ³ | Rejection | **Rejected** |
| TC-3.1d | (C) with viscosity ≥ 0 instead of > 0 | Rejection | **Rejected** |
| TC-3.1e | (D) without the negation: existence instead of breakdown | Rejection | **Rejected** |
| TC-3.1f | Euler with time T* ≤ 1/2 instead of T* ≤ 1 | Rejection | **Rejected** |
| TC-3.2 | Control: change only a comment | Acceptance | **Accepted** |
| TC-3.3 | Compare the 18 declarations with DeepMind's public text | They match | **They match**, after textual normalization |
| TC-3.4 | 11 cases on three theorems Mathlib already proves, registered before running them | Comparator rejects every change, even equivalent ones | **8 of 8 changes rejected**, 4 of them equivalent |

**What it does not prove.** A rejection only says the statement changed. The `f = 0` traps say nothing about alternatives (A) and (B) of the problem, which remain open. The comparison with DeepMind is textual: it was not verified that every name points to the same thing.

---

## US-4 · It is Clay's question

> **As** the mathematical community,
> **I want** the Lean statement to say the same as the Clay Institute's official text,
> **so that** we know whether what was proved answers alternatives (C) and (D) of the problem.

**Why it matters.** This is the **validation** step: the machine can verify a perfect computation that answers another question. No tool decides this alone; it takes a person who knows the problem.

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-4.1 | Were the 16 clauses of Clay's text reviewed one by one against the formal statement? | **Yes** | [risk review](../evidence/formal/clay-lean-risk.md) |
| AC-4.2 | Do OpenAI's theorems imply, in Lean, a literal transcription of Clay's (C) and (D)? | **Yes** | [bridges](../bridges/README.md) |
| AC-4.3 | Did an independent expert review that transcription against Clay's PDF? | **No** | [K0 review sheet](../bridges/K0_REVIEW.md), unreviewed |
| AC-4.4 | Is the reading of periodic pressure in (D) decided? | **No** | [correspondence with Clay](../evidence/formal/clay-correspondence.md) |

### Test cases and executions

| Case | What was done | Result |
| --- | --- | --- |
| TC-4.1 | Compare each Clay clause with the formal statement, ranked by risk | **16 clauses**: 6 match directly, 9 match via standard facts and **1 needs a human decision** |
| TC-4.2 | Write Clay's text in Lean as is (`ClayLiteral.lean`) and prove that OpenAI's theorems imply it | `k1_C` and `k1_D` proved for every viscosity > 0, with the three standard axioms and under both readings of "smooth" at time zero. Of 18 bridge rows: 16 proved, K0 written and non-vacuous, S7 interpretive |
| TC-4.2 | Control: check that the zero solution meets every Clay condition | It does, so the result is not vacuous |
| TC-4.3 | Ask for a review of the transcription, with 14 points to compare against the PDF | **Pending**: nobody has reviewed it |
| TC-4.4 | Ask the Clay Institute about periodic pressure in (D) | **No decision**: they did not interpret it |

**What it does not prove.** The link to Clay is only as good as my transcription, and nobody independent has reviewed it. Whether the Lean proof follows OpenAI's written paper is also not reviewed; [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) discusses that.

---

## US-5 · Someone else repeats it without me

> **As** a person who wants to review this work,
> **I want** to run the checks on my computer and get the same result,
> **so that** I do not have to trust what the author says.

**Why it matters.** Evidence that only works on its author's machine is evidence for nobody else. The **fingerprint** is a short code that sums up the result: if yours and mine match for the same data version, we saw exactly the same thing.

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-5.1 | Does `python verificar.py` give the same fingerprint on Windows, macOS and Linux? | **Yes** | [GitHub Actions](../.github/workflows/verify.yml) |
| AC-5.2 | Did other people run it on their computers and get the same fingerprint? | **Yes** | [reports](../evidence/reproductions/README.md) |
| AC-5.3 | Is there a report from a person on Linux? | **No** | [reports](../evidence/reproductions/README.md) |
| AC-5.4 | Did someone other than me rebuild the proofs in Lean? | **No** | [reproduction guide](INDEPENDENT_REPRODUCTION.md) |

### Test cases and executions

| Case | What was done | Execution | Result |
| --- | --- | --- | --- |
| TC-5.1 | Run the six checks of `verificar.py` on every push | CI on every push: Ubuntu (Python 3.12), macOS and Windows (Python 3.9 and 3.12) | Same fingerprint everywhere. Current version `c8edd482375d` → **`5292-A47D-AFA5`** |
| TC-5.2 | Ask other people to run it and report it with the form | 24 Oct · 4 reports from 3 people (Windows 11 and three Macs) | All 4 match their version: `C5F0-F1A8-2F4D` |
| TC-5.3 | Receive a report from a person on Linux | — | **Pending** |
| TC-5.4 | Rebuild in Lean without my involvement, with the guide and report template | — | **Pending** |

**What it does not prove.** None of those people is independent in the strict sense. `verificar.py` checks the saved evidence; it does not rebuild Lean, which takes more than an hour.

---

## US-6 · The evidence is traceable and the tool checks itself

> **As** an auditor,
> **I want** every result to point to an intact file and the tools to report their own failures,
> **so that** I can trust the evidence and not just the report.

**Why it matters.** A report can say "everything passed" even if a log was changed or the tool failed silently. This step tests the evidence and tests the tests.

### Acceptance criteria

| AC | Question | Met? | Evidence |
| --- | --- | --- | --- |
| AC-6.1 | Does every evidence file keep its recorded SHA-256 hash? | **Yes** | [SHA256SUMS.txt](../evidence/SHA256SUMS.txt) |
| AC-6.2 | Do the README, CLAIMS.md and the records state the same numbers? | **Yes** | [test_consistency.py](../evidence/test_consistency.py) |
| AC-6.3 | Is a changed or missing log detected, even if the published procedure does not notice? | **Yes** | [receipt check](../experiments/receipt-check/RESULTS.md) |
| AC-6.4 | Do the numerical tests catch the planted errors and keep the uncaught ones visible? | **Yes** | [numerical evidence](../evidence/README.md) |
| AC-6.5 | Does the tool report its own failures instead of a false success? | **Yes** | [test_runner.py](../evidence/numerical/source/test_runner.py) |

### Test cases and executions

| Case | What was done | Result |
| --- | --- | --- |
| TC-6.1 | Recompute the SHA-256 of every evidence file (step 1 of `verificar.py`) | OK on every CI run |
| TC-6.2 | Cross-check the README and CLAIMS.md numbers with the machine-readable records (step 4) | OK |
| TC-6.3 | On authentic files, name a log that does not exist in a receipt | The published procedure exits with code 0; the receipt check (P6) exits with code 1 and detects it |
| TC-6.4 | Run 84 numerical variants per host, on macOS and Linux | **27 PASS · 54 KILLED · 3 SURVIVED**, identical on both hosts. The 54 killed are 51 distinct behaviors; the 3 survivors are tiny changes kept visible on purpose |
| TC-6.5 | Inject failures into the oracle and the simulator | Before the fix it said `oracle_valid: true` ([D-3](#defects-found)); now it marks `INCONCLUSIVE` and exits with code 2 |

**What it does not prove.** The numerical models are synthetic: software calculations, not physical measurements. A hash detects changes against a trusted value, but it does not prove who created the file if someone can change both the file and the value.

---

## Defects found

| ID | Defect | Where | How it was found | Status |
| --- | --- | --- | --- | --- |
| D-1 | A build I believed clean (B3) had received 7 prebuilt dependencies, and the log did not show it | My work | Checking `.olean` timestamps against the build start | Fixed: B4 and B5 compile everything on the machine |
| D-2 | Two runs reported as "the same build" had used different builds | My work | Per-run receipts with their original hashes | Fixed: every run states its build |
| D-3 | The numerical runner said `oracle_valid: true` when the oracle failed or returned NaN | My work | Testing the tool itself with injected failures | Fixed: it now gives `INCONCLUSIVE` |
| — | Defects in OpenAI's proofs | — | All the stories above | **None found** within this scope |

All three defects were mine, and the audit found and fixed them in public. They are findings 1, 3 and 8 in [FINDINGS.md](../FINDINGS.md). Finding 7 is not a defect: periodic pressure in (D) is a point for mathematicians to interpret (AC-4.4).

## Traceability matrix

| Criterion | Gherkin scenario | Case | Execution | Met? |
| --- | --- | --- | --- | --- |
| AC-1.1 | Builds from the pinned commit | TC-1.1 | B1, B2, cloud 23 Oct | Yes |
| AC-1.2 | Builds without prebuilt pieces | TC-1.2 | B4, B5 | Yes |
| AC-1.3 | Only the standard axioms | TC-1.3 | B5 | Yes |
| AC-2.1 | Lean's kernel accepts | TC-2.1 | Runs 1–5 | Yes |
| AC-2.2 | nanoda accepts | TC-2.1 | Runs 1–5 | Yes |
| AC-2.3 | Kernel up to date | TC-2.3 | Source review | Yes |
| AC-2.4 | Third implementation | TC-2.4 | lean4lean | No |
| AC-3.1 | Rejects every trap | TC-3.1a–f | 6 mutants on B2 | Yes |
| AC-3.2 | Accepts the control | TC-3.2 | Control on B2 | Yes |
| AC-3.3 | Matches DeepMind | TC-3.3 | Textual comparison | Yes |
| AC-3.4 | A rejection is not a "false" | TC-3.4 | 11 Mathlib cases | Yes |
| AC-4.1 | 16 clauses reviewed | TC-4.1 | Risk review | Yes |
| AC-4.2 | Implies the Clay transcription | TC-4.2 | `k1_C`, `k1_D` | Yes |
| AC-4.3 | Transcription reviewed by an expert | TC-4.3 | — | No |
| AC-4.4 | Periodic pressure decided | TC-4.4 | — | No |
| AC-5.1 | Same fingerprint on three systems | TC-5.1 | CI on every push | Yes |
| AC-5.2 | Same fingerprint for other people | TC-5.2 | 4 reports, 24 Oct | Yes |
| AC-5.3 | Report from Linux | TC-5.3 | — | No |
| AC-5.4 | Independent rebuild | TC-5.4 | — | No |
| AC-6.1 | Hashes intact | TC-6.1 | CI | Yes |
| AC-6.2 | Documents consistent | TC-6.2 | CI | Yes |
| AC-6.3 | Altered log detected | TC-6.3 | P6 | Yes |
| AC-6.4 | Numerical traps | TC-6.4 | macOS and Linux | Yes |
| AC-6.5 | The tool reports its failures | TC-6.5 | Injected failures | Yes |

## What is missing for all 24 criteria to say yes

1. **AC-4.3:** someone who knows Lean or the problem reviews [`bridges/ClayLiteral.lean`](../bridges/ClayLiteral.lean) with the [K0 sheet](../bridges/K0_REVIEW.md).
2. **AC-4.4:** a mathematician decides how to read periodic pressure in (D).
3. **AC-5.4:** someone other than me rebuilds in Lean with the [guide](INDEPENDENT_REPRODUCTION.md).
4. **AC-5.3:** a `verificar.py` report from Linux, with the [form](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml).
5. **AC-2.4:** a third kernel implementation that works with Lean 4.34.

The first four depend on people, not machines. That is the last gate: **be the referee**.
