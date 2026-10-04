# Spec Document Reviewer Prompt Template

Use this template when a separate spec review is authorized and useful. Otherwise
apply the checks as self-review. Give the reviewer read-only scope and actual
requirements and sources, without the author's persuasive narrative.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Review after:** The spec is reviewable in the project's chosen location.

```
Subagent (general-purpose):
  description: "Review spec document"
  prompt: |
    You are a spec document reviewer. Verify this spec is complete and ready for planning.

    **Spec to review:** [SPEC_FILE_PATH]
    **Requirements and project constraints:** [SOURCE_PATHS_OR_REQUEST]
    Do not edit files or approve on behalf of the user. Your result is a
    technical assessment, not execution or user acceptance.

    ## What to Check

    | Category | What to Look For |
    |----------|------------------|
    | Completeness | TODOs, placeholders, "TBD", incomplete sections |
    | Consistency | Internal contradictions, conflicting requirements |
    | Clarity | Requirements ambiguous enough to cause someone to build the wrong thing |
    | Scope | Focused enough for a single plan — not covering multiple independent subsystems |
    | YAGNI | Unrequested features, over-engineering |

    ## Calibration

    **Only flag issues that would cause real problems during implementation planning.**
    A missing section, a contradiction, or a requirement so ambiguous it could be
    interpreted two different ways — those are issues. Minor wording improvements,
    stylistic preferences, and "sections less detailed than others" are not.

    Mark ready for planning unless serious gaps would lead to a flawed plan.

    ## Output Format

    ## Spec Review

    **Status:** Ready for planning | Issues Found

    **Issues (if any):**
    - [Section X]: [specific issue] - [why it matters for planning]

    **Recommendations (advisory, do not block planning):**
    - [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations
