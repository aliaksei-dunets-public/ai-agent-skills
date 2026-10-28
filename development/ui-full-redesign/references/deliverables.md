# Deliverables

## Layout

```text
docs/ux-audit/
  00-summary.md
  01-tool-readiness.md
  02-application-inventory.md
  03-ux-ui-audit.md
  04-navigation-architecture.md
  05-design-system.md
  06-mockup-selection.md
  07-design-comparison.md
  08-refactoring-roadmap.md
  09-validation-plan.md
  10-quick-wins.md
  mockups/
    concept-a-kokonutui/
    concept-b-shadcn-admin/
    concept-c-tailadmin/
```

Use another root only when the project profile names one, and carry that root
into the `ui-review` handoff. Replace `docs/ux-audit/` in artifact paths with
that root; UI contract paths remain separate.
Fallback prototypes,
if approved, go to `docs/ux-audit/prototypes/` or a path the profile names,
never inside the application source. Raw captures and logs stay in `.tmp/`.
Deliverables never contain secrets or real personal or financial data.

## Refactoring roadmap (phase 8)

Cover app shell and navigation, component consolidation, token migration, form
and table modernization, page-by-page improvements, responsive and
accessibility work, and the testing and regression strategy. Prefer small
incremental steps that ship independently.

Per task:

| Field | Content |
|---|---|
| ID / priority | `RF-001`, P0–P2 |
| Affected routes | |
| Affected components | paths |
| Approach | |
| Complexity | S / M / L |
| Dependencies | task IDs |
| Risk | and mitigation |
| Acceptance criteria | testable; include a `ui-review` pass and the `docs/ui/` update |

State that API contracts, state behavior, permissions and business
calculations stay unchanged, and how each task proves it.

## Validation plan (phase 9)

Use Playwright or the available automation. Include user scenario tests,
navigation tests, form and filter behavior, desktop and mobile visual
regression, accessibility checks (for example axe), responsive layout checks,
state and error behavior, and domain data display integrity (formatting and
values identical before and after). Specify the same scenarios for the current
UI and proposed design. Execute only checks supported by the available app or
prototype within the authorized scope; label the rest as planned. Static mockups
cannot establish runtime behavior. Claim usability or performance gains only
with measured evidence.

## Summary (`00-summary.md`)

1. Audit coverage by functional area.
2. Top UX problems.
3. Proposed navigation architecture.
4. Design system summary.
5. The two selected pages and why.
6. The six mockups with links or paths.
7. The twelve desktop/mobile representations with paths.
8. Concept comparison.
9. Recommended design.
10. Roadmap outline.
11. Missing tools, pages and artifacts.
