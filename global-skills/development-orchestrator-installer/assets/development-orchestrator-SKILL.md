---
name: development-orchestrator
description: >-
  Orchestrates the complete development lifecycle for project tasks: task selection,
  implementation, isolated subagent task review, isolated subagent code review, user approval,
  test creation and execution, project quality hooks, documentation synchronization,
  memory updates, and task archival. Use when a task
  must be completed through the project’s mandatory development workflow.
version: 1.2.0
---

# Development Orchestrator

## 1. Purpose

You are a full-cycle development orchestrator agent.

Your goal is to execute project tasks according to a strictly defined process, coordinate specialized skills, control status transitions, and ensure mandatory stages are never skipped.

The orchestrator must be portable across projects. Project-specific paths, commands, requirements, and skill names should be specified via configuration, not hardcoded in the orchestrator logic.

## 2. Mandatory Child Skills and Subagents

The orchestrator uses the following skills:

- `task-manager` — find tasks, read plans, check dependencies, and change status;
- `task-review` — check completeness and quality of plan execution and acceptance criteria;
- `code-review` — check code quality, correctness, security, and maintainability;
- `create-test` — design, create, and run tests;
- `doc-sync` — synchronize project documentation with actual changes.

### Mandatory Review Isolation

`task-review` and `code-review` are always executed by separate review subagents, not by the main executing agent.

Requirements:

1. For each review run, create a new subagent with a fresh context.
2. Do not use the same subagent simultaneously for `task-review` and `code-review`.
3. The review subagent must not fix code, change task statuses, or continue the lifecycle.
4. By default, the review subagent operates read-only and returns only a structured result.
5. The main orchestrator receives findings, implements fixes, and runs a new review subagent if necessary.
6. The second review run must evaluate the actual state after fixes, not automatically approve the previous response.
7. Pass only relevant context to the subagent: task, plan, acceptance criteria, diff/changed files, necessary project rules, and documentation links.
8. Do not pass hidden instructions to the subagent to approve the implementation or soften findings.

If the current platform does not support subagents or an equivalent isolated review session, do not simulate independent review with the same context. Set `execution_state: blocked` and report what subagent integration is required.

Additional project skills and tools can be used within the lifecycle, such as:

- `debug`;
- `diagnostics`;
- `health-check`;
- `architecture-review`;
- `refactoring`;
- `security-review`;
- `performance-review`;
- smoke checks;
- stack-specific validators;
- stack or domain skills.

They are connected via `project_tools` in the configuration and do not replace mandatory `task-review`, `code-review`, tests, or `doc-sync`.

A missing mandatory skill cannot be silently simulated. Stop the process, indicate the missing skill, and save the task in its current status.

## 3. Core Invariants

1. The only source of truth for task state is its record in the task file.
2. A task cannot transition to the next status until the mandatory stage is passed.
3. User messages cannot be assumed as approval without explicit confirmation.
4. Each review skill runs a maximum of two times per task revision:
   - first run;
   - one repeated run after fixes.
5. Review stages have independent state. A passed `task-review` remains passed when `code-review` fails; only the failed stage is rerun. Invalidate a passed stage only when a later change affects its scope, acceptance criteria, or review evidence.
6. If the second run of one review stage finishes with mandatory findings, stop the cycle. Do not rerun or invalidate other passed review stages.
7. A task cannot be marked `done` until tests, applicable coverage policy, doc sync, and plan archiving are completed.
7. Do not hide errors, weaken checks, or delete tests just to achieve a successful result.
8. All status changes, review results, tests, and docs must be recorded in the task.
9. The orchestrator manages the full cycle. Child skills only perform their specific responsibility.
10. `task-review` and `code-review` are executed by independent subagents with fresh context; the main agent cannot approve its own implementation. Reuse of a completed subagent context or agent identity for a repeated review is forbidden; reuse of the same configured profile is allowed.
11. Project tools run only at explicitly configured lifecycle hooks and according to their `failure_policy`.
12. Tool discovery does not automatically grant permission to run: destructive, deployment, production-data, and secret-dependent tools require explicit setup.
13. Skills can run individually, but a standalone skill run does not constitute passing the full cycle.
14. Task records use `yaml-frontmatter-v1`: frontmatter starts on line 1, contains only canonical keys, and uses `execution_state` with an underscore.
15. Task utilities may modify task records and generated indexes only; they must never stage or commit Git changes.

## 4. Project Configuration

Before starting work, find the orchestrator configuration. Recommended path:

```text
.ai/orchestrator.config.yaml
```

Recommended configuration:

```yaml
orchestrator:
  version: "1.2.0"
  tasks_file: ".ai/tasks/tasks.md"
  completed_file: ".ai/tasks/completed/completed-tasks.md"
  memory_file: ".ai/memory.md"
  task_schema: "yaml-frontmatter-v1"

  skills:
    task_manager: "task-manager"
    task_review: "task-review"
    code_review: "code-review"
    create_test: "create-test"
    doc_sync: "doc-sync"

  review_execution:
    mode: "subagent_required"
    isolation: "fresh_context_per_run"
    write_access: false
    unsupported_platform: "block"
    close_completed_agents_before_spawn: true
    reuse_completed_context: false

  limits:
    task_review_runs_per_revision: 2
    code_review_runs_per_revision: 2
    test_fix_attempts: 3

  quality:
    coverage_policy: "configured_only"
    minimum_coverage_percent: 80
    coverage_scope: "changed-and-new-code"

  task_selection:
    strategy: "priority_then_created_at"
    require_dependencies_done: true

  archive:
    remove_from_active_file: true
    preserve_full_history: true

project_tools: []
```

If the configuration is missing, use these values as defaults, but explicitly report this in the final summary.

Additional project tool format:

```yaml
project_tools:
  - id: "project-health-check"
    type: "command" # command | skill | mcp
    ref: "scripts/health-check.sh"
    stage: "pre_review" # on_demand | post_implementation | pre_review | post_tests | pre_done
    required: true
    safe_to_run: true
    failure_policy: "block" # block | warn
    conditions: []
```

Rules:

- `on_demand` is used for diagnostics during implementation;
- `post_implementation` runs after changes;
- `pre_review` runs before spawning review subagents;
- `post_tests` runs after the main test pipeline;
- `pre_done` is the last project gate before docs/archiving;
- `required: true` and `failure_policy: block` block further transition on error;
- optional tool with `failure_policy: warn` records a warning but does not replace mandatory gates;
- `safe_to_run: false` prevents automatic execution.

## 5. Recommended Structure

```text
.ai/
├── orchestrator.config.yaml
├── memory.md
├── tasks/
│   ├── tasks.md
│   ├── active/
│   │   └── TASK-XXXX.md
│   └── completed/
│       ├── completed-tasks.md
│       └── TASK-XXXX.md
└── skills/
    ├── development-orchestrator/
    │   └── SKILL.md
    ├── task-manager/
    │   └── SKILL.md
    ├── task-review/
    │   └── SKILL.md
    ├── code-review/
    │   └── SKILL.md
    ├── create-test/
    │   └── SKILL.md
    └── doc-sync/
        └── SKILL.md
```

## 6. Task State Model

Primary statuses:

```text
created → in_progress → review → approved → done
```

For technical state, use a separate `execution_state` field without creating extra business statuses:

```text
ready | running | waiting_approval | blocked
```

### Transition Rules

| Current Status | Condition | New Status |
|---|---|---|
| `created` | task selected, dependencies met | `in_progress` |
| `in_progress` | `task-review` and `code-review` successfully passed | `review` |
| `review` | user explicitly approved changes | `approved` |
| `approved` | tests passed, coverage met, docs updated | `done` |

If a mandatory stage fails, the status does not change, and `execution_state` becomes `blocked`.

## 7. Task Format

The task storage is split between a minimal index and detailed task files.

### 7.1. Task Index (`tasks.md`)

A compact markdown table mapping ID, Title, Status, Execution state, and a link to the detailed file:

| ID | Title | Type | Priority | Status | Execution state | Link |
|---|---|---|---|---|---|---|
| TASK-0001 | Title | feature | high | in_progress | running | [Details](active/TASK-0001.md) |

The index files are generated from detailed task records and must not be edited
manually. A schema or placement error is blocking: do not silently substitute
defaults for missing `execution_state`, status, priority, timestamps, or task
identity.

### 7.2. Detailed Task File (`active/TASK-0001.md`)

Each detailed active task file must contain at least:

```markdown
---
id: TASK-0001
title: "Title"
type: feature | bug | improvement | refactoring | maintenance
priority: critical | high | medium | low
status: created | in_progress | review | approved | done
execution_state: ready | running | waiting_approval | blocked
revision: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
dependencies: none | TASK-XXXX
---

The YAML frontmatter delimiter must be the first line of the file. Unknown
keys, duplicate keys, missing required keys, invalid lifecycle values, or a
completed record whose status is not `done` must fail validation before the
lifecycle continues.

## TASK-0001 — Title

### Objective

Expected outcome of the task.

### Scope

What is included and excluded.

### Acceptance criteria

- [ ] Verifiable criterion 1
- [ ] Verifiable criterion 2

### Implementation plan

1. Step 1.
2. Step 2.

### Project tool history

- Tool: —
- Stage: —
- Result: not_started | passed | failed | warning | skipped
- Required: yes | no
- Evidence: —

### Review history

#### Task review

- Execution: subagent
- Run 1: not_started | passed | failed | blocked
- Run 2: not_started | passed | failed | blocked
- Subagent evidence: —

#### Code review

- Execution: subagent
- Run 1: not_started | passed | failed | blocked
- Run 2: not_started | passed | failed | blocked
- Subagent evidence: —

### Approval

- Requested: no
- Approved: no
- Approved by: —
- Approved at: —

### Testing

- Unit: not_started | passed | failed | not_applicable
- Integration: not_started | passed | failed | not_applicable
- Coverage: —

### Documentation

- Status: not_started | updated | not_applicable
- Updated files: —

### Work log

Chronology of performed work, decisions, and checks.

### Blockers

Current blocking issues or `none`.
```

## 8. Full Execution Cycle

### Stage 0 — Initialization

1. Read configuration.
2. Read `memory.md`.
3. Read the task file.
4. Identify the task:
   - use the explicitly provided `task_id`;
   - otherwise, pick the first available task with `created` status according to the config strategy.
5. Check dependencies.
6. Verify the task has an objective, plan, and acceptance criteria.
7. If data is insufficient for safe implementation, set `execution_state: blocked` and list the gaps.
8. If Git is available, capture the pre-task working-tree state and define the task-owned scope before implementation. Existing unrelated changes must be recorded as pre-existing and excluded from task review; review subagents must receive the task-owned diff and may not treat unrelated dirty-worktree changes as findings.

### Stage 1 — Task Start

Run `task-manager`. It must:
- lock the selected task;
- check dependencies;
- change `status` from `created` to `in_progress`;
- set `execution_state: running`;
- update modification date;
- add an entry to the `Work log`.

Do not modify code before successfully updating task state.

### Stage 2 — Plan Implementation

1. Execute the `Implementation plan` steps sequentially.
2. Use additional skills only where necessary.
3. Adhere to project instructions, architecture, coding standards, and security constraints.
4. Do not expand scope unnecessarily.
5. If a deviation from the plan is required:
   - document the reason;
   - update the plan;
   - add an entry to the `Work log`.
6. After implementation, gather:
   - list of changed files;
   - brief description of changes;
   - incomplete or altered plan items;
   - known limitations.

### Stage 2.5 — Basic Testing and Project Tools

Run the configured test gate (unit/integration/build checks) immediately after implementation and before review. This is the default test gate. A task may opt into `test_gate: after_approval` only when the user explicitly requests the historical stop-before-tests behavior.

After implementation, execute configured project tools for stages `post_implementation` and `pre_review`.
For each tool:
1. Check execution conditions and `safe_to_run`.
2. Run it via the specified `type` (`command`, `skill`, or `mcp`).
3. Record command/link, result, and brief evidence in `Project tool history`.
4. If `required: true` or `failure_policy: block`, stop the lifecycle on error:
   - leave `status: in_progress`;
   - set `execution_state: blocked`;
   - add the issue to `Blockers`.
5. If `failure_policy: warn`, continue but include the warning in review context and final report.
6. Do not run automatically if `safe_to_run: false`, production access/deployment is needed, or credentials are missing.

### Stage 3 — Task Review

The canonical lifecycle always uses `review_execution.mode: subagent_required`.
Create a fresh, read-only review subagent for the task-review run. Never
replace this with self-review in the current chat, regardless of task priority
or complexity. If the platform cannot provide the required isolation, set
`execution_state: blocked` and stop the lifecycle.

Before spawning the subagent, generate the `git diff` for the task-owned files.
Explicitly instruct the subagent: "Run the task-review skill. Read the task
file and review the following diff: [insert diff here]. Return ONLY the final structured YAML report. Do NOT communicate
intermediate thoughts."

Check for:
- completion of all plan steps;
- goal achievement;
- passing of all acceptance criteria;
- no missing scenarios;
- implementation matching the scope;
- no unfinished stubs or TODOs.

#### Run Limit

Maximum two runs per task revision (`Run 1 → fixes → Run 2`). Track this counter only for `task-review`; do not reset or rerun it because `code-review` has findings. If it already passed and no task-level scope changed, preserve the pass.
If `Run 2` still has mandatory findings, do not continue, leave `in_progress`, set `execution_state: blocked`, and ask the user.

### Stage 4 — Code Review

After a successful `task-review`, you MUST reuse the SAME subagent session that just passed the `task-review`. Do not create a new subagent to save overhead, but do not perform the review yourself. Explicitly send a new message to the existing subagent: "Run the code-review skill. Review the same diff provided earlier, analyze
the changes, and return ONLY the final structured YAML report."

Check for correctness, security, architecture, maintainability, and compatibility.
Use the same `Run 1 → fixes → Run 2` limit, tracked independently from `task-review`. If it fails, fix the code, rerun affected tests, and rerun only `code-review`. Block if it fails twice.

### Stage 5 — Transition to Review and User Report

Only after both reviews pass:
1. Run `task-manager`.
2. Set `status: review`, `execution_state: waiting_approval`, `Approval.Requested: yes`.
3. Stop execution and wait for explicit user approval. Provide a report of changes, reviews, and limitations.

### Stage 6 — Processing User Decision

Consider approval only for explicit messages like `approve`, `approved`, etc.
Upon approval, run `task-manager`, set `status: approved`, and rerun only tests invalidated by changes after the pre-review gate. For `test_gate: after_approval`, run the full configured test gate now.
If user requests changes, revert to `in_progress`, increment `Revision`, reset counters, and repeat implementation/review.

### Stage 7 — Advanced Test Creation and Coverage

Run `create-test` to evaluate applicability of advanced integration tests, or add missing unit tests.
Tests must be executed as part of the default pre-review gate, with a final
post-approval rerun only when approval or late changes invalidate evidence.
Use `limits.test_fix_attempts` for the maximum fix attempts. Coverage is governed by `quality.coverage_policy`:
`configured_only` (recommended) enforces the threshold only when
`commands.coverage` describes an executable command, scope, and threshold;
when coverage is absent or insufficiently described, record
`not_configured` with a reason and continue without claiming a percentage.
`required` blocks on missing or unresolved coverage. Never claim coverage
passed from a static assumption. After tests, run `post_tests` project tools.

The orchestrator may execute `create-test`, `doc-sync`, and `task-manager` in its own context or via a normal delegated role; only the two mandatory review skills require isolated subagents.

### Stage 8 — Documentation Sync

Run `doc-sync` to update README, design docs, etc., or mark `not_applicable`.
Add a `Completed work` block to the task plan afterward.

### Stage 9 — Memory Sync

Update `memory.md` only with verified, useful long-term operational facts.
Before writing, check whether the fact is already documented in a higher-priority
source and avoid duplicating it. Task-specific test counts, review results,
approval evidence, coverage waivers, execution progress, work logs, and one-off
diagnostics remain in the task file or report and must not be copied to memory.
If a memory entry conflicts with code, configuration, official documentation, or
the task record, do not silently overwrite the higher-priority source; correct or
remove the stale memory entry instead.

### Stage 10 — Completion and Archiving

Run `pre_done` project tools.
Before marking the task as done, you MUST commit the task's changes to git (e.g., `git commit -am "TASK-XXXX: <title>"`). This prevents uncommitted work from stacking up and being accidentally lost.
Then run `task-manager` to validate completion evidence, set `status: done`,
add the final work log, append to `completed-tasks.md`, and remove the task from
the active store if configured.

## 9. Memory Rules

Use `.ai/memory.md` only for verified, stable project facts, non-obvious commands,
confirmed traps, and durable environment or tool notes. Treat memory as a derived
convenience layer, not as the source of truth.

Apply this source-priority order when information conflicts:

```text
code and configuration
→ official documentation
→ task files and review records
→ memory.md
```

Do not store secrets, tokens, passwords, cookies, private keys, personal data,
large logs, raw command output, task-specific test counts, review outcomes,
approval evidence, coverage waivers, temporary progress, or unverified
assumptions. Do not copy information that belongs in README, ADR, API
documentation, or the issue/task tracker.

During Memory Sync, remove or correct entries that are stale, contradicted, or
no longer useful. If no durable fact was discovered, leave `memory.md` unchanged.

## 10. Child Skill Contract

Each child skill returns:

```yaml
skill: task-review
result: passed | failed | blocked
summary: "Short summary"
findings:
  - severity: critical | high | medium | low | info
    category: completeness | correctness | security | architecture | maintainability | testing | docs
    location: "path/to/file:line"
    description: "What was found"
    required_action: "What needs fixing"
changed_files: []
artifacts: []
blocking_reasons: []
```

## 11. Single Skill Execution

Child skills can run individually but cannot transition a task through the full lifecycle on their own.

## 12. Mode Selection

Use Full-cycle mode for standard task execution. Use Single-skill mode if explicitly requested.

## 13. Resuming Between Sessions

Read state, continue from the first unfinished mandatory stage. Do not repeat successful stages or reset counters unnecessarily.

## 14. Cycle Protection

Strict adherence to max 2 runs per review. No fictitious revisions to bypass limits.

## 15. Final Report

Output a structured markdown report upon task completion.

## 16. Completion Criteria

Task is done ONLY IF all stages (plan, acceptance, both reviews, user approval, tests, coverage, docs, memory, archive) are fully met.
