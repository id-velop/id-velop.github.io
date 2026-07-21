# Markdown Illustration Generator

Generic skills for filling component-guide Markdown files with renderable React illustrations.

The generic workflow is:

```text
skills/md-illustration-generator/SKILL.md
```

It reads illustration placeholders in Markdown, delegates React code generation to a user-provided `react-block-generator`, and inserts `react` fenced blocks that a local documentation viewer can render directly.

## Directory Map

| Path | Purpose |
| --- | --- |
| `skills/md-illustration-generator/` | Generic Markdown illustration workflow. |
| `skills/react-block-generator/` | Legacy/example React block generator. Replace it for your own component library. |
| `skills/reference/` | Reference material retained from the previous IDS workflow. |
| `ids-doc-illustration/` | Legacy IDS/InfraD-specific generator, checker, and localization skills. |

## Generic Usage

1. Generate component Markdown with `component_writer_skill`.
2. Save the Markdown into `source-doc-cn/` or another configured output directory.
3. Replace `react-block-generator/` with your own component-library generator, or pass a custom generator path.
4. Run/use `skills/md-illustration-generator/SKILL.md` on the Markdown files.

The output should contain real renderable blocks:

````markdown
```react
function App() {
  return <YourComponent />;
}
```
````

## React Generator Contract

A replacement generator should include:

- `SKILL.md`
- component API or usage references
- allowed runtime scope variables
- the code fence language expected by the Markdown renderer, default `react`
- optional validation or preview commands

The generic Markdown workflow treats this generator as the source of truth. It does not hard-code IDS/InfraD APIs.

## Legacy IDS Workflow

The `ids-doc-illustration/` folder preserves the previous online IDS/InfraD workflow, including the internal Playground save flow and checker. Use it only for IDS/InfraD documentation or as a reference when building a new generator.
