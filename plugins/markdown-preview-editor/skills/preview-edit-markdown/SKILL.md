---
name: preview-edit-markdown
description: "Open and directly edit a local Markdown file in the browser with automatic saving. Use whenever the user asks to manually edit a local .md document."
---

# Preview/Edit Markdown

Use the bundled localhost service when a user wants to manually edit a local Markdown file. The document opens directly in its single editing mode and saves changes automatically.

## Start the preview

1. Resolve the Markdown file and the smallest root directory containing the file plus its relative images, links, and HTML references.
2. Choose an available loopback port, starting with `4177`. Check with `lsof -nP -iTCP:<port> -sTCP:LISTEN`; increment the port when a listener already exists.
3. Start the service from this skill directory and keep the process running:

```bash
node scripts/serve_markdown.mjs \
  --root <absolute-root-directory> \
  --file <markdown-path-relative-to-root> \
  --port <available-port>
```

4. Wait for `Markdown preview: http://127.0.0.1:<port>/`, then open that URL with the in-app browser when available, otherwise with the system browser.
5. Verify that the rendered document, relative images, local links, tables, and linked `.html` or `.htm` references work.
6. Return the localhost URL only while the service is running. Keep the server alive when the user is expected to continue reviewing or editing.

Do not substitute a `file://` URL, raw source view, generated HTML copy, or PDF when the task is to open the Markdown document. Do not start the server merely to read Markdown content during analysis.

## Editing and safety

The rendered document is directly editable and autosaves to the configured Markdown file. The server:

- binds only to `127.0.0.1`
- permits writes only from a loopback request
- writes only the configured Markdown file
- enforces a 5 MB document-size limit and version-conflict checks
- saves through an atomic rename
- keeps linked images and links non-editable
- serves other linked Markdown files as read-only, line-addressable source views
- applies a restrictive Content Security Policy so raw HTML cannot execute scripts or submit forms

Preserve headings, images, relative links, emphasis, lists, blockquotes, code, and tables during visual editing. If the user only wants to inspect the document, avoid making edits.

## Verification

At a narrow desktop viewport, verify wide tables scroll horizontally instead of compressing into unreadable columns. At a wide viewport, verify content order, images, links, and references remain legible. Report missing assets, broken relative paths, or unsupported Markdown constructs instead of silently changing the source.
