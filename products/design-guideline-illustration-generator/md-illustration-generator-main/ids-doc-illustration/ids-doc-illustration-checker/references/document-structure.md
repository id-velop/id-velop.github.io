# Document Structure Rules

Use these rules for full IDS / Infra component guide Markdown files.

## Required Top-Level Sections

A complete component guide should include:

- `## 1.0. 组件描述`
- `## 1.1. 组件构成`
- `## 1.2. 组件包含哪些不同类型`
- `## 1.3. 各类型典型场景案例`
- `# 2. 选型指南` or `## 2.x`
- `# 3. 细致专业部份` or `## 3.x`

## 1.1 Component Composition

Do not generate a first illustration for `1.1 组件构成`.

Keep the textual bullet list. If an old placeholder exists here, report it as removable.

## 1.2 Type Sections

Each `### 1.2.x` section should follow this order:

1. `**是什么**`
2. shape illustration
3. `**简单用法**`
4. `**典型场景**`
5. scenario illustration
6. `**替代方案**`

The checker treats any of these as an illustration:

- local placeholder comment
- Playground-linked `react` code block
- trusted remote `<img src="https://editor.shopee.io/...">` or `/uss/` image

## 1.3 Scenario Sections

Each `### 1.3.x` section should contain one comparison illustration, followed by:

```markdown
✅ **推荐：** ...

<hr>

❌ **不推荐：** ...
```

## Playground Link and Demo Hint (Blocking)

Every `react` code block that is used as a documentation illustration must have **both** of the following lines immediately above it, in this exact order:

```markdown
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=XXXX) -->
<sub>🖱️ 点击图片可在线演示</sub>
```

Flag as a **blocking error** if either line is missing or if the two lines appear in the wrong order (hint must come between the comment and the ` ```react ` block).

## MDX Compatibility (Blocking)

Flag as a **blocking error** if any prose paragraph (outside a fenced code block) contains a bare `{…}` that is not wrapped in backticks.

Examples of violations:

```
# ❌ bare brace in prose — MDX build error
gutter 可设置为对象 { xs: 8, sm: 16 }，随断点变化。
{variable} 的值会随断点变化。

# ✅ correct
gutter 可设置为对象 `{ xs: 8, sm: 16 }`，随断点变化。
`{variable}` 的值会随断点变化。
```

Exceptions (not a violation):
- Inside fenced code blocks (` ```react ```, ` ```js ```, etc.)
- JSX attribute values (`prop={value}`) inside a fenced block
