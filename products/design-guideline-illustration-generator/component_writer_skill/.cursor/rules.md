# Cursor Rules — Component Writer Skill

## Project Overview

This repository is a **Claude Code Skill** for generating enterprise B-end design system component usage guides (EDI / Infra Designer). It produces formal, reviewable Markdown documentation for product managers, designers, and frontend engineers.

---

## Architecture

### Directory Structure

```
component_writer_skill/
├── Component_skill.md       # Main skill definition (infrad-component-guide-writer)
├── AGENTS.md                # Available skills registry
├── output/                  # Generated component guides (required output location)
│   ├── Button_Component_Guide.md
│   └── Dropdown_Component_Guide.md
├── references/              # Reference documents for generation
│   ├── component_guide_example_button.md   # Primary example (canonical case)
│   └── component_guide_output_template.md # Structure quick reference
├── scripts/                 # Executable scripts (Python, Bash; currently empty)
├── assets/                  # Output resources (templates, images, fonts)
├── history_output/         # Historical / archived documents (do not overwrite)
└── .claude/skills/          # Bundled external skills (xlsx, pptx, etc.)
```

### Generation Flow

1. **Load references**: `references/component_guide_example_button.md` (primary); `references/component_guide_output_template.md` (optional structure quick reference).
2. **Retrieve component**: Look up component types from Ant Design (https://ant.design/components/overview-cn/).
3. **Generate output**: Follow fixed structure; save to `output/{ComponentName}_Component_Guide.md`; replace button content with target component content; adapt section 3.x rules to component semantics.
4. **Self-check**: Verify structure, language, rules, and image placeholders.

### Design Patterns

| Pattern | Description |
|---------|-------------|
| **Example-driven generation** | Button example is the canonical reference; other components adapt structure and style from it. |
| **Template method** | Fixed section order (1.0→4.0); variable content per component. |
| **Verifiable rules** | Every rule must be judgeable as 对/错 by reviewers. |
| **Progressive disclosure** | Skill metadata → Component_skill.md → references; load resources as needed. |
| **Dual reference** | Example (full) + template (structure outline) for efficiency. |

---

## Output Structure (Fixed, Do Not Reorder)

| Section | Content | Notes |
|---------|---------|-------|
| **1.0 组件描述** | One-sentence component value | Must be clear, verifiable, no vague terms |
| **1.1 组件构成** | Base elements list | Use `&emsp;&emsp;` for numbered items; include image placeholder |
| **1.2.1–1.2.N** | Types: 是什么, 简单用法, 典型场景, 替代方案 | Each type: 2 placeholders (example + typical scenario) |
| **1.3.1–1.3.N** | 推荐 vs. 不推荐 | Use `✅ **推荐：**` and `❌ **不推荐：**`; `<hr>` separator |
| **2.1 选择流程** | Mermaid flowchart | `flowchart TD`; decision nodes with `{condition?}` |
| **3.1–3.6** | Detailed rules | Adapt to component (e.g., 多操作策略, 危险操作, 摆放位置, 状态反馈) |
| **4.0 常见问题** | FAQ format | Q&A pairs; use `### N.` for questions |

---

## Coding & Writing Conventions

### Language

- **Primary**: Chinese for all narrative content.
- **Exceptions**: Industry terms and proper nouns (Ant Design, Markdown, Mermaid, Tooltip, Hover, Active, Disabled, Loading).
- **Avoid**: English or mixed Chinese–English in body text.
- **Quotation marks**: Prefer `「」` for Chinese quotes; `"` for inline strings.

### Rules Quality

- Every rule must be **verifiable** (评审者能用「对/错」判定).
- Base judgments only on observable information: user goals, task risk, page position, operation consequences, information hierarchy, state semantics, accessibility impact.
- **Do not include**: Properties, parameters, code, implementation details, tutorial steps (e.g., 点击、输入、配置), long derivations, or complex case studies.
- **Simple usage format**: Semicolon-separated rules; use 必须/不可/建议/宜 for obligation levels.

### Markdown Formatting

- **Headers**: `#` for top-level, `##` for sections, `###` for subsections. Use Chinese `部份` (not 部分) in section 3 title.
- **Component elements**: Use `&emsp;&emsp;N. **Bold term**` for numbered list items.
- **Section separators**: `---` between major sections (1.2, 1.3, 2, 3).
- **Recommendation blocks**: `✅ **推荐：**` and `❌ **不推荐：**` followed by one-sentence conclusion; `<hr>` between them.

### Image Placeholders

**Required format** (blockquote + HTML comment):

```markdown
> <!-- 附图占位：建议附上一张[图的类型]，[展示内容描述]，[图要传达的设计结论] -->
```

- Placeholder content is an **image suggestion** for UX designers (not a screenshot source). Designers create images based on actual business design style; the suggestion is advisory only.
- Each suggestion must describe: **image type** (示例图 / 对比图 / 场景图 / 状态图), **content to show**, and **design conclusion to convey**.
- Begin with `建议附上一张……` in Chinese.
- To generate suggestions, read the Ant Design component page and note visual form descriptions and typical scenario descriptions for each type.
- Place after 是什么 (type example) and after 典型场景 (scenario example) for each 1.2.x type.
- Place before each 1.3.x 推荐/不推荐 block.
- Place after each 3.x rule subsection that requires illustration.

### Mermaid Flowchart

- Use `flowchart TD` (top-down).
- Start node: `A[开始：...]` (describe the entry point).
- Decision nodes: `B{condition?}` with `-->|是|` and `-->|否|` edges.
- End nodes: `[类型名称]` or `[改用...]`.
- Keep node IDs short (A, B, C, L, etc.); labels in `[]` or `{}`.
- Each branch must terminate in a concrete type or alternative.
- **Ordering rule**: Before drawing the flowchart, identify the **default type** = the type with the fewest special conditions (count: special trigger method, persistent selection state, parent-child hierarchy, explicit primary/secondary action distinction). The default type must be the first terminal node reachable by answering 「是」 to the first question. Remaining types are ordered by ascending special-condition count. When counts are equal, order by descending frequency of use in typical UI design.

### Section 3 Adaptability

Section 3 (3.1–3.6) content **varies by component**. Follow the example for the target component type:

- **Button**: 多操作策略, 危险操作, 摆放位置, 顺序与对齐, 状态与交互, 视觉规范与形态选择.
- **Dropdown**: 菜单项组织与折叠策略, 危险操作, 触发方式与弹出位置, 菜单项形态, etc.
- **Other components**: Adapt rules to component semantics; preserve structure (3.1–3.6 subsections with placeholders).

### Component Types

- Maximum **7 types** per component (1.2.1–1.2.7).
- Merge by importance and risk semantics if input exceeds 7.
- Must cover core 选型分流 (selection flow).
- 1.3.x can merge related types (e.g., 1.3.4 文字和链接按钮).

---

## File Conventions

| Pattern | Purpose |
|---------|---------|
| `output/*_Component_Guide.md` | Generated component usage guides (required output location) |
| `Component_skill.md` | Main skill definition (do not rename) |
| `references/component_guide_example_*.md` | Actual case examples |
| `references/component_guide_output_template.md` | Structure quick reference |
| `history_output/*.md` | Archived / historical outputs (do not overwrite) |

### Naming

- Component guides: `{ComponentName}_Component_Guide.md` (e.g., `Button_Component_Guide.md`, `Dropdown_Component_Guide.md`).
- Use PascalCase for component names in filenames.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Documentation | Markdown |
| Diagrams | Mermaid (flowchart) |
| Component reference | Ant Design (ant.design/components/overview-cn) |
| Skill system | OpenSkills (`npx openskills read <skill-name>`) |
| Note-taking | Obsidian (optional) |

No traditional code stack (no package.json, no Python runtime) — this is a documentation/skill project. Scripts in `scripts/` are optional and not yet implemented.

---

## When Editing

| File | Impact | Guidelines |
|------|--------|------------|
| **Component_skill.md** | Affects all future generations | Preserve fixed output structure, reference links, self-check items |
| **references/component_guide_example_button.md** | Primary reference | Update when canonical format changes; keep placeholders consistent |
| **references/component_guide_output_template.md** | Structure outline | Keep in sync with example; do not add component-specific content |
| **Generated guides** | Single-component docs | Follow structure; adapt section 3 to component; use placeholders |

---

## Output Format (Skill Constraint)

- **Output**: One Markdown code block only; no explanatory text outside.
- **Single file**: One complete document per generation.
- **No code**: No properties, parameters, or implementation snippets in the guide content.

---

## Related Skills

Invoke via `npx openskills read <skill-name>` when relevant:

- `frontend-design`: UI components, pages, dashboards
- `doc-coauthoring`: Documentation workflows
- `skill-creator`: Creating or updating skills
