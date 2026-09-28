# Tooling Strategy

Select tools for the detected stack and exact snapshot. Commands are examples: verify the installed trusted executable's version/help, flags, network behavior, and exit codes. Prefer already available tools and reviewed local rules. This skill is an agent workflow, not an automatic installation script or executable Git hook.

## Execution and Evidence

- Inventory tools using the shell's lookup (`Get-Command` on PowerShell or `command -v` on POSIX); do not execute a same-named untrusted repository wrapper.
- Read configured commands before using them. Do not run `npm run security`, Make/Gradle/Maven targets, pre-commit hooks, custom Python plugins, or other project scripts just because they are named security checks.
- Do not install/resolve packages, restore dependencies, invoke builds, pull/run containers, use `npx`/`uvx` to download tools, or use auto-fix commands during a review. CodeQL extraction and some ecosystem tools may build/execute code; use existing matching analysis data or record the gap.
- In staged/commit/range modes use native snapshot support or an isolated snapshot from git-commands.md. Working-tree scans cannot attest to staged or historical content. Filter reporting by change attribution after analysis, not by discarding context before analysis.
- Capture potentially sensitive scanner output to temporary local files outside the project. Redact source snippets, credentials, URLs with embedded credentials, and personal records before exposing results. Verify that JSON/SARIF reports are redacted too; a console redaction flag may not sanitize every field in every version.
- Record command, tool/rule version, snapshot, database timestamp, duration/error, and excluded files. Interpret findings exit codes separately from crashes, timeouts, parse errors, authentication errors, or zero scanned files. Partial results remain useful but are not PASS.

## Secrets

Gitleaks examples for installed compatible versions:

```text
gitleaks git --pre-commit --staged --redact=100 --no-banner
gitleaks dir <snapshot-directory> --redact=100 --no-banner
gitleaks git <repository> --redact=100 --no-banner --log-opts=<verified-range>
```

The first checks staged changes, the second current/snapshot files, the third explicit history. Confirm supported options via `gitleaks git --help`. Use reviewed configurations and inspect suppressions/baselines; neither an ignore entry nor prior acceptance proves a credential safe. No active provider credential validation. If a scanner is unavailable, inspect narrowly with redaction and report secret-scanner coverage as partial, not equivalent.

## Source Analysis

| Detected stack | Useful candidates if already installed |
|---|---|
| JS/TS, Python, Java, Go, Ruby, PHP, other supported languages | Semgrep with reviewed rules; existing matching CodeQL/Sonar analysis |
| Python | Bandit static analysis; avoid importing target modules |
| Ruby / Rails | Brakeman |
| Go | gosec; inspect package-loading/download behavior first |
| JVM / .NET | Existing SpotBugs/FindSecBugs, CodeQL, or security analyzer results; avoid triggering a build |
| C/C++ / Rust / native code | Available static analyzers/security rules; manual memory, unsafe/FFI, integer, and parser review; compilation-based checks require separate authorization |
| Shell, PowerShell, SQL, ABAP, mobile, or unsupported language | Suitable installed native analyzers plus contextual review; explicitly report unsupported automated coverage |

Local-rule Semgrep example (replace placeholders with verified paths):

```text
semgrep scan --config <reviewed-local-rules> --metrics=off --disable-version-check --json <snapshot-directory>
```

Prefer local pinned rules. Registry/auto configurations require network access and can send project metadata; use only when compatible with the user's data constraints. Do not use cloud upload/CI modes as a substitute for local scanning. Do not enable rule validators, local builds, or auto-fix. Scanner coverage of a language does not prove coverage of the framework or all data flows.

## Dependency Vulnerabilities

Prefer lockfiles/SBOMs from the inspected snapshot. Inventory every workspace/component, including transitive and development/build dependencies that affect CI or shipped artifacts. Missing lockfiles or inconsistent manifest/lockfile resolution mean incomplete evidence; do not invent resolved versions.

In staged/commit/range review, prioritize changed manifests, lockfiles, build configuration, and dependency functionality newly used or exposed by changed code. Inspect existing packages as supporting context when needed; unrelated pre-existing advisory matches stay outside the change gate. In initial/full review, assess resolved dependencies across all components. N/A needs a scope-specific reason, not merely an unchanged lockfile.

| Evidence / ecosystem | Candidate |
|---|---|
| Supported lockfiles/SBOMs across ecosystems | OSV-Scanner; Trivy filesystem/SBOM scanning |
| npm | `npm audit --json --ignore-scripts` with existing lockfile and permitted registry queries; never `audit fix` |
| Python pinned requirements | `pip-audit --no-deps --disable-pip -r <pinned-requirements> --format json`; use only when all dependency versions are already resolved |
| Rust | `cargo audit --json` against the exact Cargo.lock; database access may be needed |
| Go | govulncheck only when its module-loading/network behavior is permitted; otherwise analyze lock/module evidence and advisories without running the package |
| Ruby | Bundler Audit against Gemfile.lock, with database freshness recorded |
| JVM, .NET, PHP, Swift, other | Available lockfile/SBOM audit tools or official advisories for known resolved packages; avoid restore/build/plugin execution |

OSV v2 example (confirm installed CLI syntax):

```text
osv-scanner scan source -r <snapshot-directory>
```

Avoid High-only output filtering: Medium findings also belong in the report. Public advisory queries can disclose package names/versions; separate private identities and internal registries. Use supported offline modes with an existing database where needed. A missing or stale cache/network failure yields a gap. Query official vendor advisories, OSV, GHSA or ecosystem advisory databases for affected/fixed ranges; do not invent a version from memory.

For each match preserve advisory ID/URL, package and resolved version, dependency path, direct/transitive status, runtime/build/dev use, and reachable/plausible/unknown vulnerable functionality. A confirmed affected package is not automatically a confirmed exploitable application. No fixed version available is a valid result; give concrete mitigation or removal options.

## Configuration, Infrastructure, Containers, and CI

Use relevant installed tools such as Trivy config/filesystem, Checkov, Hadolint, or actionlint after checking their extensions and network behavior. Prefer static configuration parsing; do not run Terraform plans, Helm plugins, local workflow scripts, or containers. Containerfile review does not establish image vulnerability status; scanning an image needs the exact intended digest and a permitted image/database source. Report absent image evidence.

Review IaC/CI/publish boundaries manually even when tools pass: identity permissions, untrusted inputs, secret exposure, artifact inclusion, and privilege. Repository settings on a hosting service are optional external context, not a prerequisite for local staged review. Do not claim branch protection, secret scanning, or dependency controls are enabled from workflow files alone. The optional templates are for separately requested setup; never install them during a scan.

## Missing Tools / Offline Operation

Continue manual analysis. State what ran, what failed or was unavailable, and the smallest next step for the missing category. A meaningful missing check yields WARN unless a known blocker already yields FAIL. Do not ask the user to install an entire scanner suite before providing the findings already supported by evidence.
