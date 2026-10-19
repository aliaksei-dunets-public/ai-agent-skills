"""Shared helpers for the skill tests. Windows PowerShell only."""

import os
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMP_FILES = REPO / "development" / "temp-files"
PROJECT_INIT = REPO / "development" / "project-init"
CLEAN_SCRIPT = TEMP_FILES / "scripts" / "clean_tmp.ps1"
INIT_SCRIPT = PROJECT_INIT / "scripts" / "init_project.ps1"
TEMPLATE = PROJECT_INIT / "assets" / "AGENTS.template.md"

POWERSHELL = ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass"]


def run_clean(project_root: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [*POWERSHELL, "-File", str(CLEAN_SCRIPT), "-ProjectRoot", str(project_root), *args],
        capture_output=True, text=True, cwd=cwd or project_root, timeout=120,
    )


def make_file(path: Path, age_days: float, content: str = "x") -> Path:
    """Create a file whose modification time is `age_days` old."""
    import time
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    stamp = time.time() - age_days * 86400
    os.utime(path, (stamp, stamp))
    return path


def make_junction(link: Path, target: Path) -> None:
    subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)


def run_init(root: Path, *args: str, temp_files: Path | None = None,
             default_temp_files: bool = True) -> subprocess.CompletedProcess:
    cmd = [*POWERSHELL, "-File", str(INIT_SCRIPT), "-ProjectRoot", str(root)]
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
