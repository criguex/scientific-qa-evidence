# Class F3 withdrawn before freezing

> **Authorship of this record.** Written by the AI assistant (Claude Code, Opus) from its own observations inside this session, for the repository author Cristian Guerra. The "What was observed" items are first-hand to the assistant: they are what the assistant saw happen to its own responses. The "Hypothesis" is the assistant's inference, not a statement from the safety system. The assistant cannot read the classifier's internals.

On 2026-10-21, while class F3 was being prepared, parts of the AI assistant's responses were stopped twice by an automated safety filter in the assistant's service. The filter did not state its reason. Work on F3 stopped at that point; the tool builds for it were halted on the test host.

To keep the experiment within the assistant's permitted scope, class F3 is removed **before** the design is frozen. The experiment continues with classes F1, F2, F4, F5, the positive control F6 and the clean cases: 21 cases in total.

The seed commitment is unaffected. The seed only decides the assignment of cases, and no assignment has been made.

The earlier feasibility record remains published as a historical record of work done before the withdrawal. It is not part of the experiment.

## What was observed

These are facts recorded by the assistant, with the limitation that the assistant cannot see the filter's internals.

- Two assistant turns were cut off by a classifier described as a safety filter in the assistant's own service, not a tool or API error. A system notice said the withheld content must not be reproduced.
- The stops happened during, and only during, work on class F3. F3 is the one class that involves running a public exploit for a Lean kernel soundness bug (CVE-2026-72844) on a deliberately outdated Lean version.
- The first stop occurred while composing a message after the exploit had already been reproduced and that result published (commit `e1e63b4`). The second occurred during an edit that was removing F3 from the design.
- No tool call was left half-applied: the working tree stayed clean at `e1e63b4` after both stops.

## Hypothesis (not confirmed)

The assistant cannot read the classifier's reason, so the following is inference, not fact.

- Most likely: the classifier reacted to the assistant generating or orchestrating exploit code for a known CVE, even though the exploit is public, inert outside Lean, and used here only to demonstrate that an up-to-date checker refuses it. Security-exploit generation is a common trigger for such filters regardless of intent.
- A weaker possibility: wording in the withheld text resembled a pattern the classifier flags. Unlikely to be the whole cause, since both stops clustered on the same topic.
- What it is probably **not**: the numerical, provenance, build-integrity, kernel-currency and statement-mutant work (F1, F2, F4, F5, F6) never triggered the filter across many turns.

## Decision

The protocol does not need F3. Checker version currency is already covered by the [kernel currency check](../../evidence/formal/kernel-currency.md), which compares the kernel source and nanoda commit against the known 2026 fixes without running any exploit. The blind experiment proceeds without F3, and this withdrawal is left in the record so the gap and its reason are traceable.
