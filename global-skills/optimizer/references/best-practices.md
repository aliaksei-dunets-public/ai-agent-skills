# Writing Guide for Fixes

Use when rewriting instructions. These are defaults, not a template: keep the
author's structure where it already works.

Use `technical-writing-ste`, loaded through the optimizer entry point, for
language rules and the behavior contract. The guidance below covers instruction
design and package repairs. Examples illustrate possible requirements; they
do not authorize adding those requirements to the text being edited.

## Say what, when, and why

- Lead with the outcome and success criteria; add procedure only where order
  matters or the agent repeatedly goes wrong.
- Write known rules as condition → action. For example, use "If tests fail,
  report the failing test and stop" only when those actions are established
  requirements. Do not infer them from "be careful with tests."
- Give the reason for non-obvious rules in one clause. A model applies a
  reasoned rule to new cases; a bare command it applies literally.
- Prefer positive instructions ("reply in the user's language") over lists of
  prohibitions. Keep prohibitions for real hazards.
- Reserve `must`, `never`, and `always` for hard requirements. Overused
  absolutes make real requirements indistinguishable and invite conflicts.

## One home per rule

- Choose the canonical location by scope: always-on facts in the project
  instruction file, task procedures in a skill, detail in a reference.
- Consolidate copies using the executor-access check in step 5 of `SKILL.md`;
  preserve necessary repetition for independent consumers.
- When layers must coexist, state precedence once.

## Progressive disclosure

- Entry point: purpose, modes, workflow, key decisions, pointers.
- References: detailed checklists, domain knowledge, long examples, platform
  or model specifics. Each pointer says when to load the file.
- Keep reference routes easy to follow. Additional levels are justified when
  they reuse a maintained dependency or separate conditional detail. Avoid
  indirection that adds no decision value and do not reload files already read.

## Descriptions and triggers

- State what the skill does, when to use it, and exclusions when needed.
  Follow the target platform's format requirements; do not change grammatical
  person solely for style.
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
- Update affected documentation and existing release metadata using step 5
  of `SKILL.md`; do not impose a new release process.
- Do not add sections, files, or frameworks the package did not need.
