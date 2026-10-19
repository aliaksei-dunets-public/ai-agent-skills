"""Shared helpers for temp-files tests. Windows PowerShell only."""

import os
import subprocess
import time
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "clean_tmp.ps1"


def run_clean(project_root: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
         "-File", str(SCRIPT), "-ProjectRoot", str(project_root), *args],
        capture_output=True, text=True, cwd=cwd or project_root, timeout=120,
    )


def make_file(path: Path, age_days: float, content: str = "x") -> Path:
    """Create a file whose modification time is `age_days` old."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    stamp = time.time() - age_days * 86400
    os.utime(path, (stamp, stamp))
    return path


def make_junction(link: Path, target: Path) -> None:
    subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        check=True, capture_output=True,
    )


@pytest.fixture
def project(tmp_path: Path) -> Path:
    root = tmp_path / "my project"  # a space in the path is deliberate
    (root / ".tmp").mkdir(parents=True)
    return root
