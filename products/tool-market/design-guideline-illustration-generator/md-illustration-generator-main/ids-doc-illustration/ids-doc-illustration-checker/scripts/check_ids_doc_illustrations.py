#!/usr/bin/env python3
"""Read-only checker for IDS component guide illustrations."""

import argparse
import glob
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

H1_RE = re.compile(r'^#\s+(.+)$')
H2_RE = re.compile(r'^##\s+(.+)$')
H3_RE = re.compile(r'^###\s+(.+)$')
PLACEHOLDER_RE = re.compile(r'<!--\s*附图占位')
REACT_FENCE_RE = re.compile(r'^```react\s*$')
PLAYGROUND_LINK_RE = re.compile(
    r'<!--\s*\[▶\s*在线演示\]\(https://infrad\.shopee\.io/playground/\?agent_code_id=\d+\)\s*-->'
)
REMOTE_IMG_RE = re.compile(
    r'<img\s+[^>]*src="https://(?:editor\.shopee\.io|[^"]*\buss[^"]*)/[^"]+"'
)

AUTO_OPEN_PATTERNS = [
    (re.compile(r'(?<=[\s])defaultOpen(?=\s*[=>\s/])(?!\s*=\s*\{?\s*false)'), 'defaultOpen'),
    (re.compile(r'(?<=[\s])defaultVisible(?=\s*[=>\s/])(?!\s*=\s*\{?\s*false)'), 'defaultVisible'),
    (re.compile(r'(?<=[\s])open(?=[\s/>])(?!\s*=)'), 'open boolean prop'),
    (re.compile(r'(?<=[\s])open\s*=\s*\{?\s*true\b'), 'open={true}'),
    (re.compile(r'(?<=[\s])visible(?=[\s/>])(?!\s*=)'), 'visible boolean prop'),
    (re.compile(r'(?<=[\s])visible\s*=\s*\{?\s*true\b'), 'visible={true}'),
]
FORBIDDEN_API_RE = re.compile(r'\b(message|notification)\.\w+\s*\(')
POPUP_COMPONENTS = [
    'Dropdown', 'Select', 'Cascader', 'TreeSelect', 'DatePicker', 'TimePicker',
    'RangePicker', 'AutoComplete', 'Tooltip', 'Popover', 'Popconfirm',
    'Mentions', 'ColorPicker',
]
PORTAL_COMPONENTS = ['Modal', 'Drawer', 'Tour']


@dataclass
class Finding:
    path: str
    line: int
    category: str
    severity: str
    message: str


def read_lines(path: str) -> List[str]:
    return Path(path).read_text(encoding='utf-8').split('\n')


def looks_like_component_guide(lines: List[str]) -> bool:
    content = '\n'.join(lines)
    return any([
        re.search(r'^##\s+1\.2', content, re.M),
        re.search(r'^##\s+1\.3', content, re.M),
        re.search(r'^###\s+1\.2\.\d', content, re.M),
        re.search(r'^###\s+1\.3\.\d', content, re.M),
    ])


def has_heading(lines: List[str], pattern: str) -> bool:
    return bool(re.search(rf'^(?:#|##)\s+{pattern}', '\n'.join(lines), re.M))


def is_illustration_line(line: str) -> bool:
    return bool(PLACEHOLDER_RE.search(line) or REACT_FENCE_RE.match(line) or REMOTE_IMG_RE.search(line))


def has_illustration(section_lines: List[Tuple[int, str]]) -> bool:
    return any(is_illustration_line(line) for _, line in section_lines)


def split_h2_sections(lines: List[str]) -> List[dict]:
    sections = []
    current = None
    body = []

    def flush(end_line: int):
        if current:
            sections.append({**current, 'end_line': end_line, 'lines': list(body)})

    for idx, line in enumerate(lines, 1):
        match = H2_RE.match(line)
        if match:
            flush(idx - 1)
            current = {'title': match.group(1).strip(), 'line': idx}
            body = []
        elif current:
            body.append((idx, line))
    flush(len(lines))
    return sections


def split_h3_sections(lines: List[str]) -> List[dict]:
    sections = []
    current_h2 = None
    current = None
    body = []

    def flush(end_line: int):
        if current:
            sections.append({**current, 'h2': current_h2, 'end_line': end_line, 'lines': list(body)})

    for idx, line in enumerate(lines, 1):
        h2 = H2_RE.match(line)
        if h2:
            flush(idx - 1)
            current_h2 = h2.group(1).strip()
            current = None
            body = []
            continue
        h3 = H3_RE.match(line)
        if h3:
            flush(idx - 1)
            current = {'title': h3.group(1).strip(), 'line': idx}
            body = []
            continue
        if current:
            body.append((idx, line))
    flush(len(lines))
    return sections


def find_marker(section_lines: List[Tuple[int, str]], marker: str) -> Optional[int]:
    for line_no, line in section_lines:
        if marker in line:
            return line_no
    return None


def window_has_illustration(section_lines: List[Tuple[int, str]], start: Optional[int], end: Optional[int]) -> bool:
    if start is None or end is None or start >= end:
        return False
    return has_illustration([(line_no, line) for line_no, line in section_lines if start < line_no < end])


def check_top_level_structure(path: str, lines: List[str]) -> List[Finding]:
    if not looks_like_component_guide(lines):
        return []
    required = [
        (r'1\.0(\.|\s|$)', '`1.0 组件描述`'),
        (r'1\.1(\.|\s|$)', '`1.1 组件构成`'),
        (r'1\.2(\.|\s|$)', '`1.2 组件包含哪些不同类型`'),
        (r'1\.3(\.|\s|$)', '`1.3 各类型典型场景案例`'),
        (r'2(\.|\s|$)', '`2.x 选型指南`'),
        (r'3(\.|\s|$)', '`3.x 细致专业部份`'),
    ]
    findings = []
    for pattern, label in required:
        if not has_heading(lines, pattern):
            findings.append(Finding(path, 1, 'document-structure', 'error', f'缺少 {label} 章节'))
    return findings


def check_11_no_first_illustration(path: str, lines: List[str]) -> List[Finding]:
    findings = []
    for section in split_h2_sections(lines):
        if not re.match(r'1\.1(\.|\s|$)', section['title']):
            continue
        for line_no, line in section['lines']:
            if PLACEHOLDER_RE.search(line):
                findings.append(Finding(path, line_no, '1.1-composition', 'error', '1.1 组件构成不应保留附图占位；保留文字要素列表即可'))
            if PLAYGROUND_LINK_RE.search(line) or REACT_FENCE_RE.match(line):
                findings.append(Finding(path, line_no, '1.1-composition', 'error', '1.1 组件构成不应生成 Playground / react 配图'))
    return findings


def check_placeholder_integrity(path: str, lines: List[str]) -> List[Finding]:
    findings = []
    current_h2 = None
    for idx, line in enumerate(lines, 1):
        h2 = H2_RE.match(line)
        if h2:
            current_h2 = h2.group(1).strip()
        if not PLACEHOLDER_RE.search(line):
            continue
        if current_h2 and re.match(r'1\.1(\.|\s|$)', current_h2):
            continue
        previous = lines[idx - 2] if idx >= 2 else ''
        if REMOTE_IMG_RE.search(line) or REMOTE_IMG_RE.search(previous):
            continue
        window = lines[idx:idx + 15]
        has_link = any(PLAYGROUND_LINK_RE.search(item) for item in window)
        has_react = False
        for item in window:
            if REACT_FENCE_RE.match(item):
                has_react = True
                break
            if H1_RE.match(item) or H2_RE.match(item) or H3_RE.match(item):
                break
        if not has_react:
            findings.append(Finding(path, idx, 'placeholder', 'error', '附图占位下方缺少 ```react 代码块'))
        elif not has_link:
            findings.append(Finding(path, idx, 'placeholder', 'error', '附图占位下方缺少 Playground 链接注释'))
    return findings


def extract_react_text_in_window(section_lines: List[Tuple[int, str]], start: int, end: int) -> List[Tuple[int, str]]:
    """Return (start_line, block_text) for each react block whose opening fence falls in (start, end)."""
    blocks = []
    in_block = False
    block_start = 0
    body = []
    for line_no, line in section_lines:
        if start is not None and end is not None and not (start < line_no < end):
            continue
        if not in_block:
            if REACT_FENCE_RE.match(line):
                in_block = True
                block_start = line_no
                body = []
        else:
            if line.rstrip() == '```':
                blocks.append((block_start, '\n'.join(body)))
                in_block = False
            else:
                body.append(line)
    return blocks


def check_page_shell(path: str, title: str, block_start: int, block_text: str) -> List[Finding]:
    findings = []
    if '#0d2b6b' not in block_text:
        findings.append(Finding(path, block_start, 'page-shell', 'warning',
                                f'`### {title}` 场景图未使用 Page Shell Topbar（background: #0d2b6b）；若组件不需要页面级场景可忽略'))
    if 'borderRight' not in block_text:
        findings.append(Finding(path, block_start, 'page-shell', 'warning',
                                f'`### {title}` 场景图未使用 Page Shell Sidebar（borderRight）；若组件不需要页面级场景可忽略'))
    # content 区域不能有 overflow:hidden，否则 fake div 下拉会被截断
    content_match = re.search(r'const content\s*=\s*\{([^}]+)\}', block_text)
    if content_match and re.search(r"overflow:\s*['\"]hidden['\"]", content_match.group(1)):
        findings.append(Finding(path, block_start, 'page-shell', 'error',
                                f'`### {title}` 场景图 content 区域有 overflow:hidden，会截断 fake div 下拉；去掉该属性'))
    return findings


def check_12_sections(path: str, lines: List[str]) -> List[Finding]:
    findings = []
    for section in split_h3_sections(lines):
        title = section['title']
        if not re.match(r'1\.2\.\d', title):
            continue
        markers = {
            'what': find_marker(section['lines'], '**是什么**'),
            'usage': find_marker(section['lines'], '**简单用法**'),
            'scene': find_marker(section['lines'], '**典型场景**'),
            'alternative': find_marker(section['lines'], '**替代方案**'),
        }
        labels = {'what': '是什么', 'usage': '简单用法', 'scene': '典型场景', 'alternative': '替代方案'}
        for key, line_no in markers.items():
            if line_no is None:
                findings.append(Finding(path, section['line'], '1.2-structure', 'error', f'`### {title}` 缺少 `**{labels[key]}**`'))
        ordered = [markers['what'], markers['usage'], markers['scene'], markers['alternative']]
        if all(ordered):
            if not (ordered[0] < ordered[1] < ordered[2] < ordered[3]):
                findings.append(Finding(path, section['line'], '1.2-structure', 'error', f'`### {title}` 顺序应为 是什么 -> 简单用法 -> 典型场景 -> 替代方案'))
            else:
                if not window_has_illustration(section['lines'], markers['what'], markers['usage']):
                    findings.append(Finding(path, section['line'], '1.2-illustration', 'error', f'`### {title}` 在 `是什么` 与 `简单用法` 之间缺少形态图'))
                if not window_has_illustration(section['lines'], markers['scene'], markers['alternative']):
                    findings.append(Finding(path, section['line'], '1.2-illustration', 'error', f'`### {title}` 在 `典型场景` 与 `替代方案` 之间缺少场景图'))
                else:
                    # 若典型场景位置已有远程 img，不要求 react block / page-shell
                    scene_window = [(ln, l) for ln, l in section['lines'] if markers['scene'] < ln < markers['alternative']]
                    has_remote_img = any(REMOTE_IMG_RE.search(l) for _, l in scene_window)
                    if not has_remote_img:
                        for block_start, block_text in extract_react_text_in_window(section['lines'], markers['scene'], markers['alternative']):
                            findings.extend(check_page_shell(path, title, block_start, block_text))
    return findings


def check_13_sections(path: str, lines: List[str]) -> List[Finding]:
    findings = []
    for section in split_h3_sections(lines):
        title = section['title']
        if not re.match(r'1\.3\.\d', title):
            continue
        if not has_illustration(section['lines']):
            findings.append(Finding(path, section['line'], '1.3-illustration', 'error', f'`### {title}` 缺少推荐/不推荐对比图'))

        recommend = find_marker(section['lines'], '✅ **推荐：**')
        reject = find_marker(section['lines'], '❌ **不推荐：**')
        divider = None
        for line_no, line in section['lines']:
            if line.strip() in ('<hr>', '---'):
                divider = line_no
                break
        if recommend is None:
            findings.append(Finding(path, section['line'], '1.3-summary', 'error', f'`### {title}` 图后缺少 `✅ **推荐：**`'))
        if divider is None:
            findings.append(Finding(path, section['line'], '1.3-summary', 'error', f'`### {title}` 图后缺少 `<hr>`'))
        if reject is None:
            findings.append(Finding(path, section['line'], '1.3-summary', 'error', f'`### {title}` 图后缺少 `❌ **不推荐：**`'))
        if recommend and divider and reject and not (recommend < divider < reject):
            findings.append(Finding(path, section['line'], '1.3-summary', 'error', f'`### {title}` 图后顺序应为 `✅ 推荐` -> `<hr>` -> `❌ 不推荐`'))
    return findings


def extract_react_blocks(lines: List[str]) -> List[dict]:
    """Extract all react blocks.

    Each block dict now carries `is_what_block: bool` — True when the block
    falls between **是什么** and **简单用法** inside a 1.2.x section.  This
    lets callers apply different rules for form-state / auto-open behaviour.
    """
    # Pre-compute line ranges that are inside 是什么 windows for 1.2.x sections.
    what_windows: List[Tuple[int, int]] = []  # (start_line_exclusive, end_line_exclusive)
    current_h3_title = ''
    in_12 = False
    what_line = None
    usage_line = None
    for idx, line in enumerate(lines, 1):
        h3 = H3_RE.match(line)
        if h3:
            # flush previous window if complete
            if in_12 and what_line and usage_line:
                what_windows.append((what_line, usage_line))
            current_h3_title = h3.group(1).strip()
            in_12 = bool(re.match(r'1\.2\.\d', current_h3_title))
            what_line = None
            usage_line = None
            continue
        if H2_RE.match(line) or H1_RE.match(line):
            if in_12 and what_line and usage_line:
                what_windows.append((what_line, usage_line))
            in_12 = False
            what_line = None
            usage_line = None
            continue
        if in_12:
            if '**是什么**' in line and what_line is None:
                what_line = idx
            if '**简单用法**' in line and usage_line is None:
                usage_line = idx
    if in_12 and what_line and usage_line:
        what_windows.append((what_line, usage_line))

    def _in_what_window(block_start: int) -> bool:
        return any(lo < block_start < hi for lo, hi in what_windows)

    blocks = []
    current_h3 = None
    in_block = False
    start = 0
    body = []
    for idx, line in enumerate(lines, 1):
        if not in_block:
            if H1_RE.match(line) or H2_RE.match(line):
                current_h3 = None
                continue
            h3 = H3_RE.match(line)
            if h3:
                current_h3 = h3.group(1).strip()
            if REACT_FENCE_RE.match(line):
                in_block = True
                start = idx
                body = []
            continue
        if line.rstrip() == '```':
            blocks.append({
                'start': start,
                'h3': current_h3,
                'text': '\n'.join(body),
                'lines': list(body),
                'is_what_block': _in_what_window(start),
            })
            in_block = False
            continue
        body.append(line)
    return blocks


def jsx_used(block_text: str, name: str) -> bool:
    return bool(re.search(rf'<{name}[\s/>]', block_text))


OPEN_TRUE_RE = re.compile(r'(?:open|defaultOpen|defaultVisible|visible)\s*=\s*\{?\s*true\b')


def check_react_blocks(path: str, lines: List[str]) -> List[Finding]:
    findings = []
    for block in extract_react_blocks(lines):
        text = block['text']
        h3 = block['h3'] or ''
        has_tour = 'Tour' in text
        is_what = block.get('is_what_block', False)

        if 'function App()' not in text:
            findings.append(Finding(path, block['start'], 'react-shape', 'error', 'react 代码块应定义单个顶层 `function App()`'))
        if re.search(r'^\s*(import|export)\s+', text, re.M):
            findings.append(Finding(path, block['start'], 'react-shape', 'error', 'react 代码块不应包含 import/export'))
        if re.search(r'\brender\s*\(', text):
            findings.append(Finding(path, block['start'], 'react-shape', 'error', 'react 代码块不应使用旧式 `render(...)` 写法'))

        # 「是什么」图：浮层组件必须用 open={true}/defaultOpen={true} 默认展示浮层，且不遮挡触发器
        if is_what:
            popup_in_what = [name for name in POPUP_COMPONENTS if jsx_used(text, name)]
            if popup_in_what and not OPEN_TRUE_RE.search(text):
                findings.append(Finding(
                    path, block['start'], 'what-block-open', 'error',
                    f'「是什么」形态图使用了 {", ".join(popup_in_what)} 但未设置 open={{true}} / defaultOpen={{true}}；'
                    f'浮层内容必须默认展开，让用户直接看到组件完整形态',
                ))
            has_height_reserve = ('minHeight' in text or 'paddingBottom' in text
                                   or bool(re.search(r'height\s*:\s*[1-9]\d{2,}', text)))
            if popup_in_what and not has_height_reserve:
                findings.append(Finding(
                    path, block['start'], 'what-block-open', 'error',
                    f'「是什么」形态图使用了浮层组件（{", ".join(popup_in_what)}）但容器无 minHeight / paddingBottom / height（≥100px）；'
                    f'需要足够高度容纳展开的浮层，不能裁剪内容',
                ))

        for offset, line in enumerate(block['lines'], 1):
            for pattern, label in AUTO_OPEN_PATTERNS:
                if pattern.search(line):
                    if has_tour:
                        continue
                    # 「是什么」图和 1.3.x 对比图允许 open={true}（需展示浮层展开态）
                    if is_what or re.match(r'1\.3\.\d', h3):
                        continue
                    findings.append(Finding(path, block['start'] + offset, 'interaction', 'error', f'禁止自动打开浮层：{label}'))
            visible_line = re.sub(r'`[^`]*`', '', line)
            if FORBIDDEN_API_RE.search(visible_line):
                findings.append(Finding(path, block['start'] + offset, 'interaction', 'error', '禁止使用 message.* / notification.*，会逸出演示容器'))
            stripped = line.strip()
            if ('<ConfigProvider' in stripped or '</ConfigProvider>' in stripped) and 'Infrad.ConfigProvider' not in stripped:
                findings.append(Finding(path, block['start'] + offset, 'react-shape', 'error', '禁止使用裸 ConfigProvider；请写 Infrad.ConfigProvider 或从 Infrad 解构'))

        if re.match(r'1\.3\.\d', h3):
            findings.extend(check_compare_block(path, block))

        popup = [name for name in POPUP_COMPONENTS if jsx_used(text, name)]
        portal = [name for name in PORTAL_COMPONENTS if jsx_used(text, name)]
        if popup and 'getPopupContainer' not in text:
            findings.append(Finding(path, block['start'], 'interaction-hint', 'hint', f'使用 {", ".join(popup)} 但未传 getPopupContainer；若浮层逸出演示区再修'))
        if portal and 'getContainer' not in text:
            findings.append(Finding(path, block['start'], 'interaction-hint', 'hint', f'使用 {", ".join(portal)} 但未传 getContainer；若浮层挂到 body 影响阅读再修'))

        # 检测 getPopupContainer 依赖父节点但 wrapper 缺 position:relative
        uses_parent_popup = bool(re.search(
            r"getPopupContainer\s*=\s*\{?\s*(?:\([^)]*\)\s*=>|function[^(]*\([^)]*\))\s*"
            r"(?:t|el|node|trigger|container)\s*\.parent(?:Element|Node)",
            text,
        ))
        relative_count = len(re.findall(r"position:\s*['\"]relative['\"]", text))
        if uses_parent_popup and popup and relative_count == 0:
            findings.append(Finding(
                path, block['start'], 'interaction', 'error',
                f'getPopupContainer 依赖 parentElement/parentNode 但 block 内无 position:relative wrapper；'
                f'浮层会定位错乱遮挡 trigger（{", ".join(popup)}）',
            ))

        # 检测 Page Shell 场景图 content style 有 overflow:hidden（最外层装饰框的 overflow:hidden 是合理的，不报）
        content_style_match = re.search(r'const content\s*=\s*\{([^}]+)\}', text)
        if content_style_match and re.search(r"overflow:\s*['\"]hidden['\"]", content_style_match.group(1)):
            findings.append(Finding(
                path, block['start'], 'interaction', 'error',
                'Page Shell 场景图 content 区域有 overflow:hidden，会截断 fake div 下拉；去掉该属性',
            ))

        absolute_count = len(re.findall(r"position:\s*['\"]absolute['\"]", text))
        if absolute_count - 2 * relative_count >= 3:
            findings.append(Finding(path, block['start'], 'interaction', 'error', f'absolute 过多且缺少 relative 包装：absolute={absolute_count}, relative={relative_count}'))
    return findings


def check_compare_block(path: str, block: dict) -> List[Finding]:
    text = block['text']
    findings = []
    looks_compare = (
        ('推荐' in text and '不推荐' in text)
        or 'gridTemplateColumns' in text
        or re.search(r'<Flex[^>]*\bgap=', text)
    )
    if not looks_compare:
        return [Finding(path, block['start'], 'compare-figure', 'error', '1.3.x react 块不像双侧推荐/不推荐对比图')]

    required_tokens = {
        '#52c41a': '推荐侧 4px 色条',
        '#ff4d4f': '不推荐侧 4px 色条',
        '#f6ffed': '推荐标签行背景',
        '#fff2f0': '不推荐标签行背景',
    }
    for token, label in required_tokens.items():
        if token not in text:
            findings.append(Finding(path, block['start'], 'compare-figure', 'error', f'1.3.x 对比图缺少 {label} token `{token}`'))
    if 'Text type="success"' in text or "type='success'" in text:
        findings.append(Finding(path, block['start'], 'compare-figure', 'error', '不要用顶部 success 文案条替代推荐标签行'))
    if 'Text type="danger"' in text and '#ff4d4f' not in text:
        findings.append(Finding(path, block['start'], 'compare-figure', 'error', '不要只用 danger 文案替代不推荐色条和标签行'))
    has_table_or_form = bool(re.search(r'<(Table|Form)[\s/>]', text))
    has_page_shell = '#0d2b6b' in text or '#001529' in text
    if not has_table_or_form and not has_page_shell:
        findings.append(Finding(path, block['start'], 'page-shell', 'warning',
                                '1.3.x 对比图 panel 未包含 Table/Form 或 Page Shell；若组件本身不适合页面级场景（如 Rate、Tag、Badge）可忽略'))

    # 检测对比图两侧等高结构：每侧外层 div 需要 display:flex + flexDirection:column，panel 需要 flex:1
    # 正确结构：side = { flex:1, display:'flex', flexDirection:'column' }，panel 加 flex:1
    uses_fixed_height_on_panel = bool(re.search(
        r"(?:const panel|panel\s*=)\s*=\s*\{[^}]*\bheight\s*:\s*\d+[^}]*\}",
        text,
    ))
    if uses_fixed_height_on_panel:
        findings.append(Finding(path, block['start'], 'compare-figure', 'error',
                                '1.3.x 对比图 panel 使用固定 height，两侧内容不同时高度会不一致；'
                                '应用 minHeight + flex:1，外层 side div 用 display:flex + flexDirection:column'))

    has_flex_column_side = bool(re.search(r"flexDirection\s*:\s*['\"]column['\"]", text))
    has_panel_flex1 = bool(re.search(r"panel[^}]*flex\s*:\s*1", text) or
                           re.search(r"flex\s*:\s*1[^}]*(?:minHeight|border)[^}]*}", text))
    if not has_flex_column_side:
        findings.append(Finding(path, block['start'], 'compare-figure', 'error',
                                '1.3.x 对比图每侧外层 div 缺少 flexDirection:column；'
                                '需要 side = { flex:1, display:\'flex\', flexDirection:\'column\' } 才能让 panel flex:1 等高撑满'))

    return findings


def collect_targets(args: List[str]) -> Tuple[List[str], List[str]]:
    if not args:
        args = ['./Component']
    files = []
    missing = []
    for target in args:
        if os.path.isdir(target):
            files.extend(sorted(glob.glob(os.path.join(target, '*.md'))))
        elif os.path.isfile(target):
            files.append(target)
        else:
            missing.append(target)
    return sorted(dict.fromkeys(files)), missing


def check_preview_residue(files: List[str]) -> List[Finding]:
    findings = []
    seen_dirs = sorted({os.path.dirname(os.path.abspath(path)) or os.getcwd() for path in files})
    seen = set()
    for directory in seen_dirs:
        for preview in glob.glob(os.path.join(directory, '*-preview.html')):
            if preview in seen:
                continue
            seen.add(preview)
            findings.append(Finding(preview, 1, 'preview-residue', 'error', '发现 *-preview.html 临时预览文件；push 前应删除'))
    return findings


def check_file(path: str) -> List[Finding]:
    lines = read_lines(path)
    findings = []
    findings.extend(check_top_level_structure(path, lines))
    findings.extend(check_11_no_first_illustration(path, lines))
    findings.extend(check_placeholder_integrity(path, lines))
    findings.extend(check_12_sections(path, lines))
    findings.extend(check_13_sections(path, lines))
    findings.extend(check_react_blocks(path, lines))
    return findings


def print_report(files: List[str], findings: List[Finding]) -> None:
    errors = [item for item in findings if item.severity == 'error']
    hints = [item for item in findings if item.severity == 'hint']
    print(f'扫描 {len(files)} 个 Markdown 文件')
    print(f'  - 阻断问题：{len(errors)}')
    print(f'  - 非阻断提示：{len(hints)}')
    if not findings:
        print('\n✅ 未发现文档配图规范问题')
        return
    print('\n=== 详细清单 ===')
    by_path = {}
    for item in findings:
        by_path.setdefault(item.path, []).append(item)
    for path, items in by_path.items():
        print(f'\n📄 {path}')
        for item in sorted(items, key=lambda finding: (finding.severity != 'error', finding.line, finding.category)):
            mark = '❌' if item.severity == 'error' else 'ℹ️'
            print(f'  {mark} L{item.line} [{item.category}] {item.message}')


def main() -> int:
    parser = argparse.ArgumentParser(description='Check IDS component guide illustration compliance.')
    parser.add_argument('targets', nargs='*', help='Markdown file(s) or directory/directories to check. Defaults to ./Component.')
    parser.add_argument('--allow-preview-html', action='store_true', help='Do not report *-preview.html residue next to checked docs.')
    ns = parser.parse_args()

    files, missing = collect_targets(ns.targets)
    if missing:
        for target in missing:
            print(f'❌ 路径不存在: {target}', file=sys.stderr)
        return 2
    if not files:
        print('⚠️  未找到 Markdown 文件')
        return 0

    findings = []
    for path in files:
        findings.extend(check_file(path))
    if not ns.allow_preview_html:
        findings.extend(check_preview_residue(files))

    print_report(files, findings)
    return 1 if any(item.severity == 'error' for item in findings) else 0


if __name__ == '__main__':
    sys.exit(main())
