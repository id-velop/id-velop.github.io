---
name: react-block-generator
description: Template contract for generating renderable React blocks for a user's component library.
argument-hint: "[component name + illustration intent + nearby markdown section]"
disable-model-invocation: false
user-invocable: true
---

# React Block Generator

This folder is the default replaceable React illustration generator used by `generic-component-doc-agent`.

Replace this folder with instructions and API references for your own component library. The pipeline calls it to turn each Markdown illustration request into a runnable React demo.

## Output Shape

Unless your Markdown renderer requires something else, return code that can be placed inside a `react` fenced block:

```jsx
function App() {
  return <div />;
}
```

## Configure for Your Library

Document these details here:

- component package or runtime namespace
- whether the renderer supports `import` statements
- allowed global variables, for example `React`, `antd`, `Icons`, or a library namespace
- provider/theme setup
- component APIs and examples
- validation or preview commands
- required code fence language, default `react`

## Generation Rules

1. Generate one top-level `function App()`.
2. Keep examples runnable in the user's Markdown renderer.
3. Prefer real target-library components over CSS-only drawings.
4. Use realistic but compact mock data when needed.
5. Match the nearby Markdown section's design conclusion.
6. For recommendation/comparison sections, show both sides in one demo.
7. Avoid unrelated explanation; return code when the caller needs code insertion.

## Validation

If this generator defines a validation command, run it before final handoff.

If no validator exists, manually check syntax, runtime scope, component names, props, and whether the illustration matches the document text.

## Legacy Note

`COMPONENTS_API.md` may still contain IDS/InfraD examples from the original project. Treat it as sample material only unless your target library is IDS/InfraD.
