# Scientific QA Evidence

**A reproducible numerical mutation campaign, alongside bounded formal-tool controls.** This package keeps those two kinds of evidence separate: finite numerical tests are not theorem proofs, and the formal examples do not certify scientific models.

![Animated RC mutation comparison: baseline and doubled time constant](docs/assets/rc-mutation.gif)

*Illustrative reconstruction from the recorded RC fixture. The dots are recorded RK4 checkpoints; the curves are analytic reconstructions. Parameters and source hashes are in [`animations/manifest.json`](animations/manifest.json).*

## Two evidence tracks

### 1. Formal reproduction and controls

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

The clean build reused cached dependencies and toolchain artifacts; it was not a full bootstrap. The later Comparator run is a bounded recorded check of the configured challenges, not a general proof of correctness. The deliberately wrong fixture changes the exported proof value while retaining its declared type and dependencies. See the [formal evidence map](CLAIMS.md) and [Comparator records](evidence/formal/comparator/README.md).

### 2. Numerical mutation QA

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

Each host recorded **27 PASS, 54 KILLED, and 3 SURVIVED** across the same **84 paired variants**—not 168 distinct variants. The paired comparison covered **738 finite values and 18 non-finite values** (represented as null); the maximum reported cross-host scaled delta was **1.11 × 10⁻¹⁶**. Survivors remain visible and are not proof of equivalence. All models and mutation inputs are synthetic fixtures, not empirical measurements.

## Explore and reproduce

- [Open the offline animation gallery](animations/index.html): six interactive scenes—RC, second-order chemistry, Newton cooling, Snell refraction, campaign summary, and formal typecheck control. Their shared manifest records evidence-file hashes.
- [Read the evidence map](CLAIMS.md), [source provenance](evidence/SOURCE_PROVENANCE.md), and [curated evidence guide](evidence/README.md).
- [Review the narrated V2 plan](video/src/visual-v2/publication.json). The rejected static-text V1 must not be uploaded.

Verify the saved numerical evidence and bundled files:

```sh
shasum -a 256 -c evidence/SHA256SUMS.txt
python3 evidence/verify_numerical.py
python3 -m unittest discover -s animations -p 'test_*.py'
```

To rerun the synthetic suite in a new, nonexistent output directory:

```sh
cd evidence/numerical/source
python3 runner.py --out /tmp/adv050-multidomain-rerun
```

This reruns the numerical suite only; it does not rebuild the formal source or rerun Comparator. The clean-source build instructions and limits are documented in [`evidence/formal/clean-build/`](evidence/formal/clean-build/). Saved evidence checks do not imply a fresh run.

## Credit and status

Created by **Cristian Guerra**, QA Automation, from **Medellín, Colombia** ([`@criguex`](https://github.com/criguex)). Original proofs are credited to their OpenAI authors; see [Authorship and AI disclosure](AUTHORSHIP.md) for attribution and tool-assistance details. Lean, mathlib, and Comparator are identified in the [dependency and fidelity records](evidence/formal/clay-lean-fidelity.md).

Six interactive HTML scenes and an RC preview loop are available for review. The narration-synced V2 source defines one long video and five shorts; their final exports are still pending. **No video or social post is represented as published.** The author has authorized the publication workflow; final rendered-media review and third-party rights checks remain separate readiness items. See [publication status](PUBLICATION_STATUS.md).

No theorem discovery, scientific certification, empirical validation, or proof of a real-world system is claimed.
