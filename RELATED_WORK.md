# Related work and novelty assessment

Is the method in this package new? This is a **targeted search**, not a systematic review. It was done on 2026-10-21 with web searches on four topics: mutation of specifications, mutation of formal verification projects, testing of proof checkers, and QA of scientific software. The verification column says how far each source was checked; "abstract" or "search record" means the full text was not read.

## What already exists

| Area | Prior work | What it does | Relation to this study | Verified |
| --- | --- | --- | --- | --- |
| Mutation testing | DeMillo, Lipton and Sayward (1978) | Seed known faults and check that tests notice them | The basis of both tracks | Standard reference |
| Specification mutation | Budd and Gopal, "Program testing by specification mutation", *Computer Languages* 10(1):63–73 (1985); Black, Okun and Yesha, "Mutation operators for specifications", ASE 2000 | Mutate the specification, not only the code | Statement mutants are specification mutants | Search record |
| Mutation of proof-assistant projects | Celik, Palmskog, Parovic, Gallego Arias and Gligoric, "Mutation Analysis for Coq", ASE 2019; Jain et al., mCoq tool demo, ICSE 2020 | Mutate Coq definitions and re-check the proofs; a mutant whose proofs still pass points to an incomplete specification | Closest prior art for formal mutation. mCoq mutates definitions and expects proofs to break; this study mutates the challenge statement and expects the statement checker to refuse. | [Slides](https://users.ece.utexas.edu/~gligoric/slides/CelikETAL19mCoq.pdf), [ASE page](https://2019.ase-conferences.org/details/ase-2019-papers/90/Mutation-Analysis-for-Coq) |
| Mutation in Lean projects | Community practice, for example [a Lean mutation gate](https://github.com/MorphIQ-Labs/tollgate/pull/23) that mutates definition bodies and requires surviving mutants to be justified | Same idea as mCoq, in Lean 4 | Shows the practice exists in Lean | Pull request text only |
| Mutation of checkers and oracles | Du, Luu, Huang and Ng, "Measuring the Checker: Mutation Analysis for GPU-Kernel Benchmark Oracles", [arXiv:2609.22220](https://arxiv.org/abs/2609.22220) (2026) | Mutation analysis aimed at the checker of a benchmark rather than at the code under test | Same aim as the statement mutants, in another domain | Title only |
| Tolerance-aware mutation for numerical code | Hook and Kelly: mutation sensitivity testing (Hook, Queen's University thesis, 2009; MATmute) | Sweep the size of a mutation to measure how small an error a test still detects, under a numerical tolerance | Fills a gap this study states openly: the detection threshold was not measured | Thesis record |
| Testing scientific software | Kanewala and Bieman, "Testing scientific software: a systematic literature review", *Information and Software Technology* (2014), [arXiv:1804.01954](https://arxiv.org/abs/1804.01954) | Surveys the oracle problem and remedies | Background for independent oracles and frozen tolerances | Abstract |
| Independent proof checkers | de Bruijn criterion; [Lean4Lean](https://arxiv.org/abs/2403.14064) (Carneiro); [nanoda](https://github.com/ammkrn/nanoda_lib) (Bailey); [Comparator](https://github.com/leanprover/comparator) and Lean's [validating-proofs guide](https://lean-lang.org/doc/reference/4.35.0/ValidatingProofs/) | Re-check proofs with small, separate kernels and check the statement against a trusted challenge | This study uses these tools; it does not extend them | Primary pages |
| Limits of independent kernels | 2026 Lean kernel soundness bugs: [#14576 postmortem](https://leodemoura.github.io/blog/2026-8-1-postmortem-for-kernel-soundness-bug-14576/), [bug-hunt postmortem](https://leodemoura.github.io/blog/2026-8-24-postmortem-for-the-kernel-soundness-bug-hunt/), [Lean 4.34.0 notes](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/) | A kernel bug and a separate nanoda bug let the same false proof through | Two agreeing kernels are not a guarantee; see [kernel currency](evidence/formal/kernel-currency.md) | Primary pages |
| Misformalized statements | Ospanov, Farnia and Yousefzadeh, "miniF2F-Lean Revisited" ([arXiv:2511.03108](https://arxiv.org/abs/2511.03108)); Poiroux, Weiss, Kunčak and Bosselut, "Reliable Evaluation and Benchmarks for Statement Autoformalization", which introduces ProofNet# ([arXiv:2406.07222](https://arxiv.org/abs/2406.07222)); Ammanamanchi, Bhat and Biderman, "Faults in Our Formal Benchmarking" ([arXiv:2606.29493](https://arxiv.org/abs/2606.29493)) | Formal statements in benchmarks often differ from the intended informal ones | Why statement provenance and the Clay review matter | Abstracts |
| Supply-chain provenance and step attestation | [in-toto](https://in-toto.io/) (`in-toto-run` records each step's command, the hashes of input and output files, return value and stdout/stderr, signed, and verifies them against a layout); [SLSA provenance](https://slsa.dev/provenance/v1) (builder, build definition and hashed resolved dependencies) | Bind every step of a build or pipeline to the exact artifacts it used and produced | The receipt check (P6 and the hash check) is a small subset of what in-toto records; detecting a changed log by SHA-256 is established practice | Documentation; added 2026-10-22 after outside review |
| **This exact proof** | Bastounis, Circelli and Hansen, "Navier-Stokes lost in translation: Why Lean verification of AI autoformalisation does not guarantee correct natural language proofs", [arXiv:2610.08144](https://arxiv.org/abs/2610.08144) (6 Oct 2026) | Argues that OpenAI's formalised Lean proof does not correspond to the natural-language proof in OpenAI's paper | A different layer from this study; see below | Abstract |

## Where this study sits

A passing Lean check involves separate questions:

| Layer | Question | This study |
| --- | --- | --- |
| Kernel acceptance | Does the Lean proof derive the formal statement? | Tested: five builds, two kernels, a fresh replay, kernel currency |
| Statement fidelity | Is the formal statement the intended problem? | Partly: textual provenance against DeepMind's statement and a reading-based review against Clay's text |
| Proof correspondence | Does the Lean proof follow the paper's argument? | **Not tested.** arXiv:2610.08144 argues it does not. Its abstract does not claim that any Lean theorem is false or that the final statement differs from Clay's. |

So the results here say that the formal theorems are accepted, repeatedly and from scratch. They say nothing about whether OpenAI's natural-language paper is correct.

## Novelty assessment

**Not new:** binding pipeline steps to hashed inputs, outputs and logs (in-toto, SLSA), mutating specifications (1985, 2000), mutating formal verification projects (mCoq, 2019), mutating a benchmark's checker (2026), independent kernels and statement checking (Comparator, nanoda, Lean4Lean), tolerance-aware mutation of numerical code (Hook and Kelly), and independent oracles for scientific software.

**Not found in the sources searched:** using one-symbol mutants of a challenge statement, with a comment-only control, as a negative control on a statement-equality checker such as Comparator; and running that together with a numerical mutation campaign under one hash-linked, reproducible protocol on a public Millennium-problem formalization.

**Conclusion.** The method is a combination and application of established techniques. A claim of methodological novelty is **not supported**. The narrower statement that the statement-mutant control was not found in the sources searched holds only for this targeted search and could be overturned by a systematic review.

## What this changes in the package

- The open "novelty" question in [CLAIMS.md](CLAIMS.md) is answered: not claimed, with prior art named.
- Proof correspondence with OpenAI's paper is listed as out of scope, citing arXiv:2610.08144.
- A [kernel currency check](evidence/formal/kernel-currency.md) was added after the search surfaced the 2026 soundness bugs.
- Hook and Kelly's mutation sensitivity testing is the natural next step for the numerical track: it measures the detection threshold this study left unmeasured.
