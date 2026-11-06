# Optimizer Guide

Optimizer reviews and repairs packages of agent instructions — skills, agent
definitions, always-on instruction files, references, examples, and their
documentation — the way an experienced prompt engineer would: it finds what is
broken, inconsistent, contradictory, duplicated, or unclear, and then fixes it.

For a single standalone prompt, a prompt-authoring skill such as `prompter`
fits better. For wording-only edits or reviews of agent-facing text, in one
file or several, use `technical-writing-ste`.

## What it checks

- **Integrity:** broken links and paths, missing or orphaned files, names and
  versions that disagree between files, malformed frontmatter or Markdown,
  outdated examples. Path checks distinguish current dependencies from examples,
  templates, generated outputs, and historical records.
- **Content:** contradictions, duplicated rules, vague instructions, weak
  activation descriptions, content in the wrong layer, unconditional loading,
  missing failure handling, unsafe tool or delegation design, unclear output
  contracts.
- **Documentation:** current documentation and existing release metadata agree.
  Historical changelog entries retain their original context; packages without
  versioning do not need to adopt it for an edit.
- **Language:** agent-facing text (skills, references, agent definitions,
  instruction files) must be in English; quoted user phrases, examples, and
  literal output templates may keep another language. Adapted STE principles
  from `technical-writing-ste` identify unclear wording in agent-facing text
  only. Human-facing documentation, such as a README or this guide, keeps its
  language and style and is checked for accuracy and consistency. Language
  edits and translations preserve meaning and behavior, including requirement
  strength and conditions. Functional repairs are reported separately.
- **Fit and footprint:** defaults that match the workflows calling the package
  and rules not hidden in conditionally loaded files. When size or context cost
  is in question, a load map gives instruction-file bytes for typical and
  maximum loading scenarios; these byte counts do not measure total context
  cost or token usage.

The full list, including instruction-design criteria, is in
`references/checklist.md`; the fix and verification steps are in
`references/fix.md`; platform notes (Codex, Claude Code, Copilot, Antigravity)
are in `references/platforms.md`.

## Modes

- **audit** — findings and proposed fixes, no changes.
- **fix** — audit, then apply the fixes and update related documentation.

If a request names no mode, optimizer runs `audit` and offers `fix`.

## Example requests

- `Audit the skill in skills/release-helper.`
- `Check this agent package for broken links and contradictions, then fix it.`
- `Clean up AGENTS.md and CLAUDE.md — they duplicate each other.`
- `Review our Copilot instructions and custom agents for conflicts.`

## What you get

1. **Findings** — severity, type (`functional`, `structural`, or `language`),
   location, problem, why it matters, fix; findings that need your decision
   are marked, with any interim fix;
2. **Changes** — files changed (fix mode);
3. **Questions** — only decisions that need you, such as which side of a
   contradiction is intended; `fix` does not stop to wait for them;
4. **Checks** — what was verified and what was not covered;
5. **Offer** — after an audit, one line offering `fix`.

Optimizer keeps the author's intent, capabilities, and safety requirements, and
the language of human-facing documentation. It changes only what its findings
justify and does not claim measured improvements it did not measure. For large
packages, it inspects coherent batches and reports which areas were not covered.

## Installation

Copy the `optimizer` folder into the skill directory of your platform, for
example `.claude/skills/optimizer/`, `.agents/skills/optimizer/`, or
`.github/skills/optimizer/`.

Copy `technical-writing-ste` into the same parent directory so the two skill
folders are siblings. Keep its `references/` directory. Optimizer reads this
dependency to review agent-facing text in both modes and for language edits in
`fix`; `audit` changes no files. If the dependency is missing, optimizer
continues the other checks and reports the incomplete STE work.
