# Evidence provenance

The package-level `SHA256SUMS.txt` is a conventional checksum list for files in this release. Original campaign records have an additional per-artifact integrity map embedded in each copied host summary and checked by `verify_numerical.py`. English prose and sanitized run summaries are derived artifacts; they do not alter or replace their originals.

| Package evidence | Original project-relative source | Integrity reference |
| --- | --- | --- |
| `numerical/paired/macos-arm64/` | `evidence/new_validation/multidomain_mac/` | Original summary SHA-256 `d45fe458dd10c1c5053cb7ba49796b84a2fd178e7627b46fa74c5e71eb95e0ec`; summary's artifact map covers 84 JSON cases and observations CSV |
| `numerical/paired/linux-x86_64/` | `evidence/new_validation/multidomain_war/` | Original summary SHA-256 `867ce78201e211a587dcec4a6c89900963d54b92b6b5f6d78a73c52f84954b17`; summary's artifact map covers 84 JSON cases and observations CSV |
| `numerical/summary.mac.json` | `evidence/new_validation/multidomain_mac/summary.json` | `d45fe458dd10c1c5053cb7ba49796b84a2fd178e7627b46fa74c5e71eb95e0ec` |
| `numerical/multidomain_derived.json` | `evidence/new_validation/multidomain_derived.json` | `b56bc9af121905fb1c962322a4b0c23fc5a8f4dd0b00601a5edf662d21cc5a50` |
| `numerical/source/` | `controls/multidomain_validation/` | Exact per-file hashes are in `SHA256SUMS.txt` |
| `numerical/fixtures/rc-baseline.json` | `evidence/new_validation/multidomain_mac/case_001.json` | `57a7df125bca23ebe94c6de859961c69e8373e65f08a429ffc71e85918cfc7d4` |
| `numerical/fixtures/rc-tau-double.json` | `evidence/new_validation/multidomain_mac/case_003.json` | `9ffa207d1a80d0410cac884d6f9ff8fe8bcf1989fb3527826ce45187694260ef` |
| `formal/clean-build/summary.en.json` | Clean03 source-build summary, translated for this package | Original summary hash `8cbe19b735665c39a9f2856822a81f7d02129d5e4d1f0ee7a90b5a972164005e`; original public manifest hash `74f7d48938be731eed3569c25d00f693ac5723216c2dd601c85eab5e8bf02385` |
| `formal/clean-build/dependency-pins.txt` | `evidence/new_validation/clean_build03/dependency_pins.txt` | SHA-256 `a61fc04ea46c53342360aa74ab1408f33b26d18c15f0cc4574e3d1d50dc45d42`; Comparator `19e111e2141cf333c7daff0f64c5f24acc91dd2e`, mathlib `85e3a25e006c35636f0e53b0e9296caca2685bc0`, LeanSearchClient and remaining pins preserved in file |
| `formal/clean-build/tool-versions.txt` and `toolchain.sha256` | `evidence/new_validation/clean_build03/` | Toolchain manifest hash `62bb47eb9f3d335be055649e09cf4daddad307078d47819b544926c3aa21341e`; Lean 4.34.0-rc2 and Lake 5.0.0 |
| `formal/kernel-mutation/raw-summary.json` | `kernel02/public/summary.json` | `bd133aa375b1895c53c3bac567e4516a92466900f8d2c166b01acaa72825f06a` |
| `formal/kernel-mutation/derived-classification.json` | `evidence/new_validation/kernel_controls_derived.json` | `33cf64988ce0d31d9b35d2ddc6491e58f53aeb6d59a37116eb339e847533f30a` |
| `formal/periodic-control/stdout.sanitized.log` | `evidence/new_validation/periodic05/stdout.log`, path-redacted | Original SHA-256 `9a2f9615903b0325d52de3785a94807aefadbabeaa9138eb793488d8928dc206` |
| `formal/comparator/README.md` | Comparator fresh run transcripts and timing records | Original transcript hashes and archive hash are documented in that file; raw archive/transcripts are not distributed |
| `video/public/english/media/flow-illustration.mp4` | Locally generated crop from the project's existing Taylor–Green visualization (`video/public/InformeV4/media/VIDEO_COMPLETO_5070_MONTAJE.mp4`, source SHA-256 `a87f54738a7021c0078c2e5f6834a7bd68a3d4b8d5e2838c542fb44bfcbc900c`) | Crop provenance: FFmpeg `-ss 33.203417 -t 39.866667 -vf crop=1920:512:0:153 -an`, H.264 CRF 19; output SHA-256 `5709a87177c85315750ade115e12ab4cae6cce17393ddd03b59d9e6458b9d959`. The transformation was not independently rerun in this review; the clip is illustrative, not evidence or a proof. |

Private temporary paths, host usernames, network addresses, provider request identifiers, API responses, and access credentials are intentionally omitted.
