# English Remotion source

This standalone source uses Remotion 4.0.537 and the installed `@remotion/media` package. The five chapter compositions and their audio lengths are registered from `src/generatedMedia.json`, which `production/prepare_media.py` writes after post-processing. A pending manifest intentionally exposes only the six still cards.

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
