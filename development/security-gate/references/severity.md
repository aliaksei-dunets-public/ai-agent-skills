# Severity, Evidence, and Gate Policy

Rate actual impact and attack prerequisites. Severity and confidence are
separate fields.

| Severity | Contextual examples |
|---|---|
| Critical | Broad unauthenticated code execution, universal account takeover, mass sensitive-data compromise, broadly privileged production signing/admin credential exposure. |
| High | Sensitive cross-user/tenant access, command/SQL injection with serious impact, privilege escalation, privileged CI execution, exploitable deserialization or internal SSRF, an effective credential or private key. |
| Medium | Demonstrated bounded exposure or abuse, meaningful misconfiguration, replay with limited impact, personal or local data that would be published. |
| Low | Low-impact issue, harmless committed artifact, or evidence-backed defense-in-depth weakness. |
| Informational | Non-vulnerable observation, applicable future control, or coverage note. |

Do not automatically classify all SQL injection as Critical, all authenticated
issues as Medium, all wildcard CORS as vulnerable, or all root containers as
Medium. Determine reachable assets, identity/credentials, permissions, and
deployment assumptions. A placeholder token is not an exposed live credential;
a hardcoded placeholder used as a real signing key can still be a
vulnerability.

## Confidence and Classification

- **High:** the relevant path or asset and the missing control are established.
- **Medium:** evidence is strong but a specific runtime, configuration, or
  reachability fact is missing. State that fact and a verification step.
- **Low:** weak or pattern-only evidence. Omit generic guesses; keep only
  concrete useful observations with their limitations.

Put unverified claims in **Potential risks / Needs verification**, not in
confirmed findings. Do not reduce impact just because certainty is low.

## Gate Rules (Apply in This Order)

1. **FAIL** if the applicable scope contains a confirmed High/Critical issue, a
   likely effective credential or private key, or bulk real personal records of
   other people. Classify secrets from format and context without attempting
   authentication. In history-secrets a likely effective credential in any
   selected ref is FAIL even when current files are clean.
2. Otherwise **WARN** for:
   - confirmed Medium issues;
   - personal or local data that would be published: absolute paths revealing
     a user name, a real person's personal email, internal host names or
     private IP addresses, system or client identifiers, artifacts holding such
     data;
   - material unverified risks, including dependency signals that need a
     decision (see the checklist);
   - content that could not be reviewed: unresolved conflicts, missing LFS
     objects or submodule commits, unreadable files, binaries that may hold
     secrets, stale snapshot;
   - an empty staged scope, or a Git-only mode without Git.
3. Otherwise **PASS**, permitting Low/Informational observations. Every
   applicable category (leaks, changed code and its context, configuration/CI/
   publication, dependency signals) must have been reviewed; mark a category
   N/A only with a concrete reason, such as no dependency files in scope.

Coverage is the review actually performed. The absence of external scanners,
and known-vulnerability lookup being outside this skill, are not gaps and do
not turn PASS into WARN. Advisory evidence supplied by the user (for example a
Dependabot alert) may be cited; never take CVEs or fixed versions from memory.

## Scope and Attribution

- Full gates consider pre-existing issues in the reviewed current files.
- Staged and working-tree gates consider issues introduced, worsened, or newly
  exposed by the changes, including a removed guard that exposes an unchanged
  sink. Use surrounding code from the same snapshot. An unstaged fix cannot
  clear the staged gate.
- History-secrets gates consider leaks in the selected refs only.
- Findings outside an explicitly narrow scope remain visible when incidentally
  discovered but do not change that scope's gate.
- Allowlists and baselines indicate prior review, not safety. Record supplied
  accepted-risk documentation; do not create exceptions or suppress existing
  secrets yourself.

PASS is a scoped result, not certification or a guarantee of safe deployment.
