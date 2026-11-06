# Audit Checklist

Loaded in every run at the content audit. Sections: 1 Purpose and activation,
2 Structure and progressive disclosure, 3 Consistency, 4 Contradictions and
precedence, 5 Clarity, 6 Context efficiency, 7 Tools, delegation, and side
effects, 8 Security and trust, 9 Output contract, 10 Maintenance.

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
  Does the caller's trigger condition agree with the `description`? Does any
  consumer describe the package differently from its entry point?

## 2. Structure and progressive disclosure

- Does the entry point contain the workflow and decisions, and leave long
  domain detail, examples, and platform specifics to references?
- Does every reference have a pointer that says **when** to load it, and does
  that condition cover every decision that depends on the file? A rule needed
  on every run must not live only in a file loaded on a narrower condition.
- Are references loaded only when needed, not "read everything first"? A
  pointer that loads a reference at the start ("before you start", "read
  first") when only a later step uses it is a candidate finding: it wastes
  context and puts examples before the rules they illustrate.
- Are reference routes clear and justified, including cross-skill dependencies,
  without unnecessary indirection or repeated loading? An additional level is
  justified when it reuses a maintained dependency or separates conditional
  detail; indirection that adds no decision value is not.
- Are always-on files (`AGENTS.md`, `CLAUDE.md`, Copilot instructions) short
  and limited to facts needed on most tasks?
- Can a reader find each part of the entry point in a predictable order? A
  typical order is: frontmatter, purpose, modes or inputs, resource load
  conditions, workflow, output contract, boundaries. This is a reference
  shape, not a template: report a deviation only when it hides a decision, a
  load condition, or an output requirement.
- Are activation conditions in the `description`? The body loads only after
  the skill is selected, so a "When to use" section in the body cannot
  trigger the skill. Body text may refine scope after activation.
- Does each reference state near its top what it covers and when it is
  loaded? Does a reference longer than about 100 lines (or the target
  platform's threshold) start with a table of contents?
- Are installation steps, change history, and human-facing explanations kept
  in README, guide, or changelog files rather than in the entry point?
- Do pointers to another file name stable section headings rather than step
  or line numbers that change when that file is edited?

## 3. Consistency

- Does each shared rule have a canonical source? Are repeated copies consistent
  and necessary for their consumers? Would removing a copy leave an executor
  without the rule when it is needed?
- Classify each group of similar rules (from the duplication comparison in
  the content audit) and propose the matching fix:

  | Class | Fix |
  | --- | --- |
  | Copy or paraphrase with the same meaning | Keep the canonical copy; replace the others with a pointer or remove them. |
  | Drift: different limit, condition, or requirement strength | Treat as a contradiction: one rule, chosen from established intent, or a question. |
  | Subsumption: one rule includes the other | Keep the broader rule; keep the narrower copy only if it adds a condition or detail. |
  | Repetition for an independent executor (one that does not load the other copy) | Keep; make the copies consistent. |
  | Repetition in files loaded in the same scenario, kept for safety or clarity | Keep only with a stated reason; make the copies consistent. Without a reason, treat it as a copy. |
  | Summary in human-facing documentation | Keep at summary level; remove procedural detail that can drift. |

- A copy in a consumer outside the package follows the Repair principles in
  `SKILL.md`: change it only when it is in the requested scope; otherwise
  report it to its owner.
- Which copy is canonical? Decide in this order; the first item that leaves
  one candidate decides, and later items do not override it:
  1. Keep only candidates that load, before the rule is needed, in every
     scenario that needs the rule.
  2. Apply the class: for subsumption, the broader rule is canonical.
  3. Across layers, choose by scope: always-on fact → instruction file, task
     procedure → skill, detail → reference.
  4. Within one layer, prefer the file dedicated to the rule's topic (a
     format reference for format rules, `technical-writing-ste` for wording
     rules), then the file that owns the step where the rule applies.

  Report the choice; a step that needs the rule keeps a pointer, not a copy.
- When the package is part of a skill collection, do sibling skills carry the
  same rule bodies? Report a candidate shared dependency; edit siblings only
  when they are in the requested scope.
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
  actually exist elsewhere in the package? Are they reserved for hard
  requirements? Overused absolutes make real requirements indistinguishable.
- When layers can disagree (system, project, skill, user, reference), is the
  precedence stated?
- Do defaults conflict between modes or sections?

## 5. Clarity

Apply the writing rules and behavior contract from `technical-writing-ste`,
loaded through the optimizer entry point, to agent-facing text only (Audience
and language in `SKILL.md`). Report only concrete issues, not stylistic
preferences. Also check:

- Is agent-facing text in English, apart from the exceptions in Audience and
  language?
- Is each rule actionable: a condition, an action, and when it is done?
- Are rules phrased as what to do, with prohibitions kept for real hazards?
- Are terms defined where first used?
- Are stop conditions and completion criteria explicit?
- Does the workflow say what to do on failure or missing input?
- Does the text explain *why* for non-obvious rules, so the agent can apply
  them to unforeseen cases?
- Is there process micromanagement where an outcome and criteria would do?

## 6. Context efficiency

- Is the same material loaded twice (in the entry point and a reference, or in
  several always-on files)?
- Are there long passages with little decision value: restated goals,
  generic advice the model already follows, narrative history?
- Are large examples or schemas loaded on every task when few tasks need them?
- Do examples show a format or a hard distinction rather than restate rules?
  Would one example do where several are similar?
- Is content needed only in one mode or a rare case (for example, fix-only
  steps) kept in a file that every run loads?
- Does a reference described as conditional load on nearly every run, so the
  split saves nothing?
- Does the entry point exceed the target platform's size guidance (see
  `platforms.md`)? Treat this as a reason to look for movable detail, not as a
  defect by itself.
- Does the workflow search before reading large files or directories?

## 7. Tools, delegation, and side effects

Only when the package uses tools or subagents.

- Does each subagent have a concrete reason to exist (different tools or
  permissions, isolated context, independent review, real parallel work)?
- Do handoffs pass only the assignment, relevant context, constraints, and
  expected output — not full history? Is the expected result compact (status,
  findings, changes, verification, blockers)?
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
- Does "be concise" stand alone, without saying what must survive? Does the
  contract separate analysis depth from answer length, and allow a longer
  answer for critical risk, failed verification, conflicts, or missing
  evidence?
- Are empty sections omitted rather than filled?
- Is the response language rule clear (user's request language, or explicit
  instruction), with code and identifiers left untouched?
- If output is machine-consumed, is there a schema rather than prose rules?

## 10. Maintenance

- Do version-specific or platform-specific claims carry a date or a note that
  they need verification?
- If the package uses release metadata, do behavior changes follow its release
  convention?
- Are there leftover files, dead sections, TODOs, or references to removed
  features?
