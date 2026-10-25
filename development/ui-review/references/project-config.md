# UI Review Project Configuration

This bundled file holds neutral defaults and is the template for a project
profile. Do not add project-specific content here.

Copy it into the project and name its path for the `ui-review` skill in project
instructions (`AGENTS.md`, `CLAUDE.md` or the platform's equivalent). The same
file may serve `ui-full-redesign`: Application and Domain profile
are shared, and each skill adds its own section. Omitted sections fall back to
the defaults. Project rules may add checks and stricter gates; they cannot
relax the skill's boundaries.

## Application

Default: discover from source; ask the user for what cannot be discovered.

```text
launch command: <e.g. npm run dev>
base URL: <e.g. http://localhost:5173>
test sign-in: <where test credentials come from; never the values>
```

## Domain profile

Default: none; generic formatting consistency checks only.

```text
domain: <e.g. finance>
extra checks:
  - <check>
rules that must not change:
  - <business rule or calculation area>
```

## UI review

Default: contract `docs/ui/`, base branch from Git, no extra commands.

```text
contract root: <path>
base branch: <e.g. main>
ui test commands: <e.g. npm run test:e2e, npm run lint>
accessibility tool: <e.g. axe via Playwright>
extra FAIL conditions:
  - <condition>
```

## Additional rules

Default: none.
