# ai-agent-skills Agent Instructions

## Git Branches for Agent Work

- Every commit made by an AI agent goes to the branch `ai_feature`, whatever the tool: Claude Code, Codex, Google Antigravity, GitHub Copilot or any other agent.
- Create `ai_feature` from `main` when it does not exist, and switch to it before committing. If it exists, continue on it.
- Never commit agent work directly to `main`.
- Do not merge or push `ai_feature` unless the user asks.
