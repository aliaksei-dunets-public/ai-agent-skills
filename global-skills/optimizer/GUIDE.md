# Optimizer Guide

Optimizer reviews and repairs packages of agent instructions — skills, agent
definitions, always-on instruction files, references, examples, and their
documentation — the way an experienced prompt engineer would: it finds what is
broken, inconsistent, contradictory, duplicated, or unclear, and then fixes it.

For a single standalone prompt, use the `prompter` skill instead.

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
- **Language:** adapted STE principles from `technical-writing-ste` identify
  unclear wording. Language edits preserve meaning and behavior, including
  requirement strength and conditions. Functional repairs are reported separately.
- **Fit and footprint:** defaults that match the workflows calling the package,
  rules not hidden in conditionally loaded files, and instruction-file bytes
  for typical and maximum loading scenarios. Files inspected as audit material
  are recorded separately, with overlaps identified. These byte counts do not
  measure total context cost or token usage.

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

Shared rules have a canonical source, but necessary repetition remains when
independent executors need it. References load under their stated conditions
or for a specific audit finding; justified cross-skill dependencies may span
more than one reference level.

For large packages, it inventories paths and inspects coherent workflow batches.
Reports state inspected/deferred/unreadable areas; a partial batch is not a
complete audit. Exhaustive requests continue across batches, and fixes include
affected incoming links and governing documents without loading unrelated files.

## Installation

Copy the `optimizer` folder into the skill directory of your platform, for
example `.claude/skills/optimizer/`, `.agents/skills/optimizer/`,
`.github/skills/optimizer/`, or `.agent/skills/optimizer/`.

Copy `technical-writing-ste` into the same parent directory so the two skill
folders are siblings. Keep its `references/` directory. Optimizer reads this
dependency for content review and language edits in both modes; `audit` still
changes no files. If the dependency is missing, optimizer continues the other
checks and reports the incomplete STE work.
