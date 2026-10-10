# Case: Well-Designed Prompt (No Material Issue)

Mode: quick

The audited prompt is 40 lines. It states one outcome and success criteria,
loads a single routed reference only for date parsing, returns output validated
by a JSON schema in the application, requires user approval for its only write
tool (enforced by the application, with an idempotency key), and reports tool
failures explicitly. Evals over 25 representative tasks show 100% schema
validity and no regressions.
