# User Guide: Development Orchestrator and Installer

## 1. Purpose

The package contains two related skills:

- **`development-orchestrator-installer`** — audits a project, finds existing instructions, skills, documentation, task management, and quality commands, then installs or upgrades the orchestrator using the project context.
- **`development-orchestrator`** — executes a development task through the mandatory lifecycle, invokes child skills, and manages task states.

Recommended usage model:

```text
Installer configures the system.
Orchestrator executes tasks.
Child skills perform only their specialized responsibilities.
```

Do not use the Installer to implement product functionality, and do not use the Orchestrator to redesign its own architecture.

---

## 2. Standard Task Lifecycle

Version `development-orchestrator` 1.2.0 uses the following lifecycle:

```text
created
  ↓
in_progress
  ↓
basic testing and project tools
  ↓
task-review by a dedicated subagent
  ↓
code-review by another subagent
  ↓
review
  ↓
explicit user approval
  ↓
approved
  ↓
test creation and execution
  ↓
coverage verification
  ↓
post-test project tools
  ↓
doc-sync
  ↓
memory sync
  ↓
archiving
  ↓
done
```

Primary task statuses:

| Status | Meaning |
|---|---|
| `created` | The task exists but has not yet been started |
| `in_progress` | The agent is implementing the plan or fixing findings |
| `review` | Implementation passed `task-review` and `code-review` and is waiting for the user |
| `approved` | The user approved the implementation; testing and documentation are in progress |
| `done` | All mandatory stages are complete and the task has been archived |

A separate field tracks technical execution state:

```text
ready | running | waiting_approval | blocked
```

`Status` represents the business stage. `Execution state` represents the current runtime condition.

---

## 3. When to Use the Installer

Use `development-orchestrator-installer` when:

- the orchestrator is being added to a repository for the first time;
- the project already has skills that must be mapped to orchestrator roles;
- the project structure, test pipeline, documentation, or task management changed;
- the `development-orchestrator` version changed;
- part of the installation was removed or damaged;
- compatibility must be checked without changing files.

The Installer supports four modes:

| Mode | Purpose |
|---|---|
| `audit` | Analyze only; do not modify the project |
| `install` | Perform the initial installation |
| `upgrade` | Upgrade an installed version while preserving project settings |
| `repair` | Restore an incomplete or inconsistent installation |

### Recommended First Run

```text
Use development-orchestrator-installer in audit mode.
Analyze the project, existing skills, instructions, documentation,
task management, tests, coverage, and CI. Do not modify files.
Produce a capability matrix, conflict list, and installation plan.
```

After reviewing the report:

```text
Use development-orchestrator-installer in install mode.
Apply the prepared installation plan. Back up affected files, install the
orchestrator, configure adapters, and run validation and a dry run.
Do not modify production code.
```

### What the User Must Verify After Installation

Installation is not fully operational until the following are confirmed:

- the active-task path;
- the completed-task archive path;
- the `memory.md` path;
- mappings for all five mandatory roles;
- a mechanism for launching independent `task-review` and `code-review` subagents;
- fresh context and read-only access for review subagents;
- an inventory of additional project tools and their hook mapping;
- real build, validation, and test commands;
- the coverage command, or an explicit `coverage_policy: configured_only` result when coverage is not configured;
- canonical documentation sources;
- successful structural and contract validation;
- a successful dry run, or an explicitly justified `static-only` dry run.

`installed_but_blocked` means files may be installed, but the full lifecycle cannot yet be executed safely.

---

## 4. When to Use Development Orchestrator

Use `development-orchestrator` when a task must be completed end to end, from selection through archiving.

### Start a Specific Task

```text
Use development-orchestrator to execute TASK-0123 through the full lifecycle.
Follow the project configuration. Stop after moving the task to review and
request my explicit approval before testing.
```

### Select the Next Task Automatically

```text
Use development-orchestrator. Select the next available task with status
created according to orchestrator.config.yaml and execute the mandatory process.
```

### Resume an Interrupted Task

```text
Resume TASK-0123 through development-orchestrator from its saved stage.
First inspect the task file, review history, approval, test results, and work log.
Do not repeat already completed stages without a reason.
```

### Approve an Implementation

At the `review` stage, the user must give unambiguous approval:

```text
approve TASK-0123
```

or:

```text
I approve the changes for TASK-0123. Continue with testing,
documentation synchronization, and task completion.
```

Messages such as “okay,” “understood,” or “I will review later” must not be treated as approval.

### Request Changes Instead of Approval

```text
I do not approve TASK-0123. Fix error handling for an empty API response,
update the plan, and create a new task revision.
```

The task returns to `in_progress`, the revision number increases, and review counters restart for the new revision.

---

## 5. Using Child Skills Separately

Mandatory child roles:

- `task-manager`;
- `task-review`;
- `code-review`;
- `create-test`;
- `doc-sync`.

Each skill may also be executed independently. This is useful for local checks, diagnostics, or one-off operations.

Example:

```text
Run code-review only for the changes in TASK-0123.
Do not change the task status and do not continue the full lifecycle.
Return a structured result with severity, location, and required_action.
```

Running a child skill separately does **not** automatically satisfy the corresponding full-cycle stage. To accept the result, the Orchestrator must:

1. associate it with a specific task and revision;
2. validate the result format;
3. record it in task history;
4. confirm that the latest version of the changes was reviewed.

Child skills must not independently:

- move the task between primary statuses;
- declare the full lifecycle complete;
- bypass approval;
- archive the task outside Orchestrator control.

### Review Subagents

The canonical Orchestrator always uses `review_execution.mode: subagent_required`.
There are no fast-track or current-chat self-review exceptions. Every
`task-review` and `code-review` run must use a separate fresh-context,
read-only subagent.

Required flow:

```text
Main agent implements the task
→ a new task-review subagent checks the plan and acceptance criteria
→ the main agent fixes findings
→ if needed, a new task-review subagent performs the second run
→ a new code-review subagent reviews the code
→ the main agent fixes findings
→ if needed, a new code-review subagent performs the second run
```

Requirements for isolated subagents:
- every review run receives fresh isolated context;
- `task-review` and `code-review` use different subagents;
- review subagents are read-only by default;
- review subagents do not change task status and do not fix code;
- each review type may run at most twice per task revision.

### Automated Task Sync

Task metadata is stored in YAML frontmatter within the `TASK-XXXX.md` files. After any state changes, the Orchestrator runs `python .ai/scripts/sync_tasks.py` to automatically regenerate the `tasks.md` index files.

If the platform does not support the required subagents, the full lifecycle
must remain `installed_but_blocked` or the task must become `blocked`. The main
agent must not silently replace the required subagent.

For a standalone review, use wording such as:

```text
Launch a separate code-review subagent with fresh context for TASK-0123.
Provide the task, acceptance criteria, diff, and project rules.
Disallow file changes and task-status changes. Return a structured review result.
```

---

## 6. Project Configuration

Primary configuration file:

```text
.ai/orchestrator.config.yaml
```

Recommended project context index:

```text
.ai/orchestrator.project.md
```

### Settings Usually Managed Through Configuration

| Area | Examples |
|---|---|
| Paths | task file, archive, `memory.md`, project context |
| Integrations | skill names and paths, native/adapter mapping |
| Review execution | subagent launcher, reviewer profiles, isolation, write access |
| Project tools | diagnostics, health checks, and other hooks with stage and failure policy |
| Project profile | languages, frameworks, source/test/docs roots |
| Commands | build, lint, typecheck, test, coverage, documentation checks |
| Task selection | priority, dependencies, selection strategy |
| Archive | whether to remove completed tasks from the active file and preserve full history |
| Context | always-loaded and on-demand documents |
| Quality | coverage threshold and scope, provided project policy is not weakened |

After manually changing the configuration, run:

```text
Use development-orchestrator-installer in repair mode.
Validate the modified orchestrator.config.yaml, references, skill mapping,
contracts, and dry run. Preserve valid manual settings.
```

### Integrating Diagnostics, Health Checks, and Other Tools

The Installer should discover additional project tools and propose Orchestrator integration. Tools are connected only after classification.

Supported decisions:

| Decision | Use case |
|---|---|
| `integrate-required` | Safe mandatory check; failure blocks the lifecycle |
| `integrate-optional` | Useful check; failure is recorded as a warning |
| `on-demand` | Diagnostic runs only when needed or explicitly requested |
| `manual-only` | Requires credentials, an external service, or user action |
| `excluded` | Destructive, performs deployment, or changes production data |
| `unresolved` | Not enough information for safe integration |

Supported hook stages:

- `on_demand` — during implementation for diagnostics;
- `post_implementation` — immediately after code changes;
- `pre_review` — mandatory gate before review subagents;
- `post_tests` — after the main test pipeline;
- `pre_done` — final project gate before completion.

Example:

```yaml
project_tools:
  - id: "project-health-check"
    type: "command"
    ref: "scripts/health-check.sh"
    stage: "pre_review"
    required: true
    safe_to_run: true
    failure_policy: "block"
    conditions: []
```

The Installer must not enable a tool merely because it found a similarly named file. It must confirm the entry point, safety, lifecycle stage, and failure policy.

After adding a new tool to the project, run:

```text
Use development-orchestrator-installer in upgrade mode.
Audit project tools again, find new diagnostics and health checks,
propose hook mapping, update the config, and perform a dry run.
Do not run destructive, deployment, or production-data tools.
```

### What Must Not Be Stored in Configuration

Do not store the following in `orchestrator.config.yaml`:

- long coding standards;
- full architecture documentation;
- large API specifications;
- secrets or tokens;
- detailed child-skill instructions;
- temporary progress for a specific task.

Configuration should reference canonical documents rather than duplicate them.

---

## 7. How to Change the Development Process Correctly

### 7.1 Classify the Change First

Changes fall into three levels.

#### Level A — Parameter Configuration

The lifecycle remains unchanged; only parameters change:

- paths;
- commands;
- source/test/docs roots;
- skill mapping;
- task selection;
- coverage threshold;
- test-fix retry count;
- archiving;
- context loading.

Make these changes in `orchestrator.config.yaml`, then validate them in `repair` mode.

#### Level B — Project Adaptation

The lifecycle remains unchanged, but the project needs additional actions:

- security scan;
- database migration check;
- performance benchmark;
- SAP activation/check;
- mobile build;
- a dedicated architecture review;
- multiple test runners;
- an external issue tracker.

Correct procedure:

1. create or connect a specialized skill, command, or MCP tool;
2. classify it as required, optional, on-demand, manual-only, or excluded;
3. define its hook stage and failure policy;
4. add a `project_tools` mapping or a thin adapter;
5. preserve the common state machine;
6. update project context and the installation report;
7. run `repair` or `upgrade` and perform a dry run.

For example, a safe health check may become a required `pre_review` gate, while expensive diagnostics may remain `on_demand` without introducing a new business status.

#### Level C — Lifecycle Change

This includes:

- changing the order of stages;
- adding or removing a mandatory approval gate;
- moving testing before user approval;
- introducing new primary statuses;
- removing `task-review` or `code-review`;
- changing the two-review limit;
- removing independent review subagents;
- allowing automatic approval;
- changing the definition of `done`;
- using a different archival model.

This is **not ordinary configuration**. In version 1.2.0 these rules are protected invariants.

A lifecycle change must be released as a new process version.

### 7.2 Lifecycle Change Procedure

#### Step 1 — Create a Process Change Proposal

Use this template:

```markdown
# Process Change Proposal: PCP-XXXX

## Reason for Change

Why the current process does not fit the project.

## Current Process

Current sequence of stages and statuses.

## Proposed Process

New sequence of stages and statuses.

## Scope

Project-specific process or a new shared skill version.

## State Machine Changes

- added statuses;
- removed statuses;
- new transitions;
- forbidden transitions.

## Gates

For each stage:

- entry condition;
- mandatory actions;
- success condition;
- failure behavior;
- retry limits;
- required artifacts.

## Active Task Migration

How existing and in-progress tasks will be handled.

## Compatibility

Which skills, adapters, task formats, and platform instructions change.

## Validation

Which scenarios the dry run must verify.

## Rollback

How to restore the previous process version.

## Approval

Who approved the process change and when.
```

#### Step 2 — Define the Change Scope

- **One project only:** create a project-specific process version or profile and record the deviation explicitly.
- **All projects:** update the canonical `development-orchestrator` and the Installer asset.

Do not modify only the installed local copy when the change must be portable. A future installation or upgrade would overwrite the local change.

#### Step 3 — Assign a New Version

Recommended versioning:

| Change | Version |
|---|---|
| Text correction without behavior change | Patch: `1.1.0 → 1.1.1` |
| New optional compatible hook or capability | Minor: `1.1.0 → 1.2.0` |
| Statuses, stage order, approval, mandatory gates | Major: `1.x → 2.0.0` |

#### Step 4 — Update All Related Contracts

For a lifecycle change, review and update together:

- canonical `development-orchestrator/SKILL.md`;
- the copy under `installer/assets/`;
- Installer invariants and contract validation;
- the `orchestrator.config.yaml` template;
- task schema and task template;
- adapters;
- state transition rules;
- installation manifest format, if needed;
- user guides;
- dry-run scenarios;
- migration rules for active tasks.

#### Step 5 — Do Not Silently Change an Active Task

For tasks in `in_progress`, `review`, or `approved`, choose one option:

1. finish the task under the old process version;
2. explicitly migrate it to the new version;
3. return it to a safe state and create a new revision.

Recommended task metadata:

```text
Process version: 1.1.0
```

After migration:

```text
Process version: 2.0.0
Migration: PCP-XXXX
```

#### Step 6 — Run Audit and Upgrade

```text
Use development-orchestrator-installer in audit mode.
Review Process Change Proposal PCP-XXXX, the new orchestrator version,
updated contracts, task schema, adapters, and migration rules.
Do not modify the project.
```

After accepting the report:

```text
Use development-orchestrator-installer in upgrade mode.
Apply process version 2.0.0 according to PCP-XXXX. Create a backup,
migrate only approved files, and run structural validation,
contract validation, and dry runs for all new transitions.
```

#### Step 7 — Validate Dry-Run Scenarios

At minimum, verify:

- normal full-cycle completion;
- findings in the first review followed by a successful rerun;
- findings in the second review followed by blocking;
- user-requested changes;
- approval;
- failed tests;
- unreachable coverage threshold under `coverage_policy: required`, and `not_configured` coverage under `configured_only`;
- a `not_applicable` test type;
- `doc-sync` failure;
- recovery after an interrupted session;
- archiving;
- migration of an active task from an older process version.

### 7.3 What Not to Do When Changing the Process

Do not:

- add a conflicting instruction only to `AGENTS.md` or `CLAUDE.md`;
- change statuses manually without updating state-transition rules;
- bypass review through a standalone skill invocation;
- create a new revision only to evade the review limit;
- modify installed `SKILL.md` without updating the Installer canonical source;
- weaken a quality gate without an explicit process-owner decision;
- combine a lifecycle change with implementation of a product task;
- migrate active tasks without recording the process version;
- declare an upgrade successful without a dry run and rollback plan.

---

## 8. Configuring Child Skills

The Installer must map existing skills to the five mandatory roles.

### Native Integration

Use native integration when an existing skill already:

- performs the required responsibility;
- accepts sufficient context;
- returns a structured result;
- does not manage another component’s lifecycle stages;
- does not conflict with Orchestrator policy.

### Adapter Integration

An adapter is required when an existing skill is useful but:

- has a different name;
- uses a different input or output format;
- returns unstructured prose;
- combines several roles;
- changes task status by itself;
- uses incompatible severity or status values.

An adapter transforms the contract. It must not duplicate knowledge from the source skill.

### Unresolved Integration

If a mandatory role is missing or incompatible, the Installer must leave it `unresolved` and must not declare the system operational.

Recommended command:

```text
Use development-orchestrator-installer in repair mode.
Re-check capability mapping for mandatory skills. Propose minimal adapters
for incompatible skills. Do not rewrite the source skills.
```

---

## 9. Rules for memory.md

`memory.md` is long-term operational memory for the agent, not project documentation.

Appropriate entries:

- non-obvious working commands;
- stable local-environment specifics;
- confirmed project traps;
- tool quirks;
- internal operating conventions;
- reasons for decisions that do not belong in formal project documentation.

Do not record:

- secrets;
- personal data;
- a complete task history;
- unverified assumptions;
- information that belongs in README, ADR, API docs, or the issue tracker;
- temporary progress for the current task.

Use this source-priority order when sources conflict:

```text
code and configuration
→ official documentation
→ task files
→ memory.md
```

Review `memory.md` periodically and remove stale entries.

---

## 10. Upgrade, Repair, and Rollback

### Upgrade

Use after updating the canonical skill or process:

```text
Use development-orchestrator-installer in upgrade mode.
Preserve manual settings, generated sections, and project-specific adapters.
Show the diff, create a backup, update the core, then run validation and a dry run.
```

### Repair

Use after changing configuration or project structure, or after detecting inconsistency:

```text
Use development-orchestrator-installer in repair mode.
Compare the manifest with actual files and restore only missing or inconsistent
managed components. Do not remove unknown files.
```

### Rollback

Rollback must use the installation manifest and session backup.

```text
Roll back the latest development-orchestrator installation.
First show the files that will be restored or removed.
Do not overwrite files modified by the user after installation without a diff and warning.
```

---

## 11. Common Problems

| Problem | Correct action |
|---|---|
| `task-manager` not found | Keep the mapping `unresolved`; create a contract or scaffold only with user permission |
| Existing code-review changes task status | Create an adapter that blocks lifecycle side effects |
| Platform does not support subagents | Keep the full lifecycle `blocked`; configure a platform launcher or use a supported environment |
| A health check was found but safety is unclear | Keep it `unresolved` or `manual-only`; do not run automatically |
| A required project tool fails | Stop the transition at that stage and record evidence in the task |
| Test command is unknown | Record `unresolved`; do not invent a command |
| Project has no UI | Mark UI tests `not_applicable` with project-profile evidence |
| Coverage is below threshold | Fix tests/code or block and request a decision; do not lower automatically |
| Second review fails again | Stop the task in `in_progress/blocked` |
| User did not provide explicit approval | Keep `review/waiting_approval` |
| Tests required a substantial production-code change | Re-run available code-review; block if the review limit is exhausted |
| Documentation is not required | Use `not_applicable` with a concrete reason |
| Task tracker is external | Use an integration or adapter; do not create a parallel backlog |
| Project process differs from 1.1.0 | Create a Process Change Proposal and release a new process version |

---

## 12. Recommended Ownership

For a team project, assign a process owner responsible for:

- the canonical orchestrator;
- the Installer asset;
- lifecycle versioning;
- task schema;
- mandatory quality gates;
- adapters;
- guide updates;
- approval of Process Change Proposals.

The project team may change commands, paths, and integration mappings through configuration. Lifecycle changes require separate review and approval.

---

## 13. Quick Working Scenarios

### Initial Installation

```text
1. Installer audit
2. Review the report
3. Installer install
4. Validation and dry run
5. Verify operational status
```

### Execute a Task

```text
1. Create a task with status created
2. Run development-orchestrator
3. Orchestrator runs project tools and two independent review subagents
4. Review the report at status review
5. Approve or request changes
6. Orchestrator creates and runs tests and post-test tools
7. Orchestrator updates documentation and memory
8. Task becomes done and moves to the completed archive
```

### Change Settings

```text
1. Edit orchestrator.config.yaml
2. Run Installer repair
3. Validate and perform a dry run
```

### Change the Process

```text
1. Create a Process Change Proposal
2. Release a new process version
3. Update Orchestrator and Installer together
4. Define active-task migration
5. Run Installer audit
6. Run Installer upgrade
7. Validate dry run and rollback
```

---

## Current Lifecycle Clarifications

- The default test gate runs immediately after implementation and before review. The documented “stop before testing” prompt is an explicit per-task exception and maps to `test_gate: after_approval`.
- Review state is tracked independently per stage. If `task-review` passed and `code-review` failed, rerun only `code-review`.
- Every repeated review uses a new isolated agent/context. A configured profile may be reused, but a completed subagent context may not be reused.
- `create-test`, `doc-sync`, and `task-manager` may run in the orchestrator context or through ordinary delegation. Isolated subagents are mandatory only for `task-review` and `code-review`.
- With `quality.coverage_policy: configured_only`, coverage is enforced only when `commands.coverage` contains an executable command, scope, and threshold. Otherwise record `not_configured` with a reason.
- `sync_tasks.py --check` must pass after installation and detects stale generated indexes.
- Before implementation, capture the pre-existing Git working-tree state and define the task-owned file scope; unrelated dirty-worktree changes must remain outside review findings.

---

## 14. Core Rule

Use configuration to change **project parameters**, adapters to change **interfaces of existing skills**, and a new Orchestrator and Installer version to change **the development process itself**.
