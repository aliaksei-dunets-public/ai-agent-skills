---
checked_at: 2026-07-14
note: Discovery paths and features change between releases; verify against the
  platform's current documentation before asserting them as facts.
---

# Platform Notes

Use when the audited package targets one of these platforms. Check only the
relevant section.

## Layers (all platforms)

| Layer | Belongs here |
|---|---|
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

- Always-on: `AGENTS.md` (nested files can override; check precedence).
- Repository skills: `.agents/skills/<name>/SKILL.md`; user/admin skill
  locations may also apply. Metadata is read first and the full skill loads on
  selection, so `name` and `description` drive activation.

## Claude Code (CLI and VS Code)

- Always-on: `CLAUDE.md`; modular and path-scoped rules in `.claude/rules/`.
- Skills: `.claude/skills/<name>/SKILL.md`, loaded on demand.
- Subagents: `.claude/agents/`; preloading large skills into them costs context.
- Hard blocks belong in hooks and permission settings, not in `CLAUDE.md`.

## GitHub Copilot (VS Code)

- Always-on: `.github/copilot-instructions.md`; `AGENTS.md` may also apply.
- Path rules: `.github/instructions/*.instructions.md` with `applyTo` globs —
  check globs that never match or match everything.
- Skills: `.github/skills/` or `.agents/skills/`; pick one canonical location.
- Custom agents: `.github/agents/*.agent.md`; check that tools match the role.

## Google Antigravity

- Repository CLI skills: `.agent/skills/<name>/SKILL.md` (singular `.agent`).
- IDE/standalone and CLI discovery may differ; do not assume parity.

## IDE versus CLI

The same product's IDE and CLI can load different instructions, tools, and
models. A claim about IDE behavior needs a check in the IDE.
