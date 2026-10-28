# UI Review Report Template

Return the report in chat. Write it to a file only when asked; in full mode
suggest `docs/ux-audit/11-post-implementation-audit.md`.

```text
UI review — <scope> — <verdict PASS | WARN | FAIL>

Scope:        <files / range / full>; routes: <list>
Snapshots:    <base and target; revision actually used for each runtime capture>
Contract:     <docs/ui/ path or "missing">
Runtime:      <app started: yes/no; viewports; tools used>
Not verified: <pages, states or checks skipped and why>
```

## Findings

| ID | Severity | Area | Location | Problem | Evidence | Fix |
|---|---|---|---|---|---|---|
| UR-001 | P0/P1/P2 | contract / states / a11y / responsive / content / logic | file:line or route | | screenshot path, rule cited | |

Severity follows the audit scale: P0 blocks a task, changes business behavior
outside the user's authorized scope, or fails WCAG A/AA on a core flow;
P1 significant friction or contract
violation; P2 polish.

## Docs drift

Entries `documentation-sync` must add, change or deprecate.

## Full mode

| Audit issue | Status | Evidence |
|---|---|---|

Then: new issues, roadmap acceptance results, validation scenario results,
and a short conclusion. Claim improvements only with evidence.
