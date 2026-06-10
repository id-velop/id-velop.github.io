# id-velop.github.io

Personal portfolio website showcasing Chrome extensions, Figma plugins, iPhone shortcuts, and creative development projects.

🌐 **Live Site**: [https://id-velop.github.io](https://id-velop.github.io)

## 📁 Project Structure

```
id-velop.github.io/
├── _config.yml          # Site configuration
├── index.html           # Main portfolio page
├── _projects/           # Project showcase files
│   ├── smart-tab-manager.md
│   ├── figma-color-palette.md
│   └── ...
├── assets/
│   └── css/
│       └── style.css    # Custom styles
└── README.md
```

## 🚀 How to Add New Projects

To add a new project to your portfolio, create a markdown file in the `_projects/` directory:

```markdown
---
title: "Your Project Name"
description: "A brief description of your project."
icon: "🚀"  # Use any emoji as an icon
tags:
  - Chrome Extension
  - JavaScript
  - Category
github_url: "https://github.com/id-velop/your-project"
demo_url: "https://your-demo-url.com"  # Optional
---
```

### Required Fields:
- `title` - Project name
- `description` - Brief project description
- `icon` - Emoji icon for visual representation
- `tags` - Category tags (e.g., Chrome Extension, Figma Plugin, iPhone Shortcut)
- `github_url` - Link to your GitHub repository

### Optional Fields:
- `demo_url` - Link to live demo or store page

## 🎨 Customization

### Change Site Info
Edit `_config.yml`:
```yaml
title: Your Name
description: Your portfolio description
github_username: your-github-username
```

### Modify Styles
Edit `assets/css/style.css` to customize colors, fonts, and layout.

## 🛠️ Local Development

1. Install Jekyll:
   ```bash
   gem install jekyll bundler
   ```

2. Run local server:
   ```bash
   jekyll serve
   ```

3. Open `http://localhost:4000` in your browser

## 📝 License

MIT License - feel free to use this template!