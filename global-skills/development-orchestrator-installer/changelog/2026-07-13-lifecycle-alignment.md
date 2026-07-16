# Lifecycle alignment: review reruns, test gate, and conditional coverage

The installer source and templates now reflect the current development-orchestrator contract.

- Tests run immediately after implementation and before review by default; `test_gate: after_approval` is an explicit task-level exception.
- Review stages have independent counters and state. Only the failed review stage is rerun.
- Repeated reviews use a fresh subagent/context; completed contexts are never reused.
- `task-manager`, `create-test`, and `doc-sync` do not require isolated subagents.
- `quality.coverage_policy: configured_only` treats absent or insufficiently described coverage commands as `not_configured` instead of an automatic blocker.
- Task index integrity is checked through `sync_tasks.py --check`.
