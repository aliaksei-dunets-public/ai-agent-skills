# AGENTS.md

## Language

- Write project documentation, plans, reports, and code comments in English
  unless the user explicitly requests another language for that artifact.
- Use the user's language for conversation.

## Documentation

- Project documentation lives in [docs/](docs/). Read the relevant documents
  there before substantive work and keep them up to date.

## Temporary files

- Follow the rules in [development/temp-files/SKILL.md](development/temp-files/SKILL.md)
  for every temporary, intermediate or diagnostic file. Keep them in `.tmp/`.

## Git Branches for Agent Work

- Every commit made by an AI agent goes to the branch `ai_feature`, whatever the tool: Claude Code, Codex, Google Antigravity, GitHub Copilot or any other agent.
- Create `ai_feature` from `main` when it does not exist, and switch to it before committing. If it exists, continue on it.
- Do not merge or push `ai_feature` unless the user asks.
