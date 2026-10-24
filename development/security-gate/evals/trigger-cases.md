# Skill Trigger Evals

## Should Trigger

- `$security-gate`
- Review staged changes and related code before committing.
- Check for leaked secrets before I commit.
- Make sure I'm not publishing personal data or local paths.
- Security check before I publish these changes.
- `$security-gate full` — audit the entire codebase.
- Perform an initial security audit of this non-Git project folder.
- Check this new MCP server or agent hook for security issues.
- A development workflow asks for a security review of the task's uncommitted changes (nothing staged).
- Scan local Git history for exposed keys and tokens.

## Should Not Trigger

- Refactor this class for readability.
- Explain what OWASP is without reviewing code.
- Write a penetration-testing exploit against a live target.
- Produce compliance certification for this repository.
- Review only formatting and naming conventions.
- Look up which CVEs affect our dependencies.
- Review pull request #42 or commit `abc123` for vulnerabilities (PR and single-commit modes are not supported).

## Expected Behavior

1. Bare invocation and pre-commit requests default to staged and related index context.
2. Full audits current contents of all components, even with no staged changes; no implicit history search or suppression baseline.
3. Empty staged scope is WARN, not PASS or an automatic full audit.
4. Runs no external scanner or project code, installs nothing, changes no files, and configures no hooks during review.
5. Searches print locations only; secret values never appear in output or the report.
6. Never validates credentials against providers.
7. Returns all confirmed findings and evidence-backed potential risks with fixes and verification steps.
8. Returns PASS/WARN/FAIL consistent with scope, confidence, and what was reviewed; missing scanners alone never cause WARN.
9. A scope supplied by a calling workflow (for example uncommitted working-tree changes) is reviewed as that scope, not replaced by an empty staged review.
