# YE Studio Tool Market Monorepo

The website and product source code for Chrome extensions, Codex plugins, Figma plugins, and focused utilities made by YE Studio.

Live site: [https://id-velop.github.io](https://id-velop.github.io)

## Routes

- `/` — Tool Market homepage with search and platform filters
- `/git-magager/` — Git Magager product page
- `/git-magager/privacy-policy.html` — Git Magager privacy policy
- `/markdown-preview-editor/` — Markdown Preview & Editor Codex plugin page
- `/plugins/markdown-preview-editor/` — Standalone Codex plugin source
- `/products/git-magager/` — Git Magager extension source and release artifacts
- `/products/design-guideline-illustration-generator/` — Component documentation agent source

The privacy policy is intentionally kept as a child page of the Git Magager product page.

## Project structure

```text
.
├── index.html
├── git-magager/
│   ├── index.html
│   └── privacy-policy.html
├── markdown-preview-editor/
│   └── index.html
├── plugins/
│   └── markdown-preview-editor/
├── products/
│   ├── git-magager/
│   │   ├── extension/
│   │   └── releases/
│   └── design-guideline-illustration-generator/
├── assets/
│   ├── css/style.css
│   ├── images/
│   └── js/market.js
└── design-qa.md
```

## Local preview

From the repository root:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
```

Then open [http://127.0.0.1:4173](http://127.0.0.1:4173).

## Product organization

- Keep public website pages and assets at the repository root so GitHub Pages can publish them directly.
- Keep Codex plugin packages in `plugins/` because their install links depend on that stable path.
- Keep all other product source and release artifacts in `products/<product-name>/`.

## Adding a tool

Add its source to `products/<product-name>/` (or `plugins/<plugin-name>/` for a Codex plugin), add its real icon to `assets/images/`, add a `.tool-card` in `index.html`, and include searchable terms in `data-search`. Use `data-platform="chrome"`, `data-platform="figma"`, or multiple space-separated values to connect it to the existing filters.
