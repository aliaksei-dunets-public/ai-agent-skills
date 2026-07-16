---
name: brainstorming
description: "Turn an idea or approved requirements into a clear design, specification, or agent-ready implementation plan. Use interactively when the user asks to think, brainstorm, design, or invent; use planning mode when an agent needs a concrete implementation plan before code changes."
---

# Brainstorming and Implementation Planning

Choose one mode before acting:

- **Interactive brainstorming** — the user asks to think, brainstorm, design,
  or invent. Preserve the hard-gate and collaborative dialogue below.
- **Planning mode** — an agent asks for an implementation plan, or an approved
  spec/requirements document is available. Optimize for execution by agents:
  inspect the repository, resolve requirements from existing evidence, and
  produce a concrete plan without unnecessary conversational turns.

In both modes, do not write code, scaffold a project, or perform implementation
work until the design or requirements have been approved or are explicitly
provided as approved input.

## Interactive brainstorming

Use this mode when the user explicitly wants ideation or design exploration.

1. Explore the project context first: files, docs, relevant history, and
   existing patterns.
2. Ask clarifying questions one at a time. Focus on purpose, constraints,
   success criteria, scope, and failure cases. Prefer choices when they make
   the decision easier.
3. Propose 2–3 viable approaches with trade-offs and a recommendation.
4. Present the design in reviewable sections. Cover architecture, components,
   data flow, error handling, and testing at a level proportional to scope.
5. Get user approval before implementation. If a section is rejected, revise
   it and continue the discussion; do not move to planning prematurely.
6. After approval, write the validated design to
   `docs/design/YYYY-MM-DD-<topic>-design.md`.
7. Self-review the spec and fix issues in place:
   - no `TBD`, `TODO`, placeholders, or vague requirements;
   - no contradictions between requirements, architecture, and behavior;
   - scope fits one implementation plan;
   - ambiguous choices are made explicit.
   If a separate spec reviewer is available, use
   `references/spec-document-reviewer-prompt.md` for that review.
8. Ask the user to review the written spec. Incorporate requested changes and
   repeat the self-review before planning.
9. Once the spec is approved, switch to Planning mode and read
   `references/writing-plans.md`.

Do not require a design conversation for a task that is already accompanied by
an approved spec or explicit implementation requirements; use Planning mode.

## Planning mode

Use this mode when the goal is to prepare an implementation plan for an agent.
Do not ask routine discovery questions if the repository, task, or approved
spec already answers them. Ask only when a missing decision would materially
change scope, behavior, or safety.

1. Read the approved spec or requirements. If none exists, derive a compact
   design from the user request and repository evidence; record assumptions
   that materially affect implementation.
2. Inspect the current project before defining work: relevant files, tests,
   interfaces, configuration, docs, and established patterns.
3. Check scope. Split independent subsystems into separate plans or state the
   decomposition needed before implementation.
4. Read `references/writing-plans.md` and follow its plan header, file map,
   task structure, step granularity, exact commands, and self-review rules.
   Treat it as the local planning reference, not as a separate skill to invoke.
5. Create the plan at
   `docs/plans/open/YYYY-MM-DD-<feature-name>.md`, unless the user gave a
   different location.
6. Make every task independently actionable and testable. Include exact file
   paths, interfaces, implementation details, tests, expected results, and
   dependencies on earlier tasks. Do not use placeholders or vague steps.
7. Self-review the finished plan for spec coverage, scope, placeholders, and
   cross-task type/interface consistency.
8. If the project or active environment provides a `task-manager` skill, invoke
   it to create a new task for the plan you just created. Pass the plan path and
   its goal; do not duplicate the plan contents in the task. If `task-manager`
   is unavailable, continue without installing or inventing one and report that
   task creation was skipped.
9. Return the plan path, material assumptions, validation commands, task-manager
   result, and any blocking decisions. Do not implement the plan in this mode.

## Shared constraints

- Keep units focused and communicate through explicit interfaces.
- Follow existing repository patterns unless the approved design intentionally
  changes them.
- Apply YAGNI: include only behavior required by the request and its constraints.
- Preserve security, correctness, compatibility, and failure reporting while
  making the design or plan shorter.
- Separate user-facing discussion from agent-facing plan detail: interactive
  responses should be understandable; plans should be precise and executable.
- The only bundled planning dependencies are `references/writing-plans.md` and
  `references/plan-document-reviewer-prompt.md`.
