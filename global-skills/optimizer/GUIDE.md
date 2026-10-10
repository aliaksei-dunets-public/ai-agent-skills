# Optimizer Guide

Optimizer reviews and repairs packages of agent instructions — skills, agent
definitions, always-on instruction files, references, examples, and their
documentation — the way an experienced prompt engineer would: it finds what is
broken, inconsistent, contradictory, duplicated, or unclear, and then fixes it.

For a single standalone prompt, use the `prompter` skill instead.

## What it checks

- **Integrity:** broken links and paths, missing or orphaned files, names and
  versions that disagree between files, malformed frontmatter or Markdown,
  outdated examples.
- **Content:** contradictions, duplicated rules, vague instructions, weak
  activation descriptions, content in the wrong layer, unconditional loading,
  missing failure handling, unsafe tool or delegation design, unclear output
  contracts.
- **Documentation:** README/guide, changelog, and version reflect the current
  behavior.

The full list is in `references/checklist.md`; the rules used when rewriting
are in `references/best-practices.md`; platform notes (Codex, Claude Code,
Copilot, Antigravity) are in `references/platforms.md`.

## Modes

- **audit** — findings and proposed fixes, no changes.
- **fix** — audit, then apply the fixes and update related documentation.

## Example requests

- `Audit the skill in skills/release-helper.`
- `Check this agent package for broken links and contradictions, then fix it.`
- `Clean up AGENTS.md and CLAUDE.md — they duplicate each other.`
- `Review our Copilot instructions and custom agents for conflicts.`

## What you get

1. **Findings** — severity, location, problem, fix;
2. **Changes** — files changed (fix mode);
3. **Questions** — only decisions that need you, such as which side of a
   contradiction is intended;
4. **Checks** — what was verified after the changes.

Optimizer keeps the author's intent, capabilities, language, and safety
requirements, changes only what its findings justify, and does not claim
measured improvements it did not measure.

## Installation

Copy the `optimizer` folder into the skill directory of your platform, for
example `.claude/skills/optimizer/`, `.agents/skills/optimizer/`,
`.github/skills/optimizer/`, or `.agent/skills/optimizer/`.
