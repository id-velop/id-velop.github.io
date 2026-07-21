#!/usr/bin/env python3
"""Launch a local configuration UI for the generic component-doc agent."""

from __future__ import annotations

import html
import json
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / ".generic-component-doc-agent"
REQUEST_PATH = STATE_DIR / "request.json"
HISTORY_PATH = STATE_DIR / "request-history.jsonl"


DEFAULTS = {
    "docs_url": "",
    "component_filter": "",
    "crawl_mode": "overview",
    "max_components": "",
    "language": "zh-CN",
    "output_dir": "source-doc-cn/",
    "file_naming": "{ComponentName}_Component_Guide.md",
    "writer_skill_path": "component_writer_skill/",
    "writer_reference_path": "component_writer_skill/.claude/skills/pdf/reference.md",
    "react_block_generator_path": "md-illustration-generator-main/skills/react-block-generator/",
    "illustration_skill_path": "md-illustration-generator-main/skills/md-illustration-generator/",
    "code_fence": "react",
    "runtime_scope": "React",
    "allow_imports": "false",
    "preview_command": "",
    "validation_command": "",
    "keep_placeholders": "false",
    "notes": "",
}


def load_existing() -> dict[str, str]:
    if not REQUEST_PATH.exists():
        return DEFAULTS.copy()
    try:
        data = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULTS.copy()
    merged = DEFAULTS.copy()
    for key in merged:
        value = data.get(key)
        if value is not None:
            merged[key] = str(value)
    return merged


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def selected(current: str, value: str) -> str:
    return " selected" if current == value else ""


def checked(current: str, value: str = "true") -> str:
    return " checked" if current == value else ""


def render_form(values: dict[str, str]) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Generic Component Doc Agent</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f4f6f8;
      --panel: #ffffff;
      --line: #d9dee7;
      --text: #1f2328;
      --muted: #687385;
      --blue: #1f6feb;
      --blue-soft: #eef5ff;
      --green: #0f7b45;
      --green-soft: #ecfdf3;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    header {{
      background: #111827;
      color: #fff;
      padding: 22px 32px;
      border-bottom: 1px solid #0b1220;
    }}
    header h1 {{ margin: 0; font-size: 22px; line-height: 1.25; }}
    header p {{ margin: 8px 0 0; color: #c9d2e3; line-height: 1.5; }}
    main {{
      max-width: 1080px;
      margin: 28px auto 48px;
      padding: 0 20px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      gap: 20px;
    }}
    form {{
      display: grid;
      gap: 16px;
    }}
    section, aside {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    section {{ padding: 22px; }}
    aside {{
      align-self: start;
      position: sticky;
      top: 18px;
      padding: 18px;
    }}
    h2 {{ margin: 0 0 14px; font-size: 16px; }}
    label {{ display: block; margin: 14px 0 7px; font-weight: 650; }}
    input, textarea, select {{
      width: 100%;
      border: 1px solid #c8ced8;
      border-radius: 6px;
      padding: 10px 12px;
      font: inherit;
      background: #fff;
      color: var(--text);
    }}
    textarea {{ min-height: 84px; resize: vertical; }}
    .grid-2 {{
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }}
    .hint {{ margin-top: 6px; color: var(--muted); font-size: 13px; line-height: 1.45; }}
    .choice {{
      display: flex;
      gap: 8px;
      align-items: flex-start;
      margin-top: 10px;
      color: var(--text);
    }}
    .choice input {{ width: auto; margin-top: 3px; }}
    .path {{
      background: #f6f8fa;
      border: 1px solid #e4e7ec;
      border-radius: 6px;
      padding: 10px 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
      overflow-wrap: anywhere;
    }}
    .status {{
      background: var(--green-soft);
      border: 1px solid #b7e4c7;
      color: var(--green);
      border-radius: 6px;
      padding: 10px 12px;
      font-size: 13px;
      line-height: 1.45;
    }}
    .button-row {{
      display: flex;
      gap: 10px;
      align-items: center;
      margin-top: 4px;
    }}
    button {{
      border: 0;
      border-radius: 6px;
      padding: 11px 16px;
      background: var(--blue);
      color: #fff;
      font-weight: 700;
      cursor: pointer;
      font-size: 14px;
    }}
    button.secondary {{
      background: #eef2f7;
      color: #273142;
    }}
    code {{
      background: #eef2f7;
      border-radius: 4px;
      padding: 2px 5px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
    }}
    ul {{ margin: 10px 0 0 18px; padding: 0; color: var(--muted); line-height: 1.55; }}
    @media (max-width: 860px) {{
      main {{ grid-template-columns: 1fr; }}
      aside {{ position: static; }}
      .grid-2 {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Generic Component Doc Agent</h1>
    <p>配置组件文档来源、写作规则和 React 插图生成器。提交后，agent 会读取 JSON 并自动跑完整流程。</p>
  </header>
  <main>
    <form method="post" action="/submit">
      <section>
        <h2>1. 组件文档来源</h2>
        <label for="docs_url">组件文档入口链接</label>
        <input id="docs_url" name="docs_url" type="url" value="{esc(values['docs_url'])}" required placeholder="https://ant.design/components/overview-cn/">
        <div class="hint">可以是组件总览页，也可以是单个组件文档页。agent 会优先读取开发文档、示例和 API 语义。</div>

        <div class="grid-2">
          <div>
            <label for="crawl_mode">读取范围</label>
            <select id="crawl_mode" name="crawl_mode">
              <option value="overview"{selected(values['crawl_mode'], 'overview')}>从总览页发现组件</option>
              <option value="single"{selected(values['crawl_mode'], 'single')}>只处理这个链接对应的组件</option>
              <option value="filtered"{selected(values['crawl_mode'], 'filtered')}>只处理下方指定组件</option>
            </select>
          </div>
          <div>
            <label for="max_components">最多处理组件数</label>
            <input id="max_components" name="max_components" inputmode="numeric" value="{esc(values['max_components'])}" placeholder="留空表示不限制">
          </div>
        </div>

        <label for="component_filter">组件范围</label>
        <textarea id="component_filter" name="component_filter" placeholder="Button, Input, Table 或留空表示全部组件">{esc(values['component_filter'])}</textarea>
      </section>

      <section>
        <h2>2. 文档输出</h2>
        <div class="grid-2">
          <div>
            <label for="language">文档语言</label>
            <select id="language" name="language">
              <option value="zh-CN"{selected(values['language'], 'zh-CN')}>中文</option>
              <option value="en"{selected(values['language'], 'en')}>English</option>
            </select>
          </div>
          <div>
            <label for="output_dir">Markdown 输出目录</label>
            <input id="output_dir" name="output_dir" value="{esc(values['output_dir'])}" required>
          </div>
        </div>
        <label for="file_naming">文件命名模板</label>
        <input id="file_naming" name="file_naming" value="{esc(values['file_naming'])}" required>
        <div class="hint">可使用 <code>{{ComponentName}}</code> 占位符。</div>
      </section>

      <section>
        <h2>3. Writer 和插图 Skill</h2>
        <label for="writer_skill_path">组件文档 writer 路径</label>
        <input id="writer_skill_path" name="writer_skill_path" value="{esc(values['writer_skill_path'])}" required>

        <label for="writer_reference_path">文档格式参考</label>
        <input id="writer_reference_path" name="writer_reference_path" value="{esc(values['writer_reference_path'])}" required>

        <label for="illustration_skill_path">Markdown 插图生成 skill 路径</label>
        <input id="illustration_skill_path" name="illustration_skill_path" value="{esc(values['illustration_skill_path'])}" required>
      </section>

      <section>
        <h2>4. React 插图生成器</h2>
        <label for="react_block_generator_path">React 代码生成器路径</label>
        <input id="react_block_generator_path" name="react_block_generator_path" value="{esc(values['react_block_generator_path'])}" required>
        <div class="hint">这里应该替换为用户自己的组件库生成器；默认目录只是模板。</div>

        <div class="grid-2">
          <div>
            <label for="code_fence">Markdown 代码块语言</label>
            <input id="code_fence" name="code_fence" value="{esc(values['code_fence'])}" required>
          </div>
          <div>
            <label for="runtime_scope">运行时 scope</label>
            <input id="runtime_scope" name="runtime_scope" value="{esc(values['runtime_scope'])}" placeholder="React, antd, Icons">
          </div>
        </div>

        <label class="choice">
          <input type="checkbox" name="allow_imports" value="true"{checked(values['allow_imports'])}>
          <span>React demo 允许写 <code>import</code> / <code>export</code></span>
        </label>
        <label class="choice">
          <input type="checkbox" name="keep_placeholders" value="true"{checked(values['keep_placeholders'])}>
          <span>保留 <code>附图占位</code> 注释作为渲染元数据</span>
        </label>
      </section>

      <section>
        <h2>5. 校验与补充说明</h2>
        <label for="preview_command">预览命令（可选）</label>
        <input id="preview_command" name="preview_command" value="{esc(values['preview_command'])}" placeholder="例如 npm run preview-docs">

        <label for="validation_command">校验命令（可选）</label>
        <input id="validation_command" name="validation_command" value="{esc(values['validation_command'])}" placeholder="例如 npm run validate-docs">

        <label for="notes">补充规则</label>
        <textarea id="notes" name="notes" placeholder="组件库主题、渲染器限制、组件 API 注意事项等">{esc(values['notes'])}</textarea>
      </section>

      <section>
        <div class="button-row">
          <button type="submit">保存配置并交给 Agent</button>
          <button class="secondary" type="reset">恢复本次打开时的值</button>
        </div>
      </section>
    </form>

    <aside>
      <h2>配置保存位置</h2>
      <div class="path">{esc(str(REQUEST_PATH))}</div>
      <div class="status" style="margin-top: 14px;">提交后这个窗口可以关闭。回到 agent 后，它会继续读取配置并生成文档。</div>
      <h2 style="margin-top: 20px;">输出要求</h2>
      <ul>
        <li>最终 Markdown 默认写入 <code>source-doc-cn/</code></li>
        <li>插图必须是可渲染的 <code>react</code> 代码块</li>
        <li>React 代码生成规则以用户配置的 generator 为准</li>
      </ul>
    </aside>
  </main>
</body>
</html>
"""


class RequestHandler(BaseHTTPRequestHandler):
    server_version = "GenericComponentDocAgent/1.1"

    def do_GET(self) -> None:
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        self._send_html(render_form(load_existing()))

    def do_POST(self) -> None:
        if self.path != "/submit":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")
        fields = urllib.parse.parse_qs(raw_body, keep_blank_values=True)
        payload = DEFAULTS.copy()
        for key in payload:
            if key in ("allow_imports", "keep_placeholders"):
                payload[key] = "true" if fields.get(key, ["false"])[0] == "true" else "false"
            else:
                payload[key] = fields.get(key, [payload[key]])[0].strip()
        payload["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        payload["project_root"] = str(ROOT)

        STATE_DIR.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        REQUEST_PATH.write_text(encoded, encoding="utf-8")
        with HISTORY_PATH.open("a", encoding="utf-8") as history:
            history.write(json.dumps(payload, ensure_ascii=False) + "\n")

        message = f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>Saved</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 48px; color: #1f2328; }}
pre {{ background: #f6f8fa; border: 1px solid #d9dee7; border-radius: 8px; padding: 16px; overflow: auto; }}
a {{ color: #1f6feb; }}
</style></head>
<body>
<h1>配置已保存</h1>
<p>可以回到 agent 继续执行。配置文件：</p>
<pre>{html.escape(str(REQUEST_PATH))}</pre>
<p><a href="/">返回继续修改</a></p>
</body></html>"""
        self._send_html(message)
        threading.Thread(target=self.server.shutdown, daemon=True).start()

    def log_message(self, format: str, *args: object) -> None:
        return

    def _send_html(self, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), RequestHandler)
    host, port = server.server_address
    url = f"http://{host}:{port}/"
    print("Generic Component Doc Agent UI")
    print(f"Project root: {ROOT}")
    print(f"Opening: {url}")
    print(f"Configuration will be saved to: {REQUEST_PATH}")
    webbrowser.open(url)
    server.serve_forever()
    if REQUEST_PATH.exists():
        print("\nSaved configuration:")
        print(REQUEST_PATH.read_text(encoding="utf-8"))
        return 0
    print("No request was saved.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
