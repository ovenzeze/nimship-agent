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