# Maintainer notes

Updated 2026-10-21. Working rules for anyone (human or agent) changing this repository. For what is public and what is pending, see [PUBLICATION_STATUS.md](PUBLICATION_STATUS.md).

- The repository is public, and the author authorized publication on 2026-10-20. Rights remain reserved; see [LICENSE_STATUS.md](LICENSE_STATUS.md).
- The documentation is bilingual: [README.md](README.md) (English) and [README.es.md](README.es.md) (Spanish). Change both together. The detailed records (CLAIMS, evidence guides, contract) stay in English.
- Numerical and formal evidence are curated allowlists. Never rewrite an original evidence file; English summaries are derived translations. After editing any file listed in `evidence/SHA256SUMS.txt`, update its entry and run `shasum -a 256 -c evidence/SHA256SUMS.txt`.
- The narration is frozen to the paid voice responses already generated, five per language. Do not edit or regenerate it without author approval; `production/synthesize.py --dry-run` is the only safe inspection. Raw provider responses stay outside the repository.
- The static-text animation draft and the narrated V1 video were rejected and must not be uploaded. V2 (one long video and five shorts per language) is the approved target; renders and human review of the rendered media are still pending.
- English audio has 1.20× and Spanish audio 1.25× speed baked in; review both at player speed 1×.
- Known evidence caveats are listed under "Known limitations" in the README and in [CLAIMS.md](CLAIMS.md). Keep counts honest: 54 KILLED cases are 51 distinct behaviors.
- When producing the Remotion lockfile, work in a package directory without a reused `node_modules` symlink, then verify with a fresh offline `npm ci --ignore-scripts`.
- Before any commit, check that no private IPs, host usernames, private paths, credentials or employer names have entered the diff.
