# Security Check Report Contract

Use the user's language. Keep an empty report short; expand actionable findings. Do not leave unresolved template placeholders in delivered reports.

## Decision

**Overall: PASS | WARN | FAIL** — one-sentence reason and what needs attention before commit/publication.

For project mode, add **Project gate** and **Staged-change gate** (N/A when nothing is staged). Do not imply that a chat verdict installs or enforces a hook.

## Scope

- Project/root, mode, time, target revision(s), and reviewed snapshot(s).
- Detected components/stacks and attribution basis (HEAD, parent, merge base, or unavailable).
- Changed files reviewed and project areas inspected; identify sampling/exclusions.
- For initial/full audits, include a compact per-component coverage summary covering each detected stack, its source, secrets, dependencies, and configuration. Show unreviewed components explicitly.
- Staged versus current-file differences, untracked/ignored files, history/submodules/artifacts included or excluded.

## Coverage

| Category | Tool/version or manual method | Snapshot / extent | Status | Evidence / limitations |
|---|---|---|---|---|
| Secrets and sensitive data | ... | ... | ... | ... |
| Source / SAST | ... | ... | ... | ... |
| Dependencies / advisories | ... | ... | ... | ... |
| Config / IaC / CI / publication | ... | ... | ... | ... |
| Contextual security analysis | ... | ... | ... | ... |

Statuses: **Completed**, **Partial**, **Unavailable**, **Error**, **N/A**. “Completed” describes execution, not absence of findings. Give a reason for N/A and gaps. Include actual sanitized commands, exit status, rules/database freshness, and significant suppressions in brief notes where relevant. Never claim scans ran without results.

## Confirmed Vulnerabilities

Include **all severities**, not only blockers. Sort by severity and action priority. State “No confirmed vulnerabilities found within the checked scope” when empty.

| ID | Severity / confidence | Location + snapshot | Attribution | Issue / impact | Gate effect |
|---|---|---|---|---|---|

For every actionable finding give:

- **Evidence:** exact file/line and snapshot; sanitized excerpt or structural description. Use an artifact/config key or advisory ID when a source line is unavailable; never invent a line.
- **Attack path and impact:** attacker input/identity, boundary, missing control, affected asset, and realistic prerequisites. For configuration/secrets use the equivalent exposure path.
- **Fix:** smallest concrete root-cause correction.
- **Verification:** safe regression test or static check; suggested tests are not tests already run.
- **Reference:** CWE when confidently applicable; for dependencies include advisory URL/ID, resolved version, dependency path, affected range, runtime/build/dev use, reachability, verified fixed version or “not verified / no fix available”.

## Potential Risks / Needs Verification

| ID | Potential severity / confidence | Location + snapshot | Evidence and missing fact | Consequence | Fix or verification step |
|---|---|---|---|---|---|

Include concrete concerns by default, especially deployment assumptions, scanner-only candidates, and unverified reachability. Do not present them as confirmed vulnerabilities. State “None identified” when empty. Optional hardening observations belong in a short separate list and must be grounded in this project.

## Fix Order and Remaining Gaps

1. Urgent containment/rotation for likely real exposed credentials or active exposure.
2. Blocking fixes before commit/publication, referencing finding IDs.
3. Resolve material unknowns, Medium issues, and missing checks; then Low hardening work.

List excluded surfaces and exact next steps for incomplete coverage. Explain in one sentence that results apply to the inspected snapshots and do not prove absence of vulnerabilities. Never call a project clean because tools failed or the diff was empty.
