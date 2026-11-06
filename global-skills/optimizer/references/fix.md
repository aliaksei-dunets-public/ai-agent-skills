# Fix and Verify

Load in `fix` mode after the report described in `SKILL.md`. The checklist,
`technical-writing-ste` (its `edit` mode, for agent-facing text), and the
Repair principles and Audience and language sections in `SKILL.md` stay in
effect. Write each repair so that it passes the relevant checklist questions.

## Fix

1. Fix integrity defects exactly. Repoint a broken link only when the package
   identifies the target (for example, the same file name at a new path);
   otherwise follow the Repair principles in `SKILL.md`.
2. Resolve each contradiction to one rule. Where intent is clear from the
   rest of the package, choose it and state the choice. Otherwise, apply the
   interim rule from the Repair principles in `SKILL.md` when it applies;
   leave other contradictions unchanged and mark them as needing a decision.
3. Establish a canonical source for each shared rule, using the class and
   canonical-copy criteria in the checklist's Consistency section. Replace or
   remove a copy only if every affected executor can access and load the
   source before the rule is needed. Preserve consistent repetition required
   for independent execution, safety, or understanding without external
   context.
4. Rewrite ambiguous rules as concrete conditions and actions when the intended
   meaning is established. Otherwise retain the wording and report the ambiguity.
5. Move detail out of the entry point into references when it is needed only
   for some tasks, and add a clear pointer saying when to load it. Relocate
   misplaced content as the Repair principles in `SKILL.md` state.
6. Update every affected document within the requested scope in the same
   pass: guide/README, examples, and anything that names a changed file or
   option. Report affected consumers outside the scope as the Repair
   principles state. Update changelog and version metadata according to the
   package's existing release convention; do not introduce a versioning scheme
   solely for this edit. If the existing metadata already disagrees, follow the
   Repair principles.

Separate functional repairs from structural and language edits; edit text as
the Audience and language section in `SKILL.md` states. A functional repair
may change defective behavior when the requested scope and established intent
support it; explain that change as a repair, not as stylistic cleanup.

## Verify

Re-run integrity checks on the affected scope: links resolve, incoming paths
remain valid, new/moved resources are reachable, and names/versions agree.
Account for pre-existing unlinked files and deferred/unreadable areas instead
of claiming package-wide absence of defects. Re-read the changed files together
and confirm the fixes introduced no new contradiction or duplication.
For language edits (including translations) and structural edits, compare
conditions, requirement strength, permissions, exceptions, and action order with
the original.
