# Task approval state and dirty-worktree scope

- `update_task.py --approve` now updates canonical `Approved`, `Approved by`, and `Approved at` fields instead of appending contradictory evidence.
- The orchestrator records a pre-task working-tree baseline and passes only task-owned changes to mandatory review subagents.
- Task-specific test counts and temporary evidence do not belong in `.ai/memory.md`; memory stores stable operational facts only.
