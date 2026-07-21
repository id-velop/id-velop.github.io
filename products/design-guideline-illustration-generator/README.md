# 通用组件文档生成 Agent

这个项目可以把任意 React 组件库的开发文档，转换成组件使用规范 Markdown，并自动补上可直接渲染的 React 插图。

它最初是给 IDS / InfraD 组件库做文档和插图生成的，现在已经改成通用流程：用户 clone 项目后，只需要替换自己的 React 代码生成器，再让 agent 调用主 skill，就可以为自己的组件库批量生成文档。

## 主 Skill

使用：

```text
generic-component-doc-agent/SKILL.md
```

本地配置 UI 可以由 agent 启动，也可以手动在终端运行：

```bash
python3 generic-component-doc-agent/scripts/collect_request.py
```

配置 UI 支持填写：

- 组件文档入口链接
- 读取模式和组件过滤范围
- React 代码生成器路径
- Markdown 输出目录
- writer 和 illustration skill 路径
- 预览命令和校验命令
- 文档语言

提交后会写入：

```text
.generic-component-doc-agent/request.json
```

## 完整流程

1. 用户提供组件文档链接，例如 `https://ant.design/components/overview-cn/`。
2. Agent 读取组件总览和每个组件的开发文档。
3. Agent 调用 `component_writer_skill/`，参考固定格式生成组件使用规范 Markdown。
4. 用户用自己的组件库 React 代码生成器替换 `react-block-generator/` 或 `md-illustration-generator-main/skills/react-block-generator/`。
5. Agent 调用 `md-illustration-generator-main/skills/md-illustration-generator/`，把文档里的插图占位替换成可渲染 React 插图。
6. 最终 Markdown 文件保存到 `source-doc-cn/`。

## 重要目录

| 路径 | 用途 |
| --- | --- |
| `generic-component-doc-agent/` | 顶层编排 skill，负责串起完整流程。 |
| `component_writer_skill/` | 通用组件文档写作 skill。 |
| `md-illustration-generator-main/skills/md-illustration-generator/` | 通用 Markdown 插图生成流程。 |
| `react-block-generator/` | 默认可替换 React 代码生成器模板。 |
| `md-illustration-generator-main/skills/react-block-generator/` | 插图流程默认调用的 React 代码生成器路径，接入新组件库时应替换。 |
| `source-doc-cn/` | 默认中文 Markdown 输出目录。 |
| `source-doc-en/` | 可选英文翻译输出目录。 |

## React 插图格式

最终文档里的插图应该是可被浏览器或 agent 文档视图直接渲染的 `react` 代码块：

````markdown
```react
function App() {
  return <YourComponent />;
}
```
````

不要把插图写成普通的 `js`、`jsx`、`tsx` 或 `markdown` 代码展示块，否则用户浏览 Markdown 时看到的只会是一段代码，而不是可交互插图。

## 旧 IDS 内容

`md-illustration-generator-main/ids-doc-illustration/` 目录和现有 API 示例是历史 IDS / InfraD 工作流的保留内容。

只有在继续处理 IDS / InfraD 文档，或需要参考旧实现时，才使用这些内容。

---

# Generic Component Documentation Agent

This project turns a component library's developer documentation into component usage guides with renderable React illustrations.

It was originally built for an IDS/InfraD workflow. The default workflow is now generic: users can clone this repository, replace the React block generator with one for their component library, and run a single skill to generate Markdown docs.

## Main Skill

Use:

```text
generic-component-doc-agent/SKILL.md
```

The local configuration UI can be launched by the agent, or from a terminal:

```bash
python3 generic-component-doc-agent/scripts/collect_request.py
```

The UI configures:

- component documentation URL
- crawl mode and component filter
- React block generator path
- output directory
- writer and illustration skill paths
- preview and validation commands
- document language

The form writes:

```text
.generic-component-doc-agent/request.json
```

## End-to-End Flow

1. User provides a component docs URL, for example `https://ant.design/components/overview-cn/`.
2. The agent discovers component pages and reads the developer docs.
3. The agent calls `component_writer_skill/` to write component guide Markdown using the reference structure.
4. The user replaces `react-block-generator/` or `md-illustration-generator-main/skills/react-block-generator/` with a generator for their component library.
5. The agent calls `md-illustration-generator-main/skills/md-illustration-generator/` to fill illustration placeholders with renderable React blocks.
6. Final Markdown files are saved to `source-doc-cn/`.

## Important Paths

| Path | Purpose |
| --- | --- |
| `generic-component-doc-agent/` | Top-level orchestration skill. |
| `component_writer_skill/` | Generic component guide writer. |
| `md-illustration-generator-main/skills/md-illustration-generator/` | Generic Markdown illustration workflow. |
| `react-block-generator/` | Default replaceable React block generator template. |
| `md-illustration-generator-main/skills/react-block-generator/` | Generator path used by the illustration package; replace for your library. |
| `source-doc-cn/` | Default final Markdown output directory. |
| `source-doc-en/` | Optional translated Markdown output directory. |

## React Illustration Contract

Final docs should contain renderable React fences:

````markdown
```react
function App() {
  return <YourComponent />;
}
```
````

Do not leave illustrations as inert code examples when the user's Markdown viewer expects live React blocks.

## Legacy IDS Content

The `md-illustration-generator-main/ids-doc-illustration/` folder and existing API examples are retained as legacy IDS/InfraD references. Use them only for IDS/InfraD docs or as examples when creating a new generator.
