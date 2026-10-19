---
name: project-init
description: >
  Onboard a new project folder on Windows: local git repository, AGENTS.md
  (existing agent instructions are audited and normalized to the standard),
  docs/, .agents/, optional .claude/, .tmp/ with .gitignore, the temp-files
  skill as a stub pointing to its original, and optional onboarding of ai-graph-guide and
  ai-task-manager. Safe to rerun: existing artifacts are skipped, instructions
  are changed only after a confirmed diff. Use when setting up an empty or new
  project folder. Not for updating the graph core or reinstalling components.
---

# Project Init

Prepares a project root for agent work. Each step checks whether its result
already exists and skips it if so. Nothing is deleted; existing instruction
files change only through step 3 with the user's confirmation. The skill never
commits.

## 1. Inputs and decisions

- `<root>`: the project root (current folder by default; confirm if it is not
  obvious).
- `<temp-files>`: the `temp-files` folder next to this skill's real folder
  (`../temp-files`). If it does not resolve, stop and tell the user.
- Ask all decisions at once, before changing anything; skip a question whose
  answer is already visible (for example `.git` exists):
  1. initialize a git repository (only if `<root>/.git` is missing);
  2. create `.claude/` (Claude Code is used);
  3. install ai-graph-guide;
  4. install ai-task-manager.
- Track each step as `created`, `fixed`, `skipped`, `declined` or `failed`. On
  `failed`, continue with independent steps and report it at the end.

## 2. Deterministic setup (script)

Run [init_project.ps1](scripts/init_project.ps1) once with the decisions from
step 1. It creates only what is missing and never modifies or deletes anything:
git repository (`-GitInit`), `docs/` with `README.md`, `.agents/skills/`,
`.tmp/` and its `.gitignore` line (append only), `AGENTS.md` from
[the template](assets/AGENTS.template.md), and the stub
`.agents/skills/temp-files/SKILL.md`. With `-Claude` it also creates
`.claude/` and `.claude/skills/temp-files`. It never creates `CLAUDE.md`:
`AGENTS.md` is the single instruction file.

```powershell
powershell -ExecutionPolicy Bypass -File <skill_path>/scripts/init_project.ps1 -ProjectRoot <root> -TempFilesPath <temp-files> [-GitInit] [-Claude] [-DryRun]
```

The stub holds only the original skill's frontmatter (so the agent can trigger
it) and the path to the original `<temp-files>/SKILL.md`; the skill itself is
never copied or linked as a folder. The script accepts `-TempFilesPath` only if
its `SKILL.md` has `name: temp-files`. Because the stub holds this machine's
path, the script also appends the stub folders it created to `.gitignore`. Pass
`-TempFilesPath` explicitly when this skill is reached through a link. Run with
`-DryRun` first when the folder is not empty. Do not recreate by hand what the
script does.

Read its report, one line per item: `created`, `skipped`, `would-create`,
`needs-review` or `failed` (exit code 1). A `failed` item does not stop the
others; report it. `needs-review` means an existing artifact was left untouched
and needs your judgment: an existing `AGENTS.md` (step 3), or a
link in place of the stub (an older junction; offer to replace it with a stub after
the user agrees, never delete it yourself). The stub contains this machine's
path to the original: rerun the skill on another machine.

## 3. Agent instructions

The script never touches an existing instruction file. Audit them here.

1. Read every existing instruction file first: `AGENTS.md`, `CLAUDE.md`,
   `.claude/CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`,
   `.cursorrules`, `.cursor/rules/`.
2. Compare each standard section of `AGENTS.md` (Language, Documentation,
   Temporary files, Git Branches for Agent Work; the standard text is [the template](assets/AGENTS.template.md))
   with the existing file:
   - **missing**: add it;
   - **conflicting** (contradicts the standard in meaning: another documentation
     language, another temp folder or naming, wrong paths): replace with the
     standard text;
   - **equivalent** (same meaning, different wording) or **matching**: leave it;
   - a project-specific choice that looks deliberate: list it under "needs a
     decision" instead of replacing it.
3. Keep everything outside the standard: project sections, component sections
   (such as the `ai-graph-guide-instructions` block; only the component's own
   onboarding changes it) and the order of unrelated content.
4. Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If `CLAUDE.md` exists without
   `@AGENTS.md`, propose adding that line and moving its duplicated standard rules
   into `AGENTS.md`. Handle other tools' files (`GEMINI.md`, Copilot, Cursor) the
   same way: offer a pointer to `AGENTS.md`, never silently delete.
5. Show one diff (added, replaced, removed, why, plus "needs a decision") and
   write only after the user confirms. Report each section as `created`,
   `fixed` or `unchanged`.

Component sections are appended to `AGENTS.md` by their own onboarding.

## 4. Components

Skip a component that is already installed:

- ai-graph-guide: `<root>/.agents/skills/graph-router/` exists, or an
  instruction file contains `ai-graph-guide-instructions`.
- ai-task-manager: `<root>/.ai_task_manager/config.toml` exists.

On yes, run the component's own onboarding and do not duplicate its logic:

- **ai-graph-guide**: follow `<core>/.agents/skills/graph-onboarding/SKILL.md`
  for `<root>`. Find `<core>` through `core_root` in
  `~/.ai-graph-guide/config.toml`, else ask the user. That onboarding asks about
  AI Task Manager itself: pass on the answer already given in step 1 so the user
  is not asked twice, and let it run the task manager setup when the answer is
  yes.
- **ai-task-manager** without ai-graph-guide: follow
  `<ai-task-manager core>/src/ai_task_manager/skills/ai-task-manager-onboarding/SKILL.md`
  for `<root>`; ask the user for the core checkout path.

The components write their own instruction sections and `.gitignore` lines.

## 5. Report

Print a table of step and result, then the manual actions left for the user
(first commit, git remote, restarting the agent so it reloads instructions and
skills).
