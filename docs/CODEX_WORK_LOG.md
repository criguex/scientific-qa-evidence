# Work done with OpenAI Codex, step by step

This log records what the Codex coding agent did for this study, so that a reviewer can separate what was executed from what was only discussed or illustrated. It was compiled on 2026-10-22 by Claude Code from the Codex session files kept on the author's Mac mini, after the fact. Times are UTC.

## How this log was built

1. All 213 local Codex session files and the Codex prompt history (470 entries) were read.
2. Sessions were kept when they belong to this study. Nineteen qualify, all on 2026-10-20: one main session and eighteen sub-agents it started. Each sub-agent session file names its parent and its role (for example `/root/localizar_5070`), so the tree below is read from the files, not inferred.
3. For each, the tool calls were extracted (shell commands, file patches, `git commit`, `git push`, `ssh` to the two Windows hosts), and counted.
4. The full transcripts are **not** published. They contain the author's personal data and commands that handle credentials. Instead, the SHA-256 of each session file is listed below, computed on 2026-10-22, so the files this log was built from can be identified later.

## Step by step

Roles are the names the main session gave its sub-agents. "No file patches" means the session only ran commands or read files.

| # | Session (UTC) | Role | Tool calls | What it did | Where the result lives |
| --- | --- | --- | --- | --- | --- |
| 1 | `…112a8e2f` 16:09 → 00:08 next day | main | 2,067 | Took the author's request to build and check OpenAI's proofs on the RTX 5070 host (WAR) and to widen the mutant scenarios beyond water. Installed Ubuntu 24.04 under WSL on WAR, cloned OpenAI's repository at the pinned commit, ran the hash preflight, the build and the first controls, started the sub-agents and merged their work. 11 `git push` calls, the first push of this repository among them | This repository (first 16 commits, below) and the author's private `adv-050-*` repositories |
| 2 | `…84df4b88` 16:09 → 18:35 | `localizar_5070` | 188 | Located and prepared the 5070 host; ODE scenarios (version 3), timestep checks on GUERRA, NS08 operations on WAR, a voice preview | Private `adv-050-auditoria` |
| 3 | `…2659af2c` 16:18 → 18:29 | `material_evidencia` | 354 | Assembled the evidence package (154 file patches). Its fluid simulation records run time with `time.perf_counter`, which measures how long the program runs, not any repair | Private `adv-050-auditoria` |
| 4 | `…f7e53ba8` 17:33 → 18:21 | `validacion_matematica` | 108 | Independent check of the ODE results | Private `adv-050-auditoria` |
| 5 | `…b5d648` 18:26 | `gwar_video_v4` | 2 | No file patches | none |
| 6 | `…329d11` 18:26 → 18:29 | `inventario_video_v4` | 17 | Inventory of the version 4 video; no file patches | none |
| 7 | `…bd05cc04` 18:34 → 20:35 | `entrega_v4_luna` | 762 | Version 4 of the audit: video, controls, report and paper draft | Private `adv-050-auditoria-v4` |
| 8 | `…b7fa5a99` 18:35 → 20:21 | `ns08_luna` | 546 | NS08 calibration and extra runs on WAR (138 `ssh` calls) | Private `adv-050-auditoria` |
| 9 | `…c4694b6a` 18:36 → 20:32 | `voz4060_luna` | 508 | Voice version 4 on GUERRA, and the three runnable experiments of the mutant lab | [criguex/war-paradigm](https://github.com/criguex/war-paradigm) (formerly `mutant-lab`) |
| 10 | `…0276f8` 20:05 → 20:06 | `gwar_mutant_scope` | 1 | No file patches | none |
| 11 | `…ab43b8` 20:24 → 22:54 | `gwar_elevenlabs_voice` | 34 | Voice provider check (from its role name); no file patches | none |
| 12 | `…dd2b45` 20:35 → 21:45 | `validar_correcciones_adv050` | 201 | Checked the corrections (from its role name); no file patches | none |
| 13 | `…88bc5b87` 20:44 → 21:48 | `validation_writer_luna` | 567 | Wrote the nine-model numerical suite (`CONTRACT.md`, `oracles.py`, `runner.py`, `suite.py`, `sut.py`), including Snell refraction with the `index_swap` mutation and an oracle that inverts `asin` by bisection; validation controls and documentation | Private `adv-050-auditoria-validacion`; the suite and its paired runs are in this repository under [`evidence/numerical/`](../evidence/numerical/) |
| 14 | `…3eda86` 21:46 → 22:03 | `jd_tts_a` | 8 | First blind judge of the text-to-speech safety review (from its role name) | none |
| 15 | `…93486e` 21:46 → 22:03 | `jd_tts_b` | 6 | Second blind judge of the same review (from its role name) | none |
| 16 | `…00f08820` 21:48 → 21:50 | `tts_safety_fix` | 20 | Applied the judges' text-to-speech safety notes | Private `adv-050-auditoria-tts-safety` |
| 17 | `…f920ff` 21:58 → 23:11 | `english_delivery_inventory` | 82 | Inventory of the English delivery; no file patches | none |
| 18 | `…d756876c` 22:00 → 23:35 | `english_release_writer` | 656 | English delivery package and the animated explainers, Snell scene included | Rendered media, later rebuilt in this repository's [`animations/`](../animations/) |
| 19 | `…b5febf` 22:59 → 23:40 | `animation_export_batch` | 138 | Rendered the animation MP4 files; no file patches | Media later rebuilt in this repository |

The paired numerical campaign ran on the Mac mini (macOS arm64) and on WAR (Linux x86_64); both hosts classified all 84 variants identically ([`CLAIMS.md`](../CLAIMS.md)).

## Evidence published from these sessions

The code, contracts, raw results and logs these sessions produced in the private repository are now in [`evidence/codex-2026-10-20/`](../evidence/codex-2026-10-20/), one folder per experiment, with local paths replaced by placeholders and a manifest that pairs each file with the hash of its original. Audio, voice and video stay private.

## Commits in this repository with Codex assistance

All on 2026-10-20 (UTC−5), each with a `Co-Authored-By: Codex` trailer:

`20d67e5` prepare English QA evidence and video review package · `3281ad5` clarify AI attribution and English publication identity · `b39e7d6` record rendered English delivery and review checks · `a2e063f` add animated evidence review package · `f97e8b9` improve explainer canvas attribution · `554a678` add narration-synced V2 video compositions · `0264eb8` add visual evidence landing page · `43520e2` clarify available animation preview · `df64ec1` explain each evidence animation · `4ec9814` prepare Spanish narration pipeline · `46ba636` add animated previews to evidence guides · `098f4ca` correct V2 visual claims and layout · `275e6b0` add Spanish V2 narration compositions · `a8aa21d` record X animation preview receipts · `6ac3c07` update Spanish delivery readiness · `f49fcd5` preserve proportional visual scales.

Later work (from 2026-10-21) was done with Claude Code; its commits carry `Co-Authored-By: Claude …` trailers ([`AUTHORSHIP.md`](../AUTHORSHIP.md)).

## What was not executed: the "auto-fix" scenarios

A set of illustrations titled "WarParadigm, scenarios 2–5" shows a light ray in a cube, an extra 1° bend, an index of −1, level-of-detail rendering, and a chart where an "auto-fix" corrects the light in 5 ms against a 195 ms anomaly. **None of that was ever run.**

- No session, in Codex or Claude Code, contains code for a self-correcting simulation, a monitor or regenerator, a 1° deflection, an index of −1, level-of-detail logic, or a timing of detection or repair in milliseconds. The search covered all 213 Codex sessions, the Codex prompt history, the author's shell history and project folders, and the `war-paradigm` repository.
- The illustrations are conceptual images generated with AI tools. The 5 ms and +195 ms values in the chart are part of the drawing, not measurements.
- The numbered "scenarios" that Codex read on 2026-10-20 came from a Gemini conversation the author shared, and they were different topics (Brillouin zone, cutoff factor, mesh refinement, coupling perturbations).
- What was executed with light is the Snell model above: three fixed configurations and two planted faults (swapped indices, degrees read as radians), detected against an independent oracle. Code, contract and raw results are in [`evidence/numerical/`](../evidence/numerical/).

For an outside reviewer, everything about an auto-fix experiment is therefore **not recorded**, because it was never carried out. If it is built later, it will be a new experiment, registered before it runs: what is expected, what would count against it, and how detection time, repair time and simulated time are measured separately.

## Session files (SHA-256 computed on 2026-10-22, after the fact)

```text
947073b778aadcb612eebcb33f94e45c1e6eb36a92fc228d7e20dc64a36b0f70  rollout-2026-10-20T11-08-20-01a15a12-2369-7193-a4e0-112a8e2f2ed3.jsonl
2955525c3a340d26bc71d07848f8b0cb348be5332c0746f9cc0312b4226dc57e  rollout-2026-10-20T11-09-36-01a15a13-4dba-76c1-8fe0-84df4b88d138.jsonl
c234e1e13a53b89f428d740561cfa3bb7f7a48c0d74d14b7281d8ea9cf7ad289  rollout-2026-10-20T11-18-44-01a15a1b-a98c-7b31-bab8-2659af2cdb22.jsonl
0c7c7c5022dcb246009e2164bf46c73e7f3e2cbc6adca622211a2a2daa169e73  rollout-2026-10-20T12-33-52-01a15a60-7111-7011-90f7-f7e53ba87994.jsonl
e123c26adfb4f80034e734b97305db670e3102c98544418f4c029a79d50f48ab  rollout-2026-10-20T13-26-11-01a15a90-58ac-74b2-80de-9ddb76b5d648.jsonl
9f70822f227a537273ffdc836f4d85e6d9c317158aa49924ee19f39a71b6aee2  rollout-2026-10-20T13-26-20-01a15a90-7abc-7a43-945f-850f31329d11.jsonl
05cd206fc2e287840320bfc7585db1c7d5ef367bb7f5ad582fb1e4184ffee45c  rollout-2026-10-20T13-34-46-01a15a98-318c-73a2-8e91-bd05cc04a5a8.jsonl
035b44a27a6963f4ea022b621a760f0f77816c69424a9525cff8f13bf85d69f4  rollout-2026-10-20T13-35-57-01a15a99-48a8-7fb1-b1bc-b7fa5a99ae05.jsonl
ac777c2d7f502d7fe3f2090f43fa70d3fcf10c318aae04c373fee36d40a052b9  rollout-2026-10-20T13-36-28-01a15a99-c0af-7b52-aca2-c4694b6a7785.jsonl
4769bb0b8f0382159fc9f24549f27ccf901bfee1b8d38a32c7a338f6ab620d8b  rollout-2026-10-20T15-05-58-01a15aeb-b204-7ab3-ac90-2ddb9a0276f8.jsonl
b153e81be9a8246316f99ae8f086196fa06bf7cc0d3cbe4feff8625b496bdff5  rollout-2026-10-20T15-24-51-01a15afc-fd19-79a0-955f-e7cbdeab43b8.jsonl
52e15aba0299744195729c246d163941a29263e6a7ddc7f97f50fac6e5799239  rollout-2026-10-20T15-35-52-01a15b07-112c-7940-b3c4-3c299ddd2b45.jsonl
bb294cb1d92973d978165571fdc3002ce701d6c1865ba6c2e197d37774e4d6d9  rollout-2026-10-20T15-44-42-01a15b0f-27b4-7fb0-857d-88bc5b87f848.jsonl
f3323ff5a2ab219c7a774a38875c7bcf69c39ee1363da789b365e45661475c3e  rollout-2026-10-20T16-46-22-01a15b47-9e89-7062-8cc8-a8fd933eda86.jsonl
dd2ed72cc7d471ecea4731d7aeb28862166da7cdde841587e55c4ddc2c9366db  rollout-2026-10-20T16-46-28-01a15b47-b4d3-73e0-9cfc-d560df93486e.jsonl
67e7125a6794d86b6060e8678b79ebf3cb4b581e6e30c4536fafbc55c39b6288  rollout-2026-10-20T16-48-42-01a15b49-c147-7df0-914d-00f08820c196.jsonl
4e93d8ec0c2b0a79688ddf334db2c6eac902934783c92153be9e17b48299f124  rollout-2026-10-20T16-58-41-01a15b52-e310-79c1-9e09-f2cd7ef920ff.jsonl
726ea0a998fdfcd8c79d35b78e7382f83ddf0b35bd29f603fe0ecbf19828e908  rollout-2026-10-20T17-00-52-01a15b54-e33c-78b1-8b1d-d756876cc4cb.jsonl
4ff9d3bc77a9b245033e67d272418a407436391f254faa3de8dffe911f0d685f  rollout-2026-10-20T17-59-02-01a15b8a-268d-7271-a56a-d79619b5febf.jsonl
```

File names carry the local time (UTC−5) at which each session started.

## Limits

- Built after the fact by a different AI tool, from session files that only the author holds. A reviewer can check the commits and the evidence in this repository, but not the transcripts themselves.
- Tool-call counts measure activity, not quality or correctness.
- The private repositories are not published; this log only says what they contain.
