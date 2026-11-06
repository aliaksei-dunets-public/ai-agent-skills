---
name: technical-writing-ste
description: >
  Writes, edits, reviews, or translates to English the wording of agent-facing
  text with adapted ASD-STE100 principles: skills, agent definitions,
  references, AGENTS.md, CLAUDE.md, Copilot instructions, prompts, and docs
  written for agents. Applies to English text; translates other agent-facing
  text to English on request. Wording means sentence clarity, terms, grammar,
  punctuation, ambiguous phrasing, and repetition or list layout within the
  text, in one file or several. Use to write such text when its content is
  given, or to rewrite, simplify, proofread, translate to English, or check it
  for unclear wording or unclearly worded instructions. Preserves technical
  meaning and instruction behavior. Not for text written for human readers
  (README, user guides, manuals, reports, release notes), chat replies,
  marketing copy, or fiction. Not for designing prompts or critiquing their
  task design (inputs, output contract, structure), and not for auditing a
  skill or instruction package beyond its wording (links, file structure,
  contradictions or duplication across files).
---

# Technical Writing STE

Make agent-facing technical text clear, precise, and unambiguous. Apply these
priorities: accuracy, unambiguous meaning, clarity, then brevity.

Apply this skill only to text that an agent reads as instructions or
reference. Do not apply it to text written for human readers, such as README
files, user guides, manuals, reports, or release notes, even when that text
describes agents: those readers need explanation and context that these rules
remove. Classify a file by its type and location: a file in a skill's
`references/` folder is agent-facing even when nothing links to it. In a
document that mixes both, apply it to the agent-facing sections only. If the
audience is still unclear, do not apply the rules; state why and ask which
readers the text is for. When another skill uses this skill, that skill's
modes, audience classification, and report format take precedence.

Apply the writing rules to English text only. Accept agent-facing text in
another language only to translate it to English. For any other request about
such text, stop for that text only and continue with the other text in the
request: state that the skill applies to English text only and that the text
can be translated to English on request. In a document that mixes languages,
apply the rules to the English text and list the non-English agent-facing
sections that you left unchanged.

Do not edit or translate user phrases in another language, such as trigger
words in a `description` (quoted or not), examples of non-English input or
output, or non-English literal output templates; apply the rules to the
English text around them. Keep a rule that sets the language of the agent's
replies to users, for example "Reply to the user in German"; do not change it.

ASD-STE100 was developed for English; this skill adapts its principles for
software and AI-agent instructions. It does not guarantee formal compliance
with ASD-STE100.

## Workflow

1. Identify the text's purpose, audience, and requested mode: `create`, `edit`,
   or `review`. If all of the text is for human readers or its audience is
   unclear, or all of the existing text is not in English and the request is
   not to translate it to English, stop as the scope rules above state. The
   language of the request does not matter. If the request does not make the
   mode clear, use `review`. A review alone does not authorize edits. A
   request to proofread, rewrite, simplify, or translate agent-facing text to
   English is an `edit`; a request to check or review it is a `review`.
2. Read [the writing rules](references/writing-rules.md).
3. For existing text, identify concrete clarity, accuracy, spelling, grammar,
   or punctuation problems before editing. Leave clear, accurate text unchanged.
4. In `create`, write the requested text in English. In `edit`, correct the
   identified language problems, or translate to English when asked. In
   `review`, draft a proposed wording for each problem and do not change the
   text. Preserve suitable structure. Handle claims about code, commands,
   paths, versions, and behavior as the Accuracy section of the writing rules
   states.
5. Compare edits or proposed wordings with the original. Check technical
   meaning and the behavior contract below. Remove changes that do not resolve
   a concrete problem.
6. Report unresolved ambiguities. If a clearer formulation would require
   guessing the intended behavior, retain the original and explain the issue.

## Output

- `review`: list each finding with its location, the quoted text, the problem,
  and a proposed wording. If a wording would require guessing the intended
  behavior, state the decision the author must make instead. Mark findings
  where the proposed wording could change behavior. List suspected technical
  errors separately, without a changed claim. Do not edit files.
- `edit`: apply the edits. Summarize only edits whose reason is not obvious,
  then list suspected technical errors and unresolved ambiguities.
- `create`: deliver the text. List claims that you could not check against a
  source and unresolved ambiguities.
- Stop: state that the skill does not apply and why; for an unclear audience,
  ask which readers the text is for; for text not in English, state that it
  can be translated to English on request. Do not change files.
- For a mixed document, in any mode, name the human-facing sections and the
  non-English sections left unchanged.

## Behavior contract

Language edits must preserve:

- Purpose, scope, activation triggers, conditions, and exceptions.
- Required actions and the order of dependent actions.
- Requirement strength: mandatory, recommended, and optional actions remain
  distinct, including the meaning of `must`, `should`, and `may`.
- Permissions, prohibitions, and approval requirements.
- Stop conditions, error handling, and completion criteria.
- Input and output formats, dependencies, and required references.
- Technical terms, identifiers, API names, file paths, code, and command syntax.

Do not add requirements or remove constraints to improve style or brevity.
Preserve necessary repetition when instructions must work independently.

This skill governs language quality. If the task also authorizes functional
repairs, assess and explain those changes separately from language edits.
Do not present a behavior change as a wording improvement.
