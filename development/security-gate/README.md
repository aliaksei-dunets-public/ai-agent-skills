# Security Gate

General-purpose project security review. It adapts to the project's stack and available tools, and returns its report in the language of the request. By default, it checks **staged changes and related code**. Use **initial/full** for a first audit of the entire project.

## Usage

Invoke the skill in an agent chat that has access to the `security-gate` folder:

```text
$security-gate
```

Review the version that will enter the commit. This accounts for partial staging with `git add -p`: a fix that exists only in the working file does not hide a vulnerability in the index. If nothing is staged, the skill reports that and does not silently replace the requested scope with a whole-project audit.

```text
$security-gate initial — audit the entire project before its first release
```

An initial audit examines the current files of all components: code, secrets, direct and transitive dependencies, configuration, CI/CD, infrastructure, and packaging rules. It includes pre-existing issues and does not require staged changes. `full` is an alias for `initial`. Git history has a separate mode; inaccessible files and unavailable tools are disclosed as coverage limits.

Additional requests:

```text
$security-gate project — audit the entire project and separately review the prospective commit
$security-gate working-tree — review all local changes
$security-gate — review commit <SHA>
$security-gate — review changes between <base> and <target>
$security-gate history-secrets — check Git history for leaked secrets
$security-gate initial — save the report to SECURITY-REPORT.md
```

These are example requests to the agent, not shell commands.

## Results

- `FAIL`: substantiated blocking issues were found.
- `WARN`: material risks, medium-severity issues, or incomplete coverage remain.
- `PASS`: no blocking issues or warnings were found in the reviewed scope; this does not guarantee that no vulnerabilities exist.

The report includes confirmed vulnerabilities at every severity, a separate list of potential risks, file/line and version, impact, evidence, a fix, and a way to verify it. For initial/full reviews, it also reports coverage for each project component. Secrets are replaced with `[REDACTED]`.

The skill uses available scanners and manual analysis. Missing scanners, an outdated vulnerability database, or an unverified dependency version cannot be treated as a successful check. Project code is not run, packages are not installed, and fixes or commits are not applied automatically. The report is returned in chat; a file is created on request.

## Package contents

- `SKILL.md` — the main workflow and mode selection.
- `references/` — Git handling, tools, review categories, risk assessment, report format, and scope-specific rules (`scopes.md`). `sources.md` is maintainer material (research basis); the agent does not load it.
- `agents/openai.yaml` — skill metadata and an example invocation in the Codex interface.
- `evals/` — maintainer material, not loaded at run time: behavioral scenarios, criteria, and activation examples.
- `templates/` — maintainer material: optional examples for configuring hooks and CI. They are not installed when the skill runs; the skill itself does not technically block `git commit`.
