# UI Review

Reviews UI changes in a React application against the project's UI contract in `docs/ui/`: tokens and component reuse, page templates and patterns, data states, WCAG 2.2 AA accessibility, responsive behavior and before/after screenshots. It also guards business logic: a UI change must not alter calculations, API calls, state, permissions or remove functions.

## Usage

```text
$ui-review — review current changes (working tree, else branch vs base)
$ui-review main..feature/new-shell — review a named range
$ui-review full — post-implementation audit of the whole app vs the original UX audit
```

These are example requests to the agent, not shell commands.

## Results

- `FAIL`: business logic changed, a function removed, a core flow broken, values shown wrong, or a WCAG A/AA failure on a core flow.
- `WARN`: P1 findings, contract violations, missing states, docs drift, or unverified parts.
- `PASS`: nothing above in the reviewed scope.

The report lists findings with location, evidence and fix, plus the `docs/ui/` entries to update with `documentation-sync`. Full mode also tracks every issue from `docs/ux-audit/03-ux-ui-audit.md` and the roadmap's acceptance criteria. The skill does not fix code or update docs.

## Project profile

Copy [references/project-config.md](references/project-config.md) into the project and name its path for `ui-review` in project instructions. One profile file can serve `ui-full-redesign` and `ui-review`.

## Package contents

- `SKILL.md`: boundaries, scopes, workflow and verdict.
- `references/checklist.md`: review checks and full-mode extras.
- `references/report-template.md`: report format.
- `references/project-config.md`: template for a target-project profile.
- `agents/openai.yaml`: metadata for the Codex interface.
