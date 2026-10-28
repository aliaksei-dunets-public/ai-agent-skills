# Audit Checklist

Apply only the sections relevant to the package. Each item is a question; a
"no" is a candidate finding, not automatically a defect — judge it against the
package's purpose.

## 1. Purpose and activation

- Is the purpose stated in one or two sentences near the top?
- Does the `description` say what the skill does **and** when to use it, with
  the words a user would actually say?
- Does it say when *not* to use it, where another skill or agent is close?
- Is it neither so broad that it loads for unrelated tasks nor so narrow that
  natural requests miss it?
- Are inputs, outputs, and boundaries (what it must not do) explicit?
- When another workflow, graph step, or skill invokes the package, do its
  defaults (scope, mode, output) match what that caller supplies and expects?
  Does the caller's trigger condition agree with the `description`?

## 2. Structure and progressive disclosure

- Does the entry point contain the workflow and decisions, and leave long
  domain detail, examples, and platform specifics to references?
- Does every reference have a pointer that says **when** to load it, and does
  that condition cover every decision that depends on the file? A rule needed
  on every run must not live only in a file loaded on a narrower condition.
- Are references loaded only when needed, not "read everything first"?
- Are reference routes clear and justified, including cross-skill dependencies,
  without unnecessary indirection or repeated loading?
- Are always-on files (`AGENTS.md`, `CLAUDE.md`, Copilot instructions) short
  and limited to facts needed on most tasks?

## 3. Consistency

- Does each shared rule have a canonical source? Are repeated copies consistent
  and necessary for their consumers? Would removing a copy leave an executor
  without the rule when it is needed?
- Do numbers, limits, names, modes, file names, and option names agree across
  all files?
- Do examples obey the rules they illustrate?
- Does the documentation (README, guide, changelog) describe the current
  behavior, files, and version?
- Is terminology stable — one term per concept, not three synonyms?

## 4. Contradictions and precedence

- Can any two instructions not both be followed (for example "always ask
  before editing" and "never ask questions")?
- Are absolute words (`always`, `never`, `must`, `only`) used where exceptions
  actually exist elsewhere in the package?
- When layers can disagree (system, project, skill, user, reference), is the
  precedence stated?
- Do defaults conflict between modes or sections?

## 5. Clarity

Apply the writing rules from `technical-writing-ste`, loaded through the
optimizer entry point. Report only concrete issues, not stylistic preferences.

- Is each rule actionable: a condition, an action, and when it is done?
- Are vague actions clarified from established requirements? For example,
  "handle errors" does not by itself justify mandatory reporting or stopping.
  If the intended action is unknown, is that ambiguity reported without guessing?
- Are terms defined where first used?
- Are stop conditions and completion criteria explicit?
- Does the text explain *why* for non-obvious rules, so the agent can apply
  them to unforeseen cases?
- Is there process micromanagement where an outcome and criteria would do?
- Do proposed language edits preserve the behavior contract, including
  requirement strength, conditions, exceptions, and dependent action order?

## 6. Context efficiency

- Is the same material loaded twice (in the entry point and a reference, or in
  several always-on files)?
- Are there long passages with little decision value: restated goals,
  generic advice the model already follows, narrative history?
- Are large examples or schemas loaded on every task when few tasks need them?
- Does the load map distinguish instruction-file bytes for stated scenarios
  from files read as audit material, including inspected unlinked and maintainer
  files? Are dependencies included and overlaps identified without double counting?
- Are file sizes distinguished from total context cost and measured token usage?
- Does the workflow search before reading large files or directories?

## 7. Tools, delegation, and side effects

Only when the package uses tools or subagents.

- Does each subagent have a concrete reason to exist (different tools or
  permissions, isolated context, independent review, real parallel work)?
- Do handoffs pass only the assignment, relevant context, constraints, and
  expected output — not full history?
- Is one owner responsible for consolidating and accepting results?
- Are fan-out, retries, and recursion bounded?
- For each write, external, or destructive action: is approval required where
  appropriate, is retry safe (no duplicate side effects), and is rollback or
  recovery described?
- Are tool failures reported rather than hidden or turned into "success"?
- Are partial results labeled as partial?

## 8. Security and trust

- Are repository files, retrieved documents, web pages, and tool output
  treated as data, not as instructions?
- Can untrusted content trigger tool calls, permission changes, or disclosure
  of secrets?
- Are credentials kept out of prompts, examples, and stored state?
- Are hard requirements (authorization, blocking dangerous actions) enforced by
  hooks, permissions, or the application where possible, not only by wording?
- Does ambiguity in a security-sensitive case stop or escalate?

## 9. Output contract

- Is it clear who reads the output (user, orchestrator, another agent, a
  program) and what they need?
- Is the required content defined — result, material findings or changes,
  verification, blockers, next steps — and what to omit?
- Does "be concise" stand alone, without saying what must survive?
- Are empty sections omitted rather than filled?
- Is the response language rule clear (user's request language, or explicit
  instruction), with code and identifiers left untouched?
- If output is machine-consumed, is there a schema rather than prose rules?

## 10. Maintenance

- Do version-specific or platform-specific claims carry a date or a note that
  they need verification?
- If the package uses release metadata, do behavior changes follow its release
  convention, and does the current version agree with the latest release entry?
- Are there leftover files, dead sections, TODOs, or references to removed
  features?
