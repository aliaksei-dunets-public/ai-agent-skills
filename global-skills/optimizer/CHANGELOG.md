# Changelog

## 2.3.0 — 2026-11-06

- Loading:
  - Added a Resources table in `SKILL.md` that states when each file loads;
    references repeat only their own load condition.
  - `technical-writing-ste` is used in `review` mode at steps 3–4 and in
    `edit` mode at step 5; its writing rules are linked directly.
  - `platforms.md` loads only when a check or finding needs a platform fact the
    package does not state, or must verify one that it states (for example,
    an installation path).
- Audience and language: a new section in `SKILL.md` separates agent-facing
  from human-facing text.
  - Agent-facing text must be in English. Quoted user phrases, examples of
    non-English input or output, and literal output templates are exceptions.
    Other non-English agent-facing text is a finding; `fix` translates it
    under the `technical-writing-ste` behavior contract.
  - `technical-writing-ste` applies to agent-facing text only. Human-facing
    text keeps its language and style and is checked for accuracy and
    consistency. Files are classified by type and location (an unlinked file
    in `references/` is agent-facing); a file whose audience is still unclear
    is treated as human-facing, and this classification takes precedence over
    the dependency's own rule. Examples and literal output templates are
    checked against the rules they illustrate, not against STE wording rules.
  - `technical-writing-ste` now states the same scope in its `description`
    and workflow; the optimizer `description` and guide refer wording-only
    edits or reviews of agent-facing text, in one file or several, to it.
  - The optimizer `description` no longer names `prompter`; it states that a
    single standalone prompt is out of scope, so the boundary holds when
    `prompter` is not installed. The `technical-writing-ste` description
    likewise names no sibling skill: it defines wording (sentence clarity,
    terms, grammar, punctuation, ambiguous phrasing, repetition or list
    layout within the text) and excludes prompt task design and package
    audits.
  - The `prompter` description is in third person, names no sibling skill,
    and excludes checking or editing only the wording of a prompt. The optimizer
    description defines weak instructions (missing conditions, failure
    handling, or controls), separating them from unclear wording.
  - `technical-writing-ste` writing rules: when a placeholder is needed in
    `create`; a contradiction with another file is reported, not resolved;
    one condition over several actions stays in one sentence or a lead-in
    list; an actor addressed by imperatives counts as named; a clear passive
    condition is kept.
  - `technical-writing-ste`: `create` is triggered when the content is given;
    proofreading, rewriting, simplifying, and translating agent-facing text to
    English are `edit` requests, checking and reviewing are `review`; `review` lists
    suspected technical errors separately; a mixed document stops only when
    all of it is human-facing, and the output names the human-facing
    sections left unchanged.
- Moved the fix and verify steps into the new `references/fix.md`, which loads
  only in `fix` mode. Moved the instruction-design criteria of
  `references/best-practices.md` that the checklist and `technical-writing-ste`
  did not already cover into the checklist, dropped the duplicates, and
  removed `best-practices.md`.
- Constraints on proposed fixes that `audit` also needs (relocating misplaced
  content instead of deleting it; keeping the grammatical person of a
  `description`) are in the Repair principles.
- Added a Repair principles section in `SKILL.md`, which binds proposed fixes
  in `audit` and applied fixes in `fix`: preservation, no template
  restructuring, platform guidance as recommendations, consumer scope.
  `fix` updates affected documents only within the requested scope.
- Functional repairs:
  - The load map is built only when size, context cost, or performance is in
    question, or when a file loads on every run but only some tasks use it.
  - Consumer search is limited to the package name, folder name, and
    entry-point path in the containing repository.
  - `audit` is the default for any request that names no mode. A general
    approval applies the proposals of findings not marked as needing a
    decision and does not decide the marked findings.
  - An unanswered contradiction that affects safety, approval, or external
    actions gets the more restrictive rule as an interim fix: proposed in
    `audit`, applied in `fix` (Repair principles). The same applies to a
    missing control on such an action when any file of the package states the
    restrictive option.
  - Fixes do not invent missing facts (link targets, version history,
    identifiers, criteria). Release metadata that already disagrees is left
    unchanged and marked as needing a decision.
  - Removing misplaced content moves the information its new home lacks
    instead of deleting it; only the part that conflicts with its new home
    stays in place, as needing a decision. Information whose only new home is
    release metadata that already disagrees stays in place.
  - A broken link is repointed only when the package identifies the target; a
    file with similar content is not enough.
  - Severity: critical means the workflow cannot complete, or a defect
    (including a contradiction) can lead to unsafe, irreversible, or
    unapproved external action; a contradiction without such impact, or a
    broken reference the workflow can continue without, is high.
  - The package boundary is the entry-point folder; files outside it are
    consumers.
  - In `fix`, unanswered questions from the audit are repeated with their
    finding numbers, and findings can be marked "partly fixed". `fix` does
    not stop to wait for an answer (step 4); open questions go to Questions.
  - Changes made while release metadata is inconsistent are listed in Checks.
- Findings carry a type (`functional`, `structural`, or `language`), defined
  by observable effect (a changed invocation identifier such as `name` is
  functional; unclear cases default to functional), and "why it matters".
  "Material" is defined. `Changes` appears only in `fix` mode, and `audit`
  ends with a one-line `fix` offer.
- Duplicate handling:
  - Step 2 traces exact copies of hard rules.
  - Step 3 compares rules by subject (meaning, condition, limit, requirement
    strength) for subjects in candidate findings, as a working note.
  - The checklist classifies similar rules and maps each class to a fix:
    copy, drift, subsumption, independent-executor repetition, co-loaded
    repetition with a stated reason, and human-facing summary. It also gives
    an ordered procedure for choosing the canonical copy: load filter, class,
    layer scope, topic owner, then step owner. The first decisive item wins.
    Copies in consumers outside the package are reported unless in scope.
  - Clearly marked placeholders in examples, and `platforms.md` facts labeled
    as unchecked, are not invented facts; a file with similar content does
    not identify a link target.
  - Findings that need a decision are marked in both modes, with the interim
    fix proposed (`audit`) or applied (`fix`), or "no interim fix" and why.
- Structure checks (checklist §2):
  - a reference loaded at the start when only a later step uses it is a
    candidate finding;
  - a reference section order, not a template;
  - activation conditions belong in `description`;
  - references state their scope and load condition;
  - a table of contents above about 100 lines;
  - installation and history stay out of the entry point;
  - cross-file pointers use section headings.
- Checklist:
  - §5 points to the `technical-writing-ste` rules instead of restating them.
  - §6 checks mode-specific content in always-loaded files and references
    that load nearly every run.
  - Step 3 points to the checklist's section list instead of restating it.
- `platforms.md`:
  - Re-verified against current platform documentation. Antigravity skills
    now use `.agents/skills`. Added user-level skill paths and Claude Code
    `AGENTS.md` handling.
  - Added Anthropic authoring recommendations and the Codex metadata budget.
  - Added a fallback for facts that cannot be verified.
- Descriptions of optimizer and `technical-writing-ste` are now in third
  person.

## 2.2.1 — 2026-10-28

- Synchronized `VERSION` with this release; it remained at 2.1.0 after the
  2.2.0 documentation update.
- Preserve necessary repeated rules when independent executors cannot load
  the canonical source. Removed the checklist example that implied adding
  mandatory reporting and stopping without established requirements.
- Classify paths before checking existence and distinguish historical records
  from current dependencies and release metadata.
- Clarified conditional reference loading and allowed justified cross-skill
  reference chains instead of requiring a single level.
- Separate instruction-file sizes from inspected audit materials and identify
  overlaps; do not equate file bytes with total context cost.
- Use semantic comparison and targeted duplicate searches. Removed the
  grammatical-person prescription and limited release updates to existing
  package conventions.

## 2.2.0 — 2026-10-28

- Added `technical-writing-ste` as a dependency for language review and edits,
  with installation instructions and explicit reporting when it is unavailable.
- Kept `audit` read-only and separated functional repairs from language edits
  that must preserve behavior.
- Clarified load-map instructions and ambiguous-rule handling. Corrected a
  writing-guide example that could imply adding unstated requirements.
- Added verification of requirement strength, conditions, and action order.

## 2.1.0 — 2026-10-19

- Found while auditing `security-gate` (defaults wrong for a calling workflow, a
  gate rule living only in a conditionally loaded file, size judged without
  measuring what a run loads, consumer documentation out of step): added a load
  map (byte sizes, when each file enters context) and consumer discovery to
  step 1, a restated-rule phrase search to step 2, and the *caller mismatch* and
  conditional-only-rule items to step 3.
- Checklist items for caller defaults, pointer-condition coverage and
  typical/worst-case run load; the final report includes the load map when
  context cost was in question; consumer-side mismatches are reported to their
  owner unless in scope. No capability or safety requirement was removed.

## 2.0.2 — 2026-10-19

- Merged the large-package Scope Notes bullet into step 1 and stated the
  capability-preservation rule once (in the fix step); removed its two
  duplicate copies. No capability or safety requirement was dropped.
- Note: `references/platforms.md` was last checked 2026-07-14 (over 90 days);
  its platform facts need re-verification against current platform
  documentation. Content is unchanged.

## 2.0.1 — 2026-10-12

- Clarified incremental inspection: inventory/link map first, then coherent
  scope batches and affected incoming routes. Exhaustive requests continue
  across batches; partial/unreadable coverage remains explicit.
- Scoped verification claims to inspected and affected files; unlinked files
  are investigation candidates, not automatic deletion targets.

## 2.0.0 — 2026-10-11

- Refocused optimizer on expert audit and repair of instruction packages:
  integrity checks (links, files, names, versions), content audit
  (contradictions, duplication, ambiguity, activation, layering, safety,
  output contract), and coordinated fixes across references and documentation.
- Two modes: `audit` (report only) and `fix` (audit, apply, verify).
- Consolidated references into `checklist.md`, `best-practices.md`, and
  `platforms.md`.
- Removed the platform eval harness, scripts, schemas, and fixtures, and the
  model-specific provider notes; the skill works with the agent's own file
  tools.

## 1.8.0 — 2026-10-11 (not released; superseded by 2.0.0)

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
