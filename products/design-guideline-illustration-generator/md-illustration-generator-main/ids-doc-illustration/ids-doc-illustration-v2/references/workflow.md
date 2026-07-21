# Workflow

## Responsibilities

`ids-doc-illustration-v2` edits documentation and generates React demo blocks.

`ids-doc-illustration-checker` determines whether the result is compliant.

Do not duplicate checker rules in generation logic. Use checker output as the task list.

## Default Sequence

1. Run checker on the target file.
2. Read reference baseline.
3. Edit only failing or requested sections.
4. Add `agent_code_id=TBD` links above new `react` blocks.
5. Save Playground links with `scripts/save_playground_blocks.js`.
6. Send the Playground preview links to the user section by section. Wait for explicit user approval before proceeding. Do not edit the Markdown, commit, push, or create an MR until the user confirms the illustrations look correct.
7. Run checker again.
8. Optionally render preview only when requested.

## Editing Scope

Prefer targeted edits. Do not rewrite a whole component guide just because one figure is wrong.

Keep existing remote images, user-provided content, and prose unless they directly conflict with the requested fix or checker failure.

## Git Push Rules (IDS repo)

- **Always push to `master`** — even if the document or user mentions `main` or any other branch name, push to `master`.
- **Never create a new branch.** Commit and push directly to `master`.
- **Never create a Merge Request.** All documentation changes go straight to `master`.

## Completion Criteria

A task is complete when:

- all requested sections are updated
- all new React blocks have real Playground links
- checker exits `0`
- temporary preview files are either intentionally kept for review or removed before push

11. Iterate until checker blocking issues are `0`, including missing demo-hint text and missing `<br>` spacing.