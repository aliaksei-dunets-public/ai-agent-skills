# Skill tests

Tests for the scripts and contracts of skills in `development/`. Windows,
PowerShell 5.1 and pytest are required.

```powershell
python -m pytest tests -q
```

| Folder | Covers |
|---|---|
| `temp_files/` | `clean_tmp.ps1` safety (what is deleted, what never is) and the `temp-files` SKILL.md contract |
| `project_init/` | `init_project.ps1` non-destructiveness, the AGENTS.md template and the `project-init` SKILL.md contract |
