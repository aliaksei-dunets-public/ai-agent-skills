# Severity, Evidence, and Gate Policy

Rate actual impact and attack prerequisites. A scanner's CVSS rating describes its advisory, not automatically the application's exposure. Severity and confidence are separate fields.

| Severity | Contextual examples |
|---|---|
| Critical | Broad unauthenticated code execution, universal account takeover, mass sensitive-data compromise, broadly privileged production signing/admin credential exposure. |
| High | Sensitive cross-user/tenant access, command/SQL injection with serious impact, privilege escalation, privileged CI execution, exploitable deserialization or internal SSRF. |
| Medium | Demonstrated bounded exposure or abuse, meaningful misconfiguration, replay with limited impact. |
| Low | Low-impact issue or evidence-backed defense-in-depth weakness. |
| Informational | Non-vulnerable observation, applicable future control, or coverage note. |

Do not automatically classify all SQL injection as Critical, all authenticated issues as Medium, all wildcard CORS as vulnerable, or all root containers as Medium. Determine reachable assets, identity/credentials, permissions, and deployment assumptions. A placeholder token is not an exposed live credential; a hardcoded placeholder used as a real signing key can still be a vulnerability.

## Confidence and Classification

- **High:** the relevant path/asset and missing control are established. For dependencies, an exact affected version can be confirmed independently of exploitability.
- **Medium:** evidence is strong but a specific runtime, configuration, or reachability fact is missing. State that fact and a verification step.
- **Low:** weak or pattern-only evidence. Omit generic guesses; retain only concrete useful observations with their limitations.

Put unverified claims in **Potential risks / Needs verification**, not in confirmed findings. Keep an affected dependency's advisory severity and application reachability separate. Do not reduce impact just because certainty is low.

## Gate Rules (Apply in This Order)

1. **FAIL** if the applicable scope contains a confirmed High/Critical vulnerability, a likely real exposed credential/private key, or a High/Critical affected dependency with evidenced reachable/plausible vulnerable use. Classify secrets from format and context without attempting authentication. A changed control that creates a demonstrated serious exposure is a finding; a tool being disabled alone does not prove exploitation.
2. Otherwise **WARN** for confirmed Medium issues, material unverified risks (including unresolved High/Critical dependency reachability), or material coverage gaps/errors. Missing tools for applicable categories, unsupported components, stale/unavailable advisory data, an incomplete snapshot, and unresolved conflicts are gaps. A no-findings scanner crash is not PASS.
3. Otherwise **PASS**, permitting Low/Informational observations. All applicable categories must have adequate documented coverage; mark a category N/A only with a concrete reason. Manual contextual source review is useful but does not silently replace missing automated SAST or dependency coverage.

An empty explicitly requested staged review yields WARN / “nothing staged; no commit content assessed.” In project mode an empty index does not stop the project audit; show the staged gate as N/A. For non-Git full/project reviews, absent Git metadata alone is not a coverage failure.

## Scope and Attribution

- Project/full gates consider pre-existing issues in the reviewed current project.
- Staged/commit/range gates consider issues introduced, worsened, or newly exposed by those changes, including a removed guard that exposes an unchanged sink. Use surrounding code from the target snapshot.
- Explicit project mode also assesses the index changes separately when present. An unstaged fix cannot clear the staged-change gate. Overall status is the worse of the project and staged results.
- Findings outside an explicitly narrow scope remain visible when incidentally discovered but do not silently change that scope's gate.
- Baselines indicate prior review, not safety. Record accepted-risk documentation if supplied; do not create exceptions or suppress existing secrets yourself.

PASS is a scoped result, not certification or a guarantee of safe deployment.
