---
name: reuse-auditor
description: >
  Audit existing code for canonical owners, semantic duplication, and obsolete
  candidates before decomposing components, extracting shared helpers, services,
  models, or normalization paths, or consolidating duplicates. Language-agnostic
  (Python, JavaScript/TypeScript, ABAP, Java, C#, SQL, and others). Do not use for
  trivial local edits, formatting, documentation-only work, or bug fixes that add
  no shared abstraction.
---

# Reuse Auditor

Prevent two failures: creating a parallel implementation when a canonical owner
already exists, and merging code that only looks similar. A reuse audit is
read-only; it never authorizes deletion, extraction, refactoring, or catalog edits.

## Load project configuration first

Read `<project_root>/.agents/skills/reuse-auditor/project-config.md` (or another path
named by the project instructions) once per task and reuse it while unchanged. It
may name an ownership/reuse catalog, confirmed owners, known divergences, extra
dynamic-dispatch mechanisms, search tools, and required tests. Project rules extend
this skill; they cannot relax its safety rules. Treat configuration and catalog
entries as hypotheses to verify against current source.

If the file is absent, use defaults: no catalog, owners inferred from source and
tests, targeted repository search, the project's existing test commands. Read the
bundled [project-config.md](references/project-config.md) template only when asked
to create or extend a project configuration.

## Language profile

Identify the languages of the target and its consumers. Read only the matching
sections of [language-profiles.md](references/language-profiles.md), or its generic
section for unlisted languages, when caller discovery or contract comparison
depends on language mechanisms. Always read them before assigning
`obsolete-candidate`.

## Classifications

- `confirmed-owner`: canonical component with verified consumers and contract
  tests; reuse it instead of adding a parallel implementation.
- `exact-duplicate`: inputs, outputs, errors, side effects, units, precision, and
  lifecycle match; consolidation candidate.
- `semantic-duplicate`: overlapping intent with a different boundary or behavior;
  needs a domain decision.
- `reuse-candidate`: at least two real consumers and a plausible common contract;
  evidence incomplete.
- `intentional-divergence`: similarity is superficial or separate ownership is
  safer.
- `obsolete-candidate`: no verified caller found; removal still requires the
  dynamic-reference, public-API, history, and test checks from the language profile.

## Workflow

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
5. Assign one classification and confidence (`high | medium | low`) per material
   candidate.
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

Report only results that change the decomposition or prevent duplication:

```text
concern / symbols:      <what and where>
owner:                  <current -> proposed canonical owner>
consumers:              <verified callers; note unverified dynamic references>
similar / different:    <semantic comparison>
evidence:               <contract tests, side effects, sources>
decision:               <classification, confidence, recommendation>
next validation:        <characterization tests or checks still required>
```

Do not list every symbol. If nothing material is found, say so with the evidence
searched.

## Validation of this skill

After editing this skill, run the cases in [evaluation.md](references/evaluation.md).
