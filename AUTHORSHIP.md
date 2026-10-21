# Authorship and AI disclosure

Cristian Guerra (criguex) is the human author of this QA study and independent reproduction. He is Colombian, from Medellín, and self-describes as having more than eight years of QA Automation experience. In concise CRediT terms, his roles are Conceptualization, Methodology, Software, Validation, Data curation, and Writing—original draft and review & editing. Validation here means running and reviewing the scoped QA evidence, not independent mathematical verification.

OpenAI is credited for the original proofs and the original repository. This package does not claim authorship of those proofs, discovery of a theorem, or validation of an open mathematical problem.

AI tools assisted with analysis, translation, editing, and code preparation. They are disclosed as assistance, not academic coauthors or co-discoverers. A required Git `Co-Authored-By: Codex` trailer, where used, records tool-assisted code contribution under the repository's attribution convention; it is not a claim of academic authorship. The human author remains responsible for the claims, limitations, evidence selection, and release decision. Publication authorization was given on 2026-10-20.

The synthetic numerical examples are calculations under explicit software contracts. The formal material consists of bounded fixture checks and recorded Comparator runs. Neither is represented as experimental validation or a general mathematical certification.

## AI assistant identity across this session (traceability)

For full traceability of who produced which commits, the environment's stated identity for the AI assistant changed partway through the 2026-10-21 work, and the commit trailers record it:

- Commits up to and including `e1e63b4` carry `Co-Authored-By: Claude Opus 5.5`. At that point the session environment reported the model as `claude-opus-5-5` with a June 2026 knowledge cutoff.
- From commit `aa47c98` onward the trailer is `Co-Authored-By: Claude Opus 4.8`, after a system notice changed the reported model to `claude-opus-4-8` with a January 2026 knowledge cutoff.

This is recorded as an observable fact. The assistant runs on the identity its environment declares and cannot verify from inside which label is accurate, so no claim of intent or deception is made here. The per-commit `Co-Authored-By` trailers in `git log` are the authoritative record of which label was active for each change. Human authorship, responsibility and the release decision remain with Cristian Guerra regardless of the assistant label.

Later the same day the author ran Claude Code's `/model` command, which set the model to Opus 5.5, and the commit trailers from `ae55a24` onward say `Claude Opus 5.5` again. This shows the model is selectable in the client, which is the most likely explanation for the earlier change: a model switch in the session, not a deception.
