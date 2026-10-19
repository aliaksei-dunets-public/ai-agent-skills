"""Safety tests for clean_tmp.ps1: it must delete only stale files inside .tmp/."""

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from helpers import make_file, make_junction, run_clean

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows PowerShell only")

OLD = 40
RECENT = 1


def dated(days_ago: int, name: str) -> str:
    return f"{(date.today() - timedelta(days=days_ago)):%Y.%m.%d}_{name}"


# --- what is deleted -------------------------------------------------------

def test_deletes_old_prefixed_file(project: Path):
    f = make_file(project / ".tmp/scratch" / dated(OLD, "a.txt"), OLD)
    result = run_clean(project)
    assert result.returncode == 0, result.stderr
    assert not f.exists()


def test_deletes_old_file_without_prefix_by_mtime(project: Path):
    f = make_file(project / ".tmp/scratch/plain.txt", OLD)
    run_clean(project)
    assert not f.exists()


def test_deletes_old_file_placed_directly_in_tmp(project: Path):
    f = make_file(project / ".tmp/loose.txt", OLD)
    run_clean(project)
    assert not f.exists()


def test_keeps_recent_file(project: Path):
    f = make_file(project / ".tmp/scratch" / dated(RECENT, "a.txt"), RECENT)
    run_clean(project)
    assert f.exists()


def test_keeps_recent_file_without_prefix(project: Path):
    f = make_file(project / ".tmp/scratch/plain.txt", RECENT)
    run_clean(project)
    assert f.exists()


def test_keeps_file_with_old_prefix_but_recent_mtime(project: Path):
    f = make_file(project / ".tmp/scratch" / dated(OLD, "a.txt"), RECENT)
    run_clean(project)
    assert f.exists()


def test_keeps_file_with_recent_prefix_but_old_mtime(project: Path):
    f = make_file(project / ".tmp/scratch" / dated(RECENT, "a.txt"), OLD)
    run_clean(project)
    assert f.exists()


def test_keeps_file_with_future_prefix_date(project: Path):
    future = f"{(date.today() + timedelta(days=5)):%Y.%m.%d}_a.txt"
    f = make_file(project / ".tmp/scratch" / future, OLD)
    run_clean(project)
    assert f.exists()


def test_invalid_prefix_date_does_not_crash(project: Path):
    f = make_file(project / ".tmp/scratch/2026.13.45_bad.txt", OLD)
    result = run_clean(project)
    assert result.returncode == 0, result.stderr
    assert not f.exists()


@pytest.mark.parametrize("age,expected_exists", [(29, True), (31, False)])
def test_threshold_boundary(project: Path, age: int, expected_exists: bool):
    f = make_file(project / ".tmp/scratch/edge.txt", age)
    run_clean(project)
    assert f.exists() is expected_exists


# --- what must never be deleted --------------------------------------------

def test_never_touches_keep_folder(project: Path):
    top = make_file(project / ".tmp/keep/baseline.json", 400)
    nested = make_file(project / ".tmp/keep/deep/er/ref.dat", 400)
    run_clean(project)
    assert top.exists() and nested.exists()


def test_keep_folder_name_is_case_insensitive(project: Path):
    f = make_file(project / ".tmp/KEEP/baseline.json", 400)
    run_clean(project)
    assert f.exists()


def test_keep_is_protected_only_at_first_level(project: Path):
    protected = make_file(project / ".tmp/keep/a.txt", OLD)
    stale = make_file(project / ".tmp/scratch/keep/b.txt", OLD)
    run_clean(project)
    assert protected.exists()
    assert not stale.exists()


def test_never_touches_files_outside_tmp(project: Path):
    outside = [
        make_file(project / "src/old.py", 400),
        make_file(project / "README.md", 400),
        make_file(project / ".gitignore", 400),
        make_file(project / ".tmp-other/old.txt", 400),   # similarly named sibling
        make_file(project / ".tmpx/old.txt", 400),
    ]
    make_file(project / ".tmp/scratch/stale.txt", OLD)
    run_clean(project)
    assert all(p.exists() for p in outside)


def test_does_not_follow_junction_inside_tmp(project: Path, tmp_path: Path):
    external = tmp_path / "external"
    victim = make_file(external / "precious.txt", 400)
    (project / ".tmp/scratch").mkdir()
    make_junction(project / ".tmp/scratch/link", external)
    run_clean(project)
    assert victim.exists()
    assert (project / ".tmp/scratch/link").exists(), "the junction itself must survive"


def test_refuses_when_tmp_itself_is_a_junction(tmp_path: Path):
    external = tmp_path / "external"
    victim = make_file(external / "precious.txt", 400)
    root = tmp_path / "proj"
    root.mkdir()
    make_junction(root / ".tmp", external)
    result = run_clean(root)
    assert result.returncode != 0
    assert victim.exists()


def test_locked_file_is_skipped_and_reported(project: Path):
    f = make_file(project / ".tmp/scratch/locked.txt", OLD)
    with open(f, "r"):  # open handle without delete sharing
        result = run_clean(project)
    assert result.returncode == 0
    assert f.exists()
    assert "SKIPPED" in result.stdout


# --- parameters ------------------------------------------------------------

def test_dry_run_deletes_nothing_but_lists(project: Path):
    f = make_file(project / ".tmp/scratch/stale.txt", OLD)
    result = run_clean(project, "-DryRun")
    assert result.returncode == 0
    assert f.exists()
    assert "WOULD REMOVE" in result.stdout and "stale.txt" in result.stdout


def test_dry_run_keeps_empty_nested_folders(project: Path):
    make_file(project / ".tmp/scratch/a/b/stale.txt", OLD)
    run_clean(project, "-DryRun")
    assert (project / ".tmp/scratch/a/b/stale.txt").exists()


@pytest.mark.parametrize("days", ["0", "1", "29", "-5"])
def test_threshold_below_30_is_rejected(project: Path, days: str):
    f = make_file(project / ".tmp/scratch/stale.txt", OLD)
    result = run_clean(project, "-DaysOld", days)
    assert result.returncode != 0
    assert f.exists()


def test_larger_threshold_keeps_files_younger_than_it(project: Path):
    f = make_file(project / ".tmp/scratch/stale.txt", OLD)
    run_clean(project, "-DaysOld", "60")
    assert f.exists()


def test_dot_project_root_uses_current_directory(project: Path):
    f = make_file(project / ".tmp/scratch/stale.txt", OLD)
    result = run_clean(Path("."), cwd=project)
    assert result.returncode == 0, result.stderr
    assert not f.exists()


def test_missing_tmp_is_not_an_error(tmp_path: Path):
    result = run_clean(tmp_path)
    assert result.returncode == 0
    assert "nothing to clean" in result.stdout.lower()


# --- folders ---------------------------------------------------------------

def test_removes_empty_nested_folders_but_keeps_first_level(project: Path):
    make_file(project / ".tmp/scratch/a/b/stale.txt", OLD)
    run_clean(project)
    assert (project / ".tmp/scratch").is_dir(), "first-level folder stays"
    assert not (project / ".tmp/scratch/a").exists(), "empty nested folders go"


def test_keeps_nested_folder_that_still_has_recent_files(project: Path):
    recent = make_file(project / ".tmp/scratch/a/b/new.txt", RECENT)
    make_file(project / ".tmp/scratch/a/b/stale.txt", OLD)
    run_clean(project)
    assert recent.exists()


def test_does_not_delete_old_empty_first_level_folder(project: Path):
    (project / ".tmp/logs").mkdir()
    run_clean(project)
    assert (project / ".tmp/logs").is_dir()


def test_path_with_spaces_and_unusual_names(project: Path):
    f = make_file(project / ".tmp/scratch/my file [1] (copy).txt", OLD)
    run_clean(project)
    assert not f.exists()
