---
name: temp-files
description: >
  Rules for agent temporary files on Windows: keep them in .tmp/ in the project
  root, name them YYYY.MM.DD_name, and let only clean_tmp.ps1 delete them (files
  older than 30 days). Use when creating any temporary, intermediate or
  diagnostic artifact: ad-hoc scripts, data dumps, logs, screenshots, coverage
  reports, test runs. Not for files that are part of the project.
---

# Temporary Files

Every temporary agent artifact lives in `.tmp/` in the project root. Only a
script deletes them, never the agent. The `project-init` skill creates `.tmp/`
and git-ignores it; if `.tmp/` is missing, create it and add `.tmp/` to
`.gitignore`.

## Layout

Put each file in the subfolder for its purpose, creating it on first use. Never
put files directly in `.tmp/`; use `scratch/` when nothing else fits. Propose a
new subfolder to the user before adding one.

| Subfolder | Contents |
|---|---|
| `scratch/` | One-off experiments and drafts |
| `scripts/` | Helper scripts: investigation, migration, one-off checks |
| `tests/` | Temporary tests outside the project; runner base dirs (pytest `basetemp`) |
| `data/` | API dumps, exports, input/output datasets, one-off fixtures |
| `logs/` | Server, process, build and test logs |
| `playwright/` | Screenshots, videos, traces, HTML reports of browser checks |
| `coverage/` | Coverage reports |
| `reports/` | Analysis, audit and linter results, generated md/json reports |
| `e2e/` | End-to-end run artifacts |
| `keep/` | Files to preserve (baselines, reference data); never cleaned. Use only when the user asks |

## Names

`YYYY.MM.DD_name`, for example `.tmp/scripts/2026.10.19_dump_orders.py`.

- Date: the creation day from the system clock, never guessed.
- `name`: lowercase Latin words joined by `_`.
- A tool that writes many files gets its own `YYYY.MM.DD_name/` directory.
- Rerun on the same day: overwrite. Another day: new file with the new date.
- Do not rename directories created by tools (`pytest-of-user`); their files
  are aged by modification time.

## Usage

- Do not leave temporary files in the project root, source or test folders, or
  system `%TEMP%`. Point tools that default to the system temp dir (pytest,
  coverage, playwright, build tools) at `.tmp/<subfolder>/` via their settings
  or `TMP`, `TEMP`, `TMPDIR`.
- Never store secrets, tokens or personal data in `.tmp/`.
- Deliverables belong in the project; move anything needed after 30 days there.

## Cleanup

Only [clean_tmp.ps1](scripts/clean_tmp.ps1) deletes files (Windows PowerShell).
Do not delete from `.tmp/` by hand (`rm`, `Remove-Item`) or write other cleanup
commands.

The script works only inside `<root>/.tmp/`. It deletes a file only when both
the name's date prefix (if any) and the modification time are older than 30
days (the threshold cannot be lowered). It skips `keep/`, never follows or
deletes symlinks and junctions, skips locked files and reports them, and
removes empty nested folders afterwards (first-level folders stay).

```powershell
powershell -ExecutionPolicy Bypass -File <skill_path>/scripts/clean_tmp.ps1 -ProjectRoot .          # clean
powershell -ExecutionPolicy Bypass -File <skill_path>/scripts/clean_tmp.ps1 -ProjectRoot . -DryRun  # preview
```

Run once, on successful task completion; not after a failure, so artifacts stay
for diagnosis. If the script is unavailable or fails, tell the user instead of
cleaning manually.
