# Platform Detection and Tool Readiness

Identify the platform from the session's own environment information (system
prompt, available tools, environment variables), not from project files. Verify
each tool by checking that it is listed and, where cheap, by a read-only call.
Do not assume a command, skill or MCP server exists because this file names it.

## Mandatory design tool per platform

| Platform | Design tool | Substitute allowed |
|---|---|---|
| Claude Code (CLI, desktop, web, IDE) | Claude Design | No; Stitch is not a substitute here |
| Google Antigravity | Google Stitch | No |
| OpenAI Codex | Google Stitch | No |
| Any other agent | None defined | Report the platform and ask the user which tool to use |

The only fallback is the user-approved isolated HTML prototype described in
SKILL.md.

## Claude Code — Claude Design

Claude Design capabilities depend on the account and the client. Check which
of these the session offers:

- the `/design-sync` skill (user-started) to import the existing design system
  into a Claude Design design-system project;
- a Design artifact type or the `/design` command to create mockups and
  interactive prototypes;
- export or sharing of design links.

Workflow:

1. Inspect the React project first (phase 1).
2. If `/design-sync` is available, ask the user to run it or confirm its use,
   then review the imported components, typography, colors, spacing and tokens.
3. Treat the imported system as technical context, not as the target: the
   redesign may change it.
4. Create the concepts and mockups with the design tool; keep design work
   separate from the production source.
5. Record every project and screen link; save exports to `docs/ux-audit/mockups/`.

If the service reports that a project or tool has closed or moved, quote its
message and treat the tool as unavailable.

## Antigravity and Codex — Google Stitch

1. Check that the Stitch MCP server is listed, connected and authenticated
   (Codex: also list the installed Stitch plugins and skills).
2. Check which Stitch agent skills exist. Preferred, when available:
   `stitch::extract-design-md`, `stitch::code-to-design`,
   `stitch::generate-design`, `stitch::manage-design-system`,
   `stitch::upload-to-stitch`. Use `stitch::react-components` only after the
   user approves implementation.
3. If something is missing, find the required configuration in the official
   Stitch documentation and present the steps; ask before changing anything.
4. Import the existing design system and UI references when possible, with
   synthetic data only.
5. Generate the concept screens, compare variants, export images and assets,
   and record project and screen links.
6. Prepare React integration notes without touching production code.

## Supporting tools

- **Browser automation**: Playwright MCP, the platform's built-in browser, or
  an equivalent. Needed for the audit, screenshots at 1440 × 900 and 390 × 844,
  and the fallback prototypes.
- **DevTools**: console, network and accessibility tree for evidence.
- **React project**: source readable; launch command known; test sign-in known
  when pages require it.

## Tool Readiness Report

`01-tool-readiness.md` starts with the detected platform and this table:

| Tool | Available | Configured | Action needed |
|---|---|---|---|
| Mandatory design tool (Claude Design / Stitch) | | | |
| Browser automation (Playwright or equivalent) | | | |
| Browser DevTools | | | |
| React project (source, launch, test sign-in) | | | |
| Screenshot capability | | | |
| Design export capability | | | |

Under the table, list what was verified and how, what is blocked, and which
phases each gap affects.
