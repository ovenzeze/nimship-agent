# Nimship Agent

Nimship Agent 是一个灵活的、可配置的 AI agent 框架，基于 phidata 库构建。

PhiiData 是一个用于构建 AI 应用程序的库，它提供了一组工具和功能，使开发人员能够轻松地构建、部署和管理 AI 应用程序。

文档导航文件: [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)

## 主要特性

- 使用 JSON 配置文件定义agents和workflow，更易于管理和维护
- 支持多种语言模型，包括 OpenAI、HuggingFace 和 Anthropic（PhiiData能力）
- 支持多种工具，包括搜索引擎、计算器和日期工具（PhiiData能力）
- 可扩展的工具集成，允许用户添加自己的工具
- 美观的UI界面（PhiiData能力）
- 支持无头模式运行, WebUI 运行，CLI交互式运行（PhiiData能力）

## 安装

1. 克隆仓库：
   ```
   git clone https://github.com/your-username/nimship-agent.git
   cd nimship-agent
   ```

2. 创建并激活虚拟环境：
   ```
   python3.9 -m venv venv
   source venv/bin/activate
   ```

3. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

## 项目结构

```
nimship-agent/
├── agents/
├── config/
├── docs/
│   └── DOCUMENTATION_GUIDE.md
├── scripts/
│   └── run_agent.py
├── tests/
├── tools/
│   └── litellm/
├── utils/
├── workflows/
├── .env
├── .gitignore
├── DEV_GUIDE.md
├── main.py
├── playground.py
├── README.md
└── requirements.txt
```

## 使用方法

1. 创建或编辑 agent 配置文件（例如 `config/example_agent.config.json`）

2. 运行 agent：
   ```
   python scripts/run_agent.py config/example_agent.config.json "Your prompt here"
   ```

## 配置文件格式

agent 配置文件应包含以下字段：

- `name`: agent 的名称
- `description`: agent 的描述
- `model`: 包含 `type` 和 `name` 的对象，指定要使用的语言模型
- `tools`: 要使用的工具列表

示例：

```json
{
 "name": "example_agent",
 "description": "An example agent for demonstration",
 "model": {
     "type": "openai",
     "name": "gpt-3.5-turbo"
 },
 "tools": ["search", "calculator"]
}
```

## 开发指南

有关开发和贡献的详细信息，请参阅项目根目录中的 `DEV_GUIDE.md` 文件。

## 文档

完整的文档可以在 `docs` 目录中找到。主要的文档导航文件是 [docs/DOCUMENTATION_GUIDE.md](docs/DOCUMENTATION_GUIDE.md)。
