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

## Pass criteria

- A is not rejected merely because it has only two consumers.
- B is not consolidated because of textual similarity.
- C is not declared dead from static search alone.
- D identifies the differing failure behavior.
- No case causes source edits, deletion, or catalog changes.
- Each result names owner, consumers, evidence, confidence, and next validation.
