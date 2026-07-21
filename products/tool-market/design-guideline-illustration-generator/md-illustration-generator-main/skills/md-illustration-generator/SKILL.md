---
name: md-illustration-generator
description: Fill component-guide Markdown illustration placeholders with renderable React blocks using a user-configured React block generator.
argument-hint: "[markdown file or directory] [optional react_block_generator_path]"
disable-model-invocation: false
user-invocable: true
---

# Markdown Illustration Generator

This is the generic illustration workflow for component documentation.

It scans Markdown component guides, reads `附图占位` comments and nearby section text, calls the configured React block generator, and inserts renderable `react` fenced code blocks.

Do not assume IDS, InfraD, Shopee, or an internal Playground unless the configured React block generator explicitly requires them.

## Inputs

- `target`: a Markdown file or directory, usually `source-doc-cn/`.
- `react_block_generator_path`: local folder/skill used to generate demos.
  - Default: `react-block-generator/`.
- `code_fence`: Markdown fence language.
  - Default: `react`.
- optional preview/check command from the configured generator.

## Required Reading

Before editing Markdown:

1. Read the target Markdown section that contains the placeholder.
2. Read `${react_block_generator_path}/SKILL.md`.
3. If the generator references API files, read only the files needed for the current component.

The generator is the source of truth for runtime scope variables, allowed components, imports, validation, and preview behavior.

## Placeholder Detection

Treat these as illustration requests:

- `<!-- 附图占位：... -->`
- `<!-- illustration: ... -->`
- `<!-- demo: ... -->`
- a section whose text clearly asks for a visual comparison, state example, or usage scenario

For each request, use the placeholder plus the nearest heading and paragraph text to determine the image intent.

## Generation Rules

1. Generate one runnable React demo per illustration request.
2. Prefer a single top-level `function App()`.
3. Use the target component library's real components when available.
4. Keep examples focused on the design conclusion described by the document.
5. For recommendation/comparison sections, show both the recommended and not-recommended behavior in the same demo unless the document says otherwise.
6. Do not insert inert code blocks. The final Markdown must use the configured renderable fence, default:

````markdown
```react
function App() {
  return <div />;
}
```
````

7. Do not preserve unresolved placeholders unless the user's renderer uses them as metadata.

## Validation

After editing:

- every intended illustration has a nearby renderable React block
- no accidental `jsx`, `tsx`, `js`, or `markdown` fence is used for renderable illustrations unless configured
- code follows the configured generator's runtime contract
- no unresolved placeholder remains unless intentionally retained
- the Markdown still follows the component guide structure

If the configured generator provides a validation command, run it. If no validator exists, do a static read-through and state that runtime rendering was not verified.

## IDS Legacy Workflow

The folders under `ids-doc-illustration/` remain available as legacy IDS workflows. Use them only when the target component library is IDS/InfraD or when the user explicitly requests the old IDS checker/Playground behavior.
