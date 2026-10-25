# UI Review Checklist

Apply the items that the scope touches. Cite file and line or screenshot for
each finding.

## Contract conformance (`docs/ui/`)

- Tokens: no hard-coded colors, spacing, font sizes, radii or shadows where a
  token exists; semantic status tokens for statuses.
- Components: documented components reused; no near-duplicate of an existing
  component (use `reuse-auditor` when available for doubtful cases); props
  used as documented; no `deprecated` component in new code.
- Layout: page uses the matching page template and app-shell regions.
- Patterns: tables, filters, search, forms, dialogs and notifications follow
  `patterns.md`.

## States and feedback

Loading, empty, zero, error, success, disabled and missing-permission states
exist and match the patterns; destructive actions confirm; errors say what to
do next.

## Accessibility (WCAG 2.2 AA)

Keyboard reachability and order, visible focus, focus return after dialogs,
accessible names and labels, roles and landmarks, contrast, target size, no
information by color alone, reduced motion respected.

## Responsive behavior

Layout at 1440, 768 and 390 widths: no horizontal page scroll, tables usable on
mobile, navigation reachable, touch targets adequate.

## Content and domain

Terminology and formatting per `content.md` and the Domain profile; values,
totals and formats identical to the base version for the same data.

## Business-logic guard

Changes to calculations, rounding, data mapping, API requests, state stores,
routing guards or permissions inside UI work; removed functions, routes or
fields. Each is P0 unless the user's request explicitly covers it.

## Full mode extras

- Every issue from `03-ux-ui-audit.md`: `resolved`, `partly resolved`, `open`
  or `not verifiable`, with evidence.
- New issues introduced since the audit.
- Roadmap tasks: acceptance criteria met or not.
- Validation plan scenarios: run where automation exists; report results.
- Contract coverage: implemented UI that `docs/ui/` does not describe.
