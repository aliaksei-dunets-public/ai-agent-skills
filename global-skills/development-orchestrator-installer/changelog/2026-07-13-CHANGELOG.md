# Changelog

All notable changes to the Development Orchestrator and Installer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-07-13

### Added
- **Mandatory Review Isolation**: Every lifecycle review uses a fresh, read-only subagent; self-review is not an allowed fallback.
- **Automated Task Indexing**: Introduced a Python script (`sync_tasks.py`) that automatically parses task metadata to generate the markdown task indexes.
- **Task State Automation**: Added `update_task.py` utility to validate YAML frontmatter transitions, update log entries atomically, and synchronize indexes without Git side effects.

### Changed
- **Subagent Execution Logic**: Delegated `git diff` generation and context gathering directly to review subagents. Subagents are now instructed to generate unified diffs independently, reducing orchestrator cognitive load and token context limits.
- **Actionable Review Findings**: Review subagents now must output copy-pasteable code snippets or unified git diffs in the `required_action` field to accelerate fixes by the orchestrating agent.
- **Task Metadata Format**: Task state management is maintained as YAML frontmatter embedded directly inside `TASK-XXXX.md` files. This keeps metadata tightly coupled with the task content while avoiding Git merge conflicts. The `sync_tasks.py` script parses this frontmatter.
- **Optional Agentic E2E Testing**: E2E testing via browser subagents is no longer strictly mandatory for every task. It is now only required for tasks that significantly alter complex UI workflows, otherwise falling back to standard unit/integration tests.
