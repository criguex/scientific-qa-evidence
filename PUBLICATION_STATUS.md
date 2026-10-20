# Publication status

Updated 2026-10-20.

| Deliverable | Status | Notes |
| --- | --- | --- |
| Six interactive evidence scenes | Ready for review | Offline HTML in `animations/`; square and portrait Remotion compositions are source targets. |
| RC animation preview | Available for review | The GIF preview is embedded in the README. It is not a narrated short. |
| Narrated long video V2 | Source ready; render pending | Uses the existing English narration and aligned captions. |
| Five narrated shorts V2 | Source ready; renders pending | These are the five planned short-form pieces. |
| Spanish V2 narration | Script ready for review; audio not generated | Five Spanish chapters derived from the current English narration; separate 1.25× post-processing and media manifest. |
| X introduction thread | Posted | [Opening post](https://x.com/criguex/status/2112679712157753441) with replies [1](https://x.com/criguex/status/2112679713659334688), [2](https://x.com/criguex/status/2112679715744231538), [3](https://x.com/criguex/status/2112679717954580901), and [4](https://x.com/criguex/status/2112679719292248576). The opening post includes the 20-second RC MP4. |
| YouTube / TikTok uploads | Not posted | No long-form YouTube video or TikTok short has been uploaded. |

The author has authorized proceeding with the publication workflow. That authorization does not replace final review of rendered media, captions, claims, or third-party rights. The static-text V1 is superseded and is not approved for upload. See [`video/src/visual-v2/publication.json`](video/src/visual-v2/publication.json) for composition IDs and render targets.

## Spanish V2 plan

The five-chapter source is [`production/narration.es.json`](production/narration.es.json), translated from the current English narration rather than the stale bilingual draft. The historical Spanish master uses a Chatterbox voice that is not approved for reuse in this delivery. The planned Spanish generation uses five new requests with the user-approved multilingual voice; do not reuse the legacy audio. Provider generation, post-processing, Spanish captions, and renders remain pending. No paid API request was made while preparing this source.

After human script review, inspect the no-network request plan:

```sh
python3 production/synthesize.py --dry-run --language es --out /tmp/adv050-es-review
```

Generation, if approved, must use a new private output directory. Post-processing and media preparation use `--language es` and a separate `video/src/generatedSpanishMedia.json` plus `video/public/spanish/`; aligned Spanish captions must come from the new Spanish provider response, never from English timing.

The public repository is [github.com/criguex/scientific-qa-evidence](https://github.com/criguex/scientific-qa-evidence); public `main` currently contains commit `43520e2`. This documentation update has not yet been pushed.
