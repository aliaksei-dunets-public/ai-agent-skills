"""Static contract checks for temp-files: SKILL.md must agree with the script."""

import re
from pathlib import Path

from helpers import CLEAN_SCRIPT as SCRIPT, TEMP_FILES as SKILL_DIR

SKILL = SKILL_DIR / "SKILL.md"


def test_skill_name_matches_folder():
    text = SKILL.read_text(encoding="utf-8")
    assert re.search(r"^name:\s*temp-files\s*$", text, re.M)
    assert SKILL_DIR.name == "temp-files"


def test_skill_has_no_draft_marker():
    assert "DRAFT" not in SKILL.read_text(encoding="utf-8")
    assert "DRAFT" not in SCRIPT.read_text(encoding="utf-8")


def test_relative_links_resolve():
    for target in re.findall(r"\]\(([^)#]+)\)", SKILL.read_text(encoding="utf-8")):
        if "://" not in target:
            assert (SKILL_DIR / target).exists(), target


def test_retention_in_skill_matches_script_minimum():
    script = SCRIPT.read_text(encoding="utf-8")
    assert "[ValidateRange(30, 3650)]" in script
    assert "[int]$DaysOld = 30" in script
    assert "30 days" in SKILL.read_text(encoding="utf-8")


def test_every_layout_folder_is_documented_once():
    text = SKILL.read_text(encoding="utf-8")
    folders = re.findall(r"^\| `(\w+)/` \|", text, re.M)
    assert "keep" in folders and "scratch" in folders
    assert len(folders) == len(set(folders))


def test_script_only_deletes_inside_tmp():
    script = SCRIPT.read_text(encoding="utf-8")
    assert "Test-InsideTmp" in script
    removals = re.findall(r"Remove-Item[^\n]*", script)
    assert len(removals) == 2, "only the file and empty-folder removals are allowed"
    assert all("-LiteralPath" in r for r in removals), "never use wildcard-expanding -Path"
    assert "-Recurse" not in script


def test_skill_folder_contains_no_tests():
    """Tests live in the repository-level tests/ folder, never next to the skill."""
    assert not (SKILL_DIR / "tests").exists()


def test_every_removal_is_guarded_by_a_fresh_link_check():
    """No Remove-Item without Test-PlainPath on the lines just before it (swap-after-walk guard)."""
    lines = SCRIPT.read_text(encoding="utf-8").splitlines()
    removals = [i for i, line in enumerate(lines) if "Remove-Item" in line]
    assert len(removals) == 2
    for i in removals:
        assert any("Test-PlainPath" in line for line in lines[max(0, i - 10):i]), lines[i]
