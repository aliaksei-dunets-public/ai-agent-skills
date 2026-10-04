# Python Review Report Contract

Use the user's language and the shortest form that preserves material evidence.
Omit empty sections. A focused review does not require an executive summary,
architecture essay, strengths list, or completed checklist in its final answer.

## Default result

1. **Findings:** order by severity using the policy in [SKILL.md](../SKILL.md).
   For each item include location/snapshot, triggering scenario, evidence and
   causal impact, minimal correction or acceptance condition, and confidence.
   Consolidate systemic issues with representative locations. Distinguish
   confirmed findings, concrete unresolved risks, and optional suggestions.
   State briefly when no material issue is found.
2. **Scope and verification:** identify reviewed target and relevant context,
   refs/snapshot when applicable, coverage limits, checks actually run, their
   observed results, and skipped required checks. State what static tracing or
   green tests cannot establish.
3. **Verdict, when requested or expected for merge:** use the entry point's
   verdict policy. Explain any blocker or insufficient evidence. A review verdict
   does not merge code, complete implementation, or express user approval.

A changed-code finding can be as compact as:

```text
[Severity] Title — path:line (snapshot)
Trigger and evidence; causal impact.
Correction or acceptance condition. Confidence: high / medium / low.
```

Do not invent line numbers where a symbol, configuration key, or architectural
boundary is the available evidence. Keep secrets and private data redacted.

## Expand only when useful

For a requested detailed report, project audit, or important cross-boundary risk,
add only necessary, non-repeating material:

- system model: affected workflow, boundaries, state/invariants, failure behavior;
- architecture: demonstrated systemic risks or strengths with evidence;
- scenario traces: normal/failure paths and established or unknown outcomes;
- project coverage: inspected, sampled, and uninspected components;
- test assessment: contracts protected, boundary fidelity, and material gaps;
- verification table: command, scope/snapshot, result, relevance, limitations;
- independent review: actual mechanism, new evidence, rejected findings, and limits;
- required actions and residual risks.

Do not reproduce the entire internal investigation. Independent-review status is
required when a separate review was used or required; disclose self-review and
unmet acceptance gates without presenting it as independent execution.
