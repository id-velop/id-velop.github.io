# 插图标准

## A. 参考基线（动笔前必做）

- 处理 IDS / Infra 组件文档前，先列出 `../../skills/reference/` 下可用参考文件，按组件类型挑 **2 篇以上**同类或相近文档对照，再开始生成。只参考一篇就批量生成，会把错误习惯复制到整批。
- 参考优先级：用户提供 → `../../skills/reference/` → 目标仓库 `Component/` → InfraD / AntD 真实渲染。
- 若 `reference/` 暂无同类参考，回到 `Component/` 找相近组件（Modal 参考 Drawer / Popconfirm / Message 等）。
- 若仍缺少参考，先说明"缺少同类参考"，再按最接近的已验证基线生成，并用 HTML 预览或截图做视觉复核。

绘制前必须打开并检查真实渲染的 InfraD / AntD 示例：Modal、Drawer 等打开态；浮层、展开态、悬浮态、加载态、空态等需要精确还原组件视觉的状态；当前参考资料没有覆盖的组件特定视觉细节。手写实现必须先找到真实组件基线，对齐基线里的设计 token 与样式表现，不要把某个组件或某次截图里的固定数值写成通用规则。

若某个 section 已有来自 `editor.shopee.io` 或 `/uss/` 的远程图片，将它视为用户提供的视觉内容，除非用户明确说它是错的，否则不要替换。

## B. 组件类型决策

- 先判断目标组件是否涉及浮层、展开态、悬浮态、加载态、空态或页面级状态。
- 若涉及精确视觉状态，先建立真实组件基线，再决定用真实组件、静态模拟还是页面级场景图。
- 手写相关组件展示可以接受，但必须对齐真实组件基线里的设计 token 和样式表现，不要把某个组件或某张截图的固定数值写成通用标准。

### B1. 同一类型两张图的一致性

同一个 `1.2.x` 小节内，「是什么」示例图和「典型场景」场景图必须使用**相同的触发器形态**（都用文字按钮、或都用图标按钮），且业务内容必须属于同一情境。

常见错误：示例图用「文字按钮 + 账户菜单」，典型场景图用「图标按钮 + 表格操作列」——读者会以为这是两种不同的组件形态。

生成两张图后，检查：
1. 触发器形态是否一致
2. 菜单/内容是否属于同一业务情境，不要一张画「账户场景」、另一张画「订单操作」

## React 代码块结构

每个代码块只使用一个顶层 `function App()`。

不要使用：

- `import`
- `export`
- TypeScript 类型标注
- 旧式 `render(...)` 调用
- 模块级 helper 声明

常量和 helper 函数都放在 `App` 内部定义。helper 写成返回 JSX 的普通函数（`renderTopBar()`），不要写成 React 组件（`<PSTopBar />`）。

只使用预注入 scope：`React`、`Infrad`、`Icons`、`InfradPro`、`SpaceBiz`。文档 `react` 块不要写裸 `<ConfigProvider>`；使用 `<Infrad.ConfigProvider>`，或先 `const { ConfigProvider } = Infrad` 再使用。

## Playground 链接与小字格式（每个 react block 必须）

每个 `react` block 上方必须紧跟以下两行，顺序固定，缺一不可：

```
<!-- [▶ 在线演示](https://infrad.shopee.io/playground/?agent_code_id=XXXX) -->
<sub>🖱️ 点击图片可在线演示</sub>
```

**禁止**把 Playground 链接写成正式 Markdown 链接格式（`[▶ 在线演示](...)`）——这会在文档里渲染出蓝色超链接文字，破坏排版。只允许注释格式。

## 1.1 组件构成

不要为 `1.1 组件构成` 生成第一张插图。

编辑该 section 时可以移除旧的占位注释，但保留文字形式的元素说明列表。

如果用户明确要求保留 1.1 里的既有附图，或文章已有远程/Markdown 图片必须暂时保留，则该附图上下必须各紧跟一行独立 `<br>`：

```
<br>
<img src="..." />
<br>
```

不要把 `<br>` 放到段落后面，也不要只加其中一侧。

## 1.2 类型说明

每个 `1.2.x` 类型 section 应包含：

- `**是什么**` 下方的一张形态示意图。
- `**典型场景**` 下方的一张具体场景图。

使用真实组件主体，不要用抽象标签或通用卡片冒充组件。

`**是什么**` 或 `**典型场景**` 下方若已有 `editor.shopee.io` / `/uss/` 远程图，该位置视为已完成，不生成 React block，不写 Playground 链接，不做 Page Shell 检查。只需在没有任何配图的位置补图。

## 1.3 典型场景案例

- `1.3.x` 小节默认必须生成推荐 / 不推荐双侧对比图，不降级为单张示意图。
- 若占位符同行或紧邻上一行已有 `editor.shopee.io` 或 `/uss/` 远程图，保留远程图；只清理多余 blockquote 前缀，不生成 React block，不写 Playground 链接。
- 没有占位符的小节——必须根据该小节场景描述**主动补齐**占位符再生成代码。
- `1.3.x` 对比图必须表达具体业务场景与后果，panel 内要有表单、列表、发布流、同步任务、数据看板等上下文；不能只画孤立控件。
- 两侧必须是"正确做法 vs 对应错误做法"，不能把两个正确方案并排当对比图。

### 图文对齐检查（生成代码前必做，不可跳过）

**在写任何 React 代码之前**，先完成以下三步：

1. 逐字读取该 `1.3.x` 小节的 ✅ 推荐描述和 ❌ 不推荐描述。
2. 用一句话写出：
   - 推荐侧要让用户**看到**的具体组件行为或视觉状态是什么
   - 不推荐侧要让用户**看到**的具体组件行为或视觉状态是什么
3. 把这两句话和文章的 ✅/❌ 文字**逐字核对**：
   - 图里展示的行为 = 文字描述的行为 → 可以写代码
   - 不一致 → 停下来，重新理解文字，再回到第 2 步

**反例（不能这样做）**：文章说「在需对比多组信息的场景中强制使用手风琴」是不推荐，但生成的图只放了孤立 FAQ 列表，看不出「对比」场景，图文不符。

### 推荐 / 不推荐对比图骨架

每侧使用三段垂直堆叠：

1. 白色场景面板：`border: '1px solid #f0f0f0'`，`borderBottom: 'none'`，高度由内容自然撑开，使用 `minHeight` 设最低高度（**不用固定 `height`**），加 `flex: 1` 撑满外层 side div；同章节所有对比图的 `minHeight` 值必须统一。
2. 4px 色条：`height: 4`，紧贴 panel 下沿，无间距；推荐 `#52c41a`，不推荐 `#ff4d4f`。
3. 标签行：`border: '1px solid #b7eb8f'`（推荐）/ `'1px solid #ffccc7'`（不推荐），`borderTop: 'none'`，`padding: '10px 14px'`，`fontWeight: 700`，`fontSize: 14`，字色 `#389e0d`（推荐）/ `#cf1322`（不推荐），背景 `#f6ffed`（推荐）/ `#fff2f0`（不推荐），**不加 `textAlign: 'center'`**。

**等高结构（必须严格遵守）**：

两侧内容高度不同时，仅靠父容器 `alignItems: 'stretch'` 无法让 panel 等高——panel 本身高度仍由内容决定。正确做法是**每侧外层 div 用 flex column**，panel 用 `flex: 1` 撑满，这样两侧始终等高，色条和标签行位置对齐：

```js
const side = { flex: 1, display: 'flex', flexDirection: 'column' };
const panel = { background: '#fff', border: '1px solid #f0f0f0', borderBottom: 'none', padding: 12, minHeight: 200, flex: 1 };

<Flex gap={16} style={{ width: '100%', alignItems: 'stretch' }}>
  <div style={side}>
    <div style={panel}>{/* 推荐侧内容 */}</div>
    <div style={{ height: 4, background: '#52c41a' }} />
    <div style={labelGood}>推荐</div>
  </div>
  <div style={side}>
    <div style={panel}>{/* 不推荐侧内容 */}</div>
    <div style={{ height: 4, background: '#ff4d4f' }} />
    <div style={labelBad}>不推荐</div>
  </div>
</Flex>
```

禁止写法：`panel = { ..., height: 240 }`——固定高度会在两侧内容不同时导致其中一侧留白或被截断。

不要用纯文字的成功 / 危险色条替代这个骨架。不要在 panel 顶部用 `Text type="success"` / `Text type="danger"` 加中文解释条冒充对比骨架。关系类配图必须画组件本体形态，不要用 Tag、彩色胶囊或文字卡片替代组件。非推荐 / 不推荐对比图（组件用法示例、典型场景、单张说明图）**不加**色条和标签行。

**标签行必须严格复制以下代码，禁止任何修改：**

```js
// 推荐
<div style={{ background: '#f6ffed', border: '1px solid #b7eb8f', borderTop: 'none', padding: '10px 14px', fontWeight: 700, fontSize: 14, color: '#389e0d' }}>推荐</div>

// 不推荐
<div style={{ background: '#fff2f0', border: '1px solid #ffccc7', borderTop: 'none', padding: '10px 14px', fontWeight: 700, fontSize: 14, color: '#cf1322' }}>不推荐</div>
```

## 场景型插图与 Page Shell

凡是用于说明真实业务场景的插图，都应放在完整场景页面中展示，而不是只画孤立组件。场景页面需要包含 Topbar 和 Sidebar，让读者能理解组件在页面结构、导航层级和业务上下文中的位置。

触发关键词：摆放位置、页面场景、独立列表页、卡片内嵌、弹窗内、侧边抽屉、页面级、应用级。

**重新生成与修复的默认行为**：对 `1.2.x` 典型场景图执行重新生成或修复操作时，**必须默认加入完整 Page Shell（Topbar + Sidebar）**，不需要用户额外说明。只有当用户明确指出「不需要页面框架」「只展示组件本身」时，才可以省略 Page Shell。场景图里的所有组件也必须保持可交互（onClick / onChange 等），不能退化为静态展示。

**Page Shell 视觉规范：**

| 要素 | 规范值 |
|------|--------|
| Topbar 背景色 | `#0d2b6b` |
| Topbar 高度 | `56px` |
| Topbar 左侧 | 产品名文字（白色 14px 700），不放 logo 图标 |
| Topbar 右侧 | 圆形头像（28px，`#4a90e2` 底，白色字母），不放 bell 图标 |
| 侧边导航宽度 | `180px`，白底，`borderRight: '1px solid #f0f0f0'` |
| 导航 item 高度 | `padding: '8px 14px'`，`fontSize: 13` |
| 导航激活项 | 文字 `#2673dd`，背景 `#e6efff`，无左边框色条 |
| 导航普通项 | 文字 `#555`，透明背景 |
| 内容区背景 | `#f5f7fa` |
| 内容区 padding | `16px 20px` |
| 页面 frame 边框 | `border: '1px solid #d9d9d9'`，`borderRadius: 2`，`overflow: 'hidden'` |

frame 高度：独立列表页（内容多）`height: 480`；其他场景 `height: 380`。所有样式常量和 render helper 必须定义在 `App` 函数内部。多个页面场景必须竖向排列（`Flex vertical gap={32}`），每个场景独占一行。

弹窗用纯 CSS 绝对定位模拟，不用 Antd Modal / Drawer。弹窗容器：`background: '#fff'`，`borderRadius: 2`，`boxShadow: '0 6px 16px rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)'`，遮罩 `rgba(0,0,0,0.45)`。遮罩层必须套在 frame 的 `position: relative` 容器内。

## 浮层与 Portal 组件

有展开态的组件（Dropdown、Select、DatePicker、TimePicker、ColorPicker 等），「是什么」图必须用真实组件 + `open={true}` 默认展开面板，让 Playground 用户可直接交互。禁止只展示收起态触发器，禁止用 fake div / renderMenu / renderSplit 等静态方式模拟菜单或浮层内容。1.3.x 对比图如需展示菜单内容同样适用此规则——对比图里的 Dropdown、Select 等也必须是真实组件 + `open={true}` + `getPopupContainer`。

**防止浮层飞动**，必须同时满足：① wrapper div 加 `position: 'relative'`，② 组件加 `getPopupContainer={() => ref.current}`，③ MutationObserver fix 使用正确 selector。缺少任意一条浮层会跟随鼠标或 fix 无效。

**各组件对照表（DROPDOWN_CLASS / TRIGGER_CLASS）**：

MutationObserver fix 的 `table,tr / th,td` 清理是防御性修复：stackedit 给整个文档注入全局 CSS，会污染 demo 区域内任何 `table/tr/th/td`（不限于组件面板内部）。**所有含浮层的组件都必须加，无例外。**

| 组件 | `DROPDOWN_CLASS` | `TRIGGER_CLASS` |
|------|-----------------|----------------|
| Select / TreeSelect / AutoComplete | `.ant-select-dropdown` | `.ant-select-selector` |
| DatePicker / TimePicker / RangePicker | `.ant-picker-dropdown` | `.ant-picker` |
| ColorPicker | `.ant-color-picker`（禁止 `.ant-color-picker-dropdown`） | `.ant-color-picker-trigger` |
| Cascader | `.ant-cascader-dropdown` | `.ant-cascader` |
| Mentions | `.ant-mentions-dropdown` | `.ant-mentions` |
| Dropdown | `.ant-dropdown` | 触发器本身（Button / a 等，无固定 class） |
| Tooltip | `.ant-tooltip` | 触发器本身 |
| Popover / Popconfirm | `.ant-popover` | 触发器本身 |

Dropdown 特别说明：浮层用 `open` prop（布尔值 shorthand）控制；`getPopupContainer` + MutationObserver fix 同样必须加。

**禁止硬编码 `top: 'Npx'`**——必须用 `getBoundingClientRect()` 动态计算（见下方模板）。

**标准写法模板**：

```jsx
function App() {
  const { 组件名 } = Infrad;
  const ref = React.useRef(null);
  React.useEffect(() => {
    if (!ref.current) return;
    const fix = () => {
      const trigger = ref.current.querySelector('TRIGGER_CLASS');
      const dropdowns = ref.current.querySelectorAll('DROPDOWN_CLASS');
      if (!dropdowns.length) return;
      const offsetTop = trigger ? trigger.offsetTop + trigger.offsetHeight + 4 : 40;
      dropdowns.forEach(el => {
        el.style.position = 'absolute';
        el.style.top = offsetTop + 'px';
        el.style.left = '0px';
        el.style.bottom = 'auto';
        el.style.right = 'auto';
        el.style.transform = 'none';
      });
    };
    fix();
    const obs = new MutationObserver(fix);
    obs.observe(ref.current, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class'] });
    return () => obs.disconnect();
  }, []);
  return (
    <div ref={ref} style={{ position: 'relative', minHeight: 容纳浮层的最小高度 }}>
      <组件名 open getPopupContainer={() => ref.current} />
    </div>
  );
}
```

**日历类组件额外 fix**（DatePicker、TimePicker、RangePicker），在 `fix()` 里追加：

```js
ref.current.querySelectorAll('table,tr').forEach(el => {
  el.style.border = 'none';
  el.style.background = 'transparent';
});
ref.current.querySelectorAll('th,td').forEach(el => {
  el.style.border = 'none';
  el.style.background = 'transparent';
  el.style.padding = '';
});
```

ColorPicker、Select、Cascader 等非日历组件不需要这段。

**场景图（典型场景）**：浮层组件保持收起态，用户点击可展开；frame 高度需容纳展开后浮层，内容区不得设 `overflow: hidden`。场景图不需要加 MutationObserver fix。

**场景图内容量（含滚动联动）**：场景图里如果有滚动联动（锚点导航、目录等），每个章节的内容量必须让容器能实际滚动。最小内容原则：每节至少 5–8 条色块行，确保总内容高度 > 容器高度。

**容器内滚动定位必须用 `getBoundingClientRect`，禁止用 `offsetTop`**：容器有 padding 时，`el.offsetTop` 是相对 offsetParent 的绝对值，不等于相对滚动容器的距离，会导致滚动位置偏移。正确写法：
```js
container.scrollTop += el.getBoundingClientRect().top - container.getBoundingClientRect().top - 8;
```
同样，`handleScroll` 里判断高亮也必须用 `getBoundingClientRect().top` 减去容器顶部，不能用 `el.offsetTop <= container.scrollTop`。

**1.3.x 对比图双侧浮层专项规则**：每侧独立的 `ref` 必须挂在外层 wrapper div（`position: relative`）上；视觉 panel div 只负责 border / background / padding，**不设任何 height 或 minHeight**。两侧 wrapper 通过父容器 `alignItems: 'stretch'` 保证等高。

**关键：panel 必须加 `paddingBottom` 撑出 dropdown 空间。** dropdown 是 `position: absolute` 不占文档流，若不在 panel 底部预留空间，dropdown 会覆盖下方的色条和标签行。参考值：4 条选项 ≈ 160px，条目更多时相应增大。

**定位必须用 `getBoundingClientRect`，禁止用 `offsetTop`/`offsetLeft`。** panel 有 padding 时，`offsetTop` 是相对 offsetParent 的值，不等于相对 wrapper 的距离，会导致 dropdown 位置偏移。正确写法：

```js
const cRect = ref.current.getBoundingClientRect();
const tRect = trigger.getBoundingClientRect();
const top = tRect.bottom - cRect.top + 4;
const left = tRect.left - cRect.left;
```

```jsx
// ✅ 正确
const wrapper = { flex: 1, position: 'relative' };
const panel = { background: '#fff', border: '1px solid #f0f0f0', borderBottom: 'none', padding: 16, paddingBottom: 160 };
<Flex gap={16} style={{ width: '100%', alignItems: 'stretch' }}>
  <div style={wrapper} ref={refGood}>
    <div style={panel}><AutoComplete open getPopupContainer={() => refGood.current} /></div>
    <div style={{ height: 4, background: '#52c41a' }} />
    <div style={labelStyle}>推荐</div>
  </div>
  <div style={wrapper} ref={refBad}>
    <div style={panel}><AutoComplete open getPopupContainer={() => refBad.current} /></div>
    <div style={{ height: 4, background: '#ff4d4f' }} />
    <div style={labelStyle}>不推荐</div>
  </div>
</Flex>

// ❌ 错误 — panel 无 paddingBottom，dropdown 会盖住色条和标签行
const panel = { background: '#fff', border: '1px solid #f0f0f0', borderBottom: 'none', padding: 16 };

// ❌ 错误 — 用 offsetTop 在有 padding 的嵌套结构里定位会偏移
const top = trigger.offsetTop + trigger.offsetHeight + 4;
const left = trigger.offsetLeft;
```

**Modal / Drawer 专属规则**：遮罩使用 `position: fixed`，`overflow: hidden` 无法限制，弹层会跑到 viewport 层级。必须同时满足以下三条：① `getContainer={() => ref.current}`，② 容器加 `transform: 'translateZ(0)'`，③ 容器加 `position: 'relative'` + `overflow: 'hidden'`。ref 必须挂在**最外层 Page Shell div**（包含 topbar + sidebar + content 的那个）。

```jsx
<div ref={ref} style={{ position: 'relative', overflow: 'hidden', transform: 'translateZ(0)', height: 480 }}>
  {/* topbar + sidebar + content */}
  <Modal open={open} getContainer={() => ref.current} onCancel={() => setOpen(false)}>
    {/* content */}
  </Modal>
</div>
```

注意：这套规则只适用于 Modal/Drawer。Select、DatePicker 等下拉浮层是 `position: absolute`，用 `getPopupContainer + position: relative` 即可，不需要 `transform`。

**浮层 CSS 模拟规范**：

- B1. 单气泡演示：气泡和触发器是流式 Flex 的两个兄弟节点，气泡不做 absolute，不依赖祖先 relative。
- B2. 工具栏内气泡：触发器外包 `<div style={{ position: 'relative' }}>` 只包触发器本身，气泡 `position: 'absolute'`；父容器须留足气泡生长空间（单行约 30px，双行约 52px，含按钮 Popover 约 100–140px）。
- B3. 多气泡拼图：用 CSS Grid 分区，禁止用 absolute 坐标散点拼图。
- B4. 演示容器宽度：单图整体宽度 ≤ 560px；对比图每栏约 440px；超宽图用 `maxWidth: '100%'` + `overflow: 'auto'` 自包。

**浮层阴影 token**：`{ background: '#fff', border: '1px solid #f0f0f0', boxShadow: '0 6px 16px rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)', borderRadius: 2, padding: '12px 16px' }`。气泡文字色：标题 `#000000e0`（`fontSize: 14, fontWeight: 600`），正文 `#000000a6`（`fontSize: 14`）。

## 组件 size 规范

IDS 组件的 size 层级为：`small` < `default`（default 比 small 大一号）。

**生成配图时，凡组件有 `size` prop，统一使用 `size="default"`，不使用 `size="small"`。**

适用范围：Form、Input、Select、Button、Switch、Table 等所有支持 size prop 的 InfraD 组件。

**禁止出现的写法（每条都是历史 bug，不得重复）：**

- `fontSize: 12`（或任何 fontSize）→ 不写 fontSize，浏览器默认 14px
- `justifyContent: 'center'` → 不加，文字靠左
- `color: '#52c41a'` 或 `color: '#ff4d4f'` → 必须用深色 `#389e0d` / `#cf1322`
- `height: 32` + flex 居中 → 改用 `padding: '10px 14px'`
- 缺 `border: '1px solid #b7eb8f'` / `'1px solid #ffccc7'`
- 标签行文字加任何解释（如「推荐：操作按钮不超过3个」）→ 只写「推荐」或「不推荐」四字

## 代码语法严格性

### 禁止猜测 prop 格式（最高优先级）

任何非字符串、非数字的 prop 值（对象、数组、特殊格式），必须先从以下来源之一查到明确格式，再写代码：

1. `COMPONENTS_API.md`
2. InfraD 组件文档 / AntD 官方文档
3. 已在 Playground 验证过的既有 code block

找不到明确文档的，选最保守的写法（纯字符串或已知有效值）。禁止猜测复杂对象格式。

### 语法规则

生成代码前逐行检查：

- 字符串值必须加引号：`value: 'apple'` ✅ / `value: apple` ❌
- CSS 百分比必须是字符串：`width: '100%'` ✅ / `width: 100%` ❌
- 数组中的字符串元素必须加引号：`['apple', 'cherry']` ✅ / `[apple, cherry]` ❌
- 空字符串不能省略：`?? ''` ✅ / `?? ` ❌
- JSX 属性字符串用双引号：`type="primary"` ✅
- 对象 key/value 中的字符串用单引号：`{ value: 'apple', label: 'Apple' }` ✅
- 演示内链接用 `<a href="#ill" onClick={(e) => e.preventDefault()}>` 防止跳回顶部，不用 `href="#"`。

## 组件选择与数据质量

组件选择优先级：

| 场景 | Scope | 示例 |
|------|-------|------|
| 基础 UI | `Infrad` | Button, Table, Form, Modal, Tag |
| 复杂表格/表单 | `InfradPro` | ProTable, ProForm, EditableProTable |
| 业务模板 | `SpaceBiz` | SpaceProTable, SpaceFormModal |
| 图标 | `Icons` | SearchOutlined, PlusOutlined |

- 使用真实业务 mock 数据（如省市区、商品分类、订单状态），不用 `test`/`foo`/`bar` 等无意义数据。
- 自绘容器 `div` 的 `borderRadius` 默认用 `2`（= Infrad token）；圆形头像用 `'50%'`。**禁止**使用 4/6/8 等不在 token 内的值（除非占位描述明确要求圆角卡片）。

## 界面文案规范

配图中的全部界面文案必须符合企业软件后台语境。

### 默认业务域

仅限以下三类：

- **企业云产品**：实例、集群、节点、命名空间、访问策略、资源配额、运行状态、发布版本、监控告警、日志
- **数据分析套件**：数据集、指标、维度、图表、报表、看板、查询任务、调度周期、数据源、更新时间
- **AI 能力平台**：模型、知识库、工作流、Agent、Prompt 模板、推理任务、评测结果、调用量、响应时长、安全策略

### 禁止使用

电商、零售、供应链、内容平台语义，包括但不限于：商品、类目、补货、库存、订单、店铺、购物车、优惠券、发货、直播、达人。

### 生成原则

- 文案必须采用简体中文，语气专业、克制、真实，像后台管理系统中的占位信息。
- 根据组件用途自动匹配最合适的业务语境。
- 优先使用短字段、短标签、短提示语；避免强叙事和具体行业故事。
- 文案服务于组件演示，不可过度抢占视觉重点；当组件是基础类组件时，优先生成「中性、通用、平台化」的界面文案。

## 配图内文字规则

- 只保留业务 mock 数据文字（通知标题、描述、按钮文案、菜单项等组件本身的内容文字），**不加任何 UI 图例标注文字**（如「标题：700 字重」「主操作，视觉突出」「顶部右侧」等）。
- 多场景示意图中各场景名称标签同样**不加**，场景差异通过布局和内容本身体现。
- 推荐 / 不推荐对比图的标签行只写「推荐」或「不推荐」，**不在标签行里写任何解释文字**。
- `1.3.x` 对比图的 panel 内**禁止放任何解释性文字**（包括 `Text type="secondary"`、`Text type="danger"` 或任何说明性 `<div>`）。靠组件本身的视觉差异说明问题，标签行只写「推荐」或「不推荐」。
- 「不推荐」侧演示区仅需展示恰好能说明问题的最少内容；如需表达「过多内容」反例，用 5 条以内数据配合 `overflow: hidden` 裁切，不要真的渲染几十条数据。

## 可交互性（核心原则）

- **所有 `1.2.x` 插图——无论「是什么」图还是「典型场景」图——都应尽量使用真实 InfraD 组件，让 Playground 里的用户能直接操作。**
- **fake div / 纯 CSS 静态模拟只允许在技术上无法用真实组件稳定展示的情况下使用**（如：无法用 `open={true}` 常驻展开、浮层展开态难以稳定截取）；此类例外必须是「是什么」图，且必须是浮层展开态的静态示意，不得用在场景图里。
- 场景图（「典型场景」）里的所有组件都必须可交互：Button 可点、Select 可展开、Input 可输入、Switch 可切换、Checkbox/Radio 可选中。不要用 div 替代任何有交互语义的组件。
- 生成插图后，逐项检查：图里有哪些组件？每个组件在 Playground 里用户能操作吗？不能操作的换成真实组件。

## 禁用与替代

- 不使用 `message.*` / `notification.*` 这类全屏 toast；改用内嵌 `Alert` 或静态反馈区。
- 「是什么」图的浮层组件**必须用 `open={true}`** 默认展开，禁止只展示收起态触发器。同时必须加 `getPopupContainer`，否则面板跟随鼠标飞动影响阅读。
- 静态 Affix 插图不要用真 `Affix`，用 CSS `position: sticky` 模拟固定效果，避免内容飞出 demo。
- 当小节说明组件关系时，图里要画出各组件的真实视觉形态；不要用 Tag、彩色胶囊或文字卡片代替组件本身。

## MDX 兼容写作规范（严格遵守，违反会导致构建报错）

来自 IDS 仓库 `AGENTS.md`。文档通过 MDX 渲染，MDX 比普通 Markdown 更严格。

**prose 里的裸 `{…}` 必须用反引号包住。** MDX 把 `{…}` 当 JavaScript 表达式解析，裸写会触发构建报错。

```
# ❌ 构建报错
gutter 可设置为对象 { xs: 8, sm: 16, md: 24 }，随断点变化。

# ✅ 正确
gutter 可设置为对象 `{ xs: 8, sm: 16, md: 24 }`，随断点变化。
```

适用范围：JS/CSS 对象字面量、模板变量占位符（`{variable}`）、任何出现在普通段落文字中的 `{…}`。

**例外**：fenced code block 内部（` ```react ` 等）和 JSX 属性值（`prop={value}`）不受影响。

## 预览与推送

- 默认不生成 HTML preview，不开 HTTP server，不主动打开浏览器预览；只有用户明确要求时才执行。
- 生成 preview 后，推送文档前移除临时 preview 文件，除非用户明确要求保留。
- 推送前必须确认 checker 通过。
- 严禁默认使用 `git push --no-verify` 绕过检查；需要跳过时必须先向用户说明原因并获得明确同意。

## Do NOT（历史 bug 速查）

- 在 `App` 函数内部定义嵌套 React 组件（`const Scene = () => <div />`，然后 `<Scene />`）——会导致 Babel standalone 编译失败。正确做法：把 helper 写成返回 JSX 的普通 render 函数（`const renderScene = () => (...)`），用 `{renderScene()}` 调用。
- 在 `App` 函数外定义模块级 `const` / `function`——Playground 的 react-live 只接受单个顶层表达式，会报 `SyntaxError: Unexpected token (1:9)`。
- 在文档 `react` 块里写裸 `<ConfigProvider>` / `</ConfigProvider>`——react-live 运行时不会注入这个全局变量，会报 `ReferenceError: ConfigProvider is not defined`；改用 `Infrad.ConfigProvider`。
- 给**单组件演示**套装饰居中盒子（`height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center'`）——能 `return <组件 />` 就不包 div。
- 给浮层组件的**静态形态图**包 `useRef` + `getPopupContainer` + 小尺寸容器——浮层在静态预览里本就不会展开，包了无意义且浮层真展开时会被容器裁切。
- 在组件外无必要地加 `padding: 16`——`.demo-mount` 已统一处理 padding，双层 padding 导致间距过大。
- 硬编码统一高度（`height: 200/220/260`）让所有 demo 尺寸一致——高度由内容自然撑开；对比图另有规范。
- 对比图演示区使用固定 `height`——必须用 `minHeight` 让内容自然撑开；panel 加 `flex: 1`，每侧外层 div 用 `display: 'flex', flexDirection: 'column'`，父容器 `alignItems: 'stretch'`，三者配合才能让两侧等高；同章节所有对比图的 `minHeight` 值必须统一。
- 每侧外层 div 只写 `flex: 1` 而不写 `display: flex` + `flexDirection: column`——仅靠 `alignItems: stretch` 无法让 panel 等高，必须让外层 div 成为 flex column 容器，panel 才能用 `flex: 1` 撑满。
- 同一章节内不同对比图使用不同的 `minHeight` 值——同章节所有对比图演示区 `minHeight` 必须统一。
- 「不推荐」侧堆砌大量数据条目——用 5 条以内 + `overflow: hidden` 裁切来表达「过多」的反例。
- 在配图内加注释性说明文字（如「标题：700字重，主信息层级」「主操作，视觉突出」）——图示只展示组件本身，解释放正文。
- 在推荐/不推荐标签行里写解释文字（如「推荐：操作按钮不超过3个」）——标签行只写「推荐」或「不推荐」四字。
- 在 `Tree` 的 `title` 里手动塞拖拽手柄图标（如 `HolderOutlined`）——开启 `draggable` 后自带拖拽指示图标，手动再加会导致每行出现两个手柄图标。
- 企图通过 `style={{ borderRadius: 2 }}` 改 Input / Button / 选中条圆角——这些由主题 token 驱动，必须在 `ConfigProvider` 上改 token。
- 浮层交互演示里让触发按钮居中 `justifyContent: 'center'`——浮层朝 placement 方向会撞容器边界被裁；触发器应居左上，留出 placement 方向足够空间。
- Page Shell 场景图的 content 区域加 `overflow: hidden`——这会截断 fake div 下拉列表（或其他自绘浮层），导致 dropdown 被裁切；content 区域禁止设 `overflow: hidden`，不能用加大 Flex 高度来补偿，高度必须由内容自然撑开。
- 在 `1.2.x` **任何插图**里用 fake div / 纯 CSS 模拟有交互语义的组件（Select、Dropdown、Cascader、Button、Switch、Checkbox、Radio、Input、DatePicker、TimePicker 等）——所有插图里的组件都应尽量使用真实 InfraD 组件，让 Playground 里用户能直接操作；fake div 只在技术上无法稳定展示的浮层展开态静态示意中例外，且只允许在「是什么」图中，场景图里一律禁用。
- 用 `renderMenu` / `renderSplit` / fake div 手画静态菜单代替真实 `Infrad.Dropdown`——Dropdown 的菜单内容必须通过 `menu={{ items }}` prop 传给真实 `Dropdown` 组件渲染，不能用手写 div 拼菜单外观；1.3.x 对比图里同样禁止。
- 只参考 1 篇文档的代码风格就开始批量生成——必须对照 2+ 篇同类早期定稿，避免把错误习惯复制到整批。
- 页面级场景示意图使用简单组件 demo 风格——涉及页面/摆放位置场景时**必须**使用 Page Shell 框架。
- 页面级场景横向并排——多个页面场景必须竖向排列（`Flex vertical gap={32}`），每个场景独占一行。
- 页面级场景中使用 Modal / Drawer 时不加完整容器套装——Modal/Drawer 遮罩是 `position: fixed`，必须在最外层 Page Shell div 上同时加 `transform: 'translateZ(0)'` + `position: 'relative'` + `overflow: 'hidden'` + `getContainer={() => ref.current}`，四者缺一弹层就会跑出配图框。
- 跳过「1.3 各类型典型场景案例」中没有占位符的小节——必须根据该小节场景描述**主动补齐**占位符再生成代码。
- 为 `### 1.3.x` 小节生成单张推荐图——**1.3.x 小节必须一律生成推荐 + 不推荐双侧对比图**。
- 使用无意义的 mock 数据（test、foo、bar 等）——必须使用符合企业软件后台语境的真实业务文案，参见「界面文案规范」章节。
- 在配图中使用电商、零售、供应链、内容平台语义（商品、类目、补货、库存、订单、店铺、购物车、优惠券、发货、直播、达人等）——禁止使用，必须替换为企业云产品、数据分析套件或 AI 能力平台语义。
- 自绘容器使用 4/6/8 等不在 Infrad token 内的 `borderRadius` 值——只用 `2` 或 `'50%'`。
- 在 prose 文字（非 code block）里写裸 `{…}`（如 `{ xs: 8 }`、`{variable}`）——MDX 会把它当 JS 表达式解析，导致构建报错；必须用反引号包住：`` `{ xs: 8 }` ``。
- 1.3.x 对比图 panel 不加 `paddingBottom`——dropdown 是 `position: absolute` 不占文档流，会直接盖住下方的色条和标签行；panel 必须加 `paddingBottom: 160`（4条选项参考值，条目更多时增大）给 dropdown 留出空间。
- 1.3.x 对比图用 `offsetTop`/`offsetLeft` 定位 dropdown——panel 有 padding 时这两个值是相对 offsetParent 的，不是相对 wrapper 的，会导致 dropdown 位置偏移；必须改用 `getBoundingClientRect()` 计算相对 wrapper 的真实距离。
- 只加 `getPopupContainer` 不加 MutationObserver——组件库会在每次渲染后重算浮层坐标；仅 `getPopupContainer` 不足以固定浮层位置，必须同时加 MutationObserver fix。
- 对 ColorPicker 使用 `.ant-color-picker-dropdown` 作为面板 selector——ColorPicker 的面板 class 是 `.ant-color-picker`，不带 `-dropdown` 后缀；使用 `.ant-color-picker-dropdown` 将匹配不到任何元素，浮层 fix 无效。

