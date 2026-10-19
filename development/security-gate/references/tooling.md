# Tooling Strategy

Select tools for the detected stack and the exact snapshot. Commands are examples: verify the installed trusted executable's version/help, flags, network behavior, and exit codes. Prefer tools that are already available and reviewed local rules. This skill is an agent workflow, not an installer or an executable Git hook; the prohibitions in SKILL.md ("Authority and data boundaries") apply to every tool below.

## Execution and Evidence

- Inventory tools with the shell's lookup (`Get-Command` on PowerShell, `command -v` on POSIX). Never execute a same-named wrapper from the repository.
- Read configured commands before using them. Do not run `npm run security`, Make/Gradle/Maven targets, pre-commit hooks, custom plugins, or other project scripts just because they are named security checks.
- Do not use `npx`/`uvx` to download tools or auto-fix commands. CodeQL extraction and some ecosystem tools build or execute code: use existing matching analysis data or record the gap.
- In staged/commit/range modes use native snapshot support or an isolated snapshot from git-commands.md. Working-tree scans cannot attest to staged or historical content. Filter reporting by change attribution after analysis, not by dropping context before it.
- Capture potentially sensitive output in temporary local files outside the project. Redact snippets, credentials, URLs with embedded credentials, and personal records before returning anything. Verify that JSON/SARIF reports are redacted too: a console redaction flag may not sanitize every field in every version.
- Record command, tool/rule version, snapshot, database timestamp, duration or error, and excluded files. Interpret findings exit codes separately from crashes, timeouts, parse errors, authentication errors, and zero scanned files. Partial results remain useful but are not PASS.

## Secrets

Use an installed secret scanner that can redact its output. Check its help for redaction, staged/directory/history input, and network behavior, then run it on the exact snapshot:

| Scope | Input |
|---|---|
| staged / commit / range | Native staged mode, or a private snapshot directory (git-commands.md) |
| current files (initial, full, project, working-tree) | The project directory |
| history-secrets | Only the explicitly selected refs or range |

Use reviewed configuration and inspect suppressions and baselines: neither an ignore entry nor prior acceptance proves a credential safe. No active provider credential validation.

Without a scanner, search manually and report secret coverage as Partial, never as equivalent. Print locations only (`file:line`), never matched text:

- current or index content: `git grep -I -n -E <patterns>` (`--cached` for the index);
- a selected revision: the same command with the verified SHA, or `git log -G <pattern> --format=%H -- <path>` to list the commits that touched a match;
- patterns: private-key headers, provider token prefixes, URLs with embedded credentials, and high-entropy assignments to sensitive names (`password`, `secret`, `token`, `api_key`).

## Source Analysis

| Detected stack | Useful candidates if already installed |
|---|---|
| JS/TS, Python, Java, Go, Ruby, PHP, other supported languages | Semgrep with reviewed rules; existing matching CodeQL/Sonar analysis |
| Ruby / Rails | Brakeman |
| Go | gosec; inspect package-loading/download behavior first |
| JVM / .NET | Existing SpotBugs/FindSecBugs, CodeQL, or security analyzer results; avoid triggering a build |
| C/C++ / Rust / native code | Available static analyzers/security rules; manual memory, unsafe/FFI, integer, and parser review; compilation-based checks need separate authorization |
| Shell, PowerShell, SQL, ABAP, mobile, or unsupported language | Suitable installed native analyzers plus contextual review; explicitly report unsupported automated coverage |

Never import target modules to analyze them (Python included). Local-rule Semgrep example (replace placeholders with verified paths):

```text
semgrep scan --config <reviewed-local-rules> --metrics=off --disable-version-check --json <snapshot-directory>
```

Prefer local pinned rules. Registry/auto configurations need network access and can send project metadata; use them only when compatible with the user's data constraints. Do not use cloud upload/CI modes as a substitute for local scanning, and do not enable rule validators, local builds, or auto-fix. Scanner coverage of a language does not prove coverage of the framework or all data flows.

## Dependency Vulnerabilities

Prefer lockfiles/SBOMs from the inspected snapshot. Inventory every workspace/component, including transitive and development/build dependencies that affect CI or shipped artifacts. A missing lockfile, unpinned range, or inconsistent manifest/lockfile resolution is incomplete evidence: do not invent resolved versions or run a package manager to resolve them.

- Staged/commit/range: prioritize changed manifests, lockfiles, build configuration, and dependency functionality newly used or exposed by changed code. Existing packages are supporting context; unrelated pre-existing advisory matches stay outside the change gate.
- Initial/full: assess resolved dependencies across all components. N/A needs a scope-specific reason, not merely an unchanged lockfile.

| Evidence / ecosystem | Candidate |
|---|---|
| Supported lockfiles/SBOMs across ecosystems, including pinned Python requirements and lock files | OSV-Scanner; Trivy filesystem/SBOM scanning |
| npm | `npm audit --json --ignore-scripts` with an existing lockfile and permitted registry queries; never `audit fix` |
| Rust | `cargo audit --json` against the exact Cargo.lock; database access may be needed |
| Go | govulncheck only when its module-loading/network behavior is permitted; otherwise analyze lock/module evidence and advisories without running the package |
| Ruby | Bundler Audit against Gemfile.lock, with database freshness recorded |
| JVM, .NET, PHP, Swift, other | Available lockfile/SBOM audit tools or official advisories for known resolved packages; avoid restore/build/plugin execution |

OSV v2 example (confirm installed CLI syntax):

```text
osv-scanner scan source -r <snapshot-directory>
```

Do not filter output to High only: Medium findings belong in the report. Public advisory queries disclose package names/versions, so keep private identities and internal registries out of them; use supported offline modes with an existing database where needed. A missing or stale cache or a network failure is a gap. Take affected and fixed ranges from official vendor advisories, OSV, GHSA, or ecosystem databases; never from memory.

For each match keep the advisory ID/URL, package and resolved version, dependency path, direct/transitive status, runtime/build/dev use, and reachable/plausible/unknown vulnerable functionality. An affected package is not automatically an exploitable application. "No fixed version available" is a valid result: give a concrete mitigation or removal option.

## Configuration, Infrastructure, Containers, and CI

Use relevant installed tools such as Trivy config/filesystem, Checkov, Hadolint, or actionlint after checking their extensions and network behavior. Prefer static parsing; do not run Terraform plans, Helm plugins, local workflow scripts, or containers. A Containerfile review does not establish image vulnerability status: scanning an image needs the exact intended digest and a permitted image/database source, and absent image evidence is reported.

Review IaC/CI/publish boundaries manually even when tools pass: identity permissions, untrusted inputs, secret exposure, artifact inclusion, and privilege. Repository settings on a hosting service are optional external context. Do not claim branch protection, secret scanning, or dependency controls are enabled from workflow files alone. The optional checklist in `templates/` is for separately requested setup; never apply it during a scan.

## Missing Tools / Offline Operation

Continue manual analysis. State what ran, what failed or was unavailable, and the smallest next step for the missing category. A meaningful missing check yields WARN unless a known blocker already yields FAIL. Do not ask the user to install a whole scanner suite before reporting the findings already supported by evidence.
