# 配图共享规则（Single Source of Truth）

本文件是 `ids-doc-illustration-v2`（生成器）和 `ids-doc-illustration-checker`（检查器）共同遵守的规则基准。

**修改规则时只改这里，其他文件引用本文件，不要在各处各自维护重复内容。**

---

## 1. 文档结构规则

### 必要顶层章节

完整的组件指南应包含：

- `## 1.0. 组件描述`
- `## 1.1. 组件构成`
- `## 1.2. 组件包含哪些不同类型`
- `## 1.3. 各类型典型场景案例`
- `# 2. 选型指南` 或 `## 2.x`
- `# 3. 细致专业部份` 或 `## 3.x`

### 1.1 组件构成

- 不为 `1.1 组件构成` 生成配图。
- 编辑该 section 时**不应移除**旧的占位注释，保留文字形式的元素说明列表。

### 1.2.x 类型章节——两张图规则

每个 `### 1.2.x` 章节**必须包含两张配图**，按以下顺序排列：

1. `**是什么**` — 下方放**形态示意图**（组件本体形态）
2. `**简单用法**`
3. `**典型场景**` — 下方放**场景图**（真实业务上下文中的使用场景）
4. `**替代方案**`

缺少任意一张都是缺陷。使用真实组件主体，不要用抽象标签或通用卡片冒充组件。

检查器将以下任意一项视为配图：
- 本地附图占位注释 `<!-- 附图占位：... -->`
- 带 Playground 链接的 `react` 代码块
- 可信远程图片 `<img src="https://editor.shopee.io/...">` 或 `/uss/` 图片

### 1.3.x 场景章节——推荐 / 不推荐对比图规则

- 每个 `### 1.3.x` 章节**必须**包含一张推荐 / 不推荐双侧对比图，**不降级**为单张示意图。
- 两侧必须是同一业务情境的正确 vs 错误对比，**不能**把两个均合理的方案并排当对比图。
- 对比图后紧跟：

```markdown
✅ **推荐：** ...

<hr>

❌ **不推荐：** ...
```

---

## 2. 推荐 / 不推荐对比图视觉骨架

**这是最高频出错的规则，逐条核查，不得凭记忆写。**

### 结构

每侧从上到下三段垂直堆叠：

```
┌─────────────────────────────┐
│  白色场景 panel（固定高度）   │  border: '1px solid #f0f0f0', borderBottom: 'none'
├─────────────────────────────┤
│  4px 色条                   │  height: 4, 紧贴 panel 下沿，无间距
├─────────────────────────────┤
│  标签行                     │  见下表
└─────────────────────────────┘
```

### 色条颜色

| 侧 | 颜色 |
|---|---|
| 推荐 | `#52c41a` |
| 不推荐 | `#ff4d4f` |

### 标签行完整样式（权威）

| 属性 | 推荐 | 不推荐 |
|---|---|---|
| background | `#f6ffed` | `#fff2f0` |
| border | `1px solid #b7eb8f` | `1px solid #ffccc7` |
| borderTop | `none`（与色条无缝拼接，**必须**） | `none` |
| padding | `10px 14px` | `10px 14px` |
| fontWeight | `700` | `700` |
| color（文字） | `#389e0d` | `#cf1322` |
| fontSize | `14` | `14` |
| textAlign | **不加**（禁止居中） | **不加**（禁止居中） |

### 标签行文字

只能是 `推荐` 或 `不推荐`，**禁止**加任何解释文字（如「推荐：操作按钮不超过3个」）。

### 高度规则

- panel 高度必须用 `height` 固定，**禁止**用 `minHeight`。
- 同一章节所有对比图的 panel `height` 值**必须统一**，不同图之间不能用不同值。
- panel 内容区加 `overflow: hidden`，防止内容溢出破坏等高布局。

### 常见错误（生成器 / 检查器都要拦截）

- ❌ 标签行用 `textAlign: 'center'` 或 `justifyContent: 'center'`
- ❌ panel 用 `minHeight` 而不是 `height`
- ❌ 同章节不同对比图 `height` 值不一致
- ❌ 标签行 `borderTop` 未设为 `none`（色条和标签行之间出现缝隙）
- ❌ 在 panel 顶部用 `Text type="success"` / `Text type="danger"` 加解释条冒充骨架
- ❌ 非对比图（单张用法示例、典型场景图）加了色条和标签行

---

## 3. 业务场景要求

### 场景型插图（通用）

凡是用于说明真实业务场景的插图，都应放在有业务上下文的场景中展示，而不是只画孤立组件。

场景内容因组件和诉求而异，可以是：
- 表格、表单、审批流、弹窗、设置面板
- 带 Topbar + Sidebar 的后台页框架
- 任何能清晰表达业务诉求的真实场景

### 1.3.x 对比图 panel 内容要求

- panel 内必须展示能清晰说明业务诉求的真实场景（如表单、列表、审批流、弹窗、设置面板等）。
- **禁止**只放孤立的目标组件 + Typography.Text 说明文字。
- 「不推荐」侧演示区用最少内容说明问题；如需表达「过多内容」反例，用 5 条以内数据配合 `overflow: hidden` 裁切，不要真的渲染几十条数据。
- 关系示意图必须绘制组件实体，不能用 Tag、彩色胶囊或文字卡片代替组件。

---

## 4. 可交互插图小字规则

每张可交互插图（有 Playground 链接 + `react` 代码块）上方**必须**紧跟一行小字：

```
<sub>🖱️ 点击图片可在线演示</sub>
```

- 小字紧贴在占位注释的正上方一行，不留空行。
- 静态远程图不需要加小字。

---

## 5. React 代码块规则

### 生成流程（强制）

**所有可交互 react 块必须通过 `react-block-generator` Skill 生成并保存到 Playground，获得 agent_code_id 后再写入文档。**

理由：`react-block-generator` 会调用 `POST /apis/faas/agent-code/save` 做语法校验，并在 InfraD Playground 环境中渲染，输出的 `agent_code_id` 对应的预览效果就是文档实际显示的效果。跳过这一步、直接手写 react 块写入文档，会导致语法错误无法发现、且样式无法与 InfraD 真实主题对齐。

工作流：
1. 根据小节需求用 `react-block-generator` 生成代码 + 保存到 Playground
2. 获得预览链接（`https://infrad.shopee.io/playground/?agent_code_id=xxx`）
3. 将 `agent_code_id` 写成 Playground 链接注释，将代码写入 ` ```react ` 块
4. 禁止在接口未返回 200 的情况下写入文档

### 代码格式规则

- 每个代码块只使用一个顶层 `function App()`。
- 所有 `const` 和 render helper 定义在 `App` 内部。
- helper 写成返回 JSX 的普通函数（`const renderXxx = () => (...)`），用 `{renderXxx()}` 调用；**不要**写成额外 React 组件（`const Xxx = () => <div />`，然后 `<Xxx />`）。
- 禁止：`import`、`export`、TypeScript 类型标注、旧式 `render(...)` 调用、模块级声明。
- 只使用预注入 scope：`React`、`Infrad`、`Icons`、`InfradPro`、`SpaceBiz`。
- 禁止裸写 `<ConfigProvider>`，改用 `<Infrad.ConfigProvider>` 或 `const { ConfigProvider } = Infrad`。

### 禁止的运行时模式（blocking）

- `defaultOpen` / `defaultVisible` / `open={true}` / `visible={true}` / 裸写 `open` 或 `visible`
- `message.*` / `notification.*`

---

## 6. 浮层与展开态

### 优先级（从高到低）

1. **静止态**：能直接 `return <组件 />` 就不要包装饰盒、`useRef` 或 `position: relative`。
2. **真实组件 + 交互控制**：可交互 demo 优先保留真实组件，用 `getPopupContainer` / `getContainer` 把浮层限制在演示区内，目标是浮层不逃出演示区、不跟随整页滚动、不遮挡正文。
3. **CSS 静态模拟**：仅当真实组件在 Playground 里无法稳定展示打开态（如 Modal、Drawer 的打开态、多方向集合图）时才使用 CSS 静态模拟，模拟视觉必须对齐真实 InfraD 样式。

**禁止**：不应因为"浮层有 portal 风险"就直接跳到静态模拟，应先尝试用 `getPopupContainer` 解决。

### 真实组件交互 demo 规则

- 真实交互演示的目标是浮层不逃出演示区、不跟随整页滚动、不遮挡正文。`getPopupContainer` / `getContainer` 是首选手段。
- 缺少 `getPopupContainer` 为提示项，不自动阻断；**仅当浮层真正逃出配图区域或影响阅读时才必须处理**。
- 触发器位置：留出浮层生长方向的足够空间（触发器应居左上，留出 placement 方向足够空间，浮层朝中心方向展开）。
- 多气泡或多位置示意不要用人工 px 坐标硬摆；优先使用 CSS Grid 分区，或在足够大的受限容器内展示完整集合。

### 可交互 demo 样式异常修法（不要改为静态模拟）

真实组件在 Playground 渲染时可能出现面板内部空行、间距异常。用 `<style>` 标签注入 CSS 覆盖修复，**不要改为静态模拟**：

```jsx
function App() {
  return (
    <>
      <style>{`/* 针对性 CSS 修复 */`}</style>
      <真实组件 />
    </>
  );
}
```

常见修法：
- DatePicker / RangePicker 日期面板 gap：`.ant-picker-date-panel .ant-picker-content thead { display: none; }`

### CSS 浮层模拟布局规范（仅在必须静态模拟时使用）

| 场景 | 做法 |
|---|---|
| B1. 单气泡演示 | 气泡和触发器是流式 Flex 的两个兄弟节点，气泡不做 absolute |
| B2. 工具栏内气泡 | 触发器外包 `<div style={{ position: 'relative' }}>`（只包触发器本身），气泡 `position: 'absolute'`；父容器须留足气泡生长空间（单行约 30px，双行约 52px，含按钮 Popover 约 100–140px） |
| B3. 多气泡拼图 | 用 CSS Grid 分区，禁止用 absolute 坐标散点拼图 |
| B4. 演示容器宽度 | 单图整体宽度 ≤ 560px；对比图每栏约 440px；超宽图用 `maxWidth: '100%'` + `overflow: 'auto'` 自包 |

### 浮层静态模拟视觉基线

以下参数均基于 InfraD 实际渲染，colorPrimary = `#2673dd`，borderRadius = `2`。

#### Tooltip（黑色气泡）

```javascript
{
  background: 'rgba(0,0,0,0.85)',
  borderRadius: 6,          // Tooltip 特例，不用 2
  padding: '6px 8px',
  fontSize: 14,
  color: '#fff',
  maxWidth: 200,
}
```

#### Popover / 白色气泡面板

```javascript
{
  background: '#fff',
  border: '1px solid #f0f0f0',
  borderRadius: 2,
  boxShadow: '0 6px 16px rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)',
  padding: '12px 16px',
  // 标题
  titleColor: '#000000e0',  titleFontSize: 14, titleFontWeight: 600,
  // 正文
  bodyColor: '#000000a6',   bodyFontSize: 14,
}
```

#### Modal 打开态（CSS 绝对定位模拟，禁止用真实 Antd Modal）

遮罩层（套在 `position: 'relative'` 的 frame 容器内）：

```javascript
{
  position: 'absolute', inset: 0,
  background: 'rgba(0,0,0,0.45)',
  display: 'flex', alignItems: 'center', justifyContent: 'center',
  zIndex: 100,
}
```

Modal 容器：

```javascript
{
  background: '#fff',
  borderRadius: 2,
  boxShadow: '0 6px 16px rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12), 0 9px 28px 8px rgba(0,0,0,0.05)',
  width: 520,
  padding: '20px 24px',
  // 标题
  titleFontSize: 16, titleFontWeight: 600, titleColor: '#000000e0',
  // 正文
  bodyFontSize: 14, bodyColor: '#000000a6',
  // Footer：marginTop: 12, textAlign: 'right'，Cancel + OK 按钮，gap: 8
}
```

#### Drawer 打开态（CSS 绝对定位模拟，禁止用真实 Antd Drawer）

```javascript
{
  position: 'absolute', top: 0, right: 0, bottom: 0,
  width: 260,
  background: '#fff',
  borderLeft: '1px solid #e8e8e8',
  boxShadow: '-6px 0 16px rgba(0,0,0,0.08)',
  // 遮罩同 Modal，background: 'rgba(0,0,0,0.45)'
}
```

#### DatePicker 日历面板（静态 CSS 模拟，colorPrimary = `#2673dd`）

```javascript
const panelStyle = {
  background: '#fff',
  border: '1px solid #f0f0f0',
  borderRadius: 2,
  boxShadow: '0 6px 16px rgba(0,0,0,0.12)',
  width: 300,
  padding: '8px 12px',
};
// 头部导航按钮
const navBtn = { background: 'none', border: 'none', color: '#595959', fontSize: 12 };
// 头部月/年标题
const headerTitle = { fontSize: 14, fontWeight: 700, color: '#000000e0' };
// 星期行（Su Mo Tu We Th Fr Sa，英文缩写）
const weekdayCell = { fontSize: 12, color: '#8c8c8c', height: 28, textAlign: 'center' };
// 普通日期格
const dateCell = { width: 36, height: 32, fontSize: 14, borderRadius: 2, textAlign: 'center', lineHeight: '32px' };
// 选中日期
const selectedCell = { background: '#2673dd', color: '#fff', fontWeight: 700 };
// 今天（未选中）
const todayCell = { border: '1px solid #2673dd', color: '#000000e0' };
// 非本月日期
const outOfMonthCell = { color: '#bfbfbf' };
// 底部"今天"链接
const footer = { borderTop: '1px solid #f0f0f0', marginTop: 8, fontSize: 13, color: '#2673dd' };
```

> **注意**：历史代码中可能出现 `#1677ff`（AntD 默认蓝），InfraD 正确值是 `#2673dd`，发现时必须替换。

---

## 7. InfraD Token 与组件样式基线

### 为什么自定义 CSS 无法保证样式正确

InfraD 的视觉样式由组件库内部的 Design Token 系统驱动（`colorPrimary: #2673dd`、`borderRadius: 2` 等），这些 token 会通过 CSS 变量、class 名和计算逻辑自动应用到组件的每一个细节（圆角、色阶、阴影、字重、间距……），**任何手写 CSS 都无法精确复现这套 token 驱动的视觉**。

**唯一能保证样式与 InfraD 完全一致的方式**：在 react 代码块里直接使用 `const { Xxx } = Infrad` 真实组件，通过 `react-block-generator` 在 Playground 环境渲染验证。

### CSS 模拟的适用范围与限制

CSS 静态模拟（第6节 B1-B4 规则）**只允许**用于：
- 无法在 Playground 中稳定展示的"打开态"（如 Modal、Drawer 的遮罩+弹窗叠层）
- 多方向集合图（同时展示上下左右四个气泡方向）

**禁止**用 CSS 模拟 InfraD 组件的普通静态形态（如 DatePicker 输入框、Select 下拉框、Button 等），这些直接 `return <组件 />` 即可，用 CSS 手绘必然出现色值、字号、间距偏差。

### Token 速查

**Token 参考文件**：`skills/reference/infrad-tokens-default.json`（产品：Space/Default，Light 模式）

历史代码中常见错误：`#1677ff`（AntD 默认蓝），InfraD 正确值是 `#2673dd`，发现时必须替换。

关键 token：

| Token | 值 |
|---|---|
| colorPrimary | `#2673dd` |
| colorSuccess | `#52c41a` |
| colorError | `#ff4d4f` |
| colorSuccessBg | `#f6ffed` |
| colorErrorBg | `#fff2f0` |
| borderRadius | `2` |
| borderRadiusLG | `2` |
| fontSize | `14` |
| fontSizeSM | `12` |
| fontWeightStrong | `600` |
| controlHeight | `32` |
| lineHeight | `22` |

配图中所有组件必须使用 InfraD 组件，视觉样式应与 InfraD 实际渲染一致。不得使用原生 AntD 样式、自定义 CSS 模拟组件外观，或用色块 / 标签代替真实组件。

自绘容器 `div` 的 `borderRadius` 默认用 `2`（InfraD token）；圆形头像用 `'50%'`。**禁止**使用 4/6/8 等不在 token 内的值。

---

## 8. 演示容器规则

- 能让组件自己说明问题时，不要额外包装饰 div。
- `.demo-mount` 已有统一 padding，组件外不要再加 `padding: 16`。
- 高度优先由内容自然撑开；对比图需要固定同章节 panel 高度时再固定。
- 超宽图需要自包 `maxWidth: '100%'` 和 `overflow: 'auto'`，不要撑破文档预览区域。

禁止四种坏习惯：
1. 给单组件演示套居中装饰盒 `height: 160, display: 'flex', alignItems: 'center', justifyContent: 'center'`
2. 硬编码统一高度 `height: 160/200/260` 让所有 demo 尺寸一致
3. 给浮层组件的静态形态图包 `useRef` + `position: relative` + 小尺寸容器
4. 组件外额外加 `padding: 16`

---

## 9. 数据与内容质量

- 使用真实业务 mock 数据（省市区、商品分类、订单状态等），禁止用 `test` / `foo` / `bar` 等无意义数据。
- 配图内只保留业务 mock 数据文字，**不加任何 UI 图例标注文字**（如「标题：700字重」「主操作，视觉突出」）。
- 演示内链接用 `<a href="#ill" onClick={(e) => e.preventDefault()}>` 防止跳回顶部，不用 `href="#"`。
