# Writing Implementation Plans

Read this reference only in `planning` mode. Prepare enough detail for an agent
to execute without rediscovering requirements; scale detail to the change.

## Ownership and location

Read project instructions before choosing a path or format. Reuse a supplied
plan and its requirements source; do not create a competing copy.

Without an existing convention, save a needed standalone plan to
`docs/plans/YYYY-MM-DD-<topic>.md`. A request for an outline can be satisfied in
the conversation. Do not create a file or tracking record solely for a template.

## Plan contents

Include the goal, requirements/design source, scope, constraints, assumptions,
file map, task dependencies, and validation. Keep accepted architecture in its
canonical design document and link to it. Follow project language and formatting;
the structure below is illustrative, not a mandatory schema.

For each task describe:

- **Deliverable:** observable behavior and relevant acceptance criteria.
- **Files:** actual paths to create, modify, or inspect, with symbols where useful.
- **Interfaces:** inputs, outputs, compatibility constraints, and dependencies.
- **Actions:** enough implementation detail to avoid material ambiguity; exact
  code is optional and should not replace investigation of unknown interfaces.
- **Validation:** appropriate commands, prerequisites, expected behavior, and
  failure signals. Label commands not yet run and checks that cannot run locally.

Split tasks at meaningful acceptance or dependency boundaries. Combine setup,
configuration, and documentation with the deliverable they support. Do not impose
a time limit per step, a fresh reviewer per task, or fixed test-first ceremonies.

Use behavior tests for substantive code changes and project-required checks for
configuration or documentation. Do not invent tests for low-impact reversible
edits or assertions that merely mirror implementation text.

## Uncertainty and review

An actionable plan must not hide a material unknown behind “implement later” or
“add appropriate handling.” State the missing evidence, the investigation step,
and the decision that depends on it. Do not invent signatures or claim a command
has passed. Unresolved blockers prevent calling the plan execution-ready; minor
documented assumptions need not block the whole plan.

Check requirement coverage, task ordering, file existence, interface consistency,
scope, and validation proportionality. Correct contradictions before handing off.
Use [the plan review reference](plan-document-reviewer-prompt.md) when a separate
review is authorized and adds value.

## Execution handoff

Return the plan location or outline, decision status, checks, and material
unknowns. For a planning-only request, stop after preparation. For an authorized
execution request, hand control back to its workflow without an extra approval
gate. Do not present writing the plan as completion of implementation, and do not
commit it automatically.
