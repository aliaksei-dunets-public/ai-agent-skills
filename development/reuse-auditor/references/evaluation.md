# Synthetic Evaluation

Run these cases after changing the skill. Evaluate each independently and compare
with the expected decision; do not show the expected decision to an independent
evaluator before it finishes.

## Case A: exact duplicate (Python)

`orders.py` defines `normalize_side(value)`: read an enum `.value`, convert to text,
trim, uppercase. `fills.py` defines `canonical_side(value)` with the same accepted
inputs, output, errors, and no side effects. Both have production consumers and
equivalent tests.

Expected: `exact-duplicate`, high confidence; recommend one canonical owner and keep
characterization tests for both consumers. No code edits during the audit.

## Case B: look-alike rounding (any language)

`wallet` rounds display currency to two decimals, half-up. `orders` rounds order
quantity down to the exchange step size before placement. Both call a function
named `quantize` and return a decimal type.

Expected: `intentional-divergence`, high confidence; different units, rounding
semantics, side effects, and owners. Keep separate.

## Case C: no static callers (ABAP)

Class `ZCL_PRICE_ROUNDING` has no hits in the ADT where-used list. A customizing
table stores class names that are instantiated with `CREATE OBJECT TYPE (lv_class)`.

Expected: not removable; at most `obsolete-candidate` with low or medium confidence.
Next validation: inspect customizing entries, transports, and dynamic instantiation
sites before any removal.

## Case D: semantic duplicate (TypeScript)

`formatAmount(value: number)` in the UI returns `""` for `null` and `undefined`;
`formatAmount(value: number)` in a report exporter throws on `null`. Implementations
are otherwise identical.

Expected: `semantic-duplicate`, high confidence; error behavior differs, so
consolidation needs a domain decision and characterization tests for both paths.

## Case E: planned helper with an existing owner (Python)

A plan proposes a new `utils/money.py:to_minor_units(amount, currency)`.
`finance/currency.py:minor_units()` already converts amounts with the same
rounding and currency table, has three production consumers, and contract tests.

Expected: `exact-duplicate` of the existing owner, owner status `confirmed-owner`,
high confidence; recommend `reuse-existing` and no new helper.

## Case F: skill text without its files (any language)

The skill is delivered as `SKILL.md` text only (for example through a guidance
server); `references/language-profiles.md` cannot be read. A Java class has no
static callers.

Expected: the report states that the language profile was unavailable, applies the
obsolete gate from `SKILL.md`, and assigns at most `obsolete-candidate` with `low`
confidence.

## Case G: configuration routing

Check three setups: (1) project instructions name `.ai-graph-guide/reuse-auditor.md`
and a project-local Claude install also has a `project-config.md`; (2) only a
project-local install with `SKILL.md` and `project-config.md`; (3) a
`.agents/skills/reuse-auditor/` folder holding only `project-config.md`, and the
project has `.ai-graph-guide/project-config.md`.

Expected: (1) the named path wins; (2) the sibling config is used; (3) defaults,
because neither file is named for the skill and the folder is not an install. No
cross-platform scan, no merge of files, no config edits.

## Case H: missing selected policy and external callers

Project instructions explicitly select a missing policy file. Local source has
no callers of an exported class; the external client repository is unavailable.

Expected: report both gaps, do not substitute another policy, and do not infer
that external callers are absent. Ownership decisions affected by the policy
remain provisional; further validation is required before removal.

## Case I: catalog proposal during an audit

An audit finds a plausible new owner and a stale catalog row. The user requested
only an audit, not documentation changes.

Expected: propose the catalog correction without editing. New entries remain
candidates until implementation verification; a later documentation request
authorizes a separate task, not an exception to read-only audit behavior.

## Pass criteria

- A is not rejected merely because it has only two consumers.
- B is not consolidated because of textual similarity.
- C is not declared dead from static search alone.
- D identifies the differing failure behavior.
- E recommends reusing the confirmed owner instead of adding a parallel helper.
- F caps confidence and names the missing profile instead of skipping the gate.
- G selects exactly one policy source per setup.
- H reports missing policy and external evidence without inventing defaults or
  proof of absence.
- I proposes catalog changes without applying them during the audit.
- No case causes source edits, deletion, or catalog changes.
- Each result names the classification, owner and owner status, consumers,
  evidence, confidence, and next validation; a run of three or more concerns may
  use the table form.
