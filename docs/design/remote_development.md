# 远程开发设计文档

## 1. 系统架构

### 1.1 核心组件
- **文件操作工具**：提供基础的文件操作能力
- **DevOps Agent**：负责环境配置和管理
- **VS Code Server**：提供远程开发能力
- **远程服务器**：运行实际项目的服务器

### 1.2 职责划分

#### 文件操作工具
- 提供统一的文件操作接口
- 支持 Git 感知的文件更新
- 供所有 Agent 直接调用
- 处理文件的增删改查
- 支持代码补丁应用

#### DevOps Agent
- 项目环境初始化
- SSH 连接管理
- VS Code Server 集成
- Git 仓库管理
- 确保文件同步

## 2. 环境配置

### 2.1 环境变量
```bash
# 基础配置
NIMSHIP_SECRETS_PATH=./secrets
NIMSHIP_DEFAULT_HOST=replit

# 远程连接配置
NIMSHIP_REMOTE_HOSTNAME=xxx.replit.dev
NIMSHIP_REMOTE_USER=xxx
NIMSHIP_REMOTE_PORT=22
```

### 2.2 SSH 配置
```
Host replit
    HostName xxx.replit.dev
    User xxx
    Port 22
    IdentityFile ~/.ssh/replit
    ForwardAgent yes
    AddKeysToAgent yes
    StrictHostKeyChecking accept-new
```

## 3. 工作流程

### 3.1 初始化流程
1. DevOps Agent 验证环境变量配置
2. 检查 SSH 密钥和配置
3. 验证 VS Code Server 连接
4. 确保 Git 仓库正确配置
5. 验证文件操作工具可用性

### 3.2 运行时流程
1. Agent 通过文件操作工具执行更改
2. 更改通过 VS Code Server API 执行
3. Git 历史自动记录变更
4. 用户可通过 VS Code 远程连接查看变更

## 4. 接口设计

### 4.1 文件管理接口
```python
class FileManager:
    # 文件操作
    def create_file(self, path: str, content: str)
    def update_file(self, path: str, changes: Dict)
    def delete_file(self, path: str)
    def read_file(self, path: str) -> str
    
    # 目录操作
    def create_directory(self, path: str)
    def delete_directory(self, path: str)
    def list_directory(self, path: str) -> List[str]
    def move_directory(self, src: str, dst: str)
    
    # 搜索能力
    def search_files(self, 
                    pattern: str,
                    file_type: Optional[str] = None,
                    include_content: bool = False,
                    case_sensitive: bool = False) -> List[FileMatch]
    
    def search_in_files(self,
                       content_pattern: str,
                       file_pattern: Optional[str] = None,
                       context_lines: int = 0) -> List[ContentMatch]
    
    # Git 相关
    def get_file_history(self, path: str) -> List[GitCommit]
    def restore_file(self, path: str, commit_id: str)
    def restore_directory(self, path: str, commit_id: str)

### 4.2 代码补丁接口
```python
class CodePatch:
    """代码更新补丁"""
    target_type: str  # 'function', 'class', 'block'
    target_name: Optional[str] = None  # 函数名/类名
    before_context: Optional[str] = None  # 更改位置之前的代码
    after_context: Optional[str] = None   # 更改位置之后的代码
    change_type: str  # 'modify', 'insert', 'delete' 
    new_content: Optional[str] = None
```

## 5. VS Code Server 集成

### 5.1 集成方式
- 利用已配置的 VS Code Server
- 通过 SSH 配置访问远程环境
- 复用 VS Code 的文件操作能力
- 支持实时预览和编辑

### 5.2 性能优化
- VS Code Server 提供的缓存机制
- 增量文件同步
- 智能文件预加载
- 后台同步操作

## 6. 安全考虑

### 6.1 访问控制
- SSH 密钥认证
- VS Code Server 访问控制
- Git 操作审计
- 基于角色的权限管理

### 6.2 数据安全
- 文件操作日志
- 变更历史追踪
- 自动备份机制
- 敏感信息保护

## 7. 错误处理

### 7.1 同步错误
- 文件冲突解决
- 网络中断恢复
- 权限问题处理
- VS Code Server 重连

### 7.2 环境错误
- 初始化失败恢复
- 连接断开重试
- 配置错误修正
- 服务降级处理

## 8. 监控和日志

### 8.1 监控指标
- 文件操作性能
- 同步状态
- VS Code Server 状态
- 错误率统计

### 8.2 日志记录
- 操作审计
- 错误追踪
- 性能分析
- 安全事件记录
```
