# Changelog

## 1.8.0 — 2026-10-11

- Eval prompts no longer contain expected results; grading keys moved to
  `tests/expected/*.json` (rubric plus deterministic checks) and are read only
  by the new `scripts/grade_result.py` after execution.
- A zero exit code no longer means PASS: results report execution, install,
  activation, safety, schema validity, semantic checks, and a pending rubric
  review separately, with verdicts PASS, UNVERIFIED, FAIL, and BLOCKED.
- Each case runs in a disposable sandbox with a verified (path, version, hash)
  installation that excludes `tests/`; sandbox mutations fail the case;
  profiles without verified write protection are blocked unless allowed.
- Skill activation is verified from tool-call events only; Claude runs use
  `stream-json`, Codex runs skip the git-repo check.
- Canonical machine-readable result schema 2.0 aligned with the Finding
  Contract and referenced from `SKILL.md`.
- Runs are stored per unique run ID with git SHA, skill hash, CLI version,
  config, limits, usage, cost, and turns (`unknown` when unavailable); added
  `scripts/summarize_runs.py` for success rate, latency percentiles, and
  tokens and cost per successful task, including baseline/candidate comparison.
- Fixed: relative reference checking in the validator, `TimeoutExpired` bytes
  output crashing the runner, and non-atomic `--force` installation.
- Split the combined language fixture and added fixtures for stale context,
  contradictory instructions, tool failure, output overcompression, missing
  evidence, side-effect retry, partial results, and zero findings.
- Added a provider fallback rule for models without a dedicated reference file.
- Added deterministic unit tests for the scripts.

## 1.7.0 — 2026-10-04

- Clarified portable optimization boundaries: read-only
  auditing, baseline preservation, and scoped editing authorization.
- Distinguished prescribed instructions, technical enforcement, and observed
  execution.
- Added an explicit static-only validation fallback without runtime savings
  claims, and rollback guidance for observed quality regressions.
- Preserved requirements sources, criteria, evidence, freshness, and integration
  ownership in compact handoffs.

## 1.6.0 — 2026-07-15

- Added automatic user-facing report language selection.
- Made explicit user language instructions override request, source artifact, and prior-context languages.
- Added fallback to the latest substantive user request, then the most recent explicit user-facing language or configured default.
- Added mixed-language handling that excludes code, paths, identifiers, product names, and quotations from language inference.
- Preserved technical tokens and canonical machine schemas unless translation is explicitly requested.
- Added a multilingual regression fixture covering Russian automatic selection and Spanish explicit override.

## 1.5.0 — 2026-07-15

- Replaced the default multi-section audit report with four compact sections: important findings, changes, conditional questions, and metrics.
- Removed executive summary, execution model, scorecard, separate recommendations, and evaluation approach from standard output.
- Limited standard reports to five material root findings and quick reports to three, except for additional critical or high findings.
- Made deep analysis appendices explicitly opt-in and prohibited repeating the compact report.
- Added rules to omit empty questions and unavailable metric columns and to label estimated token values.
- Added an optimizer-report regression fixture.

## 1.4.0 — 2026-07-14

- Added output-contract auditing for concise but complete user and agent responses.
- Added consumer classification for user, orchestrator, peer-agent, machine, and artifact outputs.
- Added `compact`, `standard`, and `detailed` response-mode checks with explicit expansion conditions.
- Added analysis-depth versus output-length separation and prompt/runtime/schema/application placement guidance.
- Added compact delta-handoff patterns for subagents and unbounded-state detection.
- Added evaluation criteria for retained evidence, output tokens, repeated information, follow-up turns, and retries.
- Added two behavioral fixtures covering verbose user output and narrative subagent handoffs.

## 1.3.0 — 2026-07-14

- Added platform adapters for OpenAI Codex, Google Antigravity, GitHub Copilot in VS Code, and Claude Code for VS Code.
- Added explicit IDE-versus-CLI parity checks and thin-adapter guidance for multi-platform repositories.
- Added safe platform installation helper and documented canonical installation paths.
- Added non-interactive eval command profiles and a cross-platform eval runner with dry-run support.
- Added conservative sandbox, permission, persistence, budget, turn, and credit defaults where supported.
- Added four platform-focused behavioral fixtures.
- Extended validation to check platform metadata, command templates, JSON configs, install paths, and dangerous default flags.

## 1.2.0 — 2026-07-14

- Reduced the always-loaded `SKILL.md` and moved detailed checks behind a routing index.
- Added adaptive `quick`, `standard`, and `deep` report modes.
- Added explicit no-fabricated-findings and no-material-issue behavior.
- Added trust hierarchy, prompt-injection, permissions, and secret-exposure audit.
- Added write-tool side-effect, idempotency, rollback, approval, and concurrency checks.
- Added measurable token/cost/quality protocol and representative eval guidance.
- Added context selection, ordering, truncation, retrieval, and stale-state checks.
- Added confidence and evidence-type rubrics.
- Split OpenAI guidance into common and model-specific files with freshness metadata.
- Added provider/platform extension contract.
- Added self-test fixtures and a static skill validator.

## 1.1.0 — 2026-07-14

- Added eval-driven optimization and prompt/runtime separation.
- Added OpenAI GPT-5.4, GPT-5.5, and GPT-5.6 guidance.
- Added state, caching, compaction, and tool-output optimization checks.

## 1.0.0

- Initial optimizer audit skill.
