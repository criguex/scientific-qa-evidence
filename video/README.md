# English Remotion source

This standalone source uses Remotion 4.0.537 and the installed `@remotion/media` package. The five chapter compositions and their audio lengths are registered from `src/generatedMedia.json`, which `production/prepare_media.py` writes after post-processing. A pending manifest intentionally exposes only the six still cards.

The former static-text V1 is rejected and must not be uploaded. V2 is isolated behind `src/visual-v2-entry.tsx`; it reuses the existing processed English 1.20× chapter audio exactly once and the saved provider-aligned caption times. The long master uses the full five chapter tracks; each short uses the corresponding opening excerpt ending at `clip_end_frame`. V2 publication targets are in `src/visual-v2/publication.json`.

## Render targets

The project registers one 1920×1080 long video, five 1080×1920 shorts, and six 1080×1080 cards. Composition IDs are visible in Studio. Render after the generated media manifest is ready:

```sh
npx remotion studio src/index.ts
npx remotion render src/index.ts ENLong1920x1080 ../media/EN-long-1920x1080.mp4
npx remotion render src/index.ts ENShort01Method1080x1920 ../media/shorts/EN-short-01-method-1080x1920.mp4
npx remotion render src/index.ts ENShort02Models1080x1920 ../media/shorts/EN-short-02-models-1080x1920.mp4
npx remotion render src/index.ts ENShort03Formal1080x1920 ../media/shorts/EN-short-03-formal-1080x1920.mp4
npx remotion render src/index.ts ENShort04Results1080x1920 ../media/shorts/EN-short-04-results-1080x1920.mp4
npx remotion render src/index.ts ENShort05Limits1080x1920 ../media/shorts/EN-short-05-limits-1080x1920.mp4
```

Render `ENCard01Cover1080` through `ENCard06Limits1080` as PNG stills into `../media/cards/`. The source reads only processed chapter audio from `public/english/audio/`; raw provider responses stay outside the release directory.

## V2 narrated master and shorts

From `video/`, the separate V2 entry registers one 1920×1080 long video and exactly five 1080×1920 shorts. Long chapter boundaries and short durations are sourced from `src/generatedMedia.json` (30 fps, long master 13,246 frames). Audio playback remains at normal 1× because the 1.20× tempo is already baked into the processed MP3 files.

```sh
npx remotion studio --entry-point src/visual-v2-entry.tsx
npx remotion render src/visual-v2-entry.tsx EN-V2-Long ../media/EN-long-v2-1920x1080.mp4
npx remotion render src/visual-v2-entry.tsx EN-V2-Short-01-Method ../media/shorts/EN-v2-short-01-method-1080x1920.mp4
npx remotion render src/visual-v2-entry.tsx EN-V2-Short-02-Models ../media/shorts/EN-v2-short-02-models-1080x1920.mp4
npx remotion render src/visual-v2-entry.tsx EN-V2-Short-03-Formal ../media/shorts/EN-v2-short-03-formal-1080x1920.mp4
npx remotion render src/visual-v2-entry.tsx EN-V2-Short-04-Campaign ../media/shorts/EN-v2-short-04-campaign-1080x1920.mp4
npx remotion render src/visual-v2-entry.tsx EN-V2-Short-05-Limits ../media/shorts/EN-v2-short-05-limits-1080x1920.mp4
```

The V2 timelines are source-only pending render and human editorial review. Do not substitute the superseded V1 renders for these targets.
