# Python Code Review 2.2

A general-purpose skill for reviewing Python code. It first reconstructs the
behavior of the affected system, then tests hypotheses about defects and uses
relevant sections of the Python reference to look for omissions. Analyzers and
passing tests provide evidence, but do not replace engineering review.

## Review scope

- `CHANGE_REVIEW` — a diff, PR, branch, commit, range, or local changes.
- `COMPONENT_REVIEW` — a module, package, service, or subsystem.
- `PROJECT_AUDIT` — a project or large area with an explicit coverage strategy.

The skill distinguishes the review target, the necessary surrounding context,
and the broader behavior affected by a change. For a small change, its contract,
callers, and tests may be enough; a full architecture audit is not required.

Git reviews use exact snapshots: staged, working-tree, and historical files are
not interchangeable. With partial staging, a fix in the working copy does not
resolve a defect in the prospective commit. Without Git, the skill can review a
specified component but must not invent a comparison baseline.

## Process and result

The agent studies requirements and important boundaries, traces relevant normal
and failure scenarios, looks for evidence that disproves its hypotheses, and
assesses what the tests actually guarantee. Review depth depends on scope and
impact, not on a mandatory number of phases.

A typical result includes findings with their sources, triggering conditions,
impact, and fixes, along with checks performed and coverage limits. Add a
verdict when requested or for a merge review. A detailed architecture report is
needed only on request or for significant systemic risks.

Use an independent reviewer when the user or project requires one, or when
authorized delegation would add useful scrutiny. Tool availability alone does
not authorize delegation. A second pass by the same model is self-review and
does not replace required independent review.

## Boundaries

By default, the skill reviews code without changing it. A request that includes
fixes authorizes changes within the specified scope while preserving existing
work.

The skill does not install dependencies, change Git state, or run untrusted
scripts or external actions just to produce a successful report. Tests, plugins,
environment wrappers, and scanners may execute code or contact services; before
running them, the agent checks trust, side effects, and authorized scope.
Secrets and personal data must not appear in the report.

## Resources

- [SKILL.md](SKILL.md) — the main workflow, scopes, severity levels, and verdicts.
- [system-analysis](references/system-analysis.md) — techniques for analyzing complex boundaries.
- [python-review](references/python-review.md) — targeted Python review guidance.
- [tooling](references/tooling.md) — command selection, trust, and evidence.
- [independent-reviewer](reviewers/independent-reviewer.md) — a bounded reviewer assignment.
- [review-report](templates/review-report.md) — the concise result contract.
- [openai.yaml](agents/openai.yaml) — interface metadata.

Copy the entire folder into a supported skill directory for your agent, keeping
the relative paths intact.

## Example requests

```text
Use $python-code-review in CHANGE_REVIEW mode for the supplied base and target.
Review affected behavior and contracts; report concrete findings, observed
checks, coverage limits, and a merge verdict. Do not modify files.
```

```text
Use $python-code-review in PROJECT_AUDIT mode for this Python project.
Inventory components, prioritize core flows and high-risk boundaries, trace
relevant failures, and disclose inspected, sampled, and uninspected areas.
Return systemic and local findings without modifying files.
```

## Project configuration

Local instructions may define domain invariants, architecture boundaries,
supported Python versions, permitted commands and environments, data-handling
rules, and whether independent review is required. The skill follows those
constraints and does not require a specific framework or platform.
