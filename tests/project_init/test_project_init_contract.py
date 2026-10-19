"""Static contract checks for project-init: template, SKILL.md and links."""

import re
from pathlib import Path

from helpers import PROJECT_INIT as SKILL_DIR, TEMPLATE

SKILL = SKILL_DIR / "SKILL.md"


def frontmatter(text: str) -> dict[str, str]:
    block = re.match(r"---\n(.*?)\n---\n", text, re.S).group(1)
    return {m.group(1): m.group(2) for m in re.finditer(r"^(\w+):\s*(.*)$", block, re.M)}


def test_skill_name_matches_folder():
    assert frontmatter(SKILL.read_text(encoding="utf-8"))["name"] == SKILL_DIR.name


def test_skill_has_no_draft_marker():
    assert "DRAFT" not in SKILL.read_text(encoding="utf-8")


def test_relative_links_in_skill_resolve():
    text = SKILL.read_text(encoding="utf-8")
    for target in re.findall(r"\]\(([^)#]+)\)", text):
        if "://" not in target:
            assert (SKILL_DIR / target).exists(), target


def test_files_named_in_skill_exist():
    text = SKILL.read_text(encoding="utf-8")
    for rel in ("scripts/init_project.ps1", "assets/AGENTS.template.md"):
        assert rel in text, f"SKILL.md must point to {rel}"
        assert (SKILL_DIR / rel).is_file()


def test_template_has_required_rules():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "Write project documentation, plans, reports, and code comments in English" in text
    assert "Use the user's language for conversation." in text
    assert "[docs/](docs/)" in text
    assert "[.agents/skills/temp-files/SKILL.md](.agents/skills/temp-files/SKILL.md)" in text
    assert "`.tmp/`" in text


def test_template_links_match_what_the_script_creates():
    """The template links must point to paths that init_project.ps1 creates."""
    script = (SKILL_DIR / "scripts/init_project.ps1").read_text(encoding="utf-8")
    assert 'Ensure-Dir "docs"' in script
    assert 'Ensure-Stub ".agents/skills/temp-files"' in script


def test_script_never_contains_destructive_commands():
    script = (SKILL_DIR / "scripts/init_project.ps1").read_text(encoding="utf-8")
    for forbidden in ("Remove-Item", "Set-Content", "Out-File", "-Force -Recurse", "rmdir", "del "):
        assert forbidden not in script, forbidden
    assert "Clear-Content" not in script


def test_template_has_git_branch_rules():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "## Git Branches for Agent Work" in text
    assert "Every commit made by an AI agent goes to the branch `ai_feature`" in text
    assert "Create `ai_feature` from `main` when it does not exist" in text
    assert "Do not merge or push `ai_feature` unless the user asks." in text


def test_skill_lists_all_template_sections():
    skill = SKILL.read_text(encoding="utf-8")
    sections = re.findall(r"^## (.+)$", TEMPLATE.read_text(encoding="utf-8"), re.M)
    assert sections, "template has no sections"
    for name in sections:
        assert name in skill, f"SKILL.md step 3 must mention the template section '{name}'"


def test_skill_folder_contains_no_tests():
    """Tests live in the repository-level tests/ folder, never next to the skill."""
    assert not (SKILL_DIR / "tests").exists()
