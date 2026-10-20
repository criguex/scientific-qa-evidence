# ADV-050 English review package

This directory contains the English narration, a curated evidence allowlist, Remotion source, and publication drafts for human review. It is a local release candidate. No public upload or repository publication has happened.

## Quick start

Run the narration checks and inspect the request plan without contacting the voice provider:

```sh
cd production
python3 -m unittest -v test_synthesize.py test_prepare_media.py
python3 synthesize.py --dry-run --out /tmp/adv-050-english-voice
```

The approved voice generation is five English requests. Supply `GV_ELEVENLABS_API_KEY` through the process environment, and keep raw responses outside this directory:

```sh
python3 synthesize.py --generate --out /tmp/adv-050-english-voice
python3 synthesize.py --postprocess --out /tmp/adv-050-english-voice
python3 prepare_media.py \
  --source /tmp/adv-050-english-voice \
  --public ../video/public/english \
  --manifest ../video/src/generatedMedia.json
```

The provider generated audio at speed 1.0; offline post-processing applies tempo 1.20 and loudness normalization (targets `I=-16`, `TP=-1.5`, `LRA=11`) to the English copy, encoded at 44.1 kHz. The English 1.20× speed is baked into the export: play it at normal 1× to avoid applying the speed change twice. Measured loudness varies by chapter; all five measurements are recorded in `production/audio-assets.json`, and the filter targets are not claims about those measurements. The separate Spanish V4 master and any 1.25× derivative are outside this English package; their voice/speed provenance is still under review. `prepare_media.py` copies only processed MP3 files and derives long and short SRT/VTT subtitles from provider alignment and the saved post-processing summary. It refuses to replace existing media. The Remotion compositions appear after the generated manifest is ready.

The Remotion project uses the existing package versions in `video/package.json` (Remotion 4.0.537). Install the pinned dependencies with `cd video && npm ci --ignore-scripts`, then run Studio from `video/`. Render targets are listed in `video/README.md`; the review page is [index.html](index.html).

## Reproduce and verify

From this directory, verify the curated evidence files:

```sh
shasum -a 256 -c evidence/SHA256SUMS.txt
python3 evidence/verify_numerical.py
python3 production/verify_audio_assets.py
```

To rerun the synthetic numerical suite, use a new output directory:

```sh
cd evidence/numerical/source
python3 runner.py --out /tmp/adv050-multidomain-english-rerun
```

That exact command completed successfully in this environment. For another run, choose a new, nonexistent output directory. It reruns the synthetic numerical suite; it does not rebuild the formal source or rerun Comparator.

The formal source-build record is separate from the Comparator run. Repeating the recorded saved-evidence checks does not rerun Lean or Comparator. The included English contract is a translation for the self-contained numerical rerun; its hash differs from the original Spanish contract, while the runner, suite, SUT, and oracles are preserved and hash-checked. Repeating the clean source build requires the authorized source checkout at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd` and its pinned Lean toolchain and dependencies:

```sh
git rev-parse HEAD
lake --no-cache build
```

The recorded build reused cached dependencies and toolchain artifacts. This command does not represent a full bootstrap or theorem/kernel validation. Fresh Comparator reproduction instructions and sanitized run records are in `evidence/formal/comparator/` when included. No rerun is implied by checking saved evidence hashes.

## Review gates

Review [CLAIMS.md](CLAIMS.md), [AUTHORSHIP.md](AUTHORSHIP.md), the rendered long video, five shorts, and six cards before approving any external publication. Draft channel copy is in [publication.json](publication.json). Raw provider responses and the provider key are excluded. Processed English audio is included for review; final video renders are produced separately.
