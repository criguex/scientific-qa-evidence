# Publication status

Updated 2026-10-20.

| Deliverable | Status | Notes |
| --- | --- | --- |
| Six interactive evidence scenes | Ready for review | Offline HTML in `animations/`; square and portrait Remotion compositions are source targets. |
| RC animation preview | Available for review | The GIF preview is embedded in the README. It is not a narrated short. |
| Narrated long video V2 | Source ready; render pending | Uses the existing English narration and aligned captions. |
| Five narrated shorts V2 | Source ready; renders pending | These are the five planned short-form pieces. |
| Spanish V2 narration | Generated and aligned; render pending | Five new Spanish chapters use their own provider-aligned captions, 1.25× offline post-processing, and the separate Spanish media manifest. |
| X introduction thread | Posted | [Opening post](https://x.com/criguex/status/2112679712157753441) with replies [1](https://x.com/criguex/status/2112679713659334688), [2](https://x.com/criguex/status/2112679715744231538), [3](https://x.com/criguex/status/2112679717954580901), and [4](https://x.com/criguex/status/2112679719292248576). The opening post includes the 20-second RC MP4. |
| X animation previews | Posted as six GIF replies | [Chemistry](https://x.com/criguex/status/2112681973877727336), [cooling](https://x.com/criguex/status/2112682611445489945), [Snell refraction](https://x.com/criguex/status/2112682726700785965), [paired campaign](https://x.com/criguex/status/2112682812377805184), [formal control](https://x.com/criguex/status/2112682876819198184), and [separate illustrative flow context](https://x.com/criguex/status/2112682970029134277). These are animated previews, not the narrated V2 videos. |
| YouTube / TikTok uploads | Not posted | No long-form YouTube video or TikTok short has been uploaded. |

The author has authorized proceeding with the publication workflow. That authorization does not replace final review of rendered media, captions, claims, or third-party rights. The static-text V1 is superseded and is not approved for upload. No narrated V2 long video or short has been uploaded. See [`video/src/visual-v2/publication.json`](video/src/visual-v2/publication.json) for composition IDs and render targets.

## Spanish V2 plan

The five-chapter source is [`production/narration.es.json`](production/narration.es.json), translated from the current English narration rather than the stale bilingual draft. The historical Spanish master uses a Chatterbox voice that is not approved for reuse in this delivery. Five new approved provider requests completed once, with no retries; processed chapter audio, Spanish-aligned captions, and the V2 media manifest are ready. Raw provider responses remain private and are not included here. Spanish long and short V2 renders remain pending. Story panels, narration and captions are Spanish; some labels inside the shared plot artwork remain English and require final render review.

Optional regeneration plan inspection (no network, no audio generation):

```sh
python3 production/synthesize.py --dry-run --language es --out /tmp/adv050-es-review
```

The Spanish generation has already completed in five approved requests without retries. Do not rerun paid synthesis to use these assets. If regeneration is ever separately authorized, it must use a new private output directory. Post-processing and media preparation use `--language es` and the separate `video/src/generatedSpanishMedia.json` plus `video/public/spanish/`; aligned Spanish captions must come from the new Spanish provider response, never from English timing.

The public repository is [github.com/criguex/scientific-qa-evidence](https://github.com/criguex/scientific-qa-evidence). The independently verified public snapshot `46ba636` includes the six-scene animation gallery and preview assets (verified 2026-10-20).
