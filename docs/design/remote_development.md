# 远程开发设计文档

## 1. 系统架构

### 1.1 核心组件
- **FileManager Tools**: 统一的文件操作工具，自动适配本地/远程环境
- **Git Tools**: 版本控制工具集
- **DevOps Tools**: 专属的运维管理工具集

### 1.2 远程开发环境
- 通过 VSCode SSH Remote 连接到远程开发机
- 使用 .env 文件存储远程连接凭据
- 远程机器已预配置:
  - 项目代码库
  - Git配置和GitHub连接
  - 开发环境依赖

### 1.3 环境配置
环境变量(.env):

NIMSHIP_REMOTE_HOSTNAME=your_remote_host
NIMSHIP_REMOTE_USER=your_username
NIMSHIP_REMOTE_PORT=22

#### FileManager Tools (所有Agent可用)

# 抽象文件操作，自动适配本地/远程环境
class FileManagerTools(Tool):
    def create_file(self, path: str, content: str) -> FileOperationResult
    def read_file(self, path: str) -> FileOperationResult
    def update_file(self, path: str, content: str) -> FileOperationResult
    def delete_file(self, path: str) -> FileOperationResult
    def search_files(self, pattern: str) -> List[FileMatch]


#### Git Tools (所有Agent可用)

class GitTools(Tool):
    def create_branch(self, name: str) -> GitOperationResult
    def commit_changes(self, message: str) -> GitOperationResult
    def switch_branch(self, name: str) -> GitOperationResult
    def view_history(self, path: str) -> List[GitCommit]


#### DevOps Tools (仅DevOps Agent可用)

class DevOpsTools(Tool):
    def push_changes(self, remote: str, branch: str) -> DevOpsResult
    def create_pull_request(self, source: str, target: str) -> DevOpsResult
    def deploy_environment(self, env: str) -> DevOpsResult
    def manage_remote_connection(self) -> DevOpsResult


### 1.3 工具实现层
- LocalFileProvider: 本地文件系统操作
- VSCodeRemoteProvider: VS Code Server远程操作
- ProviderSelector: 自动选择合适的Provider

## 2. 使用场景

### 2.1 开发者Agent工作流
- 使用 FileManager Tools 进行代码开发
- 使用 Git Tools 管理版本
- 完全无感知底层是本地还是远程环境

### 2.2 DevOps Agent工作流
- 使用专属 DevOps Tools 处理运维任务
- 控制代码推送和发布流程
- 管理远程开发环境

## 3. 实现策略

### 3.1 Tools注册机制
- FileManager Tools 和 Git Tools 注册为通用工具
- DevOps Tools 注册为专属工具
- 工具权限自动校验

### 3.2 Provider机制
- Provider接口标准化
- 运行时自动选择Provider
- 操作结果统一封装

## 4. 错误处理
- 标准化的错误类型
- 统一的结果返回格式
- 完整的日志记录

## 5. 实现细节

### 5.1 工具实现

#### FileManagerTools
- 实现了 create_file, read_file, update_file, delete_file, search_files 等方法
- 支持本地文件系统操作
- 为远程操作预留了扩展性

#### GitTools
- 实现了 create_branch, commit_changes, switch_branch, view_history 等方法
- 使用 subprocess 模块执行 Git 命令

#### DevOpsTools
- 实现了 push_changes, create_pull_request, deploy_environment, manage_remote_connection 等方法
- 部分方法（如 create_pull_request, deploy_environment, manage_remote_connection）目前为占位实现，需要进一步开发

### 5.2 配置文件更新
- 更新了 config/tools/file_manager.tool.json 和 config/tools/devops.tool.json
- 添加了新的功能到工具的 capabilities 列表中

### 5.3 Agent 集成
- 在 agents/base_agent.py 中集成了新的工具
- 实现了动态工具加载机制

### 5.4 测试
- 新增 tests/test_remote_development.py 文件
- 包含对 FileManagerTools 和 DevOpsTools 的基本功能测试

## 6. 核心文件

文档：
- docs/workflow_developer.md - 包含工作流状态定义和开发状态
- docs/design/remote_development.md - 远程开发设计文档（本文档）

配置相关：
- config/system.config.json - 系统配置文件，定义工具注册和路径
- config/tools/*.tool.json - 工具配置文件
- config/agents/*.agent.json - Agent配置文件

代码实现：
- tools/file_manager.py - 文件管理工具实现
- tools/git_tools.py - Git 操作工具实现
- tools/devops.py - DevOps 工具实现
- agents/base_agent.py - Agent基类和工具集成
- utils/model_factory.py - 配置加载工具

测试相关：
- tests/test_workflow_controller.py - 工作流测试框架
- tests/test_integration.py - 集成测试示例
- tests/test_remote_development.py - 远程开发功能测试

参考示例：
- docs/phidata/workflows/news-report-generator.mdx - 完整工作流示例
- docs/phidata/workflows/session-state.mdx - 状态管理机制

## 7. 后续工作

1. 完善 VSCodeRemoteProvider 的实现
2. 实现 DevOpsTools 中的占位方法
3. 增加更多的单元测试和集成测试
4. 优化错误处理和日志记录
5. 考虑添加更多的远程开发相关功能，如远程调试支持
