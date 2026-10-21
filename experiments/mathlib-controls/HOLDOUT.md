# Held-out cases: how to contribute

The cases in [`DESIGN.md`](DESIGN.md) were all chosen by the author. To test the protocol without tuning to those choices, someone who has not worked on it should prepare extra cases.

1. Pick a theorem already in Mathlib (pinned commit `85e3a25`).
2. Write up to three Lean statements: the original, and any changes you like (equivalent, weaker, false, or ones you are unsure about).
3. For each, write the label you expect: SAME, CHANGED_EQUIVALENT, CHANGED_WEAKER, CHANGED_FALSE or CHANGED_UNKNOWN.
4. Put the labels in a file, publish only its SHA-256 (for example in an issue or an email), and send the statements without the labels.

The cases are run blind, the results are published, and only then the labels file is requested and compared with its hash. Received cases and their results will be listed here, with the contributor's name if they wish.

**Received so far:** none.
