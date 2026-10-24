---
name: reuse-auditor
description: >
  Audit existing code for canonical owners, semantic duplication, and unused or
  obsolete code before decomposing components, extracting shared helpers,
  services, models, or normalization paths, consolidating duplicates, or removing
  code believed to be unused. Use when asked whether something is already
  implemented, can be reused, is duplicated, or is safe to delete.
  Language-agnostic (Python, JavaScript/TypeScript, ABAP, Java, C#, SQL, and
  others). Read-only: reports decisions, never edits code. Do not use for trivial
  local edits, formatting, documentation-only work, bug fixes that add no shared
  abstraction, or general cleanup of a diff (use a simplify or code-review skill).
---

# Reuse Auditor

Prevent two failures: creating a parallel implementation when a canonical owner
already exists, and merging code that only looks similar. A reuse audit is
read-only; it never authorizes deletion, extraction, refactoring, or catalog edits.

## Load project configuration first

Select one project policy file, in this order:

1. the path named for this skill in project instructions (`AGENTS.md`,
   `CLAUDE.md`, or the platform's equivalent), for example
   `.ai-graph-guide/reuse-auditor.md`;
2. `project-config.md` beside a project-local install of this skill
   (`.agents/skills/reuse-auditor/` or `.claude/skills/reuse-auditor/` in the
   project root, holding its `SKILL.md`);
3. otherwise, the defaults below.

A user/global/shared skill copy and a general project configuration (for example
a guidance graph's `.ai-graph-guide/project-config.md`) are not this skill's
policy unless project instructions name them for it. Do not scan other platform
directories or merge conflicting files; report ambiguity that changes an
ownership decision. Read the selected file once per task. It may name an
ownership/reuse catalog, confirmed owners, known divergences, extra
dynamic-dispatch mechanisms, search tools, and required tests. Project rules
extend this skill; they cannot relax its safety rules. Verify config and catalog
entries against current source.

Defaults: no catalog, owners inferred from source and tests, targeted repository
search, the project's existing test commands. Read the bundled
[project-config.md](references/project-config.md) template only when asked to
create or extend a project configuration.

## Language profile

Identify the languages of the target and its consumers. Read only the matching
sections of [language-profiles.md](references/language-profiles.md), or its generic
section for unlisted languages, when caller discovery or contract comparison
depends on language mechanisms, and always before assigning `obsolete-candidate`.

Obsolete gate (every language, also without the profile): search string literals
and configuration for the name; check dynamic dispatch (reflection, registries,
dependency injection, string-built names), public/exported API status, external
callers (other repositories, jobs, APIs, other systems), version history, and
whether tests are the only callers. If the language profile cannot be read (for
example, the skill text was delivered without its files), say so and cap
`obsolete-candidate` at `low` confidence.

## Classifications

Classify each material candidate by its relationship to existing code. A planned
implementation is compared the same way: if an existing owner already meets its
contract, it is an `exact-duplicate` of that owner and the recommendation is
`reuse-existing`.

- `exact-duplicate`: inputs, outputs, errors, side effects, units, precision, and
  lifecycle match; consolidation candidate.
- `semantic-duplicate`: overlapping intent with a different boundary or behavior;
  needs a domain decision.
- `reuse-candidate`: at least two real consumers and a plausible common contract;
  evidence incomplete.
- `intentional-divergence`: similarity is superficial or separate ownership is
  safer.
- `obsolete-candidate`: no verified caller found; removal still requires the
  obsolete gate and the language-profile checks.

Record the owner's status separately:

- `confirmed-owner`: canonical component with verified consumers and contract
  tests; reuse it instead of adding a parallel implementation.
- `unconfirmed-owner`: plausible canonical component whose consumers or contract
  tests are not verified; reuse may still be recommended, with lower confidence
  and the missing contract tests as next validation.
- `no-owner`: nothing existing owns the concern; a new shared component may be
  proposed.

## Workflow

If an earlier reuse audit in the same task covers this scope and its inputs are
unchanged, reuse its decisions instead of repeating the search.

1. State the concern, target scope, and contracts that must stay stable.
2. Check the configured catalog or ownership map for an existing owner; without
   one, infer owners from primary source, tests, and module boundaries.
3. Inventory callers, imports, registrations, tests, and side effects with targeted
   search. If a verified code graph or index (for example Graphify) is available,
   use bounded caller/dependency queries and confirm important edges in source.
   Do not scan unrelated areas.
4. Compare candidates semantically and try to disprove reuse: signatures, accepted
   inputs, fallbacks, error behavior, units, precision/rounding, transactions,
   persistence, authorization, concurrency, and lifecycle. Matching names or text
   are hypotheses only.
5. Assign one classification, the owner status, and confidence
   (`high | medium | low`) per material candidate.
6. Recommend `reuse-existing`, `consolidate`, `keep-separate`, `investigate`, or
   `remove-later`. Keep business fixes separate from decomposition.
7. Stop when each material concern has an ownership decision and further search is
   unlikely to change it.

## Safety rules

- Consolidation or removal requires characterization tests that pin the current
  behavior of every affected consumer, plus code review. Without them, record a
  candidate and the missing evidence.
- Preserve security, financial, persistence, API, error, and compatibility
  contracts; never trade them for less code.
- Update a catalog only when the user requested documentation changes. Record new
  items as candidates; promote to confirmed only after implementation verification.

## Report

Return the report to the caller (the user or the invoking workflow step); write it
to a file only when the caller asks. Report only results that change the
decomposition or prevent duplication. For one or two concerns:

```text
concern / symbols:      <what and where>
owner:                  <current -> proposed canonical owner; owner status>
consumers:              <verified callers; note unverified dynamic references>
similar / different:    <semantic comparison>
evidence:               <contract tests, side effects, sources>
decision:               <classification, confidence, recommendation>
next validation:        <characterization tests or checks still required>
```

For three or more concerns, use one table with the columns `concern / symbols`,
`owner (status) and consumers`, `decision` (with the semantic difference and
evidence), and `next validation`.

Do not list every symbol. If nothing material is found, say so with the evidence
searched.
