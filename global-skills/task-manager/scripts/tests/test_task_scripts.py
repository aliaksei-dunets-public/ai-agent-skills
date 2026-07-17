from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
SYNC = SCRIPT_DIR / "sync_tasks.py"
UPDATE = SCRIPT_DIR / "update_task.py"
CREATE = SCRIPT_DIR / "create_task.py"


TASK = """---
id: TASK-9000
title: "Script lifecycle test"
type: improvement
priority: medium
status: created
execution_state: ready
revision: 1
created: 2026-07-13T00:00:00Z
updated: 2026-07-13T00:00:00Z
dependencies: none
---

### Objective
Verify the task lifecycle.

### Scope
- Task scripts only.

### Acceptance criteria
- State transitions and indexes remain valid.

### Implementation plan
- Run the lifecycle tests.

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


class TaskScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / ".ai" / "task-manager"
        (self.root / "open").mkdir(parents=True)
        (self.root / "close").mkdir()
        (self.root / "open" / "TASK-9000.md").write_text(TASK, encoding="utf-8")
        self.run_script(SYNC, "--tasks-root", self.root)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_script(self, script: Path, *args: object, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(script), *(str(arg) for arg in args)],
            check=check,
            capture_output=True,
            text=True,
            cwd=cwd,
        )

    def apply(self, payload: dict[str, object], task_id: str = "TASK-9000", check: bool = True) -> subprocess.CompletedProcess[str]:
        payload_path = Path(self.tmp.name) / "update.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        return self.run_script(UPDATE, task_id, "--apply", payload_path, "--tasks-root", self.root, check=check)

    def test_check_detects_index_drift(self) -> None:
        index = self.root / "open-tasks.md"
        index.write_text(index.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        result = self.run_script(SYNC, "--tasks-root", self.root, "--check", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale", result.stderr)

    def test_create_uses_task_filename_links_plan_and_selects_task(self) -> None:
        plan = Path(self.tmp.name) / "docs" / "plans" / "cache-plan.md"
        plan.parent.mkdir(parents=True)
        plan.write_text("# Cache plan", encoding="utf-8")
        result = self.run_script(CREATE, "--title", "Add API cache", "--plan", "docs/plans/cache-plan.md", "--tasks-root", self.root, cwd=Path(self.tmp.name))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TASK-9001", result.stdout)
        created = list((self.root / "open").glob("TASK-9001.md"))
        self.assertEqual(len(created), 1)
        self.assertIn("[docs/plans/cache-plan.md](../../docs/plans/cache-plan.md)", created[0].read_text(encoding="utf-8"))
        selected = self.run_script(SYNC, "--tasks-root", self.root, "--select-next")
        self.assertIn("TASK-9000", selected.stdout)
        self.assertIn("open", selected.stdout)

    def test_missing_dependency_fails_validation(self) -> None:
        invalid = TASK.replace("TASK-9000", "TASK-9001").replace("dependencies: none", "dependencies: TASK-9999")
        (self.root / "open" / "TASK-9001.md").write_text(invalid, encoding="utf-8")
        result = self.run_script(SYNC, "--tasks-root", self.root, "--check", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not exist", result.stderr)

    def test_approval_requires_explicit_approval_flag(self) -> None:
        self.apply({"status": "in_progress", "log": "Started"})
        self.apply({"status": "review", "review": "Independent review passed"})
        rejected = self.apply({"status": "approved"}, check=False)
        self.assertNotEqual(rejected.returncode, 0)
        self.apply({"approve": True, "review": "User approved"})
        content = (self.root / "open" / "TASK-9000.md").read_text(encoding="utf-8")
        self.assertIn("status: approved", content)
        self.assertIn("- Approved: yes", content)

    def test_close_moves_date_named_file_and_syncs_indexes(self) -> None:
        self.apply({"status": "in_progress", "log": "Started"})
        self.apply({"status": "review", "review": "Independent review passed"})
        self.apply({"approve": True, "review": "User approved"})
        self.apply({
            "test_evidence": "Unit tests passed",
            "documentation_evidence": "Task documentation updated",
            "completed_work": "Lifecycle implementation completed",
        })
        result = self.apply({"close": True})
        self.assertIn("Closed TASK-9000", result.stdout)
        self.assertFalse((self.root / "open" / "TASK-9000.md").exists())
        closed = self.root / "close" / "TASK-9000.md"
        self.assertTrue(closed.exists())
        self.assertIn("status: done", closed.read_text(encoding="utf-8"))
        self.assertEqual(self.run_script(SYNC, "--tasks-root", self.root, "--check").returncode, 0)


if __name__ == "__main__":
    unittest.main()
