"""Shared helpers for project-init tests. Windows PowerShell only."""

import os
import re
import subprocess
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "init_project.ps1"
TEMPLATE = SKILL_DIR / "assets" / "AGENTS.template.md"
TEMP_FILES = SKILL_DIR.parent / "temp-files"


def run_init(root: Path, *args: str, temp_files: Path | None = None,
             default_temp_files: bool = True) -> subprocess.CompletedProcess:
    cmd = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
           "-File", str(SCRIPT), "-ProjectRoot", str(root)]
    if default_temp_files:
        cmd += ["-TempFilesPath", str(temp_files or TEMP_FILES)]
    return subprocess.run(cmd + list(args), capture_output=True, text=True, timeout=120)


def statuses(result: subprocess.CompletedProcess) -> dict[str, str]:
    """Map reported item -> status from lines like `[created] docs - detail`."""
    found = {}
    for line in result.stdout.splitlines():
        match = re.match(r"\[([\w-]+)\] (\S+)", line)
        if match:
            found[match.group(2)] = match.group(1)
    return found


def snapshot(root: Path) -> dict[str, bytes]:
    """Bytes of every regular file under root; junctions and .git are not entered."""
    files = {}
    for current, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != ".git" and not os.path.isjunction(os.path.join(current, d))]
        for name in names:
            path = Path(current, name)
            files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


@pytest.fixture
def root(tmp_path: Path) -> Path:
    project = tmp_path / "my project"
    project.mkdir()
    return project
