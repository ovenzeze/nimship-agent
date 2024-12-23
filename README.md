# Nimship Agent

Nimship Agent 是一个基于 phidata 构建的多 Agent 协作开发框架，支持可配置的工作流和智能工具链。

## 主要特性

### 多Agent协作系统
- 预配置的专业角色：产品经理、技术负责人、高级工程师、测试工程师
- 基于工作流的协作机制
- 清晰的角色职责和任务分配

### 灵活的配置系统
- JSON 配置文件定义 agents 和 workflows
- 标准化的配置验证机制
- 支持多种语言模型（通过 phidata）Bedrock (Claude)

### 工具集成
- 核心工具：
   - FileManager：统一的文件操作接口
   - DevOps：环境管理和部署操作
   - DuckDuckGo：网络搜索能力
- 可扩展的工具系统
- 工具配置与实现分离

### 工作流管理
- 状态驱动的工作流引擎
- 配置化的状态转换
- 完整的验证机制
- 支持串行和并行执行

## 项目结构

```directory
nimship-agent/
├── agents/                 # Agent 实现
│   └── base_agent.py      # Agent 基类
├── config/
│   ├── agents/           # Agent 配置
│   ├── workflows/        # 工作流配置
│   └── tools/           # 工具配置
│   └── system.config.json  # 系统配置
├── docs/                 # 文档
│   └── workflow_developer.md
├── tests/               # 测试用例
│   ├── integration/    # 集成测试
│   └── test_workflow.py
├── tools/              # 工具实现
├── utils/              # 工具函数
└── workflows/          # 工作流实现
└── main.py               # 主程序入口
└── README.md             # 项目说明
└── requirements.txt      # 依赖包
```


## 安装和配置

1. 环境要求：
   - Python 3.9+
   - 虚拟环境管理工具

2. 安装步骤：
bash
# 创建虚拟环境
python3.9 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt


3. 环境配置：
bash
# 复制环境配置模板
cp .env.example .env

# 编辑 .env 文件，配置必要的环境变量：
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_REGION
- PHI_API_KEY


## 使用方法

### 1. CLI 模式
bash
python main.py


### 2. Web UI 模式
bash
python main.py --mode ui


## 开发指南

### Agent 配置规范
- 配置文件位置：`config/` 目录
- 文件后缀：`.agent.json`
- 必需字段：name、description、model、tools

### 工作流配置规范
- 配置文件位置：`config/workflows/`
- 文件后缀：`.workflow.json`
- 必需定义：状态转换和条件

### 测试规范
- 单元测试：`tests/`
- 集成测试：`tests/integration/`
- 运行测试：`pytest tests/`

## 文档

- 工作流开发指南：`docs/workflow_developer.md`
- Agent 设计文档：`docs/AGENT_DESIGN.md`
- 测试架构：`tests/test_design.md`

## 开发状态

当前处于初始开发阶段：
- ✅ 完成基础配置体系
- ✅ 完成工作流框架设计
- 🚧 实现核心功能模块
- 🚧 完善测试覆盖

## 注意事项

1. 远程开发环境配置：
   - 需要配置 VSCode Server
   - 需要设置 SSH 密钥认证
   - 需要配置 Git 和 GitHub

2. 依赖说明：
   - paramiko：用于远程操作
   - requests：用于 API 调用
   - pytest：用于测试
   - python-dotenv：环境变量管理

## 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

[许可证类型]
