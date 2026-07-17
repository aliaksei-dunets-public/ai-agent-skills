from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from sync_tasks import VALID_EXECUTION_STATES, VALID_STATUSES, load_tasks, parse_frontmatter


STATUS_TRANSITIONS = {
    "created": {"in_progress"},
    "in_progress": {"review"},
    "review": {"approved", "in_progress"},
    "approved": {"done", "in_progress"},
}


def _atomic_write(path: Path, content: str) -> None:
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def _set_frontmatter_value(content: str, key: str, value: str) -> str:
    pattern = re.compile(rf"(?m)^{re.escape(key)}:\s*.*$")
    updated, count = pattern.subn(f"{key}: {value}", content, count=1)
    if count != 1:
        raise ValueError(f"frontmatter field {key!r} is missing")
    return updated


def _append_to_section(content: str, heading: str, message: str) -> str:
    pattern = re.compile(rf"(?ms)^(### {re.escape(heading)})\r?\n(.*?)(?=^### |\Z)")
    match = pattern.search(content)
    if not match:
        raise ValueError(f"task section {heading!r} is missing")
    body = match.group(2).rstrip()
    if body == "none":
        body = ""
    replacement = match.group(1) + "\n"
    if body:
        replacement += body + "\n"
    replacement += f"- {message}\n\n"
    return content[: match.start()] + replacement + content[match.end() :]


def _section_body(content: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^### {re.escape(heading)}\r?\n(.*?)(?=^### |\Z)")
    match = pattern.search(content)
    return match.group(1) if match else ""


def _set_approval_evidence(content: str, *, approved_by: str, approved_at: str) -> str:
    """Set canonical approval fields without leaving contradictory values."""
    pattern = re.compile(r"(?ms)^(### Approval)\r?\n(.*?)(?=^### |\Z)")
    match = pattern.search(content)
    if not match:
        raise ValueError("task section 'Approval' is missing")
    body = match.group(2)
    replacements = {
        "Approved": "yes",
        "Approved by": approved_by,
        "Approved at": approved_at,
    }
    for field, value in replacements.items():
        field_pattern = re.compile(rf"(?im)^- {re.escape(field)}:\s*.*$")
        body, count = field_pattern.subn(f"- {field}: {value}", body, count=1)
        if count == 0:
            body = body.rstrip() + f"\n- {field}: {value}\n"
    return content[: match.start(2)] + body + content[match.end(2) :]


def _validate_completion(content: str) -> None:
    required_sections = {
        "Objective", "Scope", "Acceptance criteria", "Implementation plan",
        "Review history", "Approval", "Testing", "Documentation",
        "Completed work", "Work log", "Blockers",
    }
    for section in required_sections:
        if not _section_body(content, section).strip():
            raise ValueError(f"completion requires non-empty section {section!r}")

    approval = _section_body(content, "Approval")
    if not re.search(r"(?im)^-\s*approved:\s*yes\s*$", approval):
        raise ValueError("completion requires explicit approval evidence")
    if not re.search(r"(?im)^-\s*approved by:\s*\S+", approval):
        raise ValueError("completion requires approved-by evidence")
    if not re.search(r"(?im)^-\s*approved at:\s*\S+", approval):
        raise ValueError("completion requires approved-at evidence")

    for section in ("Testing", "Documentation", "Completed work"):
        body = _section_body(content, section).strip().lower()
        if body in {"none", "- none", "n/a", "- n/a"}:
            raise ValueError(f"completion requires evidence in {section!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and update one task record using a JSON payload.")
    parser.add_argument("task_id", help="Task ID (e.g., TASK-0005)")
    parser.add_argument("--apply", type=Path, help="Path to JSON file containing updates", required=True)
    parser.add_argument(
        "--tasks-root",
        type=Path,
        default=Path.cwd() / ".ai" / "task-manager",
        help="Task store root containing open/ and close/ (default: ./.ai/task-manager)",
    )
    args = parser.parse_args(argv)

    task_id = args.task_id if args.task_id.startswith("TASK-") else f"TASK-{args.task_id}"
    tasks_root = args.tasks_root.resolve()
    try:
        open_tasks = load_tasks(tasks_root / "open", closed=False)
        close_tasks = load_tasks(tasks_root / "close", closed=True)
    except (OSError, ValueError) as exc:
        print(f"Task lookup failed: {exc}", file=sys.stderr)
        return 1
    matches = [task for task in open_tasks + close_tasks if task["id"] == task_id]
    if not matches:
        print(f"Task file for {task_id} was not found in open/ or close/.", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(f"Task id {task_id} is duplicated in open/ and close/.", file=sys.stderr)
        return 1
    target = Path(matches[0]["_path"])
    open_path = tasks_root / "open" / target.name
    close_path = tasks_root / "close" / target.name

    try:
        update_data = json.loads(args.apply.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Failed to read or parse JSON file {args.apply}: {exc}", file=sys.stderr)
        return 1

    try:
        content = target.read_text(encoding="utf-8")
        metadata = parse_frontmatter(target)
        current_status = metadata["status"]

        is_close = bool(update_data.get("close", update_data.get("archive")))
        if target.parent.name == "close" and not is_close:
            raise ValueError("close tasks are immutable")
        
        if is_close:
            if target != open_path:
                raise ValueError("only open tasks can be closed")
            if close_path.exists():
                raise FileExistsError(f"close task already exists: {close_path}")
            if current_status != "approved":
                raise ValueError(f"close requires status approved, got {current_status}")
            _validate_completion(content)
            requested_status = "done"
        else:
            requested_status = update_data.get("status")

        if update_data.get("approve") and not requested_status:
            requested_status = "approved"
        if requested_status == "approved" and current_status != "approved" and not update_data.get("approve"):
            raise ValueError("transition to approved requires explicit approval evidence")

        if requested_status:
            if requested_status != current_status:
                allowed_transitions = STATUS_TRANSITIONS.get(current_status, set())
                if requested_status not in allowed_transitions:
                    raise ValueError(f"invalid status transition: {current_status} -> {requested_status}")
                content = _set_frontmatter_value(content, "status", requested_status)
        
        requested_state = update_data.get("state")
        if requested_state is not None and requested_state not in VALID_EXECUTION_STATES:
            raise ValueError(f"invalid execution state {requested_state!r}")
        if requested_state is None and requested_status == "in_progress":
            requested_state = "running"
        if requested_state is None and requested_status == "review":
            requested_state = "waiting_approval"
        if requested_state is not None:
            content = _set_frontmatter_value(content, "execution_state", requested_state)
            
        if is_close:
            content = _set_frontmatter_value(content, "execution_state", "ready")

        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        content = _set_frontmatter_value(content, "updated", now)
        
        if update_data.get("log"):
            content = _append_to_section(content, "Work log", f"[{now}] {update_data['log']}")
        if update_data.get("review"):
            content = _append_to_section(content, "Review history", update_data["review"])
        if update_data.get("approve"):
            if current_status not in {"review", "approved"} and requested_status != "approved":
                raise ValueError(f"approval requires status review or approved, got {current_status}")
            content = _set_approval_evidence(content, approved_by="user", approved_at=now)
        if update_data.get("test_evidence"):
            content = _append_to_section(content, "Testing", update_data["test_evidence"])
        if update_data.get("coverage_evidence"):
            content = _append_to_section(content, "Testing", f"Coverage evidence: {update_data['coverage_evidence']}")
        if update_data.get("documentation_evidence"):
            content = _append_to_section(content, "Documentation", update_data["documentation_evidence"])
        if update_data.get("completed_work"):
            content = _append_to_section(content, "Completed work", update_data["completed_work"])

        _atomic_write(target, content)
        if is_close:
            target.replace(close_path)
            try:
                subprocess.run(
                    [sys.executable, str(Path(__file__).with_name("sync_tasks.py")), "--tasks-root", str(tasks_root)],
                    check=True,
                )
            except Exception:
                close_path.replace(target)
                raise
            print(f"Closed {task_id} to {close_path}.")
        else:
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("sync_tasks.py")), "--tasks-root", str(tasks_root)],
                check=True,
            )
            print(f"Updated {task_id}.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"Task update failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
