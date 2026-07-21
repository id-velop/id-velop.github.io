# Component Writer Skill

Generic skill for writing component usage guides from a component library's official or developer documentation.

It is usually called by `generic-component-doc-agent`, but it can also be used directly when you already have source notes for a single component.

## Structure

```text
component_writer_skill/
├── Component_skill.md
├── output/
├── references/
│   ├── component_guide_example_button.md
│   └── component_guide_output_template.md
└── README.md
```

## How It Works

1. Read the target component documentation.
2. Extract component purpose, types, states, scenarios, and constraints.
3. Write a Markdown guide following the reference structure.
4. Save drafts to `output/{ComponentName}_Component_Guide.md`.
5. Leave specific `附图占位` comments for the illustration workflow.

## References

- `Component_skill.md` is the writer contract.
- `references/component_guide_example_button.md` is the main structure/style example.
- `references/component_guide_output_template.md` is the quick checklist.
- `.claude/skills/pdf/reference.md` is the long-form reference requested by the orchestrator workflow.

The examples may mention a specific component library, but they are examples only. The source of truth is always the user's documentation URL and notes.
