---
name: ids-doc-en-localization
description: >-
  Localize IDS component documentation from Chinese to English. Use when the
  user asks to translate IDS docs, a Component article, or a folder of IDS
  Markdown/MDX files into English, including article prose and all user-visible
  text inside React Playground demos.
---

# IDS Doc English Localization

Use this skill for IDS component documentation English localization under
`/Users/danni.yang/Documents/gitlab-sync/ids-remote/Component`.

This is not generic translation. Preserve the MDX document, React demos, image
links, Playground metadata, component APIs, and checker requirements while making
the reader-facing content English.

## Default Behavior

- Work locally only. Do not commit, push, sync, publish, open StackEdit, or open
  browser windows unless the user explicitly asks.
- Treat the requested article, article set, or folder as the full task scope.
  Do not modify unrelated articles.
- Before editing existing IDS files, follow the article source check from the
  workspace instructions: fetch latest `origin/master`, compare working tree,
  local `HEAD`, and `origin/master`, and do not overwrite unclear local changes.
- If the user asks to translate a whole folder and no output location is given,
  ask once whether to replace files in place or create English copies. Do not
  guess for the first batch.
- For batch work, process one article at a time and keep a short running record
  of changed files, updated Playground code ids, and checker results.

## What To Translate

Translate all reader-facing content:

- Article headings, paragraphs, list items, tables, notes, warnings, FAQ, and
  Mermaid labels.
- Captions, recommended/not-recommended labels, comparison copy, and figure
  explanations.
- React demo user-visible text:
  - button text, menu items, tabs, labels, placeholders, helper text
  - table column titles and cell values
  - tag/status text, empty states, loading/error/success messages
  - modal/drawer titles, confirm/cancel text, notification/message content
  - mock data names, product names, task names, descriptions, addresses, and
    other sample values shown in the rendered demo
- Inline example strings when they are visible UI copy, such as
  `message.success('Saved')`.

## What To Preserve

Do not translate or rewrite these unless required to make the demo run:

- Component names, package names, imports, props, event names, variables,
  function names, CSS class names, file paths, URLs, anchors, image paths, and
  `agent_code_id` values.
- Fenced code blocks other than visible string literals that need localization.
- JSX structure, component selection, layout logic, and state logic.
- Existing image references and Markdown/MDX link targets.
- Proper nouns and IDS/Infra Design product names unless the article already
  provides an English equivalent.

If a Chinese variable name or identifier exists inside demo code, leave it alone
unless it creates a syntax, lint, or readability problem. Prefer changing only
the displayed string value.

## React Playground Demo Rules

When a `react` code block changes:

1. Localize all visible strings and mock data in that block.
2. Keep the demo runnable as plain JavaScript React code.
3. Save or refresh the Playground block through the local React block workflow so
   the hidden Playground comment matches the updated code.
4. Keep the exact block order:
   - hidden Playground link comment
   - `<sub>🖱️ 点击图片可在线演示</sub>`
   - `react` fenced code block
   - exact standalone `<br>` immediately after the closing fence
5. Report every new or refreshed Playground code id in the final handoff.

If the visible demo behavior is hard to verify after translation, inspect the
demo with the local demo-inspector workflow before calling it done.

## MDX Safety

- Never leave bare `{...}` in prose. Wrap object literals, placeholders, or
  template-like examples in inline code.
- Preserve fenced code block delimiters and language tags.
- Avoid HTML comments in publishable article text.
- Keep JSX valid when editing string literals.
- Do not convert Markdown tables, links, or image syntax into another format.

## Style

- Use clear technical English for product documentation, not literal Chinese
  sentence order.
- Keep beginner-readable wording. Explain component usage directly and avoid
  marketing tone.
- Prefer concise imperatives in guidance: "Use Button for...", "Avoid...".
- Use consistent labels:
  - `Recommended`
  - `Not recommended`
  - `Basic usage`
  - `Component composition`
  - `Usage types`
  - `Selection guide`
  - `Detailed guidelines`
  - `FAQ`
- Keep component and prop names in code style when referenced in prose, such as
  `Button`, `disabled`, and `onChange`.

## Quality Gate

Before reporting completion:

- Check that no unintended Chinese reader-facing text remains in the scoped
  article files, except proper nouns or intentionally preserved product names.
- Check that code fence counts and Markdown link/image targets are preserved.
- Run the IDS illustration checker workflow for changed article files and
  iterate until blocking issues are `0`.
- If React demos changed, confirm refreshed Playground code ids exist.
- Review the diff for accidental rewrites of code structure, paths, anchors, or
  unrelated sections.

## Final Handoff

Report only useful local handoff information:

- changed local files
- new or refreshed Playground code id values
- checker result, including blocking count
- remaining non-blocking notes, separated from blocking issues

Do not include unrelated local files, unpushed commits, raw checker noise, or
tool output unless the user asks.
