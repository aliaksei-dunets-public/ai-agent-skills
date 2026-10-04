# Prompt Structure and Domain Techniques

Read this menu only when a complex template or a domain-specific technique needs
more structure than the entry point provides. The workflow and output rules live
in [SKILL.md](../SKILL.md); this file does not define another workflow.

## Optional sections

Include a section only when it contributes information the target needs:

| Section | Useful when |
| --- | --- |
| Role or audience | Perspective, expertise boundaries, or reader expectations affect the result |
| Context | Background changes how the task should be performed |
| Task | State the concrete action and deliverable |
| Inputs and sources | Data, documents, URLs, file paths, or input slots are required |
| Constraints | Scope, language, compatibility, tone, or action limits matter |
| Success criteria | The result needs observable acceptance conditions |
| Output format | Structure is requested or needed by the consumer |
| Examples | A non-obvious format or behavior benefits from examples |

A reusable template may have clearly named input slots. Do not label unknown
facts as filled-in values. Keep instructions separate from quoted inputs using
delimiters appropriate to the material; XML is one option, not a requirement.

## Domain choices

Use these only when the domain creates a concrete need:

- **Code:** preserve relevant interfaces, compatibility, and failure behavior.
  Request architecture discussion for meaningful design choices; a small fix may
  need only the change and verification.
- **QA:** specify observable expected results and relevant positive, negative,
  or boundary cases. Use tables when comparison is useful, not as a fixed format.
- **Data:** identify sources, units, assumptions, and checks that could falsify
  the conclusion. Request a method or visualization only when it helps.
- **Creative:** audience, tone, brand constraints, or call to action may matter.
  Ask for multiple variants or sensory detail only when the brief benefits.
- **Learning:** adapt prerequisites, explanation depth, examples, and practice
  to the learner. Do not force a beginner-to-expert sequence.
- **Agent:** describe supported tools, allowed actions, required inputs, partial
  results, failures, and completion criteria. Preserve necessary sources and
  evidence; use state tracking only for work that needs continuation.

## Additional structure

Use few-shot examples when their information outweighs their context cost.
For a machine consumer, specify the required schema and failure representation
rather than adding prose that conflicts with the format. For multi-step work,
describe dependencies and checks without requesting hidden reasoning.

When a numeric audit score is requested, state the evaluated criteria, such as
goal clarity, input sufficiency, consistency, feasibility, and output testability.
Explain the scale briefly; a static rating is not measured target-model quality.
