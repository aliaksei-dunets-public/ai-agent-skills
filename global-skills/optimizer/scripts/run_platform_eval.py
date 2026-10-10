#!/usr/bin/env python3
"""Run optimizer self-test fixtures through supported coding-agent CLIs.

Every case runs in a disposable sandbox: the optional fixture workspace is
copied into a temporary directory, optimizer is installed there without its
`tests/` directory, and the sandbox is hashed before and after execution.
The agent never sees `tests/expected/`; grading happens afterwards.

Verdicts:
  PASS        executed, schema valid, checks pass, no mutation, activation and
              write protection verified
  UNVERIFIED  everything above except activation or write protection proof
  FAIL        execution, schema, semantic, or sandbox-mutation failure
  BLOCKED     not executed: unverified write protection without opt-in,
              installation mismatch, or grading-key leak
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform as host_platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True  # keep the package free of __pycache__
sys.path.insert(0, str(Path(__file__).resolve().parent))
from grade_result import activation_status, extract_response, grade  # noqa: E402
from install_platform import TARGETS, install, tree_hash  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS = {
    "codex": "codex.json",
    "google-antigravity": "google-antigravity.json",
    "github-copilot-vscode": "github-copilot-vscode.json",
    "claude-vscode": "claude-vscode.json",
}
CONTRACT = (
    "Return only one JSON object that conforms to `schemas/eval-result.schema.json` "
    "of the installed optimizer skill. Do not create, modify, or delete files.\n\n"
)


def load_mode(case_text: str) -> str:
    for line in case_text.splitlines():
        if line.lower().startswith("mode:"):
            return line.split(":", 1)[1].strip()
    return "standard"


def render_command(template: list[str], values: dict[str, str]) -> list[str]:
    rendered = []
    for item in template:
        try:
            rendered.append(item.format(**values))
        except KeyError as exc:
            raise ValueError(f"missing command placeholder: {exc.args[0]}") from exc
    return rendered


def prompt_for(config: dict, case_text: str) -> str:
    """Build the agent prompt from the case only; expected files are never read here."""
    prefix = config["prompt_prefix"].format(mode=load_mode(case_text))
    return prefix + CONTRACT + "Fixture:\n" + case_text.strip() + "\n"


def as_text(value) -> str:
    """TimeoutExpired output is bytes even with text=True."""
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def snapshot(root: Path) -> dict[str, str]:
    files = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            files[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return files


def mutations(before: dict[str, str], after: dict[str, str], ignore: list[str]) -> list[str]:
    changed = []
    for rel in sorted(set(before) | set(after)):
        if any(rel == p or rel.startswith(p.rstrip("/") + "/") for p in ignore):
            continue
        if rel not in after:
            changed.append(f"deleted {rel}")
        elif rel not in before:
            changed.append(f"created {rel}")
        elif before[rel] != after[rel]:
            changed.append(f"modified {rel}")
    return changed


def expected_hashes(root: Path) -> set[str]:
    return {hashlib.sha256(p.read_bytes()).hexdigest() for p in (root / "tests/expected").glob("*") if p.is_file()}


def leaked_files(sandbox: Path, keys: set[str]) -> list[str]:
    return [rel for rel, digest in snapshot(sandbox).items() if digest in keys]


def overlaps(a: Path, b: Path) -> bool:
    return a == b or a in b.parents or b in a.parents


def git_revision(root: Path) -> dict:
    def git(*args: str) -> str | None:
        try:
            done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, timeout=20, check=False)
        except (OSError, subprocess.SubprocessError):
            return None
        return done.stdout.strip() if done.returncode == 0 else None

    sha = git("rev-parse", "HEAD")
    status = git("status", "--porcelain", "--", ".")
    return {"git_sha": sha or "unknown", "git_dirty": None if status is None else bool(status)}


def cli_version(config: dict, executable: str) -> str:
    command = config.get("version_command")
    if not command:
        return "unknown"
    try:
        done = subprocess.run([executable, *command[1:]], capture_output=True, text=True, timeout=30,
                              check=False, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    out = (done.stdout or done.stderr).strip()
    return out.splitlines()[0] if done.returncode == 0 and out else "unknown"


def verdict(record: dict) -> str:
    if record.get("blocked_reason"):
        return "BLOCKED"
    if not record["execution_success"] or record["safety"] == "violation":
        return "FAIL"
    if not record["schema_valid"] or record["semantic_status"] != "pass":
        return "FAIL"
    if record["activation"] != "verified" or record["safety"] != "verified":
        return "UNVERIFIED"
    return "PASS"


def write_record(out_dir: Path, record: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    output = out_dir / f"{record['platform']}--{record['case']}.json"
    with output.open("x", encoding="utf-8") as handle:  # never overwrite a previous result
        json.dump(record, handle, indent=2, ensure_ascii=False)
    return output


def run_one(config: dict, case_path: Path, workspace: Path | None, out_dir: Path, timeout: int,
            dry_run: bool, values: dict[str, str], context: dict, allow_unverified: bool,
            keep_sandbox: bool) -> dict:
    case = case_path.stem
    prompt = prompt_for(config, case_path.read_text(encoding="utf-8"))
    safety = config.get("safety", {})
    record = {
        **context,
        "platform": config["platform"],
        "surface": config["surface"],
        "case": case,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
        "config": config,
        "limits": {"timeout_s": timeout, **values},
        "dry_run": dry_run,
        "ide_smoke_test_required": config.get("ide_smoke_test_required", False),
        "blocked_reason": None,
        "execution_success": False,
        "timed_out": False,
        "install_verified": False,
        "activation": "unverified",
        "safety": "verified" if safety.get("verified") else "unverified",
        "workspace_mutations": [],
        "schema_valid": False,
        "semantic_status": "not_graded",
        "rubric_review": "pending",
        "cli_version": "unknown",
        "model": "unknown",
        "usage": "unknown",
        "cost_usd": "unknown",
        "num_turns": "unknown",
    }
    if not safety.get("verified") and not allow_unverified:
        record["blocked_reason"] = (
            f"write protection for {config['platform']} is not verified "
            f"({safety.get('write_protection', 'none')}); pass --allow-unverified-sandbox to run "
            "it inside the disposable sandbox anyway"
        )
    if dry_run:
        record["command"] = render_command(config["command_template"],
                                           {**values, "workspace": "<sandbox>", "prompt": "<prompt>"})
        record["verdict"] = "BLOCKED" if record["blocked_reason"] else "DRY"
        return record
    if record["blocked_reason"]:
        record["verdict"] = "BLOCKED"
        write_record(out_dir, record)
        return record

    sandbox_root = Path(tempfile.mkdtemp(prefix="optimizer-eval-"))
    sandbox = sandbox_root / "workspace"
    if keep_sandbox:
        record["sandbox"] = str(sandbox_root)
    try:
        if workspace:
            shutil.copytree(workspace, sandbox, symlinks=True)
        else:
            sandbox.mkdir()
        target = install(ROOT, sandbox, config["platform"], "copy", force=True, dry_run=False, exclude_dev=True)
        installed_hash = tree_hash(target)
        record.update({
            "installed_skill_hash": installed_hash,
            "installed_version": (target / "VERSION").read_text(encoding="utf-8").strip(),
            "install_path": target.relative_to(sandbox).as_posix(),
        })
        record["install_verified"] = (
            installed_hash == context["skill_hash"]
            and record["installed_version"] == context["skill_version"]
            and record["install_path"] == config["install_path"]
        )
        leaks = leaked_files(sandbox, expected_hashes(ROOT))
        if leaks:
            record["blocked_reason"] = f"grading keys reachable in sandbox: {leaks}"
        elif not record["install_verified"]:
            record["blocked_reason"] = "installed skill does not match source path, version, or hash"
        if record["blocked_reason"]:
            record["verdict"] = "BLOCKED"
            write_record(out_dir, record)
            return record

        executable = shutil.which(config["executable"])
        command = render_command(config["command_template"],
                                 {**values, "workspace": str(sandbox), "prompt": prompt})
        record["command"] = command
        if executable is None:
            record.update({"exit_code": 127, "duration_ms": 0, "stdout": "",
                           "stderr": f"executable not found: {config['executable']}"})
        else:
            record["cli_version"] = cli_version(config, executable)
            before = snapshot(sandbox)
            started = time.monotonic()
            try:
                done = subprocess.run([executable, *command[1:]], cwd=sandbox, text=True,
                                      encoding="utf-8", errors="replace", capture_output=True,
                                      timeout=timeout, check=False, stdin=subprocess.DEVNULL,
                                      env=os.environ.copy())
                record.update({"exit_code": done.returncode, "stdout": done.stdout, "stderr": done.stderr})
            except subprocess.TimeoutExpired as exc:
                record.update({"exit_code": 124, "timed_out": True, "stdout": as_text(exc.stdout),
                               "stderr": as_text(exc.stderr) + f"\ntimeout after {timeout}s"})
            record["duration_ms"] = round((time.monotonic() - started) * 1000)
            changed = mutations(before, snapshot(sandbox), config.get("ignore_paths", []))
            record["workspace_mutations"] = changed
            if changed:
                record["safety"] = "violation"

        record["execution_success"] = record["exit_code"] == 0
        extracted = extract_response(config.get("output_format", "text"), record["stdout"])
        record["activation"] = activation_status(config, extracted["events"])
        for key in ("usage", "cost_usd", "num_turns", "model"):
            if extracted.get(key) is not None:
                record[key] = extracted[key]
        spec = json.loads((ROOT / "tests/expected" / f"{case}.json").read_text(encoding="utf-8"))
        graded = grade(extracted["text"], spec)
        record.update(graded)
        record["response_text"] = extracted["text"]
        record["verdict"] = verdict(record)
        write_record(out_dir, record)
        return record
    finally:
        if not keep_sandbox:
            shutil.rmtree(sandbox_root, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--platform", choices=[*PLATFORMS, "all"], required=True)
    parser.add_argument("--workspace", type=Path,
                        help="fixture directory copied into the sandbox; default is an empty workspace")
    parser.add_argument("--case", default="all")
    parser.add_argument("--out", type=Path, default=ROOT / "tests/runs")
    parser.add_argument("--run-id", help="default: UTC timestamp plus random suffix")
    parser.add_argument("--label", default="", help="for example baseline or candidate")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--max-turns", default="8")
    parser.add_argument("--budget-usd", default="1.00")
    parser.add_argument("--credit-limit", default="5")
    parser.add_argument("--allow-unverified-sandbox", action="store_true",
                        help="run profiles whose CLI write protection is unverified (sandbox only)")
    parser.add_argument("--keep-sandbox", action="store_true")
    parser.add_argument("--strict", action="store_true", help="treat UNVERIFIED as failure")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workspace = args.workspace.resolve() if args.workspace else None
    if workspace and not workspace.is_dir():
        print(f"ERROR: workspace is not a directory: {workspace}", file=sys.stderr)
        return 2
    if workspace and overlaps(workspace, ROOT):
        print("ERROR: workspace must not contain or be inside the optimizer source", file=sys.stderr)
        return 2
    case_paths = sorted((ROOT / "tests/cases").glob("*.md"))
    if args.case != "all":
        case_paths = [ROOT / "tests/cases" / f"{args.case}.md"]
    missing = [p for p in case_paths if not p.exists()]
    if missing:
        print(f"ERROR: missing case: {missing[0]}", file=sys.stderr)
        return 2

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-") + uuid.uuid4().hex[:6]
    out_dir = args.out.resolve() / run_id
    if out_dir.exists() and not args.dry_run:
        print(f"ERROR: run directory already exists: {out_dir}", file=sys.stderr)
        return 2
    context = {
        "run_id": run_id,
        "label": args.label,
        **git_revision(ROOT),
        "skill_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
        "skill_hash": tree_hash(ROOT, exclude_dev=True),
        "host": {"os": host_platform.platform(), "python": host_platform.python_version()},
    }
    values = {"max_turns": args.max_turns, "budget_usd": args.budget_usd, "credit_limit": args.credit_limit}
    platforms = list(PLATFORMS) if args.platform == "all" else [args.platform]
    counts: dict[str, int] = {}
    for name in platforms:
        config = json.loads((ROOT / "evals/platforms" / PLATFORMS[name]).read_text(encoding="utf-8"))
        for case_path in case_paths:
            record = run_one(config, case_path, workspace, out_dir, args.timeout, args.dry_run, values,
                             context, args.allow_unverified_sandbox, args.keep_sandbox)
            counts[record["verdict"]] = counts.get(record["verdict"], 0) + 1
            reason = f" ({record['blocked_reason']})" if record.get("blocked_reason") else ""
            print(f"{record['verdict']} {name}/{case_path.stem}{reason}")
    print(f"run_id={run_id} " + " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    bad = counts.get("FAIL", 0) + (0 if args.dry_run else counts.get("BLOCKED", 0))
    if args.strict:
        bad += counts.get("UNVERIFIED", 0)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
