# Release status

- English-only release candidate in local review; no public upload or repository publication is authorized.
- Narration is frozen to the five paid voice responses already generated; do not edit or regenerate without author approval.
- Raw voice responses remain outside this package. Processed chapter audio and the illustrative flow asset are tracked for reproduction; final media exports are ignored.
- The English long video, five shorts and six cards are rendered. English acceleration is baked in at 1.20×; review at player speed 1×. Technical checks and output hashes are recorded in DELIVERY_VALIDATION.json. Human audio/editorial review remains pending.
- A separate Spanish V4 review copy uses 1.25× acceleration, retains the historical voice, and is not the updated ElevenLabs edition. It is outside this English-only package.
- Numerical and formal evidence are curated allowlists. Original evidence hashes must remain unchanged; English summaries are derived translations.
- Human author review is required before any external publication. License status remains pending.
- The first static-text animation draft was rejected; the approved direction is six data-backed animated evidence scenes with offline HTML controls, square/portrait exports and visible Cristian Guerra · QA Automation · Medellín, Colombia attribution. Nothing has been published.
- Narrated video V1 is also superseded/rejected and must not be uploaded. V2 is registered separately and reuses the existing aligned English 1.20× chapter audio for one long master plus exactly five opening-excerpt shorts; pending renders and human review remain publication gates.
- When producing the Remotion lockfile, work in a package directory without a reused `node_modules` symlink, then verify with a fresh offline `npm ci --ignore-scripts`; keep raw provider responses and private request metadata outside the package.
