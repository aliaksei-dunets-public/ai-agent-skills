# Reuse Auditor Project Configuration

This bundled file holds neutral defaults and is the template for project
customization. Do not add project-specific content here: the skill clone is shared
by many projects.

To customize a project, copy this file into the project and name its path for
the `reuse-auditor` skill in project instructions (`AGENTS.md`, `CLAUDE.md`, or the
platform's equivalent), for example `.ai-graph-guide/reuse-auditor.md`. This works
when the skill is served from a shared clone or a guidance graph. A file beside a
project-local install (`.agents/skills/reuse-auditor/project-config.md` or
`.claude/skills/reuse-auditor/project-config.md`) is used only when project
instructions name no path and that folder is the project-local install being used.
Keep one policy file per project, as described in SKILL.md, and fill only
applicable sections. Do not store target-project policy in a global/shared skill
copy. The project copy is owned by that project and survives skill updates.
Omitted sections fall back to the defaults below.
An explicitly selected but unreadable or missing policy is a reported coverage
gap, not a reason to substitute a different policy or assume defaults.

Project rules may add sources, owners, mechanisms, tests, and stricter gates. They
must not relax the skill's safety rules: characterization tests before
consolidation or removal, read-only audits, and candidate-first catalog updates
performed only in a separately requested documentation task.

## Ownership catalog

Default: none. Infer owners from source, tests, and module boundaries.

```text
catalog: <relative path, e.g. docs/architecture/reuse-catalog.md>
entry states: <confirmed | candidate | rejected, or the project's own terms>
update policy: <who may edit it and when>
```

## Confirmed owners and known divergences

Default: none. Prefer linking the catalog over duplicating its rows here.

```text
- <capability>: <canonical owner path/object> — tests: <contract tests>
- divergence: <A> vs <B> — reason: <why they must stay separate>
```

## Languages and dynamic references

Default: detect languages from the target and its consumers; use
`references/language-profiles.md`.

```text
languages: <e.g. Python 3.12, TypeScript, ABAP 7.5x>
extra dynamic mechanisms: <plugin registries, DI containers, BAdIs, config-driven dispatch, ...>
generated or external callers: <RFC/OData/REST clients, jobs, reports, other repositories>
```

## Search and index tools

Default: targeted text/symbol search in the repository.

```text
code graph/index: <e.g. Graphify MCP; freshness check>
where-used: <e.g. ADT where-used list, IDE references, language server>
excluded paths: <generated code, vendored dependencies, build output>
```

## Verification

Default: the project's existing test commands and code review.

```text
characterization tests: <location and command>
contract/integration tests: <location and command>
review requirement: <reviewer or gate>
```

## Additional rules

Default: none.
