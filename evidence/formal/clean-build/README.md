# Clean-source build fidelity

The recorded build used the authorized clean source checkout at commit `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`. It ran `lake --no-cache build`, exited 0, and completed 11,424 jobs. This reused dependency and toolchain caches; it was not a complete bootstrap and did not validate theorems or kernels.

| Component | Recorded version or commit |
| --- | --- |
| Lean | `leanprover/lean4:v4.34.0-rc2` · commit `6a10ac8c22beadecabdbb0919c2b50214762f91d` |
| Lake | `5.0.0-src+6a10ac8` |
| Comparator | `19e111e2141cf333c7daff0f64c5f24acc91dd2e` |
| mathlib | `85e3a25e006c35636f0e53b0e9296caca2685bc0` |
| lean4export | `cacf989bd75f608700820f6afc595f32e7a99a4d` |
| plausible | `d9598f07b1bc701f1e3aae163d2681c1fd978793` |
| LeanSearchClient | `ba67e212be1197b84c1f1f6299488a10a3002713` |
| importGraph | `d8823026ac7ef130c253089d95685f9877b95323` |
| proofwidgets | `a8acbfd87375ff4abe14ce09db5b7664d383bc7f` |
| aesop | `18889deb9e83ea7420ef51c160d6f88552e744e3` |
| Qq | `507746ab8f4b643ccdacb2ec4cdb5853fa9f8ab3` |
| batteries | `d54dddc581e08be364c278052863524bff7a99a9` |
| Cli | `ab3a82db9fea14cf0fd7f5a2de650f4b534640af` |

Exact pins are preserved in `dependency-pins.txt`; tool versions and executable hashes are in `tool-versions.txt` and `toolchain.sha256`. The following stdout excerpt is sanitized from original `build.stdout.log` (SHA-256 `dcbc3208f09dcb9f22a0c359931a713660727c447f6a28c9b2c028942ce25c72`): [build-output-excerpt.txt](build-output-excerpt.txt).

This record documents fidelity to the listed checkout and pins; it is not an independent audit of upstream source or mathematical correctness.
