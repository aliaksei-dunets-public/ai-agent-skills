# Changelog: 2026-07-12

## Orchestrator Workflow Updates

The `development-orchestrator`, its child skills, and the installer have been updated to align with the following improvements:

### 1. Stage 2.5: Basic Testing
- **development-orchestrator**: Updated Stage 2.5 to explicitly instruct the agent to run basic unit tests and quick verification tests *before* moving the task to review.
- **development-orchestrator-installer**: Reflected the new Stage 2.5 in the documented lifecycle graphs (`USER-GUIDE.md` & `USER-GUIDE.ru.md`).

### 2. Strict Subagent Prompts
- **task-review** & **code-review**: Added strict instructions in the `Result contract` section prohibiting conversational filler, thinking aloud, or introductory text, enforcing YAML-only output.
- **development-orchestrator**: Added explicit subagent prompts for Stages 3 and 4 to enforce the strict isolated function behavior.
- **task-review**: Added a verification boundary check to ensure basic tests were executed during Stage 2.5.

### 3. YAML Frontmatter for Task States
- **task-manager**: Rewrote the `Task contract` section to explicitly mandate reading and writing technical states (`status`, `execution_state`, `type`, `priority`, etc.) via YAML frontmatter blocks rather than markdown lists.
- **development-orchestrator-installer**: Converted the installer's active task template (`templates/tasks.md`) to use standard YAML frontmatter for technical state tracking.

### 4. Installer Assets and Consistency
- **development-orchestrator-installer**: Copied the updated orchestrator skill into the installer's `assets/` directory (`development-orchestrator-SKILL.md`) so that future project installations will inherit these improvements.
- **development-orchestrator-installer**: Updated the installer's invariants list in `SKILL.md` to capture the YAML frontmatter requirement, the Stage 2.5 testing rule, and the strict subagent rules.

### 5. Added
- **Mandatory Review Isolation**: Standardized every lifecycle review on a fresh, read-only subagent. Self-review is not a supported fallback.
- **Automated Task Indexing**: Introduced a Python script (`sync_tasks.py`) that automatically parses task metadata to generate the markdown task indexes, replacing fragile text manipulation.

### 6. Changed
- **Task Metadata Contract**: Task state remains in strict YAML frontmatter at the top of `TASK-XXXX.md`; the indexer rejects missing or unknown fields.
- **Task Utility Safety**: State updates validate lifecycle transitions, use atomic writes, return failures to callers, and never stage or commit Git changes.
- **Optional Agentic E2E Testing**: E2E testing via browser subagents is required when applicable and must otherwise be recorded as `not_applicable` with a reason.
