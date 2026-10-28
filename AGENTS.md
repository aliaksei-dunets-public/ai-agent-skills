# AGENTS.md

## Language

- Write project documentation, plans, reports, and code comments in English
  unless the user explicitly requests another language for that artifact.
- Use the user's language for conversation.

## Responses to the user

- State concrete facts and criteria. Replace vague words such as "correctly",
  "where needed", or "seems to work" with what changed, what was checked, and
  the result.
- Report what you verified and what you did not verify. Do not present an
  assumption as a fact.
- Keep each condition next to the action it governs.
- Use one term for one concept. Replace "it" or "this" with the noun when the
  reference is unclear.
- Keep requirement strength: do not turn a recommendation into a requirement
  or a prohibition.
- Prefer short sentences and active voice. Use numbered lists for ordered
  steps; do not turn every sentence into a list.
- Preserve commands, paths, and identifiers exactly.

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
