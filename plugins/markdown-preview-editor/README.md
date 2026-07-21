# Markdown Preview & Editor

A standalone Codex plugin from YE Studio for opening, visually reviewing, and safely editing local Markdown files in a polished localhost workspace.

## What it does

- Renders GitHub-flavored Markdown, images, links, code, blockquotes, and wide tables.
- Supports direct visual editing with autosave and a full source editor.
- Keeps edits local, binds only to `127.0.0.1`, and writes only the selected file.
- Detects version conflicts and uses atomic saves to protect the original document.

## Use it in Codex

Install the plugin, start a new task, then ask:

> Use `$preview-edit-markdown` to open and review `path/to/report.md`.

Codex starts the bundled local service on an available port, opens the rendered document, and keeps the preview running while you review or edit it.

## Requirements

- Codex desktop or CLI
- Node.js 18 or newer
- A local Markdown file

## Privacy

The preview server listens only on the loopback interface. It does not upload document content or require an external account.

## License

MIT
