# Preview Policy

HTML preview is optional.

Generate preview only when the user asks to see or inspect the rendered document.

Preview files are temporary:

- `Component/Foo_Component_Guide-preview.html`

Before pushing docs, remove preview files unless the user explicitly asks to keep them.

Use:

```bash
python3 scripts/render_preview.py <target.md>
```

The preview is for visual QA only. The source of truth remains the Markdown file plus Playground links.

## Taking Screenshots for Review

After rendering the preview, use `agent-browser` to take screenshots of individual demo blocks and send them to the user for direction confirmation. This is the preferred method for iterative review — much faster than asking users to open Playground links.

### Workflow

```bash
# 1. Open the preview file
agent-browser open "file:///absolute/path/to/Component-preview.html"

# 2. Get bounding boxes of the first N demo-mount elements
agent-browser eval "
  const demos = document.querySelectorAll('.demo-mount');
  const r = [];
  for (let i = 0; i < N; i++) {
    const rect = demos[i].getBoundingClientRect();
    r.push({top: Math.round(rect.top), height: Math.round(rect.height)});
  }
  JSON.stringify(r);
"

# 3. Scroll to each demo and screenshot
agent-browser eval "window.scrollTo(0, <top - 100>)"
agent-browser screenshot /tmp/demo_N.png
```

### When to use

- Before asking the user to approve a direction: screenshot the first 1-2 representative demos and send via SeaTalk.
- After fixing a specific block: screenshot just that block to confirm the fix visually.
- Do NOT screenshot all 20+ demos at once — pick the ones that communicate the direction.

### pip3 dependency

`render_preview.py` requires the `markdown` Python package. Install if missing:

```bash
pip3 install markdown -q
```
