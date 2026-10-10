#!/usr/bin/env python3
"""Aggregate optimizer eval runs and compare a baseline with a candidate.

Only measured values are reported. Missing usage or cost stays `unknown`;
no savings are derived from partial data.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUCCESS = {"PASS", "UNVERIFIED"}
# Fields that must match for a fair baseline/candidate comparison.
CONDITIONS = ("cli_version", "model", "limits")


def load_run(run_dir: Path) -> list[dict]:
    records = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(run_dir.glob("*.json"))]
    if not records:
        raise FileNotFoundError(f"no records in {run_dir}")
    return records


def percentile(values: list[float], pct: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(pct / 100 * len(ordered)) - 1)]


def total_tokens(usage) -> int | None:
    if not isinstance(usage, dict):
        return None
    # Claude reports cache traffic separately; Codex cached_input_tokens is a subset of input_tokens.
    keys = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    values = [usage[k] for k in keys if isinstance(usage.get(k), (int, float))]
    return int(sum(values)) if values else None


def summarize(records: list[dict]) -> dict:
    executed = [r for r in records if r.get("verdict") not in {"BLOCKED", "DRY"}]
    successes = [r for r in executed if r.get("verdict") in SUCCESS]
    verdicts: dict[str, int] = {}
    for r in records:
        verdicts[r.get("verdict", "unknown")] = verdicts.get(r.get("verdict", "unknown"), 0) + 1
    durations = [r["duration_ms"] for r in executed if isinstance(r.get("duration_ms"), (int, float))]
    tokens = [total_tokens(r.get("usage")) for r in executed]
    costs = [r.get("cost_usd") for r in executed]
    tokens_known = bool(executed) and all(t is not None for t in tokens)
    costs_known = bool(executed) and all(isinstance(c, (int, float)) for c in costs)
    summary = {
        "records": len(records),
        "executed": len(executed),
        "verdicts": verdicts,
        "success_rate": round(len(successes) / len(executed), 4) if executed else "unknown",
        "timeouts": sum(1 for r in executed if r.get("timed_out")),
        "safety_violations": sum(1 for r in executed if r.get("safety") == "violation"),
        "activation_unverified": sum(1 for r in executed if r.get("activation") != "verified"),
        "duration_ms": {
            "median": statistics.median(durations),
            "p90": percentile(durations, 90),
            "p95": percentile(durations, 95),
        } if durations else "unknown",
        "total_tokens": sum(tokens) if tokens_known else "unknown",
        "total_cost_usd": round(sum(costs), 6) if costs_known else "unknown",
    }
    # Failed attempts still cost tokens, so they are charged to the successful tasks.
    if successes and tokens_known:
        summary["tokens_per_successful_task"] = round(sum(tokens) / len(successes), 1)
    else:
        summary["tokens_per_successful_task"] = "unknown"
    if successes and costs_known:
        summary["cost_per_successful_task_usd"] = round(sum(costs) / len(successes), 6)
    else:
        summary["cost_per_successful_task_usd"] = "unknown"
    return summary


def by_platform(records: list[dict]) -> dict[str, dict]:
    groups: dict[str, list[dict]] = {}
    for r in records:
        groups.setdefault(r["platform"], []).append(r)
    return {name: summarize(items) for name, items in sorted(groups.items())}


def condition_mismatches(base: list[dict], cand: list[dict]) -> list[str]:
    issues = []
    base_cases = {(r["platform"], r["case"]) for r in base}
    cand_cases = {(r["platform"], r["case"]) for r in cand}
    if base_cases != cand_cases:
        issues.append("platform/case sets differ")
    for field in CONDITIONS:
        b = {json.dumps(r.get(field), sort_keys=True) for r in base}
        c = {json.dumps(r.get(field), sort_keys=True) for r in cand}
        if b != c:
            issues.append(f"{field} differs")
    return issues


def delta(before, after):
    if isinstance(before, (int, float)) and isinstance(after, (int, float)):
        return round(after - before, 6)
    return "unknown"


def compare(base: list[dict], cand: list[dict]) -> dict:
    base_sum, cand_sum = by_platform(base), by_platform(cand)
    result = {"condition_mismatches": condition_mismatches(base, cand), "platforms": {}}
    for name in sorted(set(base_sum) | set(cand_sum)):
        b, c = base_sum.get(name, {}), cand_sum.get(name, {})
        result["platforms"][name] = {
            key: {"baseline": b.get(key, "unknown"), "candidate": c.get(key, "unknown"),
                  "delta": delta(b.get(key), c.get(key))}
            for key in ("success_rate", "tokens_per_successful_task", "cost_per_successful_task_usd",
                        "timeouts", "safety_violations")
        }
        bd, cd = b.get("duration_ms"), c.get("duration_ms")
        result["platforms"][name]["median_duration_ms"] = {
            "baseline": bd["median"] if isinstance(bd, dict) else "unknown",
            "candidate": cd["median"] if isinstance(cd, dict) else "unknown",
            "delta": delta(bd["median"] if isinstance(bd, dict) else None,
                           cd["median"] if isinstance(cd, dict) else None),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=Path, default=ROOT / "tests/runs")
    parser.add_argument("--run", help="summarize one run_id")
    parser.add_argument("--baseline", help="baseline run_id")
    parser.add_argument("--candidate", help="candidate run_id")
    args = parser.parse_args()
    try:
        if args.baseline and args.candidate:
            output = compare(load_run(args.runs / args.baseline), load_run(args.runs / args.candidate))
        elif args.run:
            output = by_platform(load_run(args.runs / args.run))
        else:
            parser.error("pass --run or both --baseline and --candidate")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
