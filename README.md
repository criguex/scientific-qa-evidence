# Scientific QA Evidence

**An independent QA reproduction of OpenAI's Lean proofs of finite-time blowup for Navier–Stokes and Euler, plus a mutation-testing campaign on nine numerical models.**

By **Cristian Guerra**, QA Automation, Medellín, Colombia ([@criguex](https://github.com/criguex)) · [Leer en español](README.es.md)

> **Read this first.** The proofs belong to OpenAI ([openai/NavierStokesAndEuler](https://github.com/openai/NavierStokesAndEuler)). This repository proves nothing new, claims no Millennium Prize result, and is not a mathematical review. It is a software-QA exercise: rebuild the published artifacts from pinned sources, recheck them with two independent proof checkers, confirm that a checker rejects a deliberately wrong proof, and publish every result with hashes so anyone can audit it.

## Why this exists

In September 2026 OpenAI published Lean 4 formalizations for alternatives (C) and (D) of the Clay Navier–Stokes problem (breakdown with forcing on ℝ³ and on the periodic torus), and a separate finite-time singularity result for the 3D Euler equation ([blog post](https://openai.com/index/navier-stokes-solution/)). A machine-checked proof can only be trusted as far as the build, the statement and the checker behind it. Those are testing questions:

1. Does it build from a pinned, clean checkout?
2. Do independent kernels accept it against the official challenge statement?
3. Would the checkers notice if a proof were wrong?
4. Does the testing method itself catch mistakes? This is the numerical mutation campaign.

## Results at a glance

| Question | What was done | Result |
| --- | --- | --- |
| Does it build from pinned source? | `lake --no-cache build` on OpenAI commit `f9e8bc5`, Lean 4.34.0-rc2 | Exit 0, 11,424 jobs. Dependency caches were reused, so this is not a full bootstrap. |
| Do independent checkers accept it? | [Comparator](https://github.com/leanprover/comparator) with the Lean kernel and [nanoda](https://github.com/ammkrn/nanoda_lib) on the configured challenges | Navier–Stokes and Euler: both kernels accept (`Your solution is okay!`, exit 0) |
| Does the statement match the Clay text? | Clause-by-clause table against the Clay PDF and the DeepMind [Formal Conjectures](https://github.com/google-deepmind/formal-conjectures) statement at `8bf45ed` | Correspondence mapped and open gaps listed. Documentary only, not an expert equivalence proof. |
| Do the checkers reject a wrong proof? | A fixture whose proof value is wrong but keeps the declared type | Lean reports a type mismatch; nanoda stops with an assertion rejection |
| Do the numerical tests catch bugs? | 9 synthetic models × 3 configurations, each baseline plus known mutations: 84 variants | 27 PASS · 54 KILLED · 3 SURVIVED per host |
| Is it reproducible across machines? | The same 84 variants on macOS arm64 and Linux x86_64 | Identical classifications; maximum scaled difference 1.11 × 10⁻¹⁶ |

## Verify it yourself

Python 3 only, no dependencies, about a minute:

```sh
git clone https://github.com/criguex/scientific-qa-evidence.git
cd scientific-qa-evidence
shasum -a 256 -c evidence/SHA256SUMS.txt     # on Linux: sha256sum -c
python3 evidence/verify_numerical.py
python3 -m unittest discover -s animations -p 'test_*.py'
```

The numerical verifier should print:

```text
PASS: 2 summaries, 168 case records, 2 x 756 observation rows, 738 finite pairs, 18 null pairs; max scaled delta 1.1102230246251565e-16.
```

Those commands check the integrity and consistency of the saved evidence; they do not recompute it. To recompute the whole numerical campaign from scratch (under a second), pass an output directory that does not exist yet:

```sh
cd evidence/numerical/source
python3 runner.py --out /tmp/sqe-rerun
```

It should report 84 variants with `KILLED: 54, PASS: 27, SURVIVED: 3`. Rebuilding the Lean project and rerunning Comparator needs the OpenAI repository and a Lean toolchain; the pins and the recorded procedure are in [`evidence/formal/clean-build/`](evidence/formal/clean-build/README.md).

## Track 1: formal reproduction and controls

```mermaid
flowchart LR
    A[OpenAI-authored original proofs] --> B[Pinned source checkout]
    B --> C[Clean source build<br/>11,424 jobs · exit 0]
    C --> D[Comparator challenge run]
    D --> E[Navier–Stokes<br/>nanoda + Lean accept]
    D --> F[Euler<br/>nanoda + Lean accept]
    G[Separate controlled fixture<br/>valid proof value] --> H[Lean accepts]
    G --> I[Wrong proof value] --> J[Lean type mismatch]
    I --> K[nanoda assertion rejection<br/>classification derived from pinned source]
```

Comparator checks that the submitted solution proves exactly the theorem stated in the challenge file, using only the permitted axioms (`propext`, `Quot.sound`, `Classical.choice`). Each challenge was run once after the source build. Sanitized transcripts, timings and the hashes of the raw originals are in [`evidence/formal/comparator/`](evidence/formal/comparator/README.md). The wrong-proof fixture and the raw and derived classifications are in [`evidence/formal/kernel-mutation/`](evidence/formal/kernel-mutation/). The Clay correspondence table is [`evidence/formal/clay-lean-fidelity.md`](evidence/formal/clay-lean-fidelity.md).

## Track 2: numerical mutation testing

```mermaid
flowchart LR
    A[Contract + tolerance 10⁻⁶] --> B[Model-specific oracle]
    B --> C[Baseline implementation]
    B --> D[Synthetic mutation]
    C --> E[Fixed configurations and solver steps]
    D --> E
    E --> F[PASS / KILLED / SURVIVED]
    F --> G[Pair the same 84 variants<br/>macOS arm64]
    F --> H[Pair the same 84 variants<br/>Linux x86_64]
    G --> I[Compare outputs and classifications]
    H --> I
```

Mutation testing asks whether a test suite notices when the code is deliberately broken. The contract and its tolerance were frozen before any run ([`CONTRACT.md`](evidence/numerical/source/CONTRACT.md)). Every model has an independent oracle that does not share solver code with the implementation under test. The nine models are RC circuit, Newton cooling, second-order chemical kinetics, Beer–Lambert attenuation, logistic response, Snell refraction, thin lens, acoustic interface and Fechner response.

Each host recorded **27 PASS, 54 KILLED and 3 SURVIVED** over the same **84 paired variants**, not 168 distinct ones. The comparison covered 738 finite values and 18 non-finite values (stored as null). The three survivors are the deliberately tiny RC mutation, kept visible on purpose. All models and inputs are synthetic; none of this is an empirical measurement.

## Animations

Open the [offline gallery](animations/index.html), or read the [animation guide](animations/README.md) for equations, parameters, outcomes and source traces.

| Numerical models | Campaign and formal controls |
| --- | --- |
| <a href="animations/rc.html">RC · doubled time constant</a><br><img src="docs/assets/rc-mutation.gif" width="360" alt="RC baseline and mutation comparison"> | <a href="animations/campaign.html">Campaign · paired classifications</a><br><img src="docs/assets/campaign-preview.gif" width="360" alt="Per-host mutation campaign classifications"> |
| <a href="animations/chemistry.html">Chemistry · doubled reaction rate</a><br><img src="docs/assets/chemistry-preview.gif" width="360" alt="Second-order concentration comparison at fixed volume"> | <a href="animations/formal.html">Formal · proof-value typecheck control</a><br><img src="docs/assets/formal-preview.gif" width="360" alt="Baseline proof value accepted and wrong-type mutation rejected"> |
| <a href="animations/cooling.html">Cooling · halved rate constant</a><br><img src="docs/assets/cooling-preview.gif" width="360" alt="Cooling baseline and rate mutation comparison"> | <a href="animations/snell.html">Snell · swapped refractive indices</a><br><img src="docs/assets/snell-preview.gif" width="360" alt="Refraction rays and incidence-angle sweep"> |

![Illustrative Taylor–Green flow clip, separate from the evidence scenes](docs/assets/flow-preview.gif)

The 3D flow clip is visual context only. It is not campaign data, evidence of blowup, or a formal construction; its provenance is in [SOURCE_PROVENANCE.md](evidence/SOURCE_PROVENANCE.md).

## Known limitations

A QA report is only useful if it says what it did not test.

- **Not a full bootstrap.** The source build reused dependency and toolchain caches.
- **One recorded run per challenge.** Comparator ran once per challenge. Raw transcripts are not distributed; sanitized copies and the hashes of the originals are.
- **Two kernels.** Only the Lean kernel and nanoda were used. Other independent checkers, such as [lean4lean](https://github.com/digama0/lean4lean) or [lean4checker](https://github.com/leanprover/lean4checker), have not been run.
- **Standalone Comparator.** The run used the standalone tool pinned at `19e111e`. Comparator has since been merged into Lean core as `lake comparator` and `lake check` (Lean v4.35.0); the result has not been repeated with those.
- **A single wrong-proof fixture.** The formal control shows that the checkers reject one wrong proof value. It is not a mutation campaign over the OpenAI proofs.
- **The Clay table is documentary.** It lists the clauses and the remaining gaps; it has not been reviewed by a mathematician.
- **54 KILLED counts cases, not distinct behaviors.** In the acoustic model, `pressure_boundary_sign` and `impedance_swap` produce identical outputs in all three configurations, so there are 51 distinct killed behaviors.
- **The mutants are coarse.** The smallest killed mutant has a normalized error of 0.12, about 120,000 times the 10⁻⁶ tolerance. The only near-threshold mutant (RC `tau_tiny`, a relative change of 5 × 10⁻⁸) survives roughly 56 to 68 times below tolerance. Sizes in between were not sampled, so the campaign does not locate where detection starts.
- **Synthetic models and oracles.** No laboratory data, real system or scientific result is validated here.
- **The verifier is an integrity check.** `verify_numerical.py` compares saved records against their original hashes and across hosts; recomputation is the separate `runner.py` step above.

Each claim, its exact wording and its evidence file are mapped in [CLAIMS.md](CLAIMS.md).

## How AI was used

The work was AI-assisted and human-directed. OpenAI Codex was the main coding agent: under the author's direction it prepared code, ran builds and renders and drafted documents, and every commit in this repository records it with a `Co-Authored-By` trailer. AI assistants also helped with analysis, translation and review. Cristian Guerra chose the questions, froze the contract, decided what counts as evidence, reran the verifiers and is responsible for every claim. Details are in [AUTHORSHIP.md](AUTHORSHIP.md).

## Repository map

```text
evidence/
  formal/              clean build, Comparator logs, wrong-proof fixture, Clay–Lean table
  numerical/           frozen contract, source, 84-case runs for macOS and Linux
  verify_numerical.py  integrity and cross-host check of the saved runs
  SHA256SUMS.txt       checksums for every curated file
animations/            six offline HTML scenes, build script and tests
docs/assets/           GIF previews used in this README
production/            narration, audio pipeline and log sanitizer, with tests
video/                 Remotion source for the narrated video and five shorts
CLAIMS.md              claim → scope → evidence
AUTHORSHIP.md          authorship and AI disclosure
PUBLICATION_STATUS.md  what is published and what is pending
```

## Credit, rights and status

- **Original proofs:** their OpenAI authors. **Challenge statement:** Google DeepMind Formal Conjectures. **Tools:** Lean 4, mathlib, Comparator, nanoda.
- **This QA study:** Cristian Guerra. To cite it, use [CITATION.cff](CITATION.cff).
- **Rights:** publication is authorized, but no open-source license is granted. See [LICENSE_STATUS.md](LICENSE_STATUS.md).
- **Status:** an introductory thread with animation previews is posted on X. The narrated video (English and Spanish) is prepared as source; renders and uploads are pending. See [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md).

No theorem discovery, scientific certification, empirical validation or proof about a real-world system is claimed.
