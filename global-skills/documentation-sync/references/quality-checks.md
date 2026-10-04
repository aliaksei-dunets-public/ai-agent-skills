# Documentation Checks

Select checks by the affected claims and project requirements. Report execution
accurately: an inspected example or scenario walkthrough is not a command run.

- Resolve changed relative links, incoming links, and anchors. Check path case,
  renamed documents, indexes, and discovery wrappers.
- After migration, search the affected scope for old paths and terminology.
- Match changed API, schema, CLI, configuration, and examples against current
  contracts and implementation; label unresolved disagreements.
- Check canonical ownership and whether derived summaries retain source links.
- Run available documentation linters/builds and relevant project checks. Inspect
  side effects before running examples; publication and deletion need their own
  authorization.
- Check UTF-8, balanced code fences, and `git diff --check` or an equivalent.
- For operational instructions, verify prerequisites, expected results, failure
  signals, and recovery where relevant.
- Recheck affected claims without editing: the same evidence should require no
  further content changes. Do not rewrite timestamps or hashes on a no-op sync.

Freshness follows facts, not file dates. Removed interfaces, broken paths,
contradictory contracts, or impossible commands are evidence of a stale claim.
Old modification dates alone are not.

Report meaningful check results and skipped required checks with their reason.
Do not create generic tests that merely match documentation wording.
