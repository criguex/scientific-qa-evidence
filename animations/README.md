# Animation guide

The six standalone HTML scenes and their animated preview loops are committed in this directory's parent `docs/assets/` folder. The scenes are offline, interactive, and read the same evidence-derived manifest ([`manifest.json`](manifest.json)). Open [`index.html`](index.html) for the gallery, or open an individual scene directly. Each page has playback/seek controls, an accessible text summary, and its embedded data. The HTML and plotted curves are visual explanations; the evidence remains the saved fixtures and case records linked below.

## Numerical scenes

The three ODE scenes—RC, chemistry, and cooling—use the synthetic suite's `1e-6` normalized-error tolerance and compare an RK4 implementation with a separately coded analytic oracle. Solid curves are analytic reconstructions; hollow points are recorded 256-step RK4 outputs at quarter-interval checkpoints. The models are illustrative software tests, not physical measurements. Snell is algebraic, not an ODE: its independent oracle uses bisection, and its comparison uses the same `1e-6` tolerance.

### 1. RC circuit — one mutation, a computed difference

![RC baseline and doubled-time-constant preview](../docs/assets/rc-mutation.gif)

- **Model:** `C dV/dt = (Vin − V)/R`; oracle `V(t) = Vin + (V0 − Vin)e^(−t/RC)`.
- **Parameters and sweep:** `Vin=5 V`, `V0=0 V`, `R=1,000 Ω`, `C=0.001 F`; `τ=RC=1 s`; checkpoints at `t=0.75, 1.50, 2.25, 3.00 s`.
- **Comparison:** baseline final recorded value is **4.751 V**. The synthetic `tau_double` mutation uses `τ=2 s` and ends at **3.884 V**. Both values are recorded RK4 outputs rounded for display; the analytical curve is reconstructed from the equation. The visual capacitor fill denotes normalized charge, not water.
- **What it tests:** the numerical contract detects a changed time constant at this configuration. Separate tiny `5e-8` time-constant calibrations can legitimately survive the tolerance; that survivor result is preserved in the broader campaign.
- **Trace:** [scene](rc.html) · [baseline fixture](../evidence/numerical/fixtures/rc-baseline.json) · [mutation fixture](../evidence/numerical/fixtures/rc-tau-double.json) · [independent oracle](../evidence/numerical/source/oracles.py) · source hashes and data in [`manifest.json`](manifest.json).

### 2. Second-order chemistry — concentration changes, volume does not

![Second-order chemistry baseline and doubled-rate preview](../docs/assets/chemistry-preview.gif)

- **Model:** `dA/dt = −kA²`; oracle `A(t)=A₀/(1+kA₀t)`.
- **Parameters and sweep:** `A₀=1.2 mol/L`, `k=0.4 L/(mol·s)`, horizon `4.1667 s`; checkpoints at approximately `1.0417, 2.0833, 3.1250, 4.1667 s`.
- **Comparison:** baseline ends at **0.400 mol/L**; the synthetic `rate_double` mutation uses `k=0.8 L/(mol·s)` and ends at **0.240 mol/L**. At the first checkpoint the recorded outputs are **0.800** and **0.600 mol/L**, respectively. Vessel fill remains fixed; concentration is encoded by solute marks/color, not liquid volume.
- **What it tests:** sensitivity to a rate-constant mutation under a positive, non-increasing concentration invariant and the independent analytic oracle.
- **Trace:** [scene](chemistry.html) · [baseline case 022](../evidence/numerical/paired/macos-arm64/case_022.json) · [mutation case 024](../evidence/numerical/paired/macos-arm64/case_024.json) · oracle and hashes in [`manifest.json`](manifest.json).

### 3. Newton cooling — an invariant can pass while the oracle fails

![Newton cooling baseline and halved-rate preview](../docs/assets/cooling-preview.gif)

- **Model:** `dT/dt = −k(T−Tₐ)`; oracle `T(t)=Tₐ+(T₀−Tₐ)e^(−kt)`.
- **Parameters and sweep:** `T₀=90 °C`, ambient `Tₐ=20 °C`, `k=0.2 s⁻¹`, horizon `15 s`; checkpoints at `3.75, 7.50, 11.25, 15 s`.
- **Comparison:** baseline ends at **23.49 °C**. The synthetic `rate_half` mutation uses `k=0.1 s⁻¹` and ends at **35.62 °C**. The mutant still satisfies the temperature invariant, but its recorded normalized oracle error is **0.249236**, exceeding `1e-6`; it is therefore **KILLED** by the oracle comparison, not by the invariant.
- **What it tests:** that passing a broad invariant is insufficient when the actual modeled rate is wrong.
- **Trace:** [scene](cooling.html) · [baseline case 013](../evidence/numerical/paired/macos-arm64/case_013.json) · [mutation case 015](../evidence/numerical/paired/macos-arm64/case_015.json) · [`manifest.json`](manifest.json).

### 4. Snell refraction — an angle sweep, not a time axis

![Snell refraction baseline and swapped-index preview](../docs/assets/snell-preview.gif)

- **Model:** `n₁ sin(θ₁) = n₂ sin(θ₂)`; oracle solves for `θ₂` by bisection. Angles in the diagram are measured from the normal.
- **Parameters and sweep:** `n₁=1`, `n₂=1.5`; incidence angle increases from `0` to `0.4 rad`. The four recorded checkpoints are at `θ₁=0.1, 0.2, 0.3, 0.4 rad`.
- **Comparison:** at `θ₁=0.4 rad`, baseline recorded `θ₂` is **0.262621 rad**. The synthetic `index_swap` mutant swaps the indices and records **0.623805 rad**. The mutant's normalized oracle error is **0.361184**, above `1e-6`; all sampled angles remain below the total-internal-reflection boundary.
- **What it tests:** a known parameter-ordering mutation against the independent bisection oracle. The ray drawing is an analytic schematic, not a wave-optics simulation.
- **Trace:** [scene](snell.html) · [baseline case 040](../evidence/numerical/paired/macos-arm64/case_040.json) · [mutation case 041](../evidence/numerical/paired/macos-arm64/case_041.json) · [`manifest.json`](manifest.json).

## Campaign and formal-control scenes

### 5. Paired mutation campaign — counts, not a benchmark

![Paired mutation campaign classifications by host](../docs/assets/campaign-preview.gif)

- **Visualized data:** each host ran the same 84 paired variants: **27 PASS, 54 KILLED, 3 SURVIVED per host** on macOS arm64 and Linux x86_64. This is 84 paired variants per host, not 168 distinct variants.
- **Method:** nine synthetic models with three fixed configurations each, two known synthetic mutations per model, plus three RC calibration variants. ODE outputs use 64/128/256 steps; algebraic/integral cases are evaluated once rather than being given artificial refinement steps. A baseline passes only when outputs are finite, invariants hold, and normalized error is at most `1e-6`. A mutant is KILLED only if its baseline passes and the mutant is non-finite, violates an invariant, or exceeds tolerance. Otherwise a mutation may SURVIVE.
- **Comparison checks:** the paired records contain 738 finite value pairs and 18 non-finite pairs exported as null. The maximum cross-host scaled delta is **1.11 × 10⁻¹⁶**. The animation's reveal sequence is not timing or performance data.
- **What it tests:** repeatability of these fixed synthetic cases and consistency of saved classifications/outputs across the two recorded hosts. It does not establish behavior outside these fixtures or measure scientific systems.
- **Trace:** [scene](campaign.html) · [paired case JSON/CSV and summaries](../evidence/numerical/paired/) · [derived comparison](../evidence/numerical/multidomain_derived.json) · [suite contract](../evidence/numerical/source/CONTRACT.md) · [`manifest.json`](manifest.json).

### 6. Formal typecheck control — one deliberately mismatched proof value

![Formal control: baseline accepted, wrong-type proof value rejected](../docs/assets/formal-preview.gif)

- **Fixture:** baseline `theorem target : 0 = 0 := rfl`; control changes only the exported proof value to `True.intro` while retaining the expected type `0 = 0` and dependencies.
- **Recorded result:** Lean accepts the baseline and rejects the mutation with a type mismatch (`True` supplied, `0 = 0` expected). nanoda accepts the baseline. The nanoda mutant is derived as `TYPECHECK_ASSERTION_REJECT_DERIVED` from inspection of the pinned typechecker source; its raw summary remains `COLLECTED_PENDING_CLASSIFICATION`, and the binary output is not a structured rejection category.
- **What it tests:** this fixture's bounded wrong-type control. It is not a fresh kernel run, a theorem-discovery result, a general kernel-correctness claim, or verification of Navier–Stokes/Euler mathematics.
- **Trace:** [scene](formal.html) · [fixture](../evidence/formal/fixtures/KernelFixture.lean) · [raw and derived records](../evidence/formal/kernel-mutation/) · [`manifest.json`](manifest.json).

## C/D revalidation and statement scenes

These four scenes play in real time (20 seconds) with a caption box that explains each step in plain language. All values come from [`evidence/formal/cd-validation/results.json`](../evidence/formal/cd-validation/results.json), the [2026-10-20 Comparator record](../evidence/formal/comparator/README.md), the [statement comparison](../evidence/formal/statement-provenance/result.json) and the [Clay risk review](../evidence/formal/clay-lean-risk.md).

### 7. Rebuild from zero, check again

![Rebuild from zero and three Comparator runs](../docs/assets/rerun-preview.gif)

- **Shows:** source → from-scratch build (Mathlib modules compiled, cache downloads, jobs, time) → Comparator's three checks, then a grid of the three Comparator runs for Navier–Stokes (C, D) and Euler with recorded times.
- **Does not show:** that the formal statement matches Clay's text, or anything about (A) and (B).
- **Trace:** [scene](rerun.html) · [results](../evidence/formal/cd-validation/README.md).

### 8. Statement mutants

![Statement mutants refused and control accepted](../docs/assets/mutants-preview.gif)

- **Shows:** each case in turn, with the original challenge line, the mutated line with the changed span highlighted, and Comparator's decision. The list below accumulates the seven verdicts.
- **Does not show:** that a mutated statement is false. The `f = 0` cases are not evidence about (A) or (B).
- **Trace:** [scene](mutants.html) · [mutant diffs](../evidence/formal/cd-validation/mutants/).

### 9. Fresh kernel replay

![Fresh kernel replay and kernel implementations](../docs/assets/replay-preview.gif)

- **Shows:** `leanchecker --fresh` replay times for both solutions, then which kernel implementations have actually examined the proofs: nanoda and Lean's kernel did; lean4lean could not be built for Lean 4.34.
- **Does not show:** a third independent kernel.
- **Trace:** [scene](replay.html) · [logs](../evidence/formal/cd-validation/logs/).

### 10. Statement provenance

![OpenAI's challenge compared with DeepMind's statement](../docs/assets/provenance-preview.gif)

- **Shows:** the 18 named declarations that match after textual normalization in DeepMind's `8bf45ed` and OpenAI's `f9e8bc5` (name resolution not verified), the packaging differences, and the counts from the Clay risk review.
- **Does not show:** an expert equivalence proof with Clay's text.
- **Trace:** [scene](provenance.html) · [comparison](../evidence/formal/statement-provenance/README.md) · [risk review](../evidence/formal/clay-lean-risk.md).

### 11. Blind-fault benchmark

![Planted faults flagged by baseline and protocol, and four review rounds](../docs/assets/experiment-preview.gif)

- **Shows:** the chain that makes the run auditable (committed seed → frozen design → drawn cases → blind results → key → seed reproduced), which procedure flags each planted fault class under the corrected v2.2 evaluator, and what each of the four review rounds found.
- **Does not show:** a real-world detection rate; the faults are planted in recorded artifacts, not live Lean.
- **Trace:** [scene](experiment.html) · [results with errata](../experiments/blind-faults/RESULTS.md) · [v2 benchmark](../experiments/blind-faults/v2/README.md) · [review rounds data](../experiments/blind-faults/review_rounds.json).

## Clay and checker-meaning scenes

### 12. From OpenAI's theorem to Clay's text

![Bridge rows from OpenAI's theorem to Clay's text and the four K1 theorems](../docs/assets/bridges-preview.gif)

- **Shows:** the three layers (OpenAI's formal theorem, the Lean bridges, Clay's text written literally in Lean), every bridge row colored by the status recorded in the bridge table, and the four K1 theorems with their axioms.
- **Does not show:** that the literal rendering is faithful to Clay's PDF, which is not yet independently reviewed, or any mathematician's review. S7, periodic pressure, affects (D) only.
- **Trace:** [scene](bridges.html) · [bridge table](../evidence/formal/clay-lean-bridges.md) · [Lean files and receipt](../bridges/README.md) · [review sheet](../bridges/K0_REVIEW.md).

### 13. Mathlib controls: a refusal is not a refutation

![Eleven Mathlib cases: Comparator verdicts, second-route classes and the guard](../docs/assets/controls-preview.gif)

- **Shows:** each pre-registered case, Comparator's verdict from its receipt, the class recomputed by `verify.py` from the published logs, and the two guard lines copied from the real logs.
- **Does not show:** a detection rate; the cases are author-designed, and held-out cases are still missing.
- **Trace:** [scene](controls.html) · [design](../experiments/mathlib-controls/DESIGN.md) · [results](../experiments/mathlib-controls/RESULTS.md) · [receipts](../experiments/mathlib-controls/results/receipts.jsonl).

## Separate 3D flow context

![Taylor–Green flow context clip, separate from the campaign and model animations](../docs/assets/flow-preview.gif)

The gallery also embeds a cropped Taylor–Green flow visualization from the project's existing video asset. It is labeled illustrative context only: it is not campaign data, evidence of blow-up, a formal solution, or a synthetic physics scene generated by this animation set. Its source and crop provenance are documented in [`evidence/SOURCE_PROVENANCE.md`](../evidence/SOURCE_PROVENANCE.md).

## Rebuild, test, and export

From the repository root, regenerate the standalone HTML files and data-derived manifest, then run the deterministic tests:

```sh
python3 animations/build.py
python3 -m unittest discover -s animations -p 'test_*.py'
```

The README previews in `docs/assets/` are exported from these same HTML scenes at full 1080 × 1080 resolution: 120 frames sampled evenly across the 20-second scene and played at 15 fps as an 8-second loop, with one global 256-color palette. The four captioned C/D scenes are exported in real time instead, 200 frames at 10 fps, so the captions stay readable. Exporting needs Python Playwright with Chromium and FFmpeg:

```sh
python3 animations/export_gifs.py              # all scenes
python3 animations/export_gifs.py mutants      # one scene
```

GIF exports do not retain HTML seek controls.

Full-quality MP4 versions of all ten scenes (1080 × 1080, 30 fps, H.264, 20 seconds each) are in [`docs/media/`](../docs/media/), exported frame by frame from the same HTML scenes:

```sh
python3 animations/export_mp4.py              # all scenes
python3 animations/export_mp4.py mutants      # one scene
``` Export dimensions are not a guarantee of acceptance by every platform; check the platform's current requirements before adapting or uploading. No animation upload is implied by these source and render instructions.

Attribution: **Cristian Guerra · QA Automation · Medellín, Colombia · @criguex**.
