# UI Full Redesign

Application-wide UX/UI audit and redesign proposal for an existing multi-page React application. The agent inventories every route, audits navigation, hierarchy, interactions, states, accessibility and responsive behavior, proposes a navigation architecture and a unified design system, then creates three visual concepts with real desktop and mobile mockups of two representative pages, compares them on a scorecard, and prepares an incremental refactoring roadmap and a validation plan.

Production code is not changed. Implementation starts only after you approve a target design, as a separate request.

## Usage

```text
$ui-full-redesign
```

This is an example request to the agent, not a shell command.

## Design tools

| Platform | Mandatory design tool |
|---|---|
| Claude Code | Claude Design |
| Google Antigravity, OpenAI Codex | Google Stitch |

The agent checks tool readiness first. If the design tool is missing, it explains how to enable it and asks before installing anything. With your consent it can produce isolated HTML prototypes with screenshots instead, clearly labeled as a fallback.

## Project profile

Domain-specific checks (for example financial formatting), launch and sign-in instructions, routes to skip and design overrides belong to the target project, not to this skill. Copy [references/project-config.md](references/project-config.md) into the project and name its path for `ui-full-redesign` in the project's `AGENTS.md` or `CLAUDE.md`.

## Results

Deliverables go to `docs/ux-audit/`: tool readiness, application inventory, audit with P0/P1/P2 issues, quick wins, navigation architecture, design system, mockup selection, mockups per concept, comparison, roadmap, validation plan and a summary. Raw captures stay in `.tmp/`. Reports follow the language set by agent and project instructions, otherwise the language of the request.

## Package contents

- `SKILL.md`: boundaries, configuration and the phase workflow.
- `references/platform-tools.md`: platform detection, Claude Design and Stitch workflows, readiness report.
- `references/audit-checklist.md`: discovery, audit areas, issue format and severity.
- `references/design-concepts.md`: navigation and design-system rules, the three concepts, mockup matrix and scorecard.
- `references/deliverables.md`: file layout, roadmap, validation plan and summary.
- `references/project-config.md`: template for a target-project profile.
- `agents/openai.yaml`: metadata for the Codex interface.
