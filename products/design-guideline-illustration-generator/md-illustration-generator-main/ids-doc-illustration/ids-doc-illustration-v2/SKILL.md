---
name: ids-doc-illustration-v2
description: 生成、修复并校验 IDS / Infra 组件 Markdown 文档插图。适用于用户要求新增、重做、修复、预览或完善组件文档插图的场景，尤其是包含 `<!-- 附图占位 ... -->`、`1.2.x` 类型说明、`1.3.x` 推荐 / 不推荐案例、InfraD / AntD 视觉参考或 Playground React demo block 的 `.md` 文件。
---

# IDS 文档插图 V2

## 角色

这是 IDS / Infra 组件文档插图工作的主 skill。

本 skill 负责生成和修复 Markdown 插图；文档是否合规、哪些问题需要修，交给独立的 `ids-doc-illustration-checker` skill 判断。

## 硬性要求

- **禁止在完整读完 `references/illustration-standards.md` 之前修改任何 Markdown 文件或生成任何代码。** 即使上下文中已有 checker 输出或已知问题清单，也必须先读完这个文件再动笔，不得跳过。
- **用户说「重新生成 / 重做 / 重新修图」时，必须先逐字读取目标小节的正文内容，再决定画什么。** 生成依据优先级：文章正文 > 用户补充要求 > 既有旧图或参考图 > 通用组件模板。旧图只作为视觉状态参考，不能替代文章含义；旧图和正文冲突时，以正文为准。
- 除非用户明确要求推送 skill，否则不要推送 skill 改动。
- 除非用户明确要求推送文档，否则不要推送文档改动。
- 除非用户要求预览或视觉检查，否则不要生成 HTML preview。
- 不要为 `1.1 组件构成` 创建插图。
- 不要删除用户提供的远程图片或既有内容，除非用户明确要求。
- 如果用户明确要求保留 1.1 里的既有附图，或文章已有远程/Markdown 图片必须暂时保留，附图上一行和下一行都必须是独立 `<br>`。
- 不要把 blockquote 里的占位符当作特殊指令；只有在编辑该占位符时，才规范化或移除前面的 `>`。
- 生成的插图样式必须对齐 InfraD / AntD 真实组件基线；手写展示可以接受，但不得自造脱离组件体系的颜色、间距、圆角、阴影、状态样式或页面结构。
- 维护本 skill 时，把问题抽象成同类规则，不写某次事故、某个组件或某张截图的特殊修补。

## 标准流程

1. **阅读插图标准**

阅读 `references/illustration-standards.md`，确认组件类型、场景图、浮层、对比图、代码格式、预览和推送约束后再动笔。

2. **先使用 checker skill**

先使用独立的 `ids-doc-illustration-checker` skill 检查目标文档，并以它的输出作为问题清单。不要在本 skill 中直接调用 checker 脚本；只有当 checker skill 不可用时，才按 `references/workflow.md` 的 fallback 方式处理，并说明自动 checker 缺失。

3. **只规划失败 section**

以 checker 输出作为编辑清单。避免重写无关 section。

4. **生成前查网站，确认可用类型**

在写任何 `1.2.x` 内容之前，先用 WebFetch 拉取：

```
https://infrad.shopee.io/components/<slug>
```

只看 **Development** tab。从中找出该组件真实存在的 `type` / `variant` 或等价 prop 值列表，作为 1.2.x 内容的唯一依据。

规则：

- **只写网站上有的类型**：网站没有的 variant / style 一律不写，即使设计稿或历史文档提到过。
- **类型和尺寸分开**：`1.2.x` 类型小节只写视觉类型，不混入 size 相关内容（如"小尺寸"、`size="small"`），尺寸单独成节。
- **语言通俗易懂**：每种类型的描述用普通人能看懂的语言，说清楚它长什么样、适合什么场景，不堆砌技术 prop 名或 API 术语。

5. **生成 React block**

需要组件 API 时，优先使用已安装的 `react-block-generator` skill；在本仓库中对应路径为 `../../skills/react-block-generator/COMPONENTS_API.md`。

每个 Markdown demo block 应使用以下结构：

```jsx
function App() {
  const { Button } = Infrad;
  return <Button>Example</Button>;
}
```

5. **保存 Playground 链接**

先插入 `agent_code_id=TBD` 链接，然后运行：

```bash
node scripts/save_playground_blocks.js <target.md>
```

6. **再次校验**

再次使用 `ids-doc-illustration-checker` skill 校验。持续修复阻断问题，直到 checker 通过。

7. **仅在用户要求时预览**

如果用户要求预览：

```bash
python3 scripts/render_preview.py <target.md>
```

只有当用户要求在浏览器中查看时，才打开生成的 `*-preview.html`。

8. **结束时汇报状态并主动发 Playground 链接**

汇报：

- 改动了哪些文件。
- checker 结果。
- 如果生成了 preview，给出 preview URL 或文件。
- 哪些事情没有完成。

**必须通过 SeaTalk（`handling-seatalk-channel` skill）主动把本次生成的所有 Playground 链接发给用户**，格式示例：

```
X.Y.Z 示例图（是什么）：https://infrad.shopee.io/playground/?agent_code_id=XXXX
X.Y.Z 场景图（典型场景）：https://infrad.shopee.io/playground/?agent_code_id=YYYY
```

即使 code_id 是既有值（非新建），也必须发。用户需要点开链接做视觉确认，不能省略这一步。

## 必读参考

- `references/workflow.md`：执行顺序和职责边界。
- `references/illustration-standards.md`：插图标准与所有规则（含参考基线策略、启动前检查表）。
- `references/preview-policy.md`：preview 与临时文件规则。

只加载当前任务需要的参考文件。

## 与其他 skill 的边界

- 使用 `ids-doc-illustration-checker` 做只读检查。
- 使用本 skill 做编辑和生成。
- 只有生成单个独立 React block 时，才使用 `react-block-generator`。
