"""Safety tests for init_project.ps1: it creates what is missing and never
modifies or deletes anything that already exists."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

from conftest import TEMP_FILES, TEMPLATE, run_init, snapshot, statuses

pytestmark = pytest.mark.skipif(sys.platform != "win32", reason="Windows PowerShell only")

EXISTING_AGENTS = "# My rules\n\nWrite docs in Russian.\nDo not touch the DB.\n"


def make_junction(link: Path, target: Path) -> None:
    subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)


# --- fresh project ---------------------------------------------------------

def test_fresh_project_gets_everything(root: Path):
    result = run_init(root)
    assert result.returncode == 0, result.stdout + result.stderr
    for folder in ("docs", ".agents/skills", ".tmp"):
        assert (root / folder).is_dir()
    assert not (root / ".claude").exists(), "no .claude without -Claude"
    assert not (root / "CLAUDE.md").exists()
    assert not (root / ".git").exists(), "no git init without -GitInit"
    assert (root / ".gitignore").read_text() == ".tmp/\n"
    assert (root / "docs/README.md").is_file()
    assert (root / "AGENTS.md").read_text(encoding="utf-8") == TEMPLATE.read_text(encoding="utf-8")
    link = root / ".agents/skills/temp-files"
    assert link.is_junction()
    assert (link / "SKILL.md").is_file()


def test_claude_flag_adds_claude_artifacts(root: Path):
    result = run_init(root, "-Claude")
    assert result.returncode == 0, result.stdout
    assert (root / ".claude").is_dir()
    assert (root / "CLAUDE.md").read_text() == "@AGENTS.md\n"
    assert (root / ".claude/skills/temp-files").is_junction()
    assert (root / ".claude/skills/temp-files/SKILL.md").is_file()


def test_link_points_to_original_not_a_copy(root: Path):
    run_init(root)
    link = root / ".agents/skills/temp-files"
    assert link.is_junction()
    assert os.path.samefile(link / "SKILL.md", TEMP_FILES / "SKILL.md")


def test_second_run_is_idempotent(root: Path):
    run_init(root, "-Claude")
    before = snapshot(root)
    result = run_init(root, "-Claude")
    assert result.returncode == 0
    assert snapshot(root) == before
    assert "created" not in statuses(result).values()


# --- existing instructions must survive ------------------------------------

def test_existing_agents_md_is_never_modified(root: Path):
    (root / "AGENTS.md").write_text(EXISTING_AGENTS, encoding="utf-8")
    result = run_init(root)
    assert (root / "AGENTS.md").read_text(encoding="utf-8") == EXISTING_AGENTS
    assert statuses(result)["AGENTS.md"] == "needs-review"


def test_empty_existing_agents_md_is_not_overwritten(root: Path):
    (root / "AGENTS.md").write_text("", encoding="utf-8")
    run_init(root)
    assert (root / "AGENTS.md").read_text(encoding="utf-8") == ""


def test_existing_agents_md_bytes_are_preserved_exactly(root: Path):
    raw = "﻿# Rules\r\nCRLF and BOM\r\n".encode("utf-8")
    (root / "AGENTS.md").write_bytes(raw)
    run_init(root)
    assert (root / "AGENTS.md").read_bytes() == raw


def test_existing_claude_md_without_import_is_flagged_not_changed(root: Path):
    (root / "CLAUDE.md").write_text("my claude rules\n", encoding="utf-8")
    result = run_init(root, "-Claude")
    assert (root / "CLAUDE.md").read_text(encoding="utf-8") == "my claude rules\n"
    assert statuses(result)["CLAUDE.md"] == "needs-review"


def test_existing_claude_md_with_import_is_skipped(root: Path):
    (root / "CLAUDE.md").write_text("intro\n@AGENTS.md\nmore\n", encoding="utf-8")
    result = run_init(root, "-Claude")
    assert (root / "CLAUDE.md").read_text(encoding="utf-8") == "intro\n@AGENTS.md\nmore\n"
    assert statuses(result)["CLAUDE.md"] == "skipped"


def test_other_tools_instruction_files_are_untouched(root: Path):
    files = {
        "GEMINI.md": "gemini\n",
        ".cursorrules": "cursor\n",
        ".github/copilot-instructions.md": "copilot\n",
    }
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    run_init(root, "-Claude")
    for rel, text in files.items():
        assert (root / rel).read_text() == text


def test_existing_docs_readme_is_not_overwritten(root: Path):
    (root / "docs").mkdir()
    (root / "docs/README.md").write_text("my toc\n")
    run_init(root)
    assert (root / "docs/README.md").read_text() == "my toc\n"


# --- .gitignore is append-only ---------------------------------------------

@pytest.mark.parametrize("existing,expected", [
    ("node_modules/\n", "node_modules/\n.tmp/\n"),
    ("node_modules/", "node_modules/\n.tmp/\n"),                 # no trailing newline
    ("a\r\nb\r\n", "a\r\nb\r\n.tmp/\r\n"),                       # CRLF preserved
    ("a\r\nb", "a\r\nb\r\n.tmp/\r\n"),                           # CRLF, no trailing newline
    ("", ".tmp/\n"),
])
def test_gitignore_is_appended_without_touching_existing_lines(root: Path, existing: str, expected: str):
    (root / ".gitignore").write_bytes(existing.encode("utf-8"))
    run_init(root)
    assert (root / ".gitignore").read_bytes() == expected.encode("utf-8")


@pytest.mark.parametrize("variant", [".tmp/", "/.tmp/", ".tmp", "/.tmp", "  .tmp/  "])
def test_gitignore_with_tmp_already_present_is_byte_identical(root: Path, variant: str):
    content = f"build/\n{variant}\ndist/\n".encode("utf-8")
    (root / ".gitignore").write_bytes(content)
    run_init(root)
    assert (root / ".gitignore").read_bytes() == content


def test_gitignore_similar_names_do_not_count_as_tmp(root: Path):
    (root / ".gitignore").write_text(".tmp-cache/\nmy.tmp/\n#.tmp/\n")
    run_init(root)
    lines = (root / ".gitignore").read_text().splitlines()
    assert lines[-1] == ".tmp/" and lines.count(".tmp/") == 1


def test_gitignore_bom_is_preserved(root: Path):
    raw = b"\xef\xbb\xbfbuild/\n"
    (root / ".gitignore").write_bytes(raw)
    run_init(root)
    assert (root / ".gitignore").read_bytes().startswith(raw)


# --- links -----------------------------------------------------------------

def test_plain_copy_of_skill_is_left_untouched(root: Path):
    copy = root / ".agents/skills/temp-files"
    copy.mkdir(parents=True)
    (copy / "SKILL.md").write_text("my modified copy\n")
    result = run_init(root)
    assert (copy / "SKILL.md").read_text() == "my modified copy\n"
    assert not copy.is_junction()
    assert statuses(result)[".agents/skills/temp-files"] == "needs-review"


def test_dangling_link_is_reported_not_replaced(root: Path, tmp_path: Path):
    gone = tmp_path / "gone"
    gone.mkdir()
    (root / ".agents/skills").mkdir(parents=True)
    make_junction(root / ".agents/skills/temp-files", gone)
    gone.rmdir()
    result = run_init(root)
    assert statuses(result)[".agents/skills/temp-files"] == "needs-review"
    assert (root / ".agents/skills/temp-files").is_junction()


def test_healthy_existing_link_is_skipped(root: Path):
    (root / ".agents/skills").mkdir(parents=True)
    make_junction(root / ".agents/skills/temp-files", TEMP_FILES)
    result = run_init(root)
    assert statuses(result)[".agents/skills/temp-files"] == "skipped"


def test_missing_temp_files_skill_fails_but_rest_is_still_done(root: Path, tmp_path: Path):
    result = run_init(root, temp_files=tmp_path / "does-not-exist")
    assert result.returncode == 1
    assert statuses(result)[".agents/skills/temp-files"] == "failed"
    assert (root / "AGENTS.md").is_file() and (root / ".tmp").is_dir()
    assert not (root / ".agents/skills/temp-files").exists()


def test_default_temp_files_path_resolves_next_to_the_skill(root: Path):
    result = run_init(root, default_temp_files=False)
    assert result.returncode == 0, result.stdout
    assert (root / ".agents/skills/temp-files/SKILL.md").is_file()


# --- never deletes ---------------------------------------------------------

def test_existing_files_are_never_deleted_or_changed(root: Path):
    files = {
        "src/app.py": b"print(1)\n",
        "docs/guide.md": b"guide\n",
        ".tmp/scratch/2020.01.01_old.txt": b"old\n",   # stale, but not this skill's business
        "notes.txt": b"notes\n",
        "AGENTS.md": EXISTING_AGENTS.encode(),
    }
    for rel, data in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(data)
    run_init(root, "-Claude")
    after = snapshot(root)
    for rel, data in files.items():
        assert after[rel] == data, rel


# --- options ---------------------------------------------------------------

def test_dry_run_creates_nothing(root: Path):
    result = run_init(root, "-DryRun", "-Claude", "-GitInit")
    assert result.returncode == 0, result.stdout
    assert list(root.iterdir()) == []
    assert "would-create" in statuses(result).values()


def test_dry_run_does_not_modify_existing_gitignore(root: Path):
    (root / ".gitignore").write_text("build/\n")
    run_init(root, "-DryRun")
    assert (root / ".gitignore").read_text() == "build/\n"


def test_git_init_creates_repository(root: Path):
    result = run_init(root, "-GitInit")
    assert result.returncode == 0, result.stdout
    assert (root / ".git").is_dir()
    assert not subprocess.run(["git", "-C", str(root), "log"], capture_output=True).returncode == 0, \
        "no commits must be created"


def test_git_init_keeps_existing_repository_intact(root: Path):
    subprocess.run(["git", "-C", str(root), "init", "--quiet"], check=True)
    (root / "f.txt").write_text("x")
    subprocess.run(["git", "-C", str(root), "add", "f.txt"], check=True)
    head_before = (root / ".git/HEAD").read_bytes()
    result = run_init(root, "-GitInit")
    assert statuses(result)[".git"] == "skipped"
    assert (root / ".git/HEAD").read_bytes() == head_before
    staged = subprocess.run(["git", "-C", str(root), "diff", "--cached", "--name-only"],
                            capture_output=True, text=True).stdout
    assert "f.txt" in staged


def test_missing_project_root_fails_cleanly(tmp_path: Path):
    result = run_init(tmp_path / "nope")
    assert result.returncode != 0
    assert not (tmp_path / "nope").exists()


def test_file_in_place_of_folder_is_reported_not_replaced(root: Path):
    (root / "docs").write_text("i am a file\n")
    result = run_init(root)
    assert result.returncode == 1
    assert statuses(result)["docs"] == "failed"
    assert (root / "docs").read_text() == "i am a file\n"
