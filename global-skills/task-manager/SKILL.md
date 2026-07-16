---
name: task-manager
description: >-
  Manage the repository task source for the development-orchestrator lifecycle:
  create and select tasks, validate dependencies, update execution metadata,
  record work, and close completed tasks. Use only for explicit task-management
  operations or when invoked by development-orchestrator.
---

# Task Manager

## Canonical state

The operational task source is split into open and close indexes and detailed
task files:

- open index: `docs/plan/open-tasks.md` (auto-generated)
- open details: `docs/plan/open/TASK-XXXX.md` or
  `docs/plan/open/YYYY-MM-DD-<feature-name>.md`
- close index: `docs/plan/close/close-tasks.md` (auto-generated)
- close details: `docs/plan/close/TASK-XXXX.md` or
  `docs/plan/close/YYYY-MM-DD-<feature-name>.md`

The task ID in frontmatter remains the stable identity even when a detail file
uses the date-feature filename. `docs/plan/` is the default task root; pass
`--tasks-root` when the project uses another location.

Do not create a second backlog from another roadmap or silently migrate its
checklist items. A plan becomes an operational task only through the create
operation.

## Task contract

Each task must contain technical state (`id`, `title`, `type`, `priority`,
`status`, `execution_state`, `revision`, `created`, `updated`, `dependencies`)
in a YAML frontmatter block at the top of the detail file. The body must contain
`Objective`, `Scope`, `Acceptance criteria`, `Implementation plan`, `Review
history`, `Approval`, `Testing`, `Documentation`, `Completed work`, `Work log`,
and `Blockers` sections.

Primary status lifecycle:

```text
created -> in_progress -> review -> approved -> done
```

Technical execution state is separate:

```text
ready | running | waiting_approval | blocked
```

Never replace a primary status with an execution state.

## Operations

1. For a create operation, use `create_task.py`. It assigns a unique task ID,
   creates a date-feature detail file in `open/`, and regenerates both indexes.
2. For selection, choose an explicitly requested task, or the first
   dependency-ready `created` task by priority and creation date. Use
   `sync_tasks.py --select-next` for deterministic selection.
3. Before starting work, validate the task's objective, scope, acceptance
   criteria, plan, and completed dependencies.
4. For a start operation, atomically set `status: in_progress`,
   `execution_state: running`, update `updated`, and append a `Work log` entry.
5. Record review, approval, test, coverage, documentation, and project-tool
   evidence in the task. Review skills never change these fields directly.
6. Set `status: review` only after both independent reviews pass and set
   `execution_state: waiting_approval`.
7. Set `status: approved` only with explicit approval evidence. The update
   utility rejects a direct transition to `approved` without an approval flag.
8. Set `status: done` only during close after completion evidence passes:
   approval, testing, documentation, and completed work must be populated.
9. To close a task, move its detail file from `open/` to `close/` without
   changing its filename, set `status: done`, set `execution_state: ready`,
   and regenerate both indexes. Preserve all history.

When modifying task state or adding logs/reviews, use the provided utility
script. It validates the schema, enforces legal transitions, and accepts a JSON
payload file:

```json
{
  "status": "in_progress",
  "state": "running",
  "log": "Started working on the task"
}
```

```bash
python .ai/scripts/update_task.py TASK-0005 --apply .tmp/update.json
```

For explicit approval, use a payload containing `"approve": true`; the task
must already be in `review`:

```json
{
  "approve": true,
  "review": "Independent reviews passed"
}
```

To close a task after all completion evidence is present:

```json
{
  "archive": true
}
```

The utility never stages or commits Git changes. The caller owns any repository
commit required by the project workflow before closing a task. Never edit
`open-tasks.md` or `close-tasks.md` manually.

If a required stage fails, keep the primary status unchanged and set
`execution_state: blocked` with a concrete blocker. Do not bypass review limits,
approval, dependency checks, or close validation.

## Side-effect boundary

This skill may modify task records only for the explicit operation it owns. It
must not modify production code, run reviews as the implementing agent, or mark
a task done without the required completion evidence.

## Result contract

Return only a structured result compatible with the orchestrator:

```yaml
skill: task-manager
result: passed | failed | blocked
summary: "Short operational result"
findings: []
changed_files: []
artifacts: []
blocking_reasons: []
```
