#!/usr/bin/env node

import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import { createHash, randomBytes } from "node:crypto";
import { pathToFileURL } from "node:url";

const maxDocumentBytes = 5 * 1024 * 1024;

function parseArgs(argv) {
  const args = { host: "127.0.0.1", port: 4177 };
  for (let index = 2; index < argv.length; index += 2) {
    const key = argv[index]?.replace(/^--/, "");
    const value = argv[index + 1];
    if (!key || value == null) throw new Error(`Missing value for ${argv[index]}`);
    args[key] = key === "port" ? Number(value) : value;
  }
  if (!args.root) throw new Error("--root is required");
  if (!args.file) throw new Error("--file is required");
  if (path.extname(args.file).toLowerCase() !== ".md") throw new Error("--file must point to a Markdown file");
  if (args.host !== "127.0.0.1") throw new Error("--host must remain 127.0.0.1");
  return args;
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function contentVersion(value) {
  return createHash("sha256").update(value).digest("hex");
}

function isEditOriginRequest(request) {
  const rawHost = request.headers.host || "";
  const hostname = rawHost.startsWith("[")
    ? rawHost.slice(1, rawHost.indexOf("]"))
    : rawHost.split(":")[0];
  return hostname === args.host;
}

function sendJson(response, status, payload) {
  response.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
  });
  response.end(JSON.stringify(payload));
}

function readRequestBody(request) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    request.on("data", (chunk) => {
      size += chunk.length;
      if (size > maxDocumentBytes) {
        reject(Object.assign(new Error("Document is too large"), { status: 413 }));
        request.destroy();
        return;
      }
      chunks.push(chunk);
    });
    request.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    request.on("error", reject);
  });
}

function basicInline(value) {
  return escapeHtml(value)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\[([^\]]+)]\(([^)]+)\)/g, '<a href="$2">$1</a>');
}

function renderBasicMarkdown(markdown) {
  const blocks = [];
  let listType = null;
  let paragraph = [];
  const closeParagraph = () => {
    if (paragraph.length) blocks.push(`<p>${basicInline(paragraph.join(" "))}</p>`);
    paragraph = [];
  };
  const closeList = () => {
    if (listType) blocks.push(`</${listType}>`);
    listType = null;
  };

  for (const rawLine of markdown.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) {
      closeParagraph();
      closeList();
      continue;
    }
    const image = line.match(/^!\[([^\]]*)]\(([^)]+)\)$/);
    if (image) {
      closeParagraph();
      closeList();
      blocks.push(`<figure><img src="${escapeHtml(image[2])}" alt="${escapeHtml(image[1])}"><figcaption>${escapeHtml(image[1])}</figcaption></figure>`);
      continue;
    }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      closeParagraph();
      closeList();
      const level = heading[1].length;
      blocks.push(`<h${level}>${basicInline(heading[2])}</h${level}>`);
      continue;
    }
    const ordered = line.match(/^\d+\.\s+(.+)$/);
    const unordered = line.match(/^-\s+(.+)$/);
    if (ordered || unordered) {
      closeParagraph();
      const nextType = ordered ? "ol" : "ul";
      if (listType !== nextType) {
        closeList();
        blocks.push(`<${nextType}>`);
        listType = nextType;
      }
      blocks.push(`<li>${basicInline((ordered || unordered)[1])}</li>`);
      continue;
    }
    paragraph.push(line);
  }
  closeParagraph();
  closeList();
  return blocks.join("\n");
}

async function getMarkdownRenderer() {
  const candidates = [
    process.env.CODEX_MARKED_MODULE,
    path.join(os.homedir(), ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/marked/lib/marked.esm.js"),
  ].filter(Boolean);
  for (const candidate of candidates) {
    if (!fs.existsSync(candidate)) continue;
    const module = await import(pathToFileURL(candidate).href);
    return (markdown) => module.marked.parse(markdown, { gfm: true, breaks: true });
  }
  return renderBasicMarkdown;
}

const args = parseArgs(process.argv);
const root = path.resolve(args.root);
const markdownPath = path.resolve(root, args.file);
if (!markdownPath.startsWith(`${root}${path.sep}`) || !fs.existsSync(markdownPath)) {
  throw new Error(`Markdown file is outside root or missing: ${markdownPath}`);
}
const renderMarkdown = await getMarkdownRenderer();

const css = `
  :root { color-scheme: light; font-family: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }
  body { margin: 0; color: #1d2939; background: #f5f7fa; }
  main { max-width: 1040px; margin: 32px auto 80px; padding: 48px 64px; background: white; border: 1px solid #eaecf0; border-radius: 16px; box-shadow: 0 12px 36px rgba(16, 24, 40, .08); }
  h1 { margin: 0 0 40px; font-size: 38px; line-height: 1.25; color: #101828; }
  h2 { margin: 56px 0 20px; padding-top: 24px; border-top: 1px solid #eaecf0; font-size: 28px; color: #101828; }
  h3 { margin: 32px 0 14px; font-size: 21px; color: #344054; }
  p, li { font-size: 17px; line-height: 1.75; }
  li { margin: 10px 0; padding-left: 6px; }
  figure { margin: 28px 0 22px; }
  img { display: block; width: 100%; height: auto; border: 1px solid #d0d5dd; border-radius: 12px; }
  figcaption { margin-top: 10px; color: #667085; font-size: 14px; text-align: center; }
  code { padding: 2px 6px; border-radius: 5px; background: #f2f4f7; color: #344054; font-size: .9em; }
  blockquote { margin: 12px 0 22px; padding: 9px 14px; border-left: 3px solid #d0d5dd; background: #f8fafc; color: #667085; }
  blockquote p, blockquote li { margin: 0; font-size: 13px; line-height: 1.55; }
  blockquote ul { margin: 6px 0; padding-left: 20px; }
  blockquote li + li { margin-top: 5px; }
  a { color: #175cd3; }
  .report-toolbar { position: sticky; top: 0; z-index: 20; display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 12px 24px; border-bottom: 1px solid #d0d5dd; background: rgba(255,255,255,.97); box-shadow: 0 2px 8px rgba(16,24,40,.06); backdrop-filter: blur(8px); }
  .report-toolbar-title { color: #475467; font-size: 14px; }
  .report-toolbar-status { margin-left: auto; color: #667085; font-size: 14px; }
  .report-toolbar-status.error { color: #b42318; }
  .report-actions { display: flex; align-items: center; gap: 10px; }
  button { appearance: none; min-height: 38px; padding: 8px 14px; border: 1px solid #d0d5dd; border-radius: 8px; background: #fff; color: #344054; font: inherit; font-weight: 600; cursor: pointer; }
  button:hover { background: #f9fafb; }
  button:focus-visible, textarea:focus-visible { outline: 3px solid rgba(21,112,239,.25); outline-offset: 2px; }
  button.primary { border-color: #1570ef; background: #1570ef; color: #fff; }
  button.primary:hover { background: #175cd3; }
  button:disabled { cursor: not-allowed; opacity: .55; }
  button[hidden] { display: none; }
  .report-main.visual-editing { outline: 3px solid rgba(21,112,239,.22); outline-offset: 4px; cursor: text; }
  .report-main.visual-editing h1:hover, .report-main.visual-editing h2:hover, .report-main.visual-editing h3:hover, .report-main.visual-editing p:hover, .report-main.visual-editing li:hover, .report-main.visual-editing blockquote:hover, .report-main.visual-editing th:hover, .report-main.visual-editing td:hover { background: #eff8ff; box-shadow: 0 0 0 4px #eff8ff; }
  .report-main.visual-editing img { pointer-events: none; user-select: none; }
  .editor-panel { max-width: 1440px; margin: 24px auto 80px; padding: 24px; border: 1px solid #d0d5dd; border-radius: 16px; background: #fff; box-shadow: 0 12px 36px rgba(16,24,40,.08); }
  .editor-panel[hidden], .report-main[hidden] { display: none; }
  .editor-header { display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 16px; }
  .editor-header h1 { margin: 0; font-size: 22px; }
  .editor-status { min-height: 22px; color: #667085; font-size: 14px; }
  .editor-status.error { color: #b42318; }
  .markdown-editor { box-sizing: border-box; display: block; width: 100%; min-height: 72vh; resize: vertical; padding: 20px; border: 1px solid #98a2b3; border-radius: 10px; background: #101828; color: #f2f4f7; font: 14px/1.65 ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; tab-size: 2; }
  .table-scroll { margin: 28px 0 40px; overflow-x: auto; overscroll-behavior-inline: contain; border: 1px solid #d0d5dd; border-radius: 12px; background: #fff; box-shadow: 0 4px 14px rgba(16, 24, 40, .06); }
  table { width: 100%; min-width: 1220px; table-layout: fixed; border-collapse: separate; border-spacing: 0; }
  th, td { padding: 16px; vertical-align: top; border-right: 1px solid #d0d5dd; border-bottom: 1px solid #d0d5dd; font-size: 15px; line-height: 1.6; text-align: left; overflow-wrap: break-word; word-break: normal; }
  th { position: sticky; top: 0; z-index: 1; background: #eef4ff; color: #1849a9; font-weight: 700; }
  th:last-child, td:last-child { border-right: 0; }
  tr:last-child td { border-bottom: 0; }
  tbody tr:nth-child(even) td { background: #fcfcfd; }
  th:nth-child(1), td:nth-child(1) { width: 23%; }
  th:nth-child(2), td:nth-child(2) { width: 28%; }
  th:nth-child(3), td:nth-child(3) { width: 28%; }
  th:nth-child(4), td:nth-child(4) { width: 21%; }
  td img { width: 100%; max-width: 300px; margin: 14px auto 4px; border-radius: 8px; }
  td a { overflow-wrap: anywhere; }
  .source-toolbar { position: sticky; top: 0; z-index: 1; margin: -48px -64px 24px; padding: 14px 64px; border-bottom: 1px solid #eaecf0; background: rgba(255,255,255,.96); backdrop-filter: blur(8px); }
  .source-title { margin: 0 0 24px; font-size: 24px; color: #101828; }
  .source-lines { margin: 0; padding-left: 64px; }
  .source-lines li { margin: 0; padding: 2px 10px; scroll-margin-top: 72px; color: #98a2b3; }
  .source-lines li code { display: block; padding: 0; background: transparent; color: #344054; white-space: pre-wrap; overflow-wrap: anywhere; font-size: 13px; line-height: 1.6; }
  .source-lines li:target { background: #fff4cc; outline: 1px solid #fdb022; border-radius: 4px; }
  @media (min-width: 1280px) { main.report-main { max-width: 1440px; } main.report-main > :not(.table-scroll) { max-width: 1040px; margin-left: auto; margin-right: auto; } }
  @media (max-width: 720px) { main { margin: 0; padding: 28px 20px; border: 0; border-radius: 0; } h1 { font-size: 30px; } }
`;

function documentHtml(markdown) {
  const content = renderMarkdown(markdown)
    .replaceAll("<table>", '<div class="table-scroll" role="region" aria-label="Markdown table" tabindex="0"><table>')
    .replaceAll("</table>", "</table></div>");
  const version = contentVersion(markdown);
  const documentName = escapeHtml(path.basename(markdownPath));
  const scriptNonce = randomBytes(18).toString("base64");
  const contentSecurityPolicy = [
    "default-src 'self'",
    `script-src 'nonce-${scriptNonce}'`,
    "style-src 'unsafe-inline'",
    "img-src 'self' data: https: http:",
    "font-src 'self' data:",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'none'",
    "frame-src 'none'",
    "form-action 'none'",
  ].join("; ");
  const html = `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${documentName}</title><style>${css}</style></head><body>
  <nav class="report-toolbar" aria-label="报告工具栏">
    <span class="report-toolbar-title">${documentName}</span>
    <span id="visualStatus" class="report-toolbar-status" role="status" aria-live="polite"></span>
    <div class="report-actions">
      <button id="visualEditButton" type="button">可视化编辑</button>
      <button id="sourceEditButton" type="button">编辑源码</button>
      <button id="visualDoneButton" class="primary" type="button" hidden>完成</button>
    </div>
  </nav>
  <main id="reportPreview" class="report-main">${content}</main>
  <section id="editorPanel" class="editor-panel" hidden>
    <div class="editor-header">
      <h1>编辑 Markdown</h1>
      <div class="report-actions">
        <button id="cancelButton" type="button">取消</button>
        <button id="saveButton" class="primary" type="button">保存</button>
      </div>
    </div>
    <p id="editorStatus" class="editor-status" role="status" aria-live="polite">保存会直接更新原 Markdown 文档。</p>
    <textarea id="markdownEditor" class="markdown-editor" data-version="${version}" spellcheck="false" aria-label="Markdown 内容">${escapeHtml(markdown)}</textarea>
  </section>
  <script nonce="${scriptNonce}">
    (() => {
      const preview = document.getElementById('reportPreview');
      const panel = document.getElementById('editorPanel');
      const editor = document.getElementById('markdownEditor');
      const visualEditButton = document.getElementById('visualEditButton');
      const sourceEditButton = document.getElementById('sourceEditButton');
      const visualDoneButton = document.getElementById('visualDoneButton');
      const visualStatus = document.getElementById('visualStatus');
      const cancelButton = document.getElementById('cancelButton');
      const saveButton = document.getElementById('saveButton');
      const status = document.getElementById('editorStatus');
      let savedValue = editor.value;
      let visualSnapshot = preview.innerHTML;
      let visualDirty = false;
      let visualRevision = 0;
      let visualSaveInFlight = false;
      let visualAutosaveTimer = null;
      const visualAutosaveDelay = 900;

      const escapeText = (value, inTable = false) => value
        .replace(/\\\\/g, '\\\\\\\\')
        .replace(/([*_])/g, '\\\\$1')
        .replace(/\\|/g, inTable ? '\\\\|' : '|');

      const inlineMarkdown = (node, inTable = false) => {
        if (node.nodeType === Node.TEXT_NODE) return escapeText(node.nodeValue || '', inTable);
        if (node.nodeType !== Node.ELEMENT_NODE) return '';
        const tag = node.tagName;
        const children = () => Array.from(node.childNodes).map((child) => inlineMarkdown(child, inTable)).join('');
        if (tag === 'BR') return inTable ? '<br>' : '\\n';
        if (tag === 'STRONG' || tag === 'B') return '**' + children() + '**';
        if (tag === 'EM' || tag === 'I') return '*' + children() + '*';
        if (tag === 'CODE') {
          const tick = String.fromCharCode(96);
          return tick + (node.textContent || '').split(tick).join('\\\\' + tick) + tick;
        }
        if (tag === 'A') return '[' + children() + '](' + (node.getAttribute('href') || '') + ')';
        if (tag === 'IMG') {
          const src = node.getAttribute('src') || '';
          const alt = node.getAttribute('alt') || '';
          const width = node.getAttribute('width');
          return inTable
            ? '<img src="' + src + '" alt="' + alt.replace(/"/g, '&quot;') + '"' + (width ? ' width="' + width + '"' : '') + '>'
            : '![' + alt.replace(/]/g, '\\\\]') + '](' + src + ')';
        }
        return children();
      };

      const listMarkdown = (list) => Array.from(list.children).map((item, index) => {
        const marker = list.tagName === 'OL' ? (index + 1) + '.' : '-';
        return marker + ' ' + inlineMarkdown(item).trim().replace(/\\n/g, '\\n  ');
      }).join('\\n');

      const tableMarkdown = (table) => {
        const rows = Array.from(table.rows).map((row) => Array.from(row.cells).map((cell) => inlineMarkdown(cell, true).trim().replace(/\\n+/g, '<br>')));
        if (!rows.length) return '';
        const width = Math.max(...rows.map((row) => row.length));
        const formatRow = (row) => '| ' + Array.from({length: width}, (_, index) => row[index] || '').join(' | ') + ' |';
        return [formatRow(rows[0]), formatRow(Array(width).fill('---')), ...rows.slice(1).map(formatRow)].join('\\n');
      };

      const blockMarkdown = (node) => {
        if (node.nodeType !== Node.ELEMENT_NODE) return '';
        const tag = node.tagName;
        if (/^H[1-6]$/.test(tag)) return '#'.repeat(Number(tag.slice(1))) + ' ' + inlineMarkdown(node).trim();
        if (tag === 'P') return inlineMarkdown(node).trim();
        if (tag === 'OL' || tag === 'UL') return listMarkdown(node);
        if (tag === 'BLOCKQUOTE') {
          return Array.from(node.children).map(blockMarkdown).filter(Boolean).join('\\n\\n').split('\\n').map((line) => '> ' + line).join('\\n');
        }
        if (tag === 'PRE') {
          const fence = String.fromCharCode(96).repeat(3);
          return fence + '\\n' + (node.textContent || '').replace(/\\n$/, '') + '\\n' + fence;
        }
        if (tag === 'HR') return '---';
        if (tag === 'FIGURE') {
          const image = node.querySelector('img');
          return image ? inlineMarkdown(image) : '';
        }
        if (tag === 'TABLE') return tableMarkdown(node);
        if (node.classList.contains('table-scroll')) {
          const table = node.querySelector('table');
          return table ? tableMarkdown(table) : '';
        }
        return Array.from(node.children).map(blockMarkdown).filter(Boolean).join('\\n\\n');
      };

      const previewToMarkdown = () => Array.from(preview.children)
        .map(blockMarkdown)
        .filter(Boolean)
        .join('\\n\\n')
        .replace(/\\n{3,}/g, '\\n\\n') + '\\n';

      const setStatus = (message, isError = false) => {
        status.textContent = message;
        status.classList.toggle('error', isError);
      };

      const setVisualStatus = (message, isError = false) => {
        visualStatus.textContent = message;
        visualStatus.classList.toggle('error', isError);
      };

      const setVisualControls = (editing) => {
        visualEditButton.hidden = editing;
        sourceEditButton.hidden = editing;
        visualDoneButton.hidden = !editing;
      };

      const putDocument = async (value) => {
        const response = await fetch('/__document', {
          method: 'PUT',
          headers: {
            'content-type': 'text/markdown; charset=utf-8',
            'x-report-version': editor.dataset.version,
          },
          body: value,
        });
        const result = await response.json();
        if (!response.ok) throw new Error(result.error || '保存失败');
        editor.dataset.version = result.version;
        return result;
      };

      const enterVisualEditMode = () => {
        visualSnapshot = preview.innerHTML;
        visualDirty = false;
        preview.contentEditable = 'true';
        preview.spellcheck = true;
        preview.classList.add('visual-editing');
        preview.querySelectorAll('img, a').forEach((element) => element.setAttribute('contenteditable', 'false'));
        preview.querySelectorAll('a').forEach((link) => {
          link.addEventListener('pointerdown', (event) => {
            if (event.button !== 0 || !link.href) return;
            event.preventDefault();
            event.stopPropagation();
            window.open(link.href, '_blank', 'noopener');
          });
        });
        setVisualControls(true);
        setVisualStatus('点击文字直接编辑 · 自动保存');
        preview.focus();
      };

      const leaveVisualEditMode = () => {
        preview.contentEditable = 'false';
        preview.classList.remove('visual-editing');
        setVisualControls(false);
        setVisualStatus('已保存');
      };

      const saveVisualChanges = async () => {
        if (!preview.classList.contains('visual-editing') || !visualDirty || visualSaveInFlight) return;
        clearTimeout(visualAutosaveTimer);
        visualAutosaveTimer = null;
        visualSaveInFlight = true;
        const savingRevision = visualRevision;
        const nextMarkdown = previewToMarkdown();
        setVisualStatus('保存中…');
        try {
          await putDocument(nextMarkdown);
          editor.value = nextMarkdown;
          savedValue = nextMarkdown;
          visualSnapshot = preview.innerHTML;
          if (visualRevision === savingRevision) {
            visualDirty = false;
            setVisualStatus('已保存');
          } else {
            setVisualStatus('继续保存最新修改…');
          }
        } catch (error) {
          setVisualStatus((error.message || '自动保存失败') + '，请保留此页面并重试', true);
        } finally {
          visualSaveInFlight = false;
          if (visualDirty && visualRevision !== savingRevision) {
            visualAutosaveTimer = window.setTimeout(saveVisualChanges, visualAutosaveDelay);
          }
        }
      };

      const scheduleVisualAutosave = () => {
        clearTimeout(visualAutosaveTimer);
        setVisualStatus('编辑中…');
        visualAutosaveTimer = window.setTimeout(saveVisualChanges, visualAutosaveDelay);
      };

      const finishVisualEditing = async () => {
        clearTimeout(visualAutosaveTimer);
        while (visualSaveInFlight) await new Promise((resolve) => window.setTimeout(resolve, 50));
        if (visualDirty) await saveVisualChanges();
        if (!visualDirty) leaveVisualEditMode();
      };

      const enterEditMode = () => {
        preview.hidden = true;
        panel.hidden = false;
        visualEditButton.hidden = true;
        sourceEditButton.hidden = true;
        editor.focus();
      };

      const leaveEditMode = () => {
        panel.hidden = true;
        preview.hidden = false;
        visualEditButton.hidden = false;
        sourceEditButton.hidden = false;
        setStatus('保存会直接更新原 Markdown 文档。');
      };

      visualEditButton.addEventListener('click', enterVisualEditMode);
      sourceEditButton.addEventListener('click', enterEditMode);
      preview.addEventListener('input', () => {
        if (!preview.classList.contains('visual-editing')) return;
        visualDirty = true;
        visualRevision += 1;
        scheduleVisualAutosave();
      });
      visualDoneButton.addEventListener('click', finishVisualEditing);
      cancelButton.addEventListener('click', () => {
        if (editor.value !== savedValue && !window.confirm('放弃尚未保存的修改？')) return;
        editor.value = savedValue;
        leaveEditMode();
      });

      const save = async () => {
        saveButton.disabled = true;
        cancelButton.disabled = true;
        setStatus('正在保存…');
        try {
          const result = await putDocument(editor.value);
          savedValue = editor.value;
          setStatus('已保存，正在刷新预览…');
          window.location.reload();
        } catch (error) {
          setStatus(error.message || '保存失败', true);
          saveButton.disabled = false;
          cancelButton.disabled = false;
        }
      };

      saveButton.addEventListener('click', save);
      editor.addEventListener('keydown', (event) => {
        if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') {
          event.preventDefault();
          save();
        }
      });
      document.addEventListener('keydown', (event) => {
        if (preview.classList.contains('visual-editing') && (event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 's') {
          event.preventDefault();
          saveVisualChanges();
        }
      });
      window.addEventListener('beforeunload', (event) => {
        if ((!panel.hidden && editor.value !== savedValue) || (preview.classList.contains('visual-editing') && (visualDirty || visualSaveInFlight))) {
          event.preventDefault();
          event.returnValue = '';
        }
      });
      enterVisualEditMode();
    })();
  </script>
  </body></html>`;
  return { html, contentSecurityPolicy };
}

function sourceDocumentHtml(filePath, content) {
  const lines = content.split(/\r?\n/).map((line, index) => `<li id="L${index + 1}"><code>${escapeHtml(line || " ")}</code></li>`).join("");
  const title = escapeHtml(path.basename(filePath));
  return `<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><style>${css}</style></head><body><main><nav class="source-toolbar"><a href="/">← 返回 ${escapeHtml(path.basename(markdownPath))}</a></nav><h1 class="source-title">${title}</h1><ol class="source-lines">${lines}</ol></main></body></html>`;
}

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".htm": "text/html; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".gif": "image/gif",
  ".svg": "image/svg+xml",
};

const server = http.createServer(async (request, response) => {
  const url = new URL(request.url || "/", `http://${args.host}:${args.port}`);
  if (request.method === "PUT" && url.pathname === "/__document") {
    if (!isEditOriginRequest(request)) {
      sendJson(response, 403, { error: `Editing is available only from ${args.host}.` });
      return;
    }
    if (!(request.headers["content-type"] || "").startsWith("text/markdown")) {
      sendJson(response, 415, { error: "Expected text/markdown content." });
      return;
    }
    try {
      const current = fs.readFileSync(markdownPath, "utf8");
      const expectedVersion = request.headers["x-report-version"];
      if (!expectedVersion || expectedVersion !== contentVersion(current)) {
        sendJson(response, 409, { error: "文件已在其他地方更新。请刷新页面后重新编辑，当前修改未被覆盖。" });
        return;
      }
      const next = await readRequestBody(request);
      const stat = fs.statSync(markdownPath);
      const tempPath = path.join(path.dirname(markdownPath), `.${path.basename(markdownPath)}.${process.pid}.${Date.now()}.tmp`);
      try {
        fs.writeFileSync(tempPath, next, { encoding: "utf8", mode: stat.mode });
        fs.renameSync(tempPath, markdownPath);
      } finally {
        if (fs.existsSync(tempPath)) fs.unlinkSync(tempPath);
      }
      sendJson(response, 200, { ok: true, version: contentVersion(next) });
    } catch (error) {
      sendJson(response, error.status || 500, { error: error.message || "Save failed" });
    }
    return;
  }
  if (request.method !== "GET") {
    response.writeHead(405, { allow: "GET, PUT", "content-type": "text/plain; charset=utf-8" });
    response.end("Method not allowed");
    return;
  }
  if (url.pathname === "/" || url.pathname === `/${args.file}`) {
    const markdown = fs.readFileSync(markdownPath, "utf8");
    const document = documentHtml(markdown);
    response.writeHead(200, {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "content-security-policy": document.contentSecurityPolicy,
      "x-content-type-options": "nosniff",
    });
    response.end(document.html);
    return;
  }
  if (url.pathname === "/__health") {
    response.writeHead(200, { "content-type": "text/plain; charset=utf-8" });
    response.end("ok");
    return;
  }
  const requestedPath = path.resolve(root, `.${decodeURIComponent(url.pathname)}`);
  if (!requestedPath.startsWith(`${root}${path.sep}`) || !fs.existsSync(requestedPath) || !fs.statSync(requestedPath).isFile()) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }
  if (path.extname(requestedPath).toLowerCase() === ".md") {
    const markdown = fs.readFileSync(requestedPath, "utf8");
    response.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
    response.end(sourceDocumentHtml(requestedPath, markdown));
    return;
  }
  if ([".html", ".htm"].includes(path.extname(requestedPath).toLowerCase())) {
    const requestHost = (request.headers.host || "").split(":")[0];
    if (requestHost === args.host) {
      response.writeHead(302, {
        location: `http://localhost:${args.port}${url.pathname}${url.search}`,
        "cache-control": "no-store",
      });
      response.end();
      return;
    }
  }
  response.writeHead(200, { "content-type": mimeTypes[path.extname(requestedPath).toLowerCase()] || "application/octet-stream" });
  fs.createReadStream(requestedPath).pipe(response);
});

server.listen(args.port, args.host, () => {
  console.log(`Markdown preview: http://${args.host}:${args.port}/`);
});
