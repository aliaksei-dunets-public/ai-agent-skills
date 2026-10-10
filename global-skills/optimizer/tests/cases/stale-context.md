# Case: Stale Context Reused as Authority

Mode: standard

A coding agent stores a repository summary in shared memory once, three weeks
ago. Every new task loads that summary instead of the current files and treats
it as the source of truth. Since then, the build tool, test command, and two
module boundaries changed. The summary has no timestamp, source pointers, or
invalidation rule.
