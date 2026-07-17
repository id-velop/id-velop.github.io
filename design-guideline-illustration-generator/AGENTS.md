# 项目规则

## 默认目标

本项目是通用组件文档生成 agent，不再默认绑定 IDS / InfraD。

当用户要生成组件文档时，优先使用：

```text
generic-component-doc-agent/SKILL.md
```

默认流程：

1. 收集组件库开发文档入口链接。
2. 读取组件总览和每个组件文档页。
3. 调用 `component_writer_skill/` 生成组件使用规范 Markdown。
4. 调用 `md-illustration-generator-main/skills/md-illustration-generator/` 填充 React 插图。
5. 输出最终 Markdown 到 `source-doc-cn/`。

## React 插图生成器

`react-block-generator/` 和 `md-illustration-generator-main/skills/react-block-generator/` 是可替换生成器模板。

用户接入自己的组件库时，应替换其中的 `SKILL.md` 和 API 参考文件，让它能生成该组件库可运行的 React 示例。

最终文档里的插图必须是可被 Markdown 浏览器直接渲染的 `react` 代码块，而不是普通代码展示。

## 旧 IDS 工作流

`md-illustration-generator-main/ids-doc-illustration/` 是历史 IDS / InfraD 专用流程。

只有当用户明确处理 IDS / InfraD 文档，或明确要求使用旧 checker / Playground 流程时，才使用这些 skill。

## 翻译规范

用户如果要翻译文档，默认从：

```text
source-doc-cn/
```

翻译到：

```text
source-doc-en/
```
