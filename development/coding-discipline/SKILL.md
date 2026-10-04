---
name: coding-discipline
description: >
  Keep implementation focused, proportionate, and verifiable when creating or
  modifying code, tests, scripts, configuration, migrations, or refactoring.
  Do not use for documentation-only work, audits, or read-only diagnostics
  unless implementation changes are included.
---

# Coding Discipline

Make the smallest coherent change that satisfies the user's goal and the
project's correctness, security, and compatibility requirements. These are
implementation guidelines, not an additional approval or review workflow.

## Resolve material uncertainty

Read the request and relevant project context before editing. Reuse accepted
requirements and decisions. Ask only when a missing decision materially changes
scope, behavior, compatibility, external actions, or acceptance.

For a low-risk, reversible choice, select a reasonable approach and state the
assumption if it affects the result. Compare alternatives only when their
trade-offs matter; do not require a question or design ceremony for clear work.

## Keep the solution proportionate

- Implement required behavior and its necessary safeguards; avoid speculative
  features, configurability, and future-proofing.
- Add an abstraction when it clarifies a real boundary, responsibility, invariant,
  or repeated behavior. Single use alone is not a reason to forbid it.
- Preserve error handling and validation required by actual inputs, trust
  boundaries, and failure behavior. Omit unreachable cases only when supported
  by the contract, not because they seem unlikely.
- Judge simplicity by behavior, responsibilities, and maintenance cost rather
  than a line-count target. Shorter code that hides required behavior is not
  an improvement.

## Make scoped changes

Inspect relevant existing edits and preserve them. Follow applicable project
rules and established patterns. Change adjacent code or formatting only when
needed for the deliverable; do not bundle unrelated cleanup or redesign.

Remove imports, variables, and other code made unused by this change when safe.
Mention unrelated debt only when it materially matters; leave it for separately
assigned work. Necessary fixes across callers, tests, configuration, and
documentation belong to the same change when their contracts are affected.

Every changed file should be justified by the request, its acceptance checks,
or a direct consequence of the implementation.

## Verify the outcome

Define observable acceptance criteria. For multi-step work, use a short plan
connecting meaningful deliverables to checks; a trivial edit needs no formal plan.

- For a bug, reproduce the failing behavior and add a regression test when
  practical and valuable.
- For new behavior or refactoring, check affected contracts and relevant normal
  and failure paths; compare with the baseline when needed.
- For low-impact reversible edits, use direct inspection or an appropriate
  syntax/configuration check rather than tests that mirror the implementation.
- Use project-required checks and available trusted tools. Do not install
  dependencies, change environments, or run external/destructive actions merely
  to obtain a passing result.
- Distinguish pre-existing failures, new regressions, and environment limitations.
  Repeat checks after relevant changes or new evidence, not indefinitely.

Finish when acceptance and required checks are satisfied, or report the material
blocker and what remains unverified. Report actual changes and observed results;
do not present a plan, an unrun test, or an assumption as completed verification.
