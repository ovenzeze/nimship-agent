# Nimship Agent 多Agent协作系统设计文档

## Agent 配置规范
- 所有Agent配置文件位于 `config/` 目录，使用 `.agent.json` 后缀
- 必须包含 name、description、model、tools 等基础字段
- 所有Agent实例必须通过 `agents/base_agent.py` 中的 NimshipAgent 类初始化
- 统一使用 PhiData 提供的 Agent 能力

## 工作流设计
- 工作流配置文件位于 `config/` 目录，使用 `.workflow.json` 后缀
- 必须定义清晰的状态转换和条件
- 每个状态节点需指定负责的Agent
- 支持多Agent协作和串行/并行执行

## 开发目标
1. 构建可配置的多Agent协作框架
2. 提供标准化的Agent定义和工作流管理
3. 充分利用 PhiData 提供的模型和工具能力

## 开发策略
1. 增量开发：每个功能模块独立可测试
2. 分阶段验证：完成一个阶段即进行完整测试
3. 保持简单：避免过早优化和复杂设计
4. 文档先行：确保设计意图和使用方法清晰记录

## 当前状态
处于初始开发阶段，已完成基础配置体系和工作流框架设计，正在实现核心功能模块。

## 下一步计划

基于你的 `junior_developer.workflow.json` 和 phidata 的能力，设计方案如下：

1. 核心架构：
```
配置层 -> 控制层 -> 执行层(phidata)
```

2. 关键组件：
- WorkflowController: 状态管理和转换控制
- StateValidator: 状态验证系统
- PhiWorkflowRunner: 封装 phidata 执行能力
- ConfigLoader: 配置加载和解析

3. 工作流程：
```
加载配置 -> 初始化状态 -> 验证条件 -> 执行Agent -> 更新状态
```

4. 需要关注的点：
- 状态数据持久化：利用 phidata 的 session_state
- 验证结果缓存：避免重复验证
- Agent 执行结果与状态更新的原子性
- 错误处理和状态回滚机制
- 保持与 phidata 的解耦，便于后续升级

5. 验证方案：
从最简单的状态转换开始测试：
```
init -> requirement (仅包含基础字段验证)
```

这样可以快速验证整个架构的可行性，后续再逐步添加复杂的验证逻辑和状态转换。

基于项目结构和设计需求，以下是需要重点关注的文件和文档：

核心文档：
docs/workflow_developer.md - 包含工作流状态定义和开发状态
introduction.mdx 和 streaming.mdx - phidata 工作流的基础概念
session-state.mdx - phidata 的状态管理机制，对接状态存储很重要
关键代码文件：
workflows/workflow_controller.py - 已有的状态枚举和转换定义
workflows/simple_code_assistant.py - 简单工作流示例
config/workflows/junior_developer.workflow.json - 你的工作流配置文件
工具类文件：
utils/model_factory.py - Agent 配置加载已实现的部分
agents/base_agent.py - NimshipAgent 的基础实现
测试相关：
tests/test_workflow.py - 工作流测试框架
phidata 示例参考：
news_report_generator.mdx - 完整的多步骤工作流示例
blog_post_generator - 带缓存的工作流示例
建议按照这个顺序阅读和开发：

先深入理解 phidata 的状态管理 (session-state.mdx)
参考已有的 workflow_controller.py
实现配置加载和验证系统
编写测试用例验证
这样可以确保在开发过程中不会遗漏关键点，同时保持与现有系统的一致性。