# Documentation Ownership

This model helps classify information; it does not prescribe directories.

| Type | Owns | Links to rather than duplicates |
| --- | --- | --- |
| Canonical reference | Contract, architecture, API, or operational rule | Live progress and full change history |
| Guide or tutorial | A supported reader workflow and its prerequisites | Complete normative contracts |
| Design | Goal, constraints, alternatives, and decisions with acceptance status | Execution plan and live progress |
| Execution plan | Task actions, dependencies, and checks | Architecture rationale |
| Result report | Actual changes, checks, deviations, and evidence | Normative contracts |
| Project status | Verified snapshot with source and date/revision | Unsupported completion claims |
| Roadmap or backlog | Future directions and outstanding work | Detailed current execution |
| Archive | Historical context and provenance | New authoritative instructions |

An index or README can summarize a topic for navigation, but links to its owner
and does not introduce competing requirements. Repeated examples are acceptable
when readers need them; independently maintained copies of a contract are not.

## Conflicting sources

Use the local ownership and precedence policy. A design states intent; code and
tests show implementation; status describes an evidenced snapshot. Their
disagreement may be an implementation gap rather than obsolete documentation.
Record both claims and sources before changing an authoritative contract.

Preserve unique information when consolidating. Do not erase caveats, decisions,
or historical context simply to shorten a document. Move content only within
authorized scope, with an incoming-link map and the project's archive policy.

## Design and plan

Use the project's existing plan location and format. A design explains what is
intended, why, and what decisions have been made; a plan describes execution
steps, dependencies, and checks. Link them without copying the full sequence
into a second owner. No specific planner or external service is required.
