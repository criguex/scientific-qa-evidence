# Release status

- English-only release candidate in local review; no public upload or repository publication is authorized.
- Narration is frozen to the five paid voice responses already generated; do not edit or regenerate without author approval.
- Raw voice responses remain outside this package. Only post-processed audio may be copied to the ignored render workspace.
- Numerical and formal evidence are curated allowlists. Original evidence hashes must remain unchanged; English summaries are derived translations.
- Human author review is required before any external publication. License status remains pending.
- When producing the Remotion lockfile, work in a package directory without a reused `node_modules` symlink, then verify with a fresh offline `npm ci --ignore-scripts`; keep raw provider responses and private request metadata outside the package.
