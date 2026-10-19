# Reuse Auditor Project Configuration

This bundled file holds neutral defaults and is the template for project
customization. Do not add project-specific content here: the skill clone is shared
by many projects.

To customize a project, copy this file to the config path named in project
instructions or beside the selected project-local skill wrapper/installation.
The legacy Codex path is `<project_root>/.agents/skills/reuse-auditor/project-config.md`;
a selected Claude installation may use `.claude/skills/reuse-auditor/project-config.md`.
Use one canonical project owner as described in SKILL.md and fill only applicable
sections. Do not store target-project policy in a global/shared skill copy. The project
copy is owned by that project and survives skill updates. Omitted sections fall
back to the defaults below.

Project rules may add sources, owners, mechanisms, tests, and stricter gates. They
must not relax the skill's safety rules: characterization tests before
consolidation or removal, read-only audits, and candidate-first catalog updates.

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
