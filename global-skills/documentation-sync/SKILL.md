---
name: documentation-sync
description: >
  Create, audit, and synchronize project documentation with changed code,
  contracts, or task results. Use for documentation updates, conflicting claims,
  duplicate contracts, broken links, or an explicitly scoped documentation
  migration. Preserve canonical ownership and distinguish proposals from facts.
---

# Documentation Synchronization

Keep documentation accurate, discoverable, and consistent with its sources.
Use the project's language, structure, and ownership rules; do not impose fixed
directories, external tools, or storage assumptions.

## Scope and mode

- **Create:** choose the document type and owner within the existing structure.
- **Sync:** update claims affected by the assigned code, contract, or task change.
- **Audit:** report inconsistencies and recommended actions without editing.
- **Migrate:** move or restructure only the documents within explicit scope,
  preserving content, history, and incoming links.

A request to audit and fix authorizes scoped corrections. An audit alone does
not authorize them. Do not delete documents without explicit authorization.
Read-only archives stay read-only; moving material to an archive requires the
project's policy and authority to change its structure.

## Workflow

1. **Identify the change source.** Use the named files, task, commit range, or
   request. If the working tree is the fallback, state it and distinguish
   unrelated changes. Record relevant status/diff before editing. Preserve
   existing work; pause only conflicting edits whose ownership cannot be
   resolved, continuing unaffected work.
2. **Read local rules and entry points.** Inspect applicable instructions, README
   or index, documentation policy, and archive rules. Inspect relevant interface
   contracts only when their documented behavior is affected.
3. **Map impact before editing.** For each changed claim identify evidence, its
   canonical owner, affected readers/documents, and a decision:
   `required`, `recommended`, or `not-needed`.
   Read [impact-audit](references/impact-audit.md) for larger or conflicting scopes.
   Do not edit files merely because they are near changed code.
4. **Resolve ownership and evidence.** Keep each normative topic in one canonical
   owner; derived summaries and guides link to it. Distinguish intended contracts,
   actual implementation, current status, and historical proposals. Code proves
   behavior, not that a conflicting intended contract has been superseded. If
   project rules and evidence do not settle a material conflict, record it and
   ask the owner; do not choose silently.
5. **Make minimal consistent changes.** Update affected claims, examples, commands,
   indexes, and incoming links together. Consolidate duplicates only after
   preserving their unique information. Keep design rationale, operational
   plans, current status, results, and archives in their existing owners.
   Read [documentation-model](references/documentation-model.md) when boundaries
   are unclear or consolidation is needed.
6. **Validate the affected scope.** Check links and anchors, examples against
   current interfaces, terminology, formatting, and project-required checks.
   Read [quality-checks](references/quality-checks.md) for the relevant checks.
   Do not execute publishing or destructive commands merely to validate examples.
7. **Report the result.** State changed documents and reasons, canonical owners,
   checks actually run, and unresolved conflicts. For audit-only work, return the
   impact map and prioritized actions. Omit empty sections and repeated evidence.

Stop when affected claims and links agree with their identified sources and
required checks are complete or their limitations are reported. Unrelated
inconsistencies can be noted without expanding the assignment.

## Evidence and completion

Keep design rationale, planned work, and verified results distinguishable.
Link to existing requirements and plans rather than copying their full contents.
Documentation corrections do not by themselves complete the work they describe.
A status snapshot must identify its evidence and date/revision; do not turn
historical reports or future plans into claims of current implementation.

Use the repository and supplied evidence directly. No external service or
tracking system is required, and do not create one for documentation sync.

Commit, publish, or change other repositories only when the request includes
those actions; ordinary documentation sync does not imply them.
