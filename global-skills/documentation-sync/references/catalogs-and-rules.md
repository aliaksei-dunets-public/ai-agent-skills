# Catalogs and Agent Rules

Read this when documentation describes concrete code artifacts (components,
tokens, endpoints, configuration keys, commands, events, schemas) or holds
rules that agents and developers must follow.

## Catalog entries

- One entry per artifact, in its canonical owner. Cite the source path and the
  symbol; link to it from guides instead of repeating the entry.
- Record a status per entry:
  - `implemented`: verified in current source;
  - `planned`: approved but not built; cite the approval source (design,
    decision, accepted proposal). Unapproved proposals are not entries;
  - `deprecated`: still in source; name the replacement and removal condition.
- Verify each `implemented` entry against source: the path and symbol exist,
  the documented signature, props, parameters, defaults, variants or states
  match, and examples use the current interface. Report entries that cannot be
  verified instead of guessing.
- On sync, flip `planned` to `implemented` only after verification, add
  `deprecated` for replaced artifacts, and remove an entry only when the
  artifact is gone from source and the scope authorizes removal.
- An approved design merged into a catalog enters as `planned`; never describe
  mockups, plans or proposals as implemented.
- Examples use synthetic values: no secrets, real customer, personal or
  financial data.

## Fields per catalog kind

Use the project's existing format when one exists; otherwise these fields:

| Kind | Fields |
| --- | --- |
| UI component | path, purpose, props (name, type, default, required), variants and sizes, states, accessibility (role, keyboard, labelling), use when, do not, replaces |
| Design token | name, value per theme, purpose, source path; semantic tokens map to meaning, not color names |
| UI pattern or page template | when to use, structure and regions, components used, behavior rules, states and messages |
| API endpoint or function | signature or method and path, parameters, result, errors, side effects, auth |
| Configuration key | name, type, default, allowed values, effect, where read |
| CLI command | syntax, flags, exit codes, side effects |
| Event, message or schema | name, fields and types, producer, consumers, versioning |

## UI contract

When a project documents its UI as a contract, cover these topics, mapped onto
the project's existing owners (or `docs/ui/` when the project has none and the
create request accepts the proposal):

- index with mandatory rules for agents (see below);
- tokens: colors and semantic statuses, typography, spacing, radius, shadow,
  z-index, motion;
- components: shared component catalog;
- layout: app shell, navigation and route mapping, page templates, grid,
  breakpoints, mobile navigation;
- patterns: tables, filters, search, forms, dialogs, drawers, notifications,
  loading, empty, error and permission states;
- accessibility: project rules for WCAG 2.2 AA;
- content: terminology and formatting of numbers, dates, currency, units and
  missing versus zero values, including domain rules from project instructions.

Split a topic when distinct reader tasks or ownership boundaries make separate
documents easier to use. Length alone does not justify restructuring.

## Agent rules

When documentation is a contract that agents must follow:

- Keep the mandatory rules short and testable in the contract's index, for
  example: use documented tokens and components; add a catalog entry in the
  same change as a new shared artifact; implement the documented states; do not
  change business logic in a documentation or UI task.
- State the scope (source directories covered) and the last verified revision.
- Propose a pointer in project instructions (`AGENTS.md`, `CLAUDE.md` or the
  platform's equivalent) and add it only with the user's consent, for example:

  ```text
  - UI work: follow docs/ui/README.md; update it in the same change as new
    shared components or tokens.
  ```

- Keep rules in one owner; project instructions link to it rather than copy it.
