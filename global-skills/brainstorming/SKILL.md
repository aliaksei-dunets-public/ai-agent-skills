---
name: brainstorming
description: >
  Clarify an idea, task scope, or material uncertainty and produce a design,
  requirements handoff, or implementation plan. Use for requested brainstorming,
  design exploration, or planning, and when unresolved requirements would change
  the work. Do not force a design ceremony on clear, already authorized work.
---

# Brainstorming and Task Preparation

Turn the user's intent into a proportionate, reviewable result. Keep requirements,
design, implementation planning, and execution distinct. This skill prepares work
and returns a clear result to the user or calling agent.

## Select the result

Choose from the request and current context, not from the presence of a tool:

| Mode | Use when | Result |
| --- | --- | --- |
| `direct_response` | The user wants an explanation, answer, or comparison | Answer in the conversation; no task or file unless needed |
| `managed_work` | Work is assigned but its scope or acceptance needs clarification | Compact requirements handoff for the next step |
| `design_only` | The user asks to explore ideas or propose a design without execution | Alternatives and a recommended design, with its decision status |
| `planning` | An implementation plan is explicitly requested or required by the active workflow | Actionable plan based on requirements and repository evidence |

An execution request with clear requirements already authorizes routine choices
within that scope. Complete only the preparation it needs, then return control to
the calling workflow. Do not require another approval merely because this skill
was loaded. A design-only or planning-only request does not authorize execution.

## Establish the task

1. Read the request, applicable project instructions, and relevant context.
   Search before opening large files. If requirements or a specification are
   supplied, preserve their source and check against the latest user direction.
2. Identify the goal, expected deliverable, scope, exclusions, constraints,
   existing decisions, and observable acceptance criteria. Separate verified
   facts, accepted decisions, proposals, and assumptions; cite their sources when
   the distinction affects subsequent work.
3. Ask only about missing decisions that materially affect scope, external
   actions, compatibility, or acceptance. Prefer one concise question with
   choices when useful. Continue independent work while waiting.
4. Wait for a real answer when a decision or authorization is required. Elapsed
   time, silence, reviewer feedback, and an assumed preference are not approval.
   For a nonblocking uncertainty, state a reversible assumption and its impact.
5. Compare approaches only where trade-offs matter. Explain the recommendation;
   do not invent two alternatives for an obvious correction.

Stop discovery when the requested result can be produced with explicit scope and
testable criteria. Keep unresolved blocking decisions visible rather than
presenting a proposal as accepted.

## Design exploration

In `design_only`, present a design at a depth proportional to the problem. Cover
the behavior and relevant boundaries, interfaces, data flow, failure handling,
and verification. Short tasks can fit in one response; do not impose section
lengths or repeated approvals.

If a material new design decision is needed for assigned implementation, make it
reviewable in the conversation or handoff before asking for that decision. Reuse
existing approval and accepted requirements; do not ask again for approval of
their written copy. A reviewer's technical assessment does not substitute for a
user decision. Do not create a design or specification file unless the user
explicitly requests one.

## Implementation planning

In `planning`, read [the planning reference](references/writing-plans.md).
Build from the supplied requirements or explicit planning request, inspecting
actual files, interfaces, tests, and project conventions before assigning steps.
Do not describe unverified APIs or future capabilities as implemented facts.

Make each task actionable: identify files, dependencies, interfaces, observable
behavior, and appropriate checks with commands and expected outcomes. Record
unresolved assumptions instead of manufacturing exact code or commands. Keep
architecture rationale in the design and execution steps in the plan, linked
without copying entire documents.

Use the project-defined plan location and format first. Reuse an existing plan
instead of creating a competing copy. With no project convention, a needed
standalone plan may use `docs/plans/YYYY-MM-DD-<topic>.md`.

Self-review requirements coverage, dependencies, interface consistency, and
checks. Use [the plan review reference](references/plan-document-reviewer-prompt.md)
only for a separately authorized review. Return the plan and blocking decisions;
execution continues only within the user's request or active workflow.

## Handoff and ownership

For `managed_work`, return only what the next step needs, in the user's language:

- goal and deliverable;
- request/specification source and relevant context with source pointers;
- requirements, accepted decisions, scope, and constraints;
- observable acceptance criteria;
- material assumptions, unresolved decisions, and the next required step.

This handoff is requirements input, not an implementation plan or completion
report. When prior state is available, send the changed facts and decisions with
enough context to remain understandable; keep full evidence accessible at source.

- Do not create tracking records or other artifacts just to brainstorm.
- Do not present successful preparation as implementation, validation, or user
  acceptance. State which decisions are accepted and which remain proposals.
- Follow project rules for documents, language, and machine-readable values;
  do not impose another project's paths, tools, storage, or process.
- Preparation does not authorize installing tools, creating a worktree,
  delegating, committing, or publishing. Commit only when the user explicitly
  requests a commit.
