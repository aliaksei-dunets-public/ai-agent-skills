# Skill Trigger Evals

## Should Trigger

- `$security-gate`
- Проверь staged-изменения и связанный код перед коммитом.
- Security check before I publish these changes.
- `$security-gate initial` — проверь весь проект полностью.
- Perform an initial security audit of this non-Git project folder.
- Review this PR for auth, injection, dependency, and CI risks.
- Audit commit `abc123` for vulnerabilities and leaked credentials.
- Check this new MCP server or agent hook for security issues.
- Scan local Git history for exposed keys and tokens.

## Should Not Trigger

- Refactor this class for readability.
- Explain what OWASP is without reviewing code.
- Write a penetration-testing exploit against a live target.
- Produce compliance certification for this repository.
- Review only formatting and naming conventions.

## Expected Behavior

1. Bare invocation and pre-commit requests default to staged and related index context.
2. Initial/full explicitly audits current contents of all components, even with no staged changes; no implicit history scan or suppression baseline.
3. Empty staged scope is WARN, not PASS or an automatic full audit.
4. Does not execute project code, install tools, change files, or configure hooks during review.
5. Uses available trusted scanners plus contextual reasoning; errors and missing checks are visible.
6. Redacts suspected secrets before output and never validates credentials against providers.
7. Returns all confirmed findings and evidence-backed potential risks with fixes and verification steps.
8. Returns PASS/WARN/FAIL consistent with scope, confidence, and coverage.
