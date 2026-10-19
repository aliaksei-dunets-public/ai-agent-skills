---
name: temp-files
description: >
  Rules for agent temporary files: where to put them (.tmp/ in the project
  root), how to name them (YYYY.MM.DD_name) and how they are cleaned up
  (clean_tmp.ps1 deletes only files older than 30 days). Use when creating any
  temporary, intermediate or diagnostic artifact: ad-hoc scripts, data dumps,
  logs, screenshots, coverage reports, test runs. Do not use for files that are
  part of the project.
---

# Temporary Files

DRAFT. All temporary agent artifacts live in one place, `.tmp/` in the project
root, and are cleaned up only by a script, never by the agent. Creating `.tmp/`
and keeping it out of git is handled by a separate skill; this skill assumes
that is already done.

## 1. Folder structure

Put every file in the subfolder that matches its purpose. Create a subfolder
when first needed.

| Subfolder | Contents |
|---|---|
| `scratch/` | One-off experiments and drafts that fit no other category |
| `scripts/` | Agent helper scripts: investigation, data migration, one-off checks |
| `tests/` | Temporary tests that are not part of the project; runner base dirs (for example pytest `basetemp`) |
| `data/` | API dumps, database exports, input and output datasets, one-off fixtures |
| `logs/` | Server, process, build and test run logs |
| `playwright/` | Screenshots, videos, traces and HTML reports of browser checks |
| `coverage/` | Code coverage reports |
| `reports/` | Analysis, audit and linter results, summaries, generated markdown/json reports |
| `e2e/` | End-to-end run artifacts |
| `keep/` | Files that must not be deleted (baselines, reference data); the cleanup script never touches it |

If no subfolder fits, use `scratch/`. Do not add new subfolders without a
reason; propose them to the user first. Do not put files directly in `.tmp/`.
Use `keep/` only when the user asks to preserve a file.

## 2. File names

Format: `YYYY.MM.DD_name`, where the date is the file creation day.

- `.tmp/scripts/2026.10.19_dump_orders.py`
- `.tmp/playwright/2026.10.19_login_error.png`
- `.tmp/data/2026.10.19_api_response.json`

Rules:

- Use the local date from the system; do not guess it.
- `name` is lowercase Latin words joined by `_`, with no spaces.
- Do not rename directories created by tools (for example `pytest-of-user`);
  their age is judged by modification time.
- For a tool that produces many files, create a `YYYY.MM.DD_name/` directory
  and direct its output there.
- When rerunning on the same day, overwrite the file; on another day, create a
  new file with the new date.

## 3. Usage

- Create temporary artifacts only in `.tmp/`. Do not leave them in the project
  root, in source or test folders, or in the system `%TEMP%`.
- Point tools that write to the system temp directory by default (pytest,
  coverage, playwright, build tools) to `.tmp/<subfolder>/` through their
  settings or the `TMP`, `TEMP` and `TMPDIR` variables.
- Do not store secrets, tokens or personal data in `.tmp/`, even briefly.
- `.tmp/` is not a place for results. Deliverables belong in the project. A file
  needed after 30 days must be moved into the project.

## 4. Cleanup

Only the script [clean_tmp.ps1](scripts/clean_tmp.ps1) deletes files. The agent
does not delete files from `.tmp/` by hand (`rm`, `Remove-Item`) and does not
write its own cleanup commands. Windows and PowerShell only.

What the script does:

- works only inside `<project root>/.tmp/`; every item is checked to be inside
  that folder before deletion;
- deletes a file only when both the `YYYY.MM.DD_` date in its name and its last
  modification time are older than 30 days (without a prefix, only the
  modification time counts); this applies to files directly in `.tmp/` too;
- skips `.tmp/keep/` entirely;
- does not allow a threshold below 30 days;
- does not follow or delete symlinks and junctions;
- removes empty nested folders afterwards; first-level folders stay;
- supports `-DryRun` to list what would be deleted without deleting;
- skips locked files and reports them.

Run from the project root:

```powershell
powershell -ExecutionPolicy Bypass -File <skill_path>/scripts/clean_tmp.ps1 -ProjectRoot .
```

Preview:

```powershell
powershell -ExecutionPolicy Bypass -File <skill_path>/scripts/clean_tmp.ps1 -ProjectRoot . -DryRun
```

When to run:

- once, on successful task completion;
- not on failure, failing tests or a blocker: keep the artifacts for diagnosis
  (the script leaves files younger than 30 days alone anyway);
- if the script is unavailable or fails, tell the user instead of cleaning
  manually.
