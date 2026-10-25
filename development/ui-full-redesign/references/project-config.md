# UI Full Redesign Project Configuration

This bundled file holds neutral defaults and is the template for a project
profile. Do not add project-specific content here: the skill is shared by many
projects.

To customize a project, copy this file into the project, for example to
`docs/ui-profile.md`, and name its path for the
`ui-full-redesign` skill in project instructions (`AGENTS.md`, `CLAUDE.md` or
the platform's equivalent). The same file may serve `ui-review`:
Application and Domain profile are shared, and each skill adds its own
sections. Fill only the applicable sections; omitted sections
fall back to the defaults. Project rules may add checks and stricter gates;
they cannot relax the skill's boundaries.

## Application

Default: discover from source; ask the user for what cannot be discovered.

```text
launch command: <e.g. npm run dev>
base URL: <e.g. http://localhost:5173>
test sign-in: <where test credentials come from: seed file, fixture, ask user; never the values>
routes to skip: <route — reason>
```

## Domain profile

Default: none; generic formatting consistency checks only.

```text
domain: <e.g. finance, logistics, healthcare>
extra audit checks:
  - <check>
rules that must not change:
  - <business rule or calculation area>
terminology: <glossary path or key terms>
```

## Design

Default: the skill's three concepts and references.

```text
existing design system: <path, Storybook URL, or design-tool project link>
concept overrides: <replace or add references, keeping three concepts>
brand constraints: <colors, fonts, logo usage>
```

## Deliverables

Default: `docs/ux-audit/`.

```text
root: <path>
prototype directory: <path outside application source>
```

## Additional rules

Default: none.
