# Fresh Comparator run record

This English summary and the two full per-challenge transcripts are sanitized, derived records from the original terminal output. ANSI escapes are removed; private command lines, host usernames, workspace/tool paths, and private IPs are redacted. Original raw transcripts are not included in this distribution. Their SHA-256 values are retained below for provenance. The deterministic sanitizer is `production/sanitize_comparator_logs.py`.

| Challenge | Lean default kernel | nanoda | Comparator result | Elapsed | Maximum RSS |
| --- | --- | --- | --- | ---: | ---: |
| Navier–Stokes | accepted | accepted | `Your solution is okay!`; exit 0 | 417.56 s | 8,126,256 KiB |
| Euler | accepted | accepted | `Your solution is okay!`; exit 0 | 654.43 s | 7,921,768 KiB |

This is a recorded independent recheck of the configured challenges after the clean03 new-source build, not a theorem-discovery claim or universal verification. The logs show challenge-side `sorry` placeholders during replay; these are challenge declarations and are not a finding that the supplied Comparator solution is incomplete. The Euler output separately lists standard axioms for two declarations. Any prior axiom audit is separate; these logs are not presented as a fresh audit or human theorem review.

- [Full sanitized Navier–Stokes transcript](NavierStokes.full.sanitized.log)
- [Full sanitized Euler transcript](Euler.full.sanitized.log)

## Original transcript hashes

| Original file | SHA-256 |
| --- | --- |
| NavierStokes.typescript | `bb1c50fcbc18aba9d429e14cfb1c5a49be2a43aaf440e509aab525225f81c1c5` |
| Euler.typescript | `b808f7015c47df453fe4e8eee7753acab9015eedeb092a7b009b395acc64b500` |
| NavierStokes.time.txt | `2f4ccac6d49941754ef5dde87d48b02700d9fffacb791106bca5ab3f4411504e` |
| Euler.time.txt | `b0b36c7c62ca0ef152bee2dce7feb23ff747c7c828b53e4ce1c1a2769b8dfec1` |

Elapsed and RSS values come from the original timing files. Challenge decisions and final status come from the terminal transcripts. The archive SHA-256 is `abd1537aeca731f169a4c288a1937919fa1f6024aad7c6c8c1fd969071304421`; the archive itself is not distributed.
