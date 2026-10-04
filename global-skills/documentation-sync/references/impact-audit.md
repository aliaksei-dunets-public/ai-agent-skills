# Documentation Impact Audit

Map changed claims before editing. For small changes, a short internal list is
enough; use a table when multiple owners or conflicting sources are involved.

| Change or source | Affected claim | Canonical owner | Dependent documents | Decision | Evidence or reason |
| --- | --- | --- | --- | --- | --- |
| Describe the actual change | Identify the claim | Existing owner path | Incoming links or summaries | required / recommended / not-needed | Source path, symbol, revision, or verified result |

- `required`: without an update the claim becomes incorrect, incomplete for a
  supported workflow, or unusable.
- `recommended`: useful clarity or navigation improvement; no incorrect contract.
- `not-needed`: the change leaves the claim valid.

Inspect relevant public APIs, schemas, CLI commands, configuration, behavior,
examples, installation and recovery steps, and links to moved files. Select
topics from the assigned scope instead of scanning every category.

Two documents can duplicate a contract without identical wording. Find the owner
from project policy and preserve unique content before replacing a copy with a
link. If two authoritative sources disagree and precedence is unresolved, record
the competing claims, evidence, effect, and decision needed. Continue unrelated
corrections; do not conceal the conflict in a rewritten summary.
