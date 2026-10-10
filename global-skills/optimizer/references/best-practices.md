# Writing Guide for Fixes

Use when rewriting instructions. These are defaults, not a template: keep the
author's structure where it already works.

## Say what, when, and why

- Lead with the outcome and success criteria; add procedure only where order
  matters or the agent repeatedly goes wrong.
- Write rules as condition → action: "If tests fail, report the failing test
  and stop" instead of "be careful with tests".
- Give the reason for non-obvious rules in one clause. A model applies a
  reasoned rule to new cases; a bare command it applies literally.
- Prefer positive instructions ("reply in the user's language") over lists of
  prohibitions. Keep prohibitions for real hazards.
- Reserve `must`, `never`, and `always` for hard requirements. Overused
  absolutes make real requirements indistinguishable and invite conflicts.

## One home per rule

- Choose the canonical location by scope: always-on facts in the project
  instruction file, task procedures in a skill, detail in a reference.
- Replace other copies with a pointer ("see `references/x.md`") or delete them.
- When layers must coexist, state precedence once.

## Progressive disclosure

- Entry point: purpose, modes, workflow, key decisions, pointers.
- References: detailed checklists, domain knowledge, long examples, platform
  or model specifics. Each pointer says when to load the file.
- Keep references one level deep; a basic rule should not require following a
  chain of files.

## Descriptions and triggers

- Third person, specific: what it does + when to use it + (if needed) when not.
- Include the natural phrases users say ("audit", "clean up", "fix links").
- Mention the neighboring skill to use instead, when overlap is likely.

## Examples

- Use examples to show format or a hard distinction, not to restate rules.
- Every example must obey the current rules; an outdated example silently
  becomes a competing rule.
- Prefer one good example to several similar ones.

## Workflows and agents

- Number steps only when order matters; otherwise use a checklist.
- State stop conditions and what to do on failure or missing input.
- Delegate to a subagent only for a concrete benefit; give it a bounded
  assignment and expect a compact result (status, findings, changes,
  verification, blockers).
- Put enforcement (permissions, blocking dangerous commands, schemas) in the
  platform or application; instructions explain intent.

## Output contracts

- Name the reader and the required content; list what to omit (restating the
  task, narrating routine steps, empty sections, repeated findings).
- Separate thinking depth from answer length: analyze fully, report briefly.
- Allow expansion for critical risk, failed verification, conflicts, or
  missing evidence.

## Editing hygiene

- Preserve capabilities, constraints, safety and verification steps,
  terminology, language, and tone unless a finding requires changing them.
- Keep paths, commands, identifiers, and quotations exact.
- After moving or renaming anything, update every reference to it.
- Update the guide/README, examples, changelog, and version together with
  behavior changes.
- Do not add sections, files, or frameworks the package did not need.
