from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from sync_tasks import TASK_ID_RE, load_tasks


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip()).strip("-").lower()
    return slug or "task"


def next_task_id(open_tasks: list[dict[str, str]], close_tasks: list[dict[str, str]]) -> str:
    numbers = [int(task["id"].split("-", 1)[1]) for task in open_tasks + close_tasks if TASK_ID_RE.fullmatch(task["id"])]
    return f"TASK-{max(numbers, default=0) + 1:04d}"


def task_content(*, task_id: str, title: str, task_type: str, priority: str, now: str, plan: str, dependencies: str) -> str:
    return f"""---
id: {task_id}
title: {title!r}
type: {task_type}
priority: {priority}
status: created
execution_state: ready
revision: 1
created: {now}
updated: {now}
dependencies: {dependencies or 'none'}
---

### Objective
{title}

### Scope
- Implement the approved requirements described by the plan.

### Acceptance criteria
- The implementation satisfies the approved plan and its validation steps.

### Implementation plan
- Source plan: {plan}

### Review history
none

### Approval
- Approved: no
- Approved by: none
- Approved at: none

### Testing
none

### Documentation
none

### Completed work
none

### Work log
none

### Blockers
none
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a task in docs/plan/open and regenerate indexes.")
    parser.add_argument("--title", required=True, help="Task title")
    parser.add_argument("--plan", required=True, help="Path to the approved implementation plan")
    parser.add_argument("--type", default="feature", dest="task_type")
    parser.add_argument("--priority", choices=("critical", "high", "medium", "low"), default="medium")
    parser.add_argument("--dependencies", default="none")
    parser.add_argument("--task-id", help="Optional stable task ID; otherwise allocate the next ID")
    parser.add_argument(
        "--tasks-root",
        type=Path,
        default=Path.cwd() / "docs" / "plan",
        help="Task store root containing open/ and close/ (default: ./docs/plan)",
    )
    args = parser.parse_args(argv)

    tasks_root = args.tasks_root.resolve()
    open_dir = tasks_root / "open"
    close_dir = tasks_root / "close"
    path: Path | None = None
    try:
        open_tasks = load_tasks(open_dir, closed=False)
        close_tasks = load_tasks(close_dir, closed=True)
        task_id = args.task_id or next_task_id(open_tasks, close_tasks)
        if not TASK_ID_RE.fullmatch(task_id):
            raise ValueError(f"invalid task id {task_id!r}")
        if any(task["id"] == task_id for task in open_tasks + close_tasks):
            raise ValueError(f"task id already exists: {task_id}")

        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        base = f"{date}-{slugify(args.title)}"
        filename = f"{base}.md"
        suffix = 2
        while (open_dir / filename).exists() or (close_dir / filename).exists():
            filename = f"{base}-{suffix}.md"
            suffix += 1

        open_dir.mkdir(parents=True, exist_ok=True)
        close_dir.mkdir(parents=True, exist_ok=True)
        path = open_dir / filename
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(task_content(
                task_id=task_id,
                title=args.title,
                task_type=args.task_type,
                priority=args.priority,
                now=now,
                plan=args.plan,
                dependencies=args.dependencies,
            ))
        subprocess.run(
            [sys.executable, str(Path(__file__).with_name("sync_tasks.py")), "--tasks-root", str(tasks_root)],
            check=True,
        )
        print(f"Created {task_id} at {path}.")
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        if path is not None and path.exists():
            path.unlink()
        print(f"Task creation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
