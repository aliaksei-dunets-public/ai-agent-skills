# Technical Writing Rules

Apply these adapted STE principles in context. Use the priorities and the
behavior contract in [SKILL.md](../SKILL.md).

Sections: Accuracy, Sentences and actions, Words and terminology, Voice and
responsibility, Conditions and ambiguity, Repetition and structure, Minimal
edits, Final comparison.

## Accuracy

Check statements about code, commands, paths, versions, and behavior against
the available sources. Do not present an assumption as a fact.

- `create`: do not invent a value. Leave out an unchecked fact that the reader
  does not need. The reader needs a fact when a required action cannot be
  performed without it, such as a command the text tells the agent to run
  when neither the request nor the available files identify that command. Then insert a clearly
  marked placeholder or a visible "unverified" note in the text, and list the
  fact in the report.
- `edit` and `review`: if you cannot check a statement, or a source
  contradicts it, do not change its claim. Report it as a suspected technical
  error and name the contradicting source, if any; a contradiction with
  another file is reported, not resolved. Language fixes that keep the claim,
  such as a spelling correction, are allowed.

## Sentences and actions

Prefer short sentences with one main idea. Split a sentence only when this
improves understanding. Keep each condition attached to every action it governs:
when one condition governs several actions, keep it in one sentence or use a
lead-in with the condition and a list of the actions, as below; do not split
the actions into separate sentences that lose the condition.
Use numbered lists for ordered actions, bullets for independent items, and
paragraphs for connected explanations. Do not turn every sentence into a list.

Before: "If validation fails, record the error and stop the deployment."

Acceptable edit:

> If validation fails:
> 1. Record the error.
> 2. Stop the deployment.

Both actions remain conditional. Do not make the stop unconditional.
The original is also clear; retain it unless the list helps the reader.

## Words and terminology

Use familiar, precise words without replacing technical terms with inaccurate
approximations. Use one term for one concept; do not vary terminology for style.
Explain unfamiliar abbreviations when the audience needs the explanation.

For example, "Check the configuration" is usually clearer than
"Perform a verification of the configuration." Retain a specialized term
such as "verification" when it names a defined process.

Replace a pronoun such as "it", "this", or "that" with the noun when the
reader could link the pronoun to more than one item. Prefer a positive
statement to a double negative.

## Voice and responsibility

Prefer active voice. Use the imperative when the actor is already known.

Before: "The configuration must be checked by the agent."

After: "The agent must check the configuration."

Keep the actor explicit when several people or agents have different duties.
If a passive sentence does not name the actor, do not add one; report the
missing actor when it matters. An actor that the imperatives of the same
instruction address counts as named.

Do not turn a recommendation into a command: "The agent should check the
configuration" must remain a recommendation. Use one modal word for each
requirement strength in a document, for example `must`, `should`, and `may`.
If the intended strength of a word such as "need to" is unclear, report it
instead of changing it.

## Conditions and ambiguity

State known conditions close to their actions. Use concrete verbs and criteria.
Phrases such as "if needed," "where possible," "appropriately," and "important
components" deserve review when they hide a decision criterion. They are not
automatically wrong.

Do not replace "Update documentation if needed" with "Update documentation
if the public API changes" unless the requirements establish that exact
condition. Otherwise, retain the wording and report the missing criterion.

Do not turn "Fix test errors" into a new mandatory procedure that adds
diagnosis, retries, or reporting. Those additions need a functional basis
outside a language edit.

## Repetition and structure

Remove repetition only when it adds no meaning. Keep repeated information
needed for independent use, safety, error prevention, or understanding without
external context. Preserve a suitable document structure and section names.
When you translate to English, translate headings and report links that point
to them.
Use headings to separate topics and tables to compare structured information.
Do not add sections or impose a common template without a concrete need.

## Minimal edits

Correct identified problems rather than restyling the entire document.
For example, leave "Read the request and identify the goal" unchanged: it is
already short, clear, and unambiguous.

Preserve code, commands, identifiers, paths, and data formats exactly during
language edits. A suspected technical error is a separate finding. Do not
change the technical token in a language edit, even if you report the change.

## Final comparison

Compare the original and revised text, including its examples, with each item
of the behavior contract. Confirm that each edit addresses a concrete problem
and adds no requirement.

For example, keep "Run tests if the implementation changes" conditional.
"Always run tests" changes behavior and is not a valid language edit.
