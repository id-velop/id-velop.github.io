---
name: react-block-generator
description: Template contract for generating renderable React blocks for a user's component library.
argument-hint: "[component name + illustration intent + nearby markdown section]"
disable-model-invocation: false
user-invocable: true
---

# React Block Generator

This folder is a replaceable generator template.

When adapting this project to a component library, replace this skill and its API/reference files with instructions for that library. The generic documentation pipeline calls this generator whenever it needs a React illustration.

## Responsibility

Given a component name, an illustration request, and nearby Markdown text, produce a runnable React demo that can be embedded in a Markdown `react` fence.

Default output shape:

```jsx
function App() {
  return <div />;
}
```

## Required Library-Specific Configuration

Update this skill for the target library:

- available component package or runtime namespace
- whether imports are allowed by the Markdown renderer
- allowed global scope variables, such as `React`, `antd`, `Icons`, or a design-system namespace
- component API references
- theme/provider requirements
- validation command or preview command, if any
- code fence language, default `react`

## Generic Rules

1. Generate one top-level `function App()`.
2. Keep examples runnable in the user's Markdown renderer.
3. Prefer real target-library components over CSS-only drawings.
4. Use small realistic mock data when a component needs context.
5. Show the behavior or visual state requested by the placeholder and section text.
6. For comparison illustrations, include both recommended and not-recommended sides in one demo.
7. Avoid unrelated page chrome unless the section is about placement or layout context.
8. Do not output explanatory prose when the caller needs code for insertion.

## Validation

If this generator defines a validation command, the caller should run it before final handoff.

If no validation command exists, manually check:

- JSX syntax is valid
- the demo can run without missing imports/scope variables
- component names and props exist in the target library references
- text and layout match the design conclusion in the Markdown section

## Legacy Note

`COMPONENTS_API.md` may still contain IDS/InfraD examples from the original project. Treat it as legacy sample material only unless your target library is IDS/InfraD.
