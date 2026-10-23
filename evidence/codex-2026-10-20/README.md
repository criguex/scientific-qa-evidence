# Codex evidence of 2026-10-20

This folder publishes the evidence the Codex agent produced on 2026-10-20 that had stayed in the author's private repository (`adv-050-auditoria`, commit `6750b8f`). It holds the code, contracts, raw results and run logs of each experiment. Who did what, session by session, is in [`docs/CODEX_WORK_LOG.md`](../../docs/CODEX_WORK_LOG.md).

The imported reports are in Spanish, as written at the time. Their internal links use the private repository's layout; the table at the end maps old paths to new ones.

## How the files were copied

1. Each group below was copied from the private repository by a script, in one pass.
2. **Local paths were replaced** with placeholders, and relative links in the imported reports were rewritten to this folder's layout or to the newer public files that supersede them. 676 of the 1,886 published files were edited this way. The placeholders are: `<WIN_HOME>` (the Windows user folder), `<WIN_HOME_WSL>` (the same folder seen from WSL), `<WSL_HOME>` (the Linux user folder on WAR), `<HOME>` (the Mac user folder), `<TMP>` (temporary folders) and `<mac-host>` (the Mac's network name). Nothing else was edited.
3. **Not copied:** 361 images, videos, audio files and `.npz` arrays (about 100 MB), and 385 binary members of three archives. Voice and audio outputs stay private on purpose.
4. **[`MANIFEST.tsv`](MANIFEST.tsv)** lists, for every published file, its source path, the SHA-256 of the original bytes, the SHA-256 of the published bytes, and whether it was sanitized. Files with `sanitized = no` are byte-identical to the originals, so any hash recorded inside the runs can be checked directly. For sanitized files, a hash recorded inside a run refers to the original bytes, which stay private; the manifest pairs the two.
5. 43 links inside the imported reports still have no target, on purpose: they point to rendered images and videos, render and montage summaries, video scripts, the voice check and one superseded source archive, none of which is scientific evidence.
6. A scan of everything published found no keys, tokens, passwords or private keys. 11 JSON files written by PowerShell start with a UTF-8 byte-order mark; they are kept as written and read with `utf-8-sig`.

All results below are synthetic calculations under explicit software contracts. They test whether code and checks behave as specified. They are not physical measurements, and none of them verifies the Euler or Navier–Stokes theorems.

## What is here

### 1. [`multidomain-as-run/`](multidomain-as-run/): the numerical suite exactly as it ran

The nine-model suite behind [`evidence/numerical/`](../numerical/): RC circuit, Newton cooling, second-order kinetics, Beer–Lambert, Snell refraction, thin lens, acoustic interface, Fechner and logistic response.

- `runner.py` (SHA-256 `384c20fb…`) and the Spanish `CONTRACT.md` (`9c48dae3…`) are the exact files whose hashes the published paired runs cite as `source_sha256`. Until now only later edited versions were public.
- Example, Snell: θ₂ = asin(n₁ sin θ₁ / n₂). The mutation `index_swap` exchanges n₁ and n₂. At θ₁ = 0.4 rad with n₁ = 1.0 and n₂ = 1.5, θ₂ moves from 0.263 to 0.624 rad, and the oracle (bisection, independent of the implementation) flags it.

### 2. [`scenarios-v2/`](scenarios-v2/): heat, transport and waves

- **Models:** 1D periodic heat, advection and wave equations, solved with centred differences and RK4 at N = 32, 64 and 128, plus a repeat at N = 64 with dt/2. The oracle uses exact solutions.
- **Contract, fixed before any mutant ran:** final RMS error E₁₂₈ < 10⁻³; observed order between 1.7 and 2.3; dt versus dt/2 difference < 10⁻⁶ and < 0.02 E₆₄; drift of the mean < 10⁻¹⁰.
- **Results:** 42 runs on WAR and GUERRA. Heat on WAR: E₁₂₈ = 2.93253 × 10⁻⁵, order 1.99926. Transport: 5.77593 × 10⁻⁴, order 1.99822. Wave: 1.29854 × 10⁻⁴, order 1.99951. Per host, 13 mutants detected, 2 survived (`*_tiny_coefficient`) and 3 algebraically equivalent.
- **Contents:** the report `INFORME_ESCENARIOS_V2.md`, the plan `PLAN_VALIDACION_V2.md`, the raw runs (`run.json`, CSV, stdout and stderr per run and host) and `summarize_scenarios.py`.

### 3. [`scenario-runners/`](scenario-runners/): the runners and their contracts

`run_scenario.py` and `run_ode_scenario.py`, byte-identical to the copies used in the campaigns, together with `contratos-1d.md` and `contratos-ode-v3.md`, which state every threshold.

### 4. [`ode-v3/`](ode-v3/): oscillators and reversible reactions

- **Models:** nine oscillators and nine reversible reactions A ⇌ B, with RK4 against analytic solutions.
- **Contract:** E_fine < 10⁻⁶; order p = log₂(E_h / E_{h/2}) between 3.6 and 4.4 when both errors exceed 10⁻¹².
- **Results:** largest RMS error 4.26677 × 10⁻⁸; observed orders 3.9957 to 4.1693. 51 of 56 evaluated configuration–mutant pairs were detected and 5 survived, after excluding 16 combinations labelled `EQUIVALENT`. Example: in `rxn05`, A_eq = 0.6 and B_eq = 0.4 with τ = 2, so at t = 4 a fraction e⁻² ≈ 13.53 % of the initial deviation remains.
- **Contents:** the report `INFORME_FISICA_QUIMICA_V3.md`, raw runs from WAR and GUERRA, an independent review run on the Mac, cross-host comparisons, the PowerShell launchers and their logs, and `summarize_ode_v3.py`.

### 5. [`fluid-3d/`](fluid-3d/): 3D Navier–Stokes and Euler toy runs

- **What it is:** a spectral solver (`fluid_solver.py`) on 32³ and 64³ grids with dt 0.01 up to T = 4, and `compare_grids.py` with its output. The report itself says this is not a convergence certificate.
- **Temporal check** (`fluid_temporal_v2`): dt 0.01 versus 0.005 at N = 32. Largest divergence 1.7 × 10⁻¹⁶; Euler energy drift 1.56 × 10⁻¹¹ and 9.3 × 10⁻¹³; arrays identical between WAR and GUERRA.
- **Timing:** the solver records run time with `time.perf_counter`. That is how long the program takes, not a repair time.

### 6. [`formal-controls/`](formal-controls/): controls on the Lean verifier

- **Verifier controls** (`controles_20261020`, `_v2`, `_v3`) on OpenAI's commit `f9e8bc5`: a positive control, a negative control and a `sorry` control. Version 3 adds a hash-mutation control (`hash_original` versus `hash_mutated`). `run_controls.py` and the three `.lean` files are the code that ran them.
- **Kernel and build validation:** `kernel_validation/` (clean build, export mutation and kernel controls, with tests); `kernel01` (the first mutation attempt); `clean_build03` (PASS in 2,496 s, full stdout); `periodic05`; `kernel_fixture_v2`; and the derived summaries with `verify_evidence.py`. The later `kernel02` and the paired multidomain runs are not repeated here, because their newer form is public in [`evidence/formal/kernel-mutation`](../formal/kernel-mutation/) and [`evidence/numerical/paired`](../numerical/paired/).

### 7. [`build-5070/`](build-5070/): the first build on the RTX 5070 host

The script `build_on_5070.sh`, the hash preflight, the launcher log, `audit_static.json`, the process and simulation reports, and `resultados_5070/`:

- `lake build`: OK in 2,342 s on 6 cores.
- `mutant_force_zero`: KILLED.
- Axioms: `[propext, Classical.choice, Quot.sound]` for all four theorems.
- Comparator: SKIPPED in this first run. It ran later, in builds B1–B5 ([`evidence/formal/`](../formal/)).

### 8. [`report-v4/`](report-v4/): version 4 report and Comparator calibration

`PAPER_AUDITORIA_REPRODUCIBLE_V4.md`, the acceptance records (ACTAs), and the text members of three archives unpacked beside them. Those members are the Comparator calibration cases (positive, statement mismatch, extra axiom, alpha-renaming, hidden axiom, weakened condition), the NS08 operation scripts, and the time and guard logs.

### 9. [`provenance/`](provenance/): generation trail

`TRAZABILIDAD_GENERACION.md`, `PROCEDENCIA_IA_Y_APORTES.md` (the AI disclosure written at the time), `NS08_PROPUESTA_NO_EJECUTADA.md`, and `images_gpt/no_todo_es_agua_v1.json`, the prompt and provenance of an illustration made with GPT, which the reports label as illustrative, not as a result. The last one is a proposal that, as its name says, was **not executed**.

## What is not here

- **Kept private:** paid-provider voice and audio (ElevenLabs), the Chatterbox voice previews and every rendered video, because of licences and because they are not scientific evidence. The same applies to social-media drafts and prompts.
- **Not repeated:** the snapshot of OpenAI's source. It is cited by its archive SHA-256 in [`evidence/formal/b5/`](../formal/b5/) and is available upstream.
- **Never existed:** an "auto-fix" experiment. See [`docs/CODEX_WORK_LOG.md`](../../docs/CODEX_WORK_LOG.md#what-was-not-executed-the-auto-fix-scenarios).

## Old path → new path

| In the private repository | Here |
| --- | --- |
| `controls/multidomain_validation/` | `multidomain-as-run/multidomain_validation/` |
| `evidence/scenarios_v2/` | `scenarios-v2/scenarios_v2/` |
| `skills/escenarios-verificables/` | `scenario-runners/escenarios-verificables/` |
| `evidence/ode_v3/` | `ode-v3/ode_v3/` |
| `simulation/`, `evidence/fluid_temporal_v2/` | `fluid-3d/` |
| `controls/`, `evidence/controles_*`, `evidence/new_validation/*` | `formal-controls/` |
| `evidence/resultados_5070/`, `evidence/*.log`, `evidence/build_on_5070.sh` | `build-5070/` |
| `evidence/report_v4/` | `report-v4/report_v4/` |
