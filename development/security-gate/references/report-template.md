# Security Check Report Contract

This is an information contract, not a requirement to print every section or
table. Keep a clean report short and expand actionable findings. Omit empty
potential-risk, hardening, and fix-order sections, combine repeated scope and
coverage facts, and leave no template placeholders in delivered reports. Never
include secret values: write `[REDACTED]`.

## Decision

**Gate: PASS | WARN | FAIL** — one-sentence reason and what needs attention
before commit or publication. Do not imply that a chat verdict installs or
enforces a hook.

## Scope

- Project root, mode, time, and reviewed snapshot (index, HEAD SHA, or selected
  refs for history-secrets).
- Detected components/stacks and attribution basis (index vs HEAD, working tree
  vs HEAD, current files, or unavailable without Git).
- Files and areas reviewed; exclusions with reasons.
- For full, a compact per-component summary: leaks, source, configuration/CI/
  publication, dependency signals. Show unreviewed components explicitly.
- Staged versus current-file differences, untracked or ignored files, history,
  submodules, and artifacts included or excluded.

## Coverage

| Category | Method | Extent | Status | Limits |
|---|---|---|---|---|
| Leaks: secrets, personal/local data, artifacts | Location-only pattern search, file-name check, masked classification | ... | ... | ... |
| Source and security logic | Manual review of changes and related context | ... | ... | ... |
| Config / CI / publication | ... | ... | ... | ... |
| Dependency signals | Manifest and lockfile review | ... | ... | ... |

Statuses: **Completed**, **Partial**, **Not reviewable**, **N/A**. "Completed"
describes the review performed, not absence of findings. Give a reason for N/A
and Partial. History-secrets reports only the leaks row. State once that
known-vulnerability (CVE) lookup is outside this skill.

## Findings

Include **all severities**, leaks and code issues alike, sorted by severity and
action priority. State "No findings within the checked scope" when empty.

| ID | Severity / confidence | Category | Location + snapshot | Issue / impact | Gate effect |
|---|---|---|---|---|---|

For every actionable finding give:

- **Evidence:** exact file/line and snapshot; masked excerpt or structural
  description. For history-secrets: commit SHA, path, line, the refs that
  contain it, and whether the value is still in current files. Never invent a
  line.
- **Attack or exposure path:** attacker input/identity, boundary, missing
  control, affected asset, prerequisites; for leaks, who can read it once it is
  committed or published.
- **Fix:** the smallest concrete root-cause correction (for example move the
  value to an environment variable or secret store, replace the path with a
  relative or placeholder one, add the file to the ignore rules).
- **Verification:** a safe static check or regression test; a suggested test is
  not a test already run.
- **Reference:** CWE when confidently applicable; for a dependency signal the
  package, version or range, source, and the signal.

## Potential Risks / Needs Verification

| ID | Potential severity / confidence | Location + snapshot | Evidence and missing fact | Consequence | Fix or verification step |
|---|---|---|---|---|---|

Include concrete concerns, especially deployment assumptions, unverified
reachability, and candidates whose classification is uncertain. Do not present
them as confirmed. Optional hardening observations go in a short separate list
and must be grounded in this project.

## Fix Order and Remaining Gaps

1. Urgent containment: revoke and rotate likely real exposed credentials and
   review their exposure before removing them.
2. Blocking fixes before commit or publication, referencing finding IDs.
3. Medium issues, personal and local data, material unknowns, unreviewed
   content; then Low hygiene and hardening.

List excluded surfaces and exact next steps for incomplete coverage. State in
one sentence that results apply to the inspected snapshot and do not prove
absence of vulnerabilities. Never call a project clean because the diff was
empty or content could not be read.
