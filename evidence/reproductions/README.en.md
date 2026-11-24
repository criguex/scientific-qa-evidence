> English translation of [README.md](README.md). If they differ, the original prevails.

# Reported reproductions

Each row corresponds to a person who ran `python verificar.py` on their own computer and reported the result to me with the [reproduction form](https://github.com/criguex/scientific-qa-evidence/issues/new?template=reproduccion.yml). I keep each report as an exact copy of what that person pasted in their issue. Thanks to everyone who took the time to try it and share the result.

**How a report is accepted**

1. The report's data version and fingerprint are compared against the reference for that version. If they do not match, the report is published anyway: a different result is exactly what we are looking to find.
2. `mi_resultado.txt` is copied as is and the original issue is linked, which keeps the screenshots and other attachments.
3. I state whether the person reporting knows me. A reproduction by someone I know counts as a run on another computer, but not as an independent reproduction in the strict sense.

**How to upload evidence.** Fill out the form and drag your screenshots, a short terminal video or your `mi_resultado.txt` into the comment field, or add them later as a comment on your own issue. GitHub accepts images, short videos and `.txt` and `.zip` files. If you also keep a copy in your own account, you can link to it. That way there is also evidence outside my control.

## References

Each data version has its own fingerprint. I compare each report against the reference for the version it says it used. Runs on my Mac and on GitHub's CI do not count as reproductions.

| Data version | Fingerprint | In force | Notes |
|---|---|---|---|
| `c8edd482375d` | `5292-A47D-AFA5` | since November 3, 2026 | The version depends only on the evidence. It includes the October 23 Lean evidence in the manifest. See the [November 3 log](../bitacora/2026-11-03.md) |
| `727c5b5f98ef` | `1A86-6B19-21C7` | October 27 to November 3 | It changed only because a CI fix touched a manifest file. I received no reports for this version |
| `26791fe6546f` | `C5F0-F1A8-2F4D` | October 24 to 27 | The one I shared on Instagram. Same fingerprint on my Mac and on GitHub's CI, on Ubuntu, macOS and Windows with Python 3.9 and 3.12 ([run 40104169962](https://github.com/criguex/scientific-qa-evidence/actions/runs/40104169962), commit f461905) |

## Reports

| # | Date (UTC) | System | Python | Download | Version and fingerprint | Matches its version? | Relationship to me | Report |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-24 15:16 | Windows 11 (10.0.26200) | 3.9.13 | ZIP | `26791fe6546f` · `C5F0-F1A8-2F4D` | Yes | Knows me | [issue #1](https://github.com/criguex/scientific-qa-evidence/issues/1) · [file](2026-10-24_gowtherw_windows.txt) |
| 2 | 2026-10-24 16:16 | macOS 27.0.1, Apple Silicon | 3.14.7 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Yes | Knows me or is a relative, per their own report | [issue #2](https://github.com/criguex/scientific-qa-evidence/issues/2) · [file](2026-10-24_6uerra_macos.txt) |
| 3 | 2026-10-24 16:51 | macOS 26.5.2, Apple Silicon | 3.9.6 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Yes | Not stated | [issue #3](https://github.com/criguex/scientific-qa-evidence/issues/3) · [file](2026-10-24_akegiraldo_macos_py39.txt) |
| 4 | 2026-10-24 17:04 | macOS 26.7.1, Apple Silicon | 3.14.4 | git clone | `26791fe6546f` · `C5F0-F1A8-2F4D` | Yes | Not stated (same person as #3) | [issue #4](https://github.com/criguex/scientific-qa-evidence/issues/4) · [file](2026-10-24_akegiraldo_macos_py314.txt) |

So far I have received 4 reports from 3 people, all equal to the reference for their version. There are still no reports from Linux and no different fingerprints. Thanks to everyone who has already tried it.

---

**In English.** Each row is someone who ran `python verificar.py` on their own computer and sent me the result through the reproduction form. I keep each report as a verbatim copy of what they pasted. I publish a report whether or not its fingerprint matches the reference for its data version. I also say whether the person knows me: a run by someone I know counts as a run on another computer, but not as a strongly independent reproduction. Thank you to everyone who has tried it.
