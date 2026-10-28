---
name: technical-writing-ste
description: >
  Create, edit, or review technical documentation and agent instructions using
  adapted ASD-STE100 principles. Use for Agent Skills, README, AGENTS.md,
  CLAUDE.md, procedures, and technical reports. Improve clarity with minimal
  edits while preserving technical meaning and instruction behavior.
---

# Technical Writing STE

Make technical text clear, precise, and unambiguous. Apply these priorities:
accuracy, unambiguous meaning, clarity, then brevity.

Use the principles for English and Russian text. ASD-STE100 was developed for
English; this skill adapts its principles for software and AI-agent instructions.
It does not guarantee formal compliance with ASD-STE100.

## Workflow

1. Identify the text's purpose, audience, and requested scope: creation,
   editing, or review. A review alone does not authorize edits.
2. Read [the writing rules](references/writing-rules.md).
3. For existing text, identify concrete clarity or accuracy problems before
   editing. Leave clear, accurate text unchanged.
4. Create the requested text or correct the identified problems. Preserve
   suitable structure and use the document's language unless instructed otherwise.
5. Compare edits with the original. Check technical meaning and the behavior
   contract below. Remove changes that do not resolve a concrete problem.
6. Report unresolved ambiguities. If a clearer formulation would require
   guessing the intended behavior, retain the original and explain the issue.

## Behavior contract

Language edits must preserve:

- Purpose, scope, activation triggers, conditions, and exceptions.
- Required actions and the order of dependent actions.
- Requirement strength: mandatory, recommended, and optional actions remain
  distinct, including the meaning of `must`, `should`, and `may`.
- Permissions, prohibitions, and approval requirements.
- Stop conditions, error handling, and completion criteria.
- Input and output formats, dependencies, and required references.
- Technical terms, identifiers, API names, file paths, code, and command syntax.

Do not add requirements or remove constraints to improve style or brevity.
Preserve necessary repetition when instructions must work independently.

This skill governs language quality. If the task also authorizes functional
repairs, assess and explain those changes separately from language edits.
Do not present a behavior change as a wording improvement.
