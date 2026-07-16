from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1]
if not (SCRIPT_DIR / "sync_tasks.py").exists():
    SCRIPT_DIR = Path(__file__).resolve().parent
SYNC = SCRIPT_DIR / "sync_tasks.py"
UPDATE = SCRIPT_DIR / "update_task.py"


TASK = """---
id: TASK-9000
title: \"Script lifecycle test\"
type: improvement
priority: medium
status: created
execution_state: ready
revision: 1
created: 2026-07-13T00:00:00Z
updated: 2026-07-13T00:00:00Z
dependencies: none
---

### Review history
- Final result: passed
Historical code-review failed finding was fixed in a later run.

### Approval
- approved: yes

### Testing
- Unit: passed — unit test
- Integration: not_applicable — no integration scope
- Coverage: not_configured — project has no coverage command

### Documentation
- Status: updated — task script contract documented

### Completed work
- Added lifecycle script verification.

### Work log
none

### Blockers
none
"""


class TaskScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd() / ".tmp")
        self.root = Path(self.tmp.name) / "tasks"
        (self.root / "active").mkdir(parents=True)
        (self.root / "completed").mkdir()
        (self.root / "active" / "TASK-9000.md").write_text(TASK, encoding="utf-8")
        subprocess.run([sys.executable, str(SYNC), "--tasks-root", str(self.root)], check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_check_detects_index_drift(self) -> None:
        index = self.root / "tasks.md"
        index.write_text(index.read_text(encoding="utf-8") + "\nmanual drift\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(SYNC), "--tasks-root", str(self.root), "--check"], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("stale", result.stderr)

    def test_archive_sets_ready_and_syncs_indexes(self) -> None:
        subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--status", "in_progress", "--tasks-root", str(self.root)], check=True)
        subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--status", "review", "--tasks-root", str(self.root)], check=True)
        subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--status", "approved", "--tasks-root", str(self.root)], check=True)
        result = subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--archive", "--tasks-root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        completed = self.root / "completed" / "TASK-9000.md"
        self.assertIn("status: done", completed.read_text(encoding="utf-8"))
        self.assertIn("execution_state: ready", completed.read_text(encoding="utf-8"))
        self.assertEqual(subprocess.run([sys.executable, str(SYNC), "--tasks-root", str(self.root), "--check"]).returncode, 0)

    def test_approve_updates_canonical_fields(self) -> None:
        subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--status", "in_progress", "--tasks-root", str(self.root)], check=True)
        subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--status", "review", "--tasks-root", str(self.root)], check=True)
        result = subprocess.run([sys.executable, str(UPDATE), "TASK-9000", "--approve", "--tasks-root", str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        content = (self.root / "active" / "TASK-9000.md").read_text(encoding="utf-8")
        self.assertIn("- Approved: yes", content)
        self.assertIn("- Approved by: user", content)
        self.assertRegex(content, r"- Approved at: \d{4}-\d{2}-\d{2}T")
        self.assertNotIn("- Approved: no", content)


if __name__ == "__main__":
    unittest.main()
