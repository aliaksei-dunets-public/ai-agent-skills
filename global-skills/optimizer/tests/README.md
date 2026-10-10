# Optimizer Self-Test Fixtures

- `cases/*.md` — the only fixture text an agent under evaluation receives.
- `expected/*.json` — grading keys, read only by `scripts/grade_result.py`
  after execution. They are never placed in prompts and are excluded from
  sandbox installations.
- `unit/` — deterministic tests for the scripts; no LLM required.
- `runs/` — local eval results (one directory per run ID); not package content.

## Expected spec format

```json
{
  "rubric": {"required": ["..."], "forbidden": ["..."]},
  "checks": {
    "mode": "standard",
    "min_findings": 1,
    "max_findings": 5,
    "no_material_issue": false,
    "no_measured_metrics": true,
    "report_language": "ru",
    "required_concepts": [{"id": "routing", "any": ["rout", "index"]}],
    "forbidden_patterns": [{"id": "fabricated-savings", "pattern": "\\d+\\s*%\\s*saving"}]
  }
}
```

`checks` are deterministic and decide `semantic_status`. Concept regexes are
coarse signals, not proof of a correct audit, so `rubric` items remain
`pending` until a human or external judge reviews them. Every check key is
optional; `mode` must match the case's `Mode:` line.

## Commands

```bash
python -B -m unittest discover -s tests/unit
python scripts/grade_result.py --case zero-findings --response saved-stdout.txt --format stream-json
```

Use `-B` so test runs do not leave `__pycache__`, which the validator rejects.

## Pass criteria beyond deterministic checks

- all required root causes detected;
- no invented critical findings;
- no recommendation to remove required safety controls;
- correct reference routing;
- evidence and confidence labels present;
- output stays within the requested mode;
- response compression retains required evidence and validation;
- agent handoffs contain deltas rather than narrative history;
- default reports contain only important findings, changes, conditional
  questions, and metrics; deep appendices only when explicitly requested;
- user-facing report language follows explicit instruction or the latest
  substantive user request, while technical tokens remain unchanged.
