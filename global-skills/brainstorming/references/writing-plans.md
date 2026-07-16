---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, and how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

## Context

If working in an isolated worktree, it should have been created via the
appropriate worktree workflow at execution time.

Save plans to:
`docs/plans/YYYY-MM-DD-<feature-name>.md`
(User preferences for plan location override this default.)

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken
into sub-project specs during brainstorming. If it wasn't, suggest breaking
this into separate plans — one per subsystem. Each plan should produce working,
testable software on its own.

## File Structure

Before defining tasks, map out which files will be created or modified and what
each one is responsible for. This is where decomposition decisions get locked
in.

- Design units with clear boundaries and well-defined interfaces.
- Prefer smaller, focused files over files with several responsibilities.
- Keep files that change together together; split by responsibility.
- Follow established patterns in existing codebases. Do not unilaterally
  restructure a large file unless the plan has a focused reason to do so.

Each task should produce a self-contained change that makes sense independently.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a fresh
reviewer's gate. Fold setup, configuration, scaffolding, and documentation into
the task whose deliverable needs them. Split only where a reviewer could
meaningfully reject one task while approving its neighbor. End each task with
an independently testable deliverable.

## Bite-Sized Task Granularity

Each step is one action, normally taking 2–5 minutes:

- write the failing test;
- run it and verify failure;
- implement the minimal change;
- run the test and verify success;
- make the change available for review according to the repository workflow.

## Plan Document Header

Every plan must start with:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** Implement this plan task-by-task using the repository's approved execution workflow.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about the approach]

**Tech Stack:** [Key technologies and libraries]

## Global Constraints

[Project-wide requirements: version floors, dependency limits, naming and copy rules, platform requirements.]

---
```

Use checkbox syntax (`- [ ]`) to track steps.

## Task Structure

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file`
- Modify: `exact/path/to/existing-file:line-or-symbol`
- Test: `exact/path/to/test-file`

**Interfaces:**
- Consumes: [inputs and exact signatures from earlier tasks]
- Produces: [names, types, and behavior that later tasks rely on]

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run the test and verify the expected failure**
- [ ] **Step 3: Write the minimal implementation**
- [ ] **Step 4: Run the test and verify the expected success**
```

Each implementer must be able to understand its task without reading tasks out
of order. Include complete code or precise pseudocode for non-trivial code
steps, exact commands, and expected output.

## No Placeholders

Every step must contain the actual content an engineer needs. Never leave:

- `TBD`, `TODO`, `implement later`, or `fill in details`;
- vague instructions such as “add appropriate error handling”;
- “write tests for the above” without concrete behavior;
- “similar to Task N” instead of repeating required details;
- references to undefined types, functions, or methods.

## Self-Review

After writing the plan, check it against the spec:

1. **Spec coverage:** every requirement maps to a task.
2. **Placeholder scan:** remove vague or incomplete instructions.
3. **Type consistency:** signatures and property names match across tasks.

Fix issues in the plan before returning it.

## Execution Handoff

After saving the plan, state that it is ready for execution and identify the
repository's available execution workflow. Do not silently begin implementation
unless the user or calling agent explicitly requests execution.
