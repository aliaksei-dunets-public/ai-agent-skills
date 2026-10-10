# Platform Eval Adapters

The platform configs and `scripts/run_platform_eval.py` run optimizer fixtures
through four coding-agent environments:

- OpenAI Codex;
- Google Antigravity;
- GitHub Copilot in VS Code, using Copilot CLI as an automated proxy;
- Claude Code for VS Code, using Claude CLI as an automated proxy.

## Isolation and Safety

- Every case runs in a disposable sandbox: the optional `--workspace` fixture is
  copied to a temporary directory; the real project is never passed to an agent.
- The runner installs optimizer into the sandbox at the profile's
  `install_path` without `tests/`, then verifies path, `VERSION`, and content
  hash. A mismatch or any reachable grading key blocks the case.
- A workspace that contains, or is inside, the optimizer source is rejected.
- The sandbox is hashed before and after execution; any created, modified, or
  deleted file is a safety violation and fails the case.
- Each profile declares `safety.write_protection` and `safety.verified`.
  Profiles without verified write protection (currently Copilot and
  Antigravity) are `BLOCKED` unless `--allow-unverified-sandbox` is passed.
- Bounded turns, budget, or AI credits where supported; session persistence
  disabled where supported; no shell interpolation.

## Grading

The agent prompt contains only the case and the result contract. After
execution, `scripts/grade_result.py` reads `tests/expected/<case>.json` and
reports separately:

| Field | Meaning |
|---|---|
| `execution_success` | exit code 0 and no timeout |
| `install_verified` | installed path, version, and hash match the source |
| `activation` | `verified` only when tool-call events show the skill being loaded; agent prose does not count |
| `safety` | `verified`, `unverified`, or `violation` |
| `schema_valid` | the response is one JSON object matching `schemas/eval-result.schema.json` |
| `semantic_status` | deterministic case checks: `pass`, `fail`, or `not_graded` |
| `rubric_review` | natural-language rubric items; always `pending` for a human or external judge |

Verdicts: `PASS` (everything verified), `UNVERIFIED` (correct result but
activation or write protection not proven), `FAIL`, `BLOCKED` (not executed).
A zero exit code alone never produces `PASS`.

## Dry Run

```bash
python scripts/run_platform_eval.py --platform all --dry-run
```

## Execute

```bash
python scripts/run_platform_eval.py --platform claude-vscode --case monolithic-prompt --label baseline
```

Each invocation writes to `tests/runs/<run_id>/` and never overwrites existing
results. Records include run ID, label, git SHA and dirty state, skill version
and hash, CLI version, profile config, limits, model, usage, cost, turns,
duration, and full stdout/stderr. Values a platform does not report stay
`unknown`. Timeouts keep partial output with `exit_code` 124.

## Compare Runs

```bash
python scripts/summarize_runs.py --run <run_id>
python scripts/summarize_runs.py --baseline <run_id> --candidate <run_id>
```

Summaries report success rate, median/p90/p95 duration, timeouts, safety
violations, and tokens and cost per successful task (failed attempts are
charged to successes). A comparison lists condition mismatches (case set, CLI
version, model, limits); do not claim savings when mismatches exist or usage is
`unknown`.

## IDE Smoke Tests

Copilot CLI and Claude CLI are regression proxies for their VS Code extensions.
Antigravity CLI may also differ from its IDE/standalone surface. Complete the
platform check by verifying skill discovery, references, tools, permissions,
and selected model in the target IDE.
