# Initial, Full, and Project Scopes

Read for initial/full or project scope.

## Initial / full

"Initial audit" or "check the entire project" selects initial/full even with no
changes. Inventory all components, tracked and non-ignored untracked files, and
release-relevant material; cover each component's source, secrets, resolved
dependencies, configuration, trust and publication boundaries. Record unsupported,
unreadable, sampled, skipped, or unfinished areas as coverage gaps. Do not create
a suppression baseline or describe a partial audit as exhaustive. No implicit
history or index audit.

## Project

Audit the current project (as initial/full) and separately assess staged changes
when any exist. Report the project gate and the staged-change gate (N/A if the
index is empty); overall status equals the worse applicable result. Narrow
reviews have only their requested gate.

## Without Git

Initial/full/project can operate without Git; disclose missing change
attribution, not a false code-review failure.
