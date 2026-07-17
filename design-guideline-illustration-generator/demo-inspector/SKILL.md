---
name: demo-inspector
description: >-
  Understand and describe an existing Infra Design playground demo from a demo
  id. Use when the user provides a demo id, agent_code_id, playground URL, or
  agent-code/read URL and asks what the demo shows, what interaction/content it
  contains, or wants to reuse, modify, or insert the demo. Load the stored React
  code internally, explain the demo by default, and only output source code when
  explicitly requested.
---

# Demo Inspector

根据用户提供的 demo id 或 URL，从 InfraD agent-code read API 获取已保存的 React Block 代码，并基于源码判断这个 demo 展示的内容、组件结构和交互意图。

默认不要把源码直接返回给用户。源码是分析材料，用户通常想知道“这个 demo 是什么”。

## 可识别输入

- 纯数字 demo id：`2984`
- Playground URL：`https://infrad.shopee.io/playground/?agent_code_id=2984`
- 读取接口 URL：`https://infrad.shopee.io/apis/faas/agent-code/read?id=2984`

## 工作流程

1. 从用户消息中提取 id：
   - 优先读取 URL query 中的 `id`
   - 其次读取 URL query 中的 `agent_code_id`
   - 如果没有 URL，从消息中提取唯一的数字 id
2. 请求读取接口：

   ```bash
   SKILL_DIR="<当前 demo-inspector/SKILL.md 所在目录>"
   python3 "$SKILL_DIR/scripts/load_demo_code.py" '<demo-id-or-url>' --format json
   ```

3. 校验结果：
   - HTTP 请求成功
   - 响应为 JSON
   - JSON 中包含字符串字段 `code`
4. 阅读 `code` 字段，提炼 demo 信息：
   - 展示场景：这个 demo 想表达什么业务或设计场景
   - 组件结构：使用了哪些主要组件，以及它们如何组合
   - 可见内容：关键文案、字段、表格列、mock 数据、状态标签等
   - 交互行为：按钮点击、弹窗、表单输入、开关、选择、筛选、状态变化等
   - 适用位置：如果用户要写文档，判断它适合放在哪类章节或说明下面
5. 根据用户意图输出或继续处理：
   - 只给 demo id 或问“这是什么”：用自然语言描述 demo 内容，不输出源码
   - 明确要求“源码/代码/复制代码”：返回 ` ```react ` 代码块，可附带 id、created_at、updated_at
   - 要写入文档：将获取到的代码交给 `gitlab-docs-manager`，插入为 ` ```react ` 代码块
   - 要基于现有 demo 修改：以获取到的代码作为源代码修改；如果需要新预览，再调用 `react-block-generator` 的保存接口生成新的 playground 链接

## 默认输出风格

用简短中文说明即可，优先回答 demo 内容：

```text
这个 demo 展示的是一个「数据同步任务」配置表单。
它用 Card 承载一个纵向小尺寸表单，包含工作流名称、执行周期、访问策略和超时重试等字段；中间用 Divider 分成「网络配置」和「高级选项」两段。主要交互是用户可以编辑输入框内容，并切换「超时重试」开关。
```

如果用户需要更结构化的信息，可以拆成：

- 场景
- 主要组件
- 展示内容
- 交互行为

## 脚本用法

先定位当前加载的 `demo-inspector/SKILL.md` 所在目录，将它作为 `SKILL_DIR`。不要使用固定的本机绝对路径。

```bash
# 输出完整 JSON，便于 agent 读取 code 后分析 demo 内容
python3 "$SKILL_DIR/scripts/load_demo_code.py" 2984 --format json

# 只输出代码，便于写入文件或二次处理；不要作为默认用户输出
python3 "$SKILL_DIR/scripts/load_demo_code.py" 2984 --format code

# 输出 markdown react 代码块，仅在用户明确要源码时使用
python3 "$SKILL_DIR/scripts/load_demo_code.py" 'https://infrad.shopee.io/playground/?agent_code_id=2984' --format markdown
```

## 注意事项

- 不要凭空补写或猜测不存在的 demo 代码；接口失败时直接说明失败原因。
- 原始代码可能依赖 `React`、`Infrad`、`Icons`、`InfradPro`、`SpaceBiz` 等预注入 scope 变量，不要自动添加 import/export。
- 用户只要求理解 demo 时，不要重新保存生成新的 demo id，也不要输出源码。
