---
name: ids-doc-illustration-checker
description: Check IDS / Infra component Markdown documentation for illustration compliance without modifying files. Use when the user asks to inspect, audit, validate, review, or diagnose missing/wrong documentation illustrations, placeholder blocks, 1.2.x / 1.3.x structure, recommended/not-recommended comparison figures, floating-layer demo safety, or pre-push illustration readiness for component guide .md files.
---

# IDS Doc Illustration Checker

## Purpose

Use this skill to inspect IDS component guide Markdown files and report why their illustrations do not meet the documentation standard.

This skill is **read-only by default**:

- Do not edit Markdown.
- Do not generate React demos.
- Do not save Playground blocks.
- Do not render HTML previews.
- Do not commit or push.

If the user later asks to fix issues, use a generator skill separately after this checker has produced a clear issue list.

## Workflow

1. Identify the target Markdown file or directory.
2. Read only the references needed for the question:
   - `references/document-structure.md` for required sections and image placement.
   - `references/compare-figure-standard.md` for `1.3.x` recommended/not-recommended figures.
   - `references/interaction-rules.md` for React block and floating-layer safety.
3. Run the checker script:

```bash
python3 <skill-dir>/scripts/check_ids_doc_illustrations.py <file-or-directory>
```

You may pass more than one target:

```bash
python3 <skill-dir>/scripts/check_ids_doc_illustrations.py Component/Modal_Component_Guide.md Component/Watermark_Component_Guide.md
```

4. Report findings in priority order:
   - Blocking structural errors.
   - Missing or incomplete placeholder / Playground / React blocks.
   - `1.3.x` comparison figure errors.
   - Unsafe interaction patterns.
   - Non-blocking hints.

5. If the checker passes, say that clearly and mention any remaining non-blocking hints.

## Result Interpretation

Exit code:

- `0`: no blocking issues found. Non-blocking hints may still be printed.
- `1`: blocking compliance issues found.
- `2`: input path or script usage problem.

Do not treat non-blocking hints as push blockers unless the user asks for strict cleanup.

## Checks Covered

The script checks:

- `1.1 组件构成` should not contain generated illustration blocks.
- If `1.1 组件构成` still contains a retained image or placeholder, that illustration line must have an exact standalone `<br>` immediately above and immediately below it.
- Each `1.2.x` section has the required prose markers and two illustration positions:
  - after `**是什么**`, before `**简单用法**`
  - after `**典型场景**`, before `**替代方案**`
- Each local `<!-- 附图占位：... -->` has a nearby Playground link and `react` code block.
- Each `react` illustration block has both a Playground comment link (`<!-- [▶ 在线演示](...) -->`) and a demo hint line (`<sub>🖱️ 点击图片可在线演示</sub>`) immediately above it, in that order. Missing either is a blocking error.
- Each `1.3.x` section has an illustration and the summary order `✅ 推荐` → `<hr>` → `❌ 不推荐`.
- `1.3.x` comparison figures use the required two-side structure and green/red visual tokens.
- React blocks avoid known full-page or unsafe demo patterns.
- `*-preview.html` files are not left next to checked docs unless the user explicitly asked for preview work.

## Website Content Validation

After running the checker script, fetch the component's live page and validate the document content against it.

### How to fetch

Derive the component slug from the Markdown filename (e.g. `InputNumber_Component_Guide.md` → `input-number`). Then fetch:

```
https://infrad.shopee.io/components/<slug>
```

Use WebFetch to load the page. Look only at the **Development** tab content.

### What to check

**1.2.x type validity**

For each `1.2.x` section, collect every type / variant / style described in the document. Check whether each one maps to a real `type`, `variant`, or equivalent prop value shown on the website's Development tab.

Flag as a blocking issue if the document describes a type or style that does not exist on the website (e.g. the document mentions a "步进器" style but the website shows no such variant for InputNumber).

**1.2.x scope purity**

`1.2.x` sections must only describe visual types or variants. Flag as a blocking issue if `1.2.x` mixes in size information (e.g. `size="small"`, "小尺寸", "大号") — those belong in a separate `1.2.x` section dedicated to size, not mixed into type sections.

**Section content reasonableness**

Flag if a section's content clearly does not match its heading — for example, a type section that is actually describing a behavior or a layout pattern unrelated to component variants.

### Reporting

Add a "Website Validation" section to your report, listing:

- Types confirmed present on the website.
- Types in the document that could not be found on the website (blocking).
- Any 1.2.x sections that mix types with sizes (blocking).
- Any other content reasonableness issues found.

## Boundary With Generator Skills

Use this checker before and after generation, but keep it separate from generation:

- Checker: read, inspect, report.
- Generator: edit Markdown, generate React demos, save Playground, optionally render preview.

When both are needed, run checker first so the generator has a precise target list.
