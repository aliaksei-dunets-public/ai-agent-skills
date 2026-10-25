# Discovery and Audit Checklist

## Launching the application

- Find the dev or preview command in `package.json`, the README or project
  instructions; prefer the project profile when it names one.
- Run it in the background and point logs to `.tmp/logs/`.
- For pages behind sign-in, use test credentials from the user or the
  project's seed, fixture or example config. Never use real accounts.
- If the application cannot start, document the reason and audit from source.

## Architecture discovery

- React version and framework (Vite, Next.js, CRA, Remix, ...).
- Routing solution and the full route list, including nested and guarded routes.
- Layout components and the app shell.
- UI libraries, state management, CSS architecture.
- Design tokens and themes.
- Shared components and duplicated components.
- Responsive implementation and existing accessibility patterns.

## Page inventory

For each page record: route, purpose, main user actions, components used,
navigation dependencies, forms and interactions, data density, complexity,
UX problems, potential improvements, and audit source (`browser`,
`source only`, `not audited` with the reason). Group pages into functional
areas. Do not limit the inventory to screenshots supplied earlier.

## Audit areas

**Navigation**: information architecture, sidebar organization, hierarchy,
active page indication, breadcrumbs, contextual navigation, discoverability,
search and quick access, mobile navigation, unnecessary steps.

**Visual hierarchy**: primary versus secondary information, density,
typography consistency, proportions, spacing and alignment, decorative
elements, redundant information, use of empty space.

**Interactions**: forms, filters, search, tables, sorting, selection, dialogs
and drawers, inline editing, feedback, confirmation and error handling.

**States**: loading, empty data, zero values, errors, success notifications,
disabled controls, missing permissions.

**Accessibility**: WCAG 2.2 AA — keyboard navigation, focus order and
visibility, contrast, labels and names, semantic structure, target size.

**Responsive behavior**: layout at desktop, tablet and mobile widths; overflow,
tables on small screens, touch targets.

**Domain checks**: apply the checks of the project profile's domain section
(for example currency, precision, dates and data freshness for financial
applications). Without a profile, check consistency of number, date and unit
formatting.

## Issue format

Each issue in `03-ux-ui-audit.md`:

| Field | Content |
|---|---|
| ID | `UX-001`, ... |
| Page / route | |
| React component | file path |
| Problem | |
| Evidence | screenshot path, DOM or source reference, measured value |
| Severity | P0 / P1 / P2 |
| Recommendation | |
| Expected UX impact | |

Severity:

- **P0**: blocks a task, loses or misrepresents data, or fails a WCAG A/AA
  criterion on a core flow.
- **P1**: significant friction, inconsistency or extra steps in frequent tasks.
- **P2**: polish, minor inconsistency, low-frequency friction.

## Quick wins

`10-quick-wins.md` lists low-risk, high-impact fixes from the audit that do not
depend on the chosen concept (labels, contrast, focus, formatting, empty
states), each linked to its issue ID. They are proposals, not changes.
