# Architecture, Design System, Concepts and Mockups

## Navigation architecture (phase 3)

Produce at least two alternatives. Consider the app shell, sidebar grouping,
section grouping, workspace switching where it fits, responsive navigation,
global search, contextual actions, page templates, and consistent filtering and
table behavior. For each alternative show the structure (tree or diagram), the
mapping of every existing route, and trade-offs. Identify UX patterns reused
across modules. Never drop a route or function; mark merged or relocated ones.

## Design system (phase 4)

Cover: color and semantic status tokens, typography, spacing, layout grid,
density, buttons, inputs and forms, tables and lists, search and filtering,
navigation, cards and charts, dialogs and drawers, empty/loading/error states,
breakpoints, accessibility, light and dark mode when relevant.

For each existing shared component decide `reuse`, `improve`, `consolidate` or
`replace`, with the path. Document token names and component API conventions
(props naming, variants, sizes, composition). Do not propose migrating to a
different UI framework unless the audit shows the current one blocks the goals.

## Concepts (phase 6)

The references are visual directions, not framework replacements. All three
concepts implement the same functions, data and navigation architecture.

| Concept | Reference | Direction |
|---|---|---|
| A — KokonutUI | https://v0.app/templates/financial-dashboard-6UhtTqtAVaZ | Minimalist: simple hierarchy, clean surfaces, reduced complexity |
| B — Shadcn Admin | https://github.com/satnaing/shadcn-admin | Productivity: structured navigation, clear data presentation, consistent components |
| C — TailAdmin | https://github.com/TailAdmin/free-react-tailwind-admin-dashboard | Feature-rich: complex workflows, analytics, data-heavy screens |

If a reference cannot be opened, state that it was not verified. Use only the
direction described in the table or supplied evidence; do not invent details
of the inaccessible reference.

## Mockup matrix

| Concept | Page 1 | Page 2 |
|---|---|---|
| A — KokonutUI | A1 | A2 |
| B — Shadcn Admin | B1 | B2 |
| C — TailAdmin | C1 | C2 |

Six mockups; each at desktop 1440 × 900 and mobile 390 × 844: at least twelve
visual representations.

Each mockup shows the complete page layout, global navigation, main user
actions, realistic components, and consistent synthetic data that matches the
page's real function. Where the tool supports it: reuse imported tokens, keep
components consistent across pages, add representative interactions or
navigation, and export images or prototype references.

## Preserving mockups

Under `docs/ux-audit/mockups/concept-<a|b|c>-<name>/` save per mockup:
desktop and mobile screenshots (`page-1-desktop.png`, `page-1-mobile.png`, ...),
exports, and a `README.md` with the design project and screen links, the
specification, and component mapping notes (mockup element → existing or
proposed React component). For hosted designs that cannot be exported, keep the
exact links and state the limitation.

## Comparison scorecard (phase 7)

Score each concept 1–5 per criterion and justify every score with observable
evidence from the mockups or specifications:

navigation clarity, cognitive load, visual simplicity, information density,
usability, number of required actions (count steps for the same scenarios),
accessibility, mobile experience, component consistency, integration
complexity, maintainability.

Recommend: best overall, best for frequent users, best for simplicity, and
patterns worth combining. Do not pick a winner on aesthetics alone.
