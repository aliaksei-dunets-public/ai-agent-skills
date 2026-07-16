from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


REQUIRED_KEYS = {
    "id",
    "title",
    "type",
    "priority",
    "status",
    "execution_state",
    "revision",
    "created",
    "updated",
    "dependencies",
}
VALID_STATUSES = {"created", "in_progress", "review", "approved", "done"}
VALID_EXECUTION_STATES = {"ready", "running", "waiting_approval", "blocked"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
TASK_ID_RE = re.compile(r"^TASK-\d+$")


class TaskFormatError(ValueError):
    """Raised when a task record does not satisfy the canonical schema."""


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(filepath: Path) -> dict[str, str]:
    lines = filepath.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise TaskFormatError(f"{filepath}: YAML frontmatter must start at line 1")

    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise TaskFormatError(f"{filepath}: closing frontmatter delimiter is missing") from exc

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise TaskFormatError(f"{filepath}:{line_number}: invalid frontmatter line")
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in REQUIRED_KEYS:
            raise TaskFormatError(f"{filepath}:{line_number}: unsupported key {key!r}")
        if key in metadata:
            raise TaskFormatError(f"{filepath}:{line_number}: duplicate key {key!r}")
        metadata[key] = _unquote(value)

    missing = REQUIRED_KEYS - metadata.keys()
    if missing:
        raise TaskFormatError(f"{filepath}: missing keys: {', '.join(sorted(missing))}")
    if not TASK_ID_RE.fullmatch(metadata["id"]):
        raise TaskFormatError(f"{filepath}: invalid task id {metadata['id']!r}")
    if metadata["status"] not in VALID_STATUSES:
        raise TaskFormatError(f"{filepath}: invalid status {metadata['status']!r}")
    if metadata["execution_state"] not in VALID_EXECUTION_STATES:
        raise TaskFormatError(f"{filepath}: invalid execution_state {metadata['execution_state']!r}")
    if metadata["priority"].lower() not in VALID_PRIORITIES:
        raise TaskFormatError(f"{filepath}: invalid priority {metadata['priority']!r}")
    for key in ("created", "updated"):
        try:
            datetime.fromisoformat(metadata[key].replace("Z", "+00:00"))
        except ValueError as exc:
            raise TaskFormatError(f"{filepath}: invalid {key} timestamp") from exc
    return metadata


def load_tasks(directory: Path, *, completed: bool) -> list[dict[str, str]]:
    if not directory.exists():
        return []
    tasks = []
    seen_ids: set[str] = set()
    for filepath in sorted(directory.glob("TASK-*.md")):
        task = parse_frontmatter(filepath)
        if task["id"] in seen_ids:
            raise TaskFormatError(f"{directory}: duplicate task id {task['id']}")
        seen_ids.add(task["id"])
        if completed and task["status"] != "done":
            raise TaskFormatError(f"{filepath}: completed task must have status done")
        tasks.append(task)
    return tasks


def priority_score(priority: str) -> int:
    return {"critical": 1, "high": 2, "medium": 3, "low": 4}[priority.lower()]


def sort_tasks(tasks: list[dict[str, str]]) -> list[dict[str, str]]:
    return sorted(
        tasks,
        key=lambda task: (
            priority_score(task["priority"]),
            datetime.fromisoformat(task["created"].replace("Z", "+00:00")),
            task["id"],
        ),
    )


def _cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def generate_markdown_table(tasks: list[dict[str, str]], *, active: bool) -> str:
    lines = [
        "| ID | Title | Type | Priority | Status | Execution state | Link |",
        "|---|---|---|---|---|---|---|",
    ]
    for task in tasks:
        folder = "active" if active else "completed"
        link = f"[Details]({folder}/{task['id']}.md)" if active else f"[Details]({task['id']}.md)"
        lines.append(
            "| "
            + " | ".join(
                _cell(task[key])
                for key in ("id", "title", "type", "priority", "status", "execution_state")
            )
            + f" | {link} |"
        )
    return "\n".join(lines)


def _atomic_write(path: Path, content: str) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def write_indexes(tasks_dir: Path, active_tasks: list[dict[str, str]], completed_tasks: list[dict[str, str]]) -> None:
    active_content, completed_content = render_indexes(active_tasks, completed_tasks)
    _atomic_write(tasks_dir / "tasks.md", active_content)
    completed_dir = tasks_dir / "completed"
    _atomic_write(completed_dir / "completed-tasks.md", completed_content)


def render_indexes(active_tasks: list[dict[str, str]], completed_tasks: list[dict[str, str]]) -> tuple[str, str]:
    """Build canonical index contents without touching the filesystem."""
    active_content = (
        "# Active Tasks\n\n"
        "<!--\n"
        "  Canonical operational task source for development-orchestrator.\n"
        "  Required statuses: created | in_progress | review | approved | done\n"
        "  Required execution states: ready | running | waiting_approval | blocked\n"
        "  Generated by .ai/scripts/sync_tasks.py; do not edit manually.\n"
        "-->\n\n"
        + generate_markdown_table(active_tasks, active=True)
        + "\n"
    )
    completed_content = (
        "# Completed Tasks\n\n"
        "Completed task records preserve the original plan, acceptance criteria,\n"
        "review evidence, approval, test results, coverage, documentation,\n"
        "completed work, and final status.\n\n"
        + generate_markdown_table(completed_tasks, active=False)
        + "\n"
    )
    return active_content, completed_content


def check_indexes(tasks_dir: Path, active_tasks: list[dict[str, str]], completed_tasks: list[dict[str, str]]) -> None:
    """Fail when generated indexes are absent or drift from task records."""
    expected_active, expected_completed = render_indexes(active_tasks, completed_tasks)
    actual_active = (tasks_dir / "tasks.md").read_text(encoding="utf-8")
    actual_completed = (tasks_dir / "completed" / "completed-tasks.md").read_text(encoding="utf-8")
    if actual_active != expected_active or actual_completed != expected_completed:
        raise TaskFormatError("generated task indexes are stale; run sync_tasks.py")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate task frontmatter and regenerate task indexes.")
    parser.add_argument(
        "--tasks-root",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "tasks",
        help="Task store root containing active/ and completed/ (default: repository .ai/tasks)",
    )
    parser.add_argument("--check", action="store_true", help="Validate records without writing indexes")
    args = parser.parse_args(argv)
    tasks_dir = args.tasks_root.resolve()
    try:
        active_tasks = sort_tasks(load_tasks(tasks_dir / "active", completed=False))
        completed_tasks = sort_tasks(load_tasks(tasks_dir / "completed", completed=True))
        if args.check:
            check_indexes(tasks_dir, active_tasks, completed_tasks)
        else:
            write_indexes(tasks_dir, active_tasks, completed_tasks)
        print(f"Validated {len(active_tasks)} active and {len(completed_tasks)} completed tasks.")
        return 0
    except (OSError, TaskFormatError, KeyError) as exc:
        print(f"Task index validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
