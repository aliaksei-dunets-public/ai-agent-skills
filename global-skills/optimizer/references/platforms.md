---
checked_at: 2026-11-06
note: Discovery paths and features change between releases; verify against the
  platform's current documentation before asserting them as facts.
---

# Platform Notes

Use when a check or finding needs a platform fact that the package does not
state, or must verify one that it states: discovery or installation paths,
always-on loading, layer placement, or size and frontmatter guidance on one of
these platforms. Check only the relevant section. If you cannot verify a fact
on the target, use it and label it as unchecked in the report.

## Layers (all platforms)

| Layer | Belongs here |
| --- | --- |
| Always-on instruction file | short, durable facts needed on most tasks |
| Path-scoped rules | conventions for matching files only |
| Skill | conditional, multi-step procedure or specialized knowledge |
| Subagent / custom agent | isolated role, tools, permissions, or review boundary |
| Hook / permissions / application | deterministic blocking and authorization |

Common defects: long workflows copied into always-on files; the same workflow
copied into several platforms' files with drifting edits; security rules that
exist only as text. When one repository serves several platforms, keep one
canonical workflow and thin per-platform adapters, and do not assume one
platform discovers another's files.

## OpenAI Codex

- Always-on: global `~/.codex/AGENTS.override.md` or `AGENTS.md`, then at most
  one file per directory from the repository root to the working directory
  (`AGENTS.override.md`, `AGENTS.md`, configured fallback names). The file
  nearest the working directory wins.
- Skills: `.agents/skills/` in the working directory and each parent up to the
  repository root; user `~/.agents/skills/`; admin `/etc/codex/skills`.
  Metadata is read first and the full skill loads on selection, so `name` and
  `description` drive activation. Skill metadata shares a budget of about 2%
  of context or 8,000 characters.

## Claude Code (CLI and VS Code)

- Always-on: `CLAUDE.md` or `.claude/CLAUDE.md`, plus `CLAUDE.local.md`;
  modular and path-scoped rules in `.claude/rules/` (`paths:` frontmatter),
  user rules in `~/.claude/rules/`. `AGENTS.md` is read only when no
  `CLAUDE.md` variant exists in the working directory or above it.
- Skills: `.claude/skills/<name>/SKILL.md` (project, also nested
  `<subdir>/.claude/skills/`) and `~/.claude/skills/` (user). Descriptions are
  always in context; the full skill loads on invocation.
- Subagents: `.claude/agents/` or `~/.claude/agents/`; the `skills:` field
  preloads full skill content at startup and costs context.
- Hard blocks belong in hooks and permission settings, not in `CLAUDE.md`.
- Skill authoring recommendations (Anthropic Agent Skills best practices):
  - `name`: at most 64 characters; lowercase letters, numbers, and hyphens;
    no XML tags; no reserved words `anthropic` or `claude`.
  - `description`: non-empty, at most 1,024 characters, no XML tags, written
    in third person; it states what the skill does and when to use it.
  - Keep the `SKILL.md` body under 500 lines; split detail into references
    when approaching it.
  - Link references directly from `SKILL.md` (one level deep); Claude may
    read nested references only partially.
  - Start a reference longer than 100 lines with a table of contents.

## GitHub Copilot (VS Code)

- Always-on: `.github/copilot-instructions.md` or `AGENTS.md`.
- Path rules: `.github/instructions/*.instructions.md` with `applyTo` globs —
  check globs that never match or match everything.
- Skills: project `.github/skills/`, `.agents/skills/`, or `.claude/skills/`;
  user `~/.copilot/skills/`, `~/.agents/skills/`, or `~/.claude/skills/`.
  Pick one canonical location.
- Custom agents: `.github/agents/*.agent.md`; check that tools match the role.
- Hooks: `.github/hooks/*.json` or `~/.copilot/hooks/`.

## Google Antigravity

- Skills: `.agents/skills/<name>/` (plural; `.agent/skills` remains for
  backward compatibility); global `~/.gemini/config/skills/<name>/`.
- Rules: `.agents/rules/*.md`, `AGENTS.md`, `GEMINI.md`.
- The CLI also reads `~/.gemini/skills/` and other `~/.gemini/` skill folders
  that the app/IDE does not read; do not assume parity.

## IDE versus CLI

The same product's IDE and CLI can load different instructions, tools, and
models. A claim about IDE behavior needs a check in the IDE.
