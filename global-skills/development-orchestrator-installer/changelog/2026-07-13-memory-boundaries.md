# Memory boundary rules

## Changed

- Made `memory.md` explicitly a derived convenience layer rather than a source of truth.
- Added source-priority rules: code/configuration, official documentation, task/review records, then memory.
- Prohibited task-specific test counts, review outcomes, approval evidence, coverage waivers, work logs, raw logs, one-off diagnostics, and temporary progress in memory.
- Required removal or correction of stale or contradictory memory entries.
- Allowed leaving `memory.md` unchanged when no durable fact was discovered.

## Synchronization

The canonical orchestrator skill and the installer asset must remain byte-identical.
