#!/usr/bin/env python3
"""Render an IDS Markdown component guide into a local HTML preview."""

import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    print('Missing dependency: markdown. Install python markdown or use existing preview tooling.', file=sys.stderr)
    sys.exit(2)


def main() -> int:
    if len(sys.argv) != 2:
        print('Usage: python3 render_preview.py <file.md>', file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    if not source.exists():
        print(f'File not found: {source}', file=sys.stderr)
        return 2

    md_content = source.read_text(encoding='utf-8')
    blocks = re.findall(r'```react\n(.*?)```', md_content, re.DOTALL)
    md_for_html = re.sub(
        r'<!-- \[▶ 在线演示\]\(https://infrad\.shopee\.io/playground/\?agent_code_id=\d+\) -->\n*',
        '',
        md_content,
    )

    counter = 0

    def replace_block(_match):
        nonlocal counter
        counter += 1
        return f'<div id="demo-{counter}" class="demo-mount"></div>'

    md_for_html = re.sub(r'```react\n.*?```', replace_block, md_for_html, flags=re.DOTALL)
    body = markdown.markdown(md_for_html, extensions=['fenced_code', 'tables', 'toc'])

    ids_theme = (
        'const IDS_THEME = { theme: { token: { '
        'colorPrimary: "#2673dd", borderRadius: 2, borderRadiusLG: 2, '
        'borderRadiusSM: 2, borderRadiusXS: 2, '
        'fontFamily: "\\\'Roboto\\\', \\\'PingFang SC\\\', \\\'Microsoft YaHei\\\', -apple-system, BlinkMacSystemFont, \\\'Helvetica Neue\\\', Arial, sans-serif", '
        'fontSize: 14 } } };'
    )
    parts = ['const Infrad = antd;', 'const Icons = icons;', ids_theme, '']
    for index, block in enumerate(blocks, 1):
        code = block.strip().replace('function App()', f'function Demo{index}()', 1)
        parts.append(code)
        parts.append(
            f'ReactDOM.createRoot(document.getElementById("demo-{index}")).render('
            f'React.createElement(antd.ConfigProvider, IDS_THEME, React.createElement(Demo{index})));'
        )
        parts.append('')

    script = '<script type="text/babel">\n' + '\n'.join(parts) + '\n</script>'
    html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{source.stem} preview</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/antd@5/dist/reset.css" />
<script src="https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dayjs@1/dayjs.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/antd@5/dist/antd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@ant-design/icons@5/dist/index.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@babel/standalone/babel.min.js"></script>
<style>
body {{ max-width: 960px; margin: 0 auto; padding: 40px 24px; font: 14px/1.6 Roboto, "PingFang SC", "Microsoft YaHei", Arial, sans-serif; color: #1a1a1a; }}
h1 {{ font-size: 22px; border-bottom: 1px solid #e8e8e8; padding-bottom: 10px; }}
h2 {{ font-size: 18px; color: #2673dd; margin-top: 28px; }}
h3 {{ font-size: 15px; margin-top: 20px; }}
p, li {{ color: #595959; }}
.demo-mount {{ margin: 12px 0 20px; padding: 20px 24px; background: #fff; min-height: 60px; }}
hr {{ border: 0; border-top: 1px solid #f0f0f0; margin: 20px 0; }}
code {{ background: #f6f8fa; padding: 1px 6px; border-radius: 2px; }}
</style>
</head>
<body>
{body}
{script}
</body>
</html>'''

    output = source.with_name(f'{source.stem}-preview.html')
    output.write_text(html, encoding='utf-8')
    print(output)
    print(f'demos={len(blocks)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
