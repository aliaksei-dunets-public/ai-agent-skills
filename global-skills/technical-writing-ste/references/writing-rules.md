# Technical Writing Rules

Apply these adapted STE principles in context. Accuracy and unambiguous meaning
take priority over clarity and brevity. Use the behavior contract in
[SKILL.md](../SKILL.md) when editing instructions.

## Sentences and actions

Prefer short sentences with one main idea. Split a sentence only when this
improves understanding. Keep each condition attached to every action it governs.
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

## Voice and responsibility

Prefer active voice. Use the imperative when the actor is already known.

Before: "The configuration must be checked by the agent."

After: "The agent must check the configuration."

Keep the actor explicit when several people or agents have different duties.
Do not turn a recommendation into a command: "The agent should check the
configuration" must remain a recommendation.

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
Use headings to separate topics and tables to compare structured information.
Do not add sections or impose a common template without a concrete need.

## Minimal edits

Correct identified problems rather than restyling the entire document.
For example, leave "Read the request and identify the goal" unchanged: it is
already short, clear, and unambiguous.

Preserve code, commands, identifiers, paths, and data formats exactly during
language edits. A suspected technical error is a separate finding, not a reason
to silently change a technical token.

## Final comparison

Compare the original and revised instructions, including their examples:

- Do they require the same actions under the same conditions?
- Are requirement strength, permissions, prohibitions, and exceptions unchanged?
- Is the order of dependent actions unchanged?
- Are technical details, dependencies, and completion criteria intact?
- Does each edit address a concrete problem without adding a requirement?

For example, keep "Run tests if the implementation changes" conditional.
"Always run tests" changes behavior and is not a valid language edit.
Apply the same comparison to Russian text; do not translate a document merely
to apply these principles.
