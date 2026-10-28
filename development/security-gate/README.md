# Security Gate

Pre-commit security review for any project. The agent reads the code itself, with no external scanners: it looks for leaked secrets, credentials, personal and local data, and unwanted files, then reviews the changed code and its related context for vulnerabilities. It returns the report in the language of the request. By default it checks **staged changes and related code**.

## Usage

Invoke the skill in an agent chat that has access to the `security-gate` folder:

```text
$security-gate
```

It reviews the version that will enter the commit. This accounts for partial staging with `git add -p`: a fix that exists only in the working file does not hide a vulnerability in the index. If nothing is staged, the skill reports that and does not silently switch to a whole-codebase audit.

Other modes:

```text
$security-gate working-tree — review all local changes, staged or not
$security-gate full — audit the whole codebase for leaks and vulnerabilities
$security-gate history-secrets — check Git history for leaked secrets
$security-gate full — save the report to SECURITY-REPORT.md
```

These are example requests to the agent, not shell commands. "Initial audit" and "check the entire project" also select `full`. Git history is searched only in `history-secrets`.

## Results

- `FAIL`: an effective secret or private key, bulk real personal records, or a confirmed High/Critical vulnerability.
- `WARN`: Medium issues, personal or local data (user paths, personal email, internal hosts), unresolved risks, content that could not be reviewed, or an empty staged scope.
- `PASS`: nothing blocking or warning in the reviewed scope; this does not guarantee that no vulnerabilities exist.

The report lists findings of every severity with file/line, impact, evidence, a fix, and a way to verify it, plus a separate list of potential risks. A full audit also shows coverage for each project component. Secret searches print locations only. Candidate line contents are withheld by default; partial excerpts require a verified local redaction method. Uncertain classification remains an explicit coverage limit.

The skill uses only its own reading and read-only Git. It does not run scanners, project code, or package managers, does not install anything, and does not apply fixes or commits. Known-vulnerability (CVE) lookup for dependencies is out of scope; use Dependabot or dependency review for it. The skill does check changed dependencies for supply-chain signals such as unpinned versions, Git URLs, or install scripts. The report is returned in chat; a file is created on request.

## Package contents

- `SKILL.md`: the workflow and mode selection.
- `references/`: Git commands per mode, leak patterns and safe searching, the review checklist, severity and gate policy, and the report format.
- `agents/openai.yaml`: skill metadata and an example invocation for the Codex interface.
- `evals/`: maintainer material, not loaded at run time: behavioral scenarios, criteria, and activation examples.

## Research basis

Maintainer material; the agent does not load it.

- Git diff, raw objects, and grep: https://git-scm.com/docs/git-diff, https://git-scm.com/docs/git-cat-file, https://git-scm.com/docs/git-grep
- OWASP Top 10:2025: https://owasp.org/Top10/2025/
- MITRE CWE Top 25: https://cwe.mitre.org/top25/
- NIST Secure Software Development Framework (SSDF): https://csrc.nist.gov/projects/ssdf
- GitHub secret scanning and push protection: https://docs.github.com/en/code-security/concepts/secret-security/about-push-protection
- Agent Skills specification: https://agentskills.io/
- Anthropic skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
