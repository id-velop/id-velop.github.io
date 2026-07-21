---
name: component-guide-writer
description: Write maintainable component usage guides from any component library's official/developer documentation.
argument-hint: "[component source notes or component documentation URL]"
disable-model-invocation: true
user-invocable: true
---

# Component Guide Writer

## Goal

Generate a complete, reviewable Markdown component usage guide from the user's component library documentation.

This writer is generic. The target component library is determined by the documentation URL and source notes supplied by `generic-component-doc-agent`; do not assume IDS, InfraD, Ant Design, or any other component system unless that is the user's configured source.

## Required References

Before writing, read:

1. `.claude/skills/pdf/reference.md` for the user's required long-form reference style.
2. `references/component_guide_example_button.md` for the concrete Markdown structure and level of detail.
3. `references/component_guide_output_template.md` as a quick structure checklist.

The Button example is a structure/style reference, not a component-library source of truth.

## Input Contract

The caller should provide one component input card with:

- component name
- source documentation URL
- category or navigation group
- official description and when-to-use guidance
- observed types, variants, sizes, and states
- demo summaries from the developer docs
- any API details needed to understand behavior
- target language, default Chinese

If the caller provides only a documentation URL, read the component page before writing.

## Output Rules

1. Output one complete Markdown document.
2. Save to `output/{ComponentName}_Component_Guide.md`.
3. Use the target language consistently. Chinese output should avoid unnecessary English, except established proper nouns.
4. Write design and usage rules, not implementation tutorials.
5. Do not include raw props tables, code snippets, installation steps, or API dumps.
6. Every rule must be verifiable by observable product/design conditions.
7. Component types must come from the user's source docs. If there are more than seven variants, group them by user-facing purpose and risk.
8. Every location needing an illustration must include:

```markdown
> <!-- 附图占位：建议附上一张…… -->
```

The illustration suggestion must explain the image type, what should be shown, and the design conclusion it should communicate.

## Fixed Structure

Follow the exact heading order and density from `references/component_guide_example_button.md`:

- `1.0 组件描述`: one sentence about the component's value.
- `1.1 组件构成`: basic elements, with an illustration placeholder if useful.
- `1.2 组件包含哪些不同类型`: `1.2.1` to `1.2.N`, each type containing `是什么`, `简单用法`, `典型场景`, and `替代方案`.
- `1.3 各类型典型场景案例`: recommendation vs non-recommendation cases, each with an illustration placeholder.
- `2.1 选择流程`: Mermaid flowchart.
- `3.1` to `3.6`: detailed interaction and layout rules.
- `4.0 常见问题`: Q&A.

Do not add, remove, or reorder top-level sections unless the caller explicitly provides a different template.

## Writing Workflow

1. Read the required references.
2. Read the component source docs.
3. Extract only verifiable facts:
   - what the component is for
   - when it should be used
   - available user-facing types and states
   - key usage constraints
   - examples that clarify real scenarios
4. Identify the default type for `2.1`:
   - Count special conditions for each type, such as destructive outcome, persistent selected state, parent-child hierarchy, asynchronous loading, or explicit primary/secondary operation hierarchy.
   - The type with the fewest special conditions is the default branch.
   - If tied, prefer the type shown most frequently or earliest in official examples.
5. Write the guide using the fixed structure.
6. Self-check:
   - no unsupported component types
   - no code/API dump
   - no unverifiable advice
   - all illustration placeholders are specific enough for a React illustration generator
   - output file path matches `output/{ComponentName}_Component_Guide.md`

## Boundary Handling

- If the source docs lack enough information to write a section, mark the assumption clearly and keep it conservative.
- If official docs conflict with user-supplied notes, prefer user-supplied notes only when they are explicitly described as local design-system rules.
- If the caller requests multiple components, write one file per component and keep naming consistent.
