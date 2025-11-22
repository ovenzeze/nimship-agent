# 贡献指南

感谢你对 Nimship Agent 项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/ovenzeze/nimship-agent/issues) 中是否已有相关问题
2. 如果没有，请创建新的 Issue，包含：
   - 清晰的问题描述
   - 复现步骤（如果是 bug）
   - 预期行为和实际行为
   - 环境信息（Python 版本、操作系统等）

### 提交代码

#### 1. Fork 和克隆仓库

```bash
# Fork 仓库到你的 GitHub 账号
# 然后克隆你的 fork
git clone https://github.com/YOUR_USERNAME/nimship-agent.git
cd nimship-agent

# 添加上游仓库
git remote add upstream https://github.com/ovenzeze/nimship-agent.git
```

#### 2. 创建分支

```bash
# 从 main 分支创建新分支
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name

# 或者修复 bug
git checkout -b fix/your-bug-fix
```

**分支命名规范：**
- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关
- `chore/` - 构建/工具相关

#### 3. 开发环境设置

```bash
# 创建虚拟环境
python3.9 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖（如果有）
pip install pytest pytest-cov black flake8 mypy
```

#### 4. 编写代码

- 遵循项目的代码风格
- 添加必要的注释和文档字符串
- 确保代码通过所有测试
- 如果是新功能，请添加相应的测试用例

**代码风格：**
- 使用 Python 3.9+ 特性
- 遵循 PEP 8 代码规范
- 使用有意义的变量和函数名
- 添加类型提示（Type Hints）

#### 5. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_workflow_controller.py

# 生成覆盖率报告
pytest --cov=. --cov-report=html tests/
```

#### 6. 提交更改

```bash
# 查看更改
git status
git diff

# 添加更改
git add .

# 提交（使用清晰的提交信息）
git commit -m "feat: add new feature description"
```

**提交信息规范：**
- 使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式
- 类型：`feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- 格式：`<type>: <description>`

示例：
- `feat: add support for new model provider`
- `fix: resolve workflow state transition issue`
- `docs: update installation guide`
- `test: add tests for file manager tool`

#### 7. 推送和创建 Pull Request

```bash
# 推送分支到你的 fork
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request：

1. 访问你的 fork 仓库
2. 点击 "New Pull Request"
3. 选择你的分支
4. 填写 PR 描述，包括：
   - 更改的目的和背景
   - 实现细节
   - 测试情况
   - 相关 Issue（如果有）

### PR 审查流程

1. **自动检查**：CI/CD 会自动运行测试和代码检查
2. **代码审查**：维护者会审查你的代码
3. **反馈和修改**：根据反馈进行必要的修改
4. **合并**：审查通过后，代码会被合并到主分支

## 开发指南

### 项目结构

- `agents/` - Agent 实现
- `config/` - 配置文件
- `docs/` - 文档
- `tests/` - 测试用例
- `tools/` - 工具实现
- `utils/` - 工具函数
- `workflows/` - 工作流实现

### 添加新功能

1. **添加新的 Agent**
   - 在 `config/agents/` 创建配置文件
   - 参考现有 agent 配置格式

2. **添加新工具**
   - 在 `tools/` 实现工具类
   - 在 `config/tools/` 创建配置文件
   - 添加相应的测试

3. **添加新工作流**
   - 在 `config/workflows/` 创建工作流配置
   - 参考现有工作流格式

### 测试要求

- 新功能必须包含测试用例
- 测试覆盖率不应降低
- 确保所有测试通过

### 文档要求

- 更新相关文档（README、DEV_GUIDE 等）
- 添加代码注释和文档字符串
- 更新 CHANGELOG（如果有）

## 行为准则

### 我们的承诺

为了营造开放和友好的环境，我们承诺：

- 尊重所有贡献者
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

### 不可接受的行为

- 使用性化的语言或图像
- 人身攻击、侮辱性/贬损性评论
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息
- 其他在专业环境中不适当的行为

## 获取帮助

如果你在贡献过程中遇到问题：

1. 查看 [文档](README.md) 和 [开发指南](DEV_GUIDE.md)
2. 搜索已有的 [Issues](https://github.com/ovenzeze/nimship-agent/issues)
3. 创建新的 Issue 描述你的问题

## 许可证

通过贡献，你同意你的贡献将在与项目相同的 [MIT 许可证](LICENSE) 下发布。

---

再次感谢你对 Nimship Agent 项目的贡献！🎉
