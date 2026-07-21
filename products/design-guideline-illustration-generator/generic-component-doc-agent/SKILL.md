---
name: generic-component-doc-agent
description: Guide an agent through generating generic component documentation from a component-library documentation site, then embedding renderable React illustrations in Markdown.
argument-hint: "[optional: component docs URL]"
disable-model-invocation: false
user-invocable: true
---

# Generic Component Doc Agent

Use this skill when the user wants to generate component usage documentation for any React component library, then fill the document with renderable React illustrations.

The default output directory is `source-doc-cn/`. The generated Markdown must contain real `react` fenced blocks, not screenshots of code and not inert code examples. The user's Markdown browsing environment is expected to render those `react` blocks directly.

## Required Inputs

Collect these values before generating:

1. `docs_url`: the component library documentation entry URL, for example `https://ant.design/components/overview-cn/`.
2. `react_block_generator_path`: the local skill or folder that knows how to generate React examples for the user's component library.
   - Default: `react-block-generator/`.
   - The default generator in this repository is only a template/legacy IDS example. For another component library, the user should replace it with their own generator.
3. `output_dir`: where final Markdown files go.
   - Default: `source-doc-cn/`.
4. `language`: final document language.
   - Default: Chinese.
5. `component_filter`: optional component names or URL patterns if the user only wants part of the library.

If the user did not provide these values in the chat, open the local request form:

```bash
python3 generic-component-doc-agent/scripts/collect_request.py
```

After the form is submitted, read:

```text
.generic-component-doc-agent/request.json
```

If opening a browser is unavailable, ask for the same fields in chat and continue.

## Workflow

### 1. Discover Components

Read `docs_url` and identify component documentation pages.

For each component, collect only source facts from the official/developer docs:

- component name and category
- description and "when to use" guidance
- visible variants, types, states, and sizes
- examples/demos and their intended usage
- API details only when needed to understand behavior or generate an accurate illustration

Do not invent component types that are not present in the source docs. If the docs have contradictory pages, prefer the component's own page over overview text.

### 2. Write the Usage Guide

Use `component_writer_skill/Component_skill.md` as the writer contract.

Before writing, read these references:

- `component_writer_skill/.claude/skills/pdf/reference.md`
- `component_writer_skill/references/component_guide_example_button.md`
- `component_writer_skill/references/component_guide_output_template.md`

Generate one Markdown guide per component using the same structure as the reference:

- `1.0` component description
- `1.1` component composition
- `1.2` component types
- `1.3` typical usage cases
- `2.1` selection flow
- `3.x` interaction and layout rules
- `4.0` FAQ

Every place that needs an illustration must first contain an illustration placeholder:

```markdown
> <!-- 附图占位：建议附上一张…… -->
```

Write draft files to `component_writer_skill/output/`, then copy or move final files into `output_dir`.

### 3. Generate React Illustrations

Use `md-illustration-generator-main/skills/md-illustration-generator/SKILL.md` as the generic illustration workflow.

The illustration workflow must call the configured `react_block_generator_path`, not the IDS-specific generator unless the target library actually is IDS.

For each placeholder:

1. Read the surrounding section text.
2. Decide what the illustration should prove.
3. Ask the React block generator to produce a runnable `function App()` demo for the target component library.
4. Insert the result as a `react` fenced block near the placeholder.
5. Keep the placeholder comment only if the local renderer needs it as metadata; otherwise replace it with the final React demo.

Use this Markdown shape unless the user's generator requires a different render contract:

````markdown
```react
function App() {
  return <Example />;
}
```
````

Do not output plain JSX inside `markdown`, `js`, or `tsx` fences when the user's viewer expects `react` fences.

### 4. Validate

For each final Markdown file:

- no unresolved `附图占位` comments remain unless intentionally kept as metadata
- each illustration is a `react` fenced code block
- code blocks contain a runnable `function App()`
- no `import` / `export` appears unless the user's renderer explicitly supports it
- examples use components and props from the user's configured React generator/API notes
- generated docs are saved in `output_dir`

If a local preview/checker exists in the user's generator, run it. If not, do a static pass and report that runtime rendering was not verified.

## Replacement Contract for `react-block-generator`

The user can replace `react-block-generator/` with their own implementation. A compatible generator should provide:

- `SKILL.md`: how to turn a section/placeholder into a runnable React demo
- optional API/reference files for the target component library
- the expected Markdown code fence language, default `react`
- allowed runtime scope variables, for example `React`, `antd`, `Icons`, or a package-specific namespace
- any validation command or preview command

The orchestrator skill must treat that folder as the source of truth for React code generation.

## Handoff

Finish with:

- final Markdown file paths in `source-doc-cn/` or the configured output directory
- whether every placeholder was filled
- whether runtime rendering was verified
- any components skipped and the reason
