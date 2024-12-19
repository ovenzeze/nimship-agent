# phiData 文档导航


## 1. 介绍
- 位置：`introduction.mdx`
- 内容：phiData框架概述、主要特性、使用场景

## 2. 代理（Agents）
- 位置：`agents/`
- 描述：自主程序，使用语言模型完成任务
- 主要文档：
  - `introduction.mdx`：代理概述
  - `knowledge.mdx`：知识集成方法
  - `memory.mdx`：代理记忆功能
  - `prompts.mdx`：提示工程技巧
  - `reasoning.mdx`：代理推理能力
  - `storage.mdx`：数据存储机制
  - `structured-output.mdx`：结构化输出处理
  - `teams.mdx`：多代理协作策略
  - `tools.mdx`：工具集成指南

## 3. 模型
- 位置：`models/`
- 描述：支持的各种语言模型及其配置
- 包括：OpenAI, Azure, Google, Anthropic, AWS Bedrock, Cohere, Hugging Face等

## 4. 工具
- 位置：`tools/`
- 描述：增强代理能力的各种工具和集成
- 主要工具类别：
  - 数据处理：CSV, Pandas, DuckDB
  - 搜索：Google Search, DuckDuckGo, Wikipedia
  - API集成：GitHub, Jira, Slack, Twitter, Zoom
  - 文件操作、自然语言处理、金融数据等

## 5. 工作流
- 位置：`workflows/`
- 描述：构建复杂任务流程的指南和示例
- 关键文档：
  - `introduction.mdx`：工作流概述
  - `news-report-generator.mdx`：实际应用示例
  - `session-state.mdx`：状态管理指南
  - `streaming.mdx`：流式处理技术

## 6. 嵌入器（Embedder）
- 位置：`embedder/`
- 描述：文本嵌入技术和相关功能

## 7. 向量数据库
- 位置：`vectordb/`
- 描述：向量存储和检索解决方案

## 8. 存储
- 位置：`storage/`
- 描述：数据持久化和管理策略

## 9. 监控
- 位置：`monitoring.mdx`
- 描述：系统性能和行为监控指南

## 10. 示例和教程
- 位置：`examples/`, `more-examples.mdx`, `videos.mdx`
- 描述：实际应用案例、代码示例和视频教程

## 11. 参考文档
- 位置：`reference/`
- 描述：API参考和技术规格

## 12. 常见问题（FAQ）
- 位置：`faq/`
- 描述：常见问题解答和故障排除指南

## 13. 获取帮助
- 位置：`getting-help.mdx`
- 描述：社区支持和技术援助资源

## 14. 变更日志
- 位置：`changelog/`
- 描述：版本更新历史和新特性说明

## 15. 知识库
- 位置：`knowledge/`
- 描述：知识管理和集成指南
- 主要文档：
  - `arxiv.mdx`：arXiv论文集成
  - `combined.mdx`：组合知识源
  - `csv-url.mdx`：CSV数据集成

## 16. 操作指南
- 位置：`how-to/`
- 描述：具体任务的步骤指南
- 主要文档：
  - `install.mdx`：安装指南

## 17. 模板
- 位置：`templates/`
- 描述：各种预设模板和配置
- 包括：
  - `how-to/`：操作指南模板
    - `database-tables.mdx`：数据库表格模板

## 快速入门
要快速开始使用phiData，建议按以下顺序阅读文档：

1. `introduction.mdx`：了解框架基础
2. `agents/introduction.mdx`：学习代理的核心概念
3. `models/introduction.mdx`：选择适合您需求的语言模型
4. `tools/introduction.mdx`：探索可用的工具和集成
5. `workflows/introduction.mdx`：学习如何构建复杂的任务流程
6. `how-to/install.mdx`：了解如何安装和设置phiData

有关具体的应用示例，请参考 `examples/` 目录和 `more-examples.mdx`。

如需进一步帮助，请查阅 `faq/` 或 `getting-help.mdx`。

对于高级用户：
- 探索 `knowledge/` 目录以了解如何集成外部知识源
- 查看 `templates/` 目录以获取各种预设配置和模板
