from dataclasses import dataclass
from typing import Optional
import subprocess
from .base import Tool, OperationResult

@dataclass
class RemoteConfig:
    hostname: str
    username: str
    port: int = 22
    workspace_path: str = "~/workspace"

@dataclass
class ProjectConfig:
    repo_url: str
    branch: str = "main"

class DevOpsTools(Tool):
    name: str = "DevOps"
    description: str = "DevOps operations for remote development"
    
    def setup_workspace(self, remote_config: RemoteConfig, project_config: ProjectConfig) -> OperationResult:
        """设置远程工作空间"""
        self.remote_config = remote_config
        connect_result = self.connect_remote(remote_config)
        if not connect_result.success:
            return connect_result
            
        return OperationResult(success=True, message="Workspace setup completed")

    def connect_remote(self, remote_config: RemoteConfig) -> OperationResult:
        """连接到远程开发环境"""
        command = ["code", "--remote", f"ssh-remote+{remote_config.username}@{remote_config.hostname}"]
        return self._execute_command(command)

    def _execute_command(self, command: list) -> OperationResult:
        """执行命令并返回结果"""
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            return OperationResult(success=True, message="Command executed successfully", data={"output": output})
        except subprocess.CalledProcessError as e:
            return OperationResult(success=False, message=f"Command failed: {e.output}")

    def check_connection_status(self, remote_config: RemoteConfig) -> OperationResult:
        """检查远程连接状态"""
        command = ["code", "--status"]
        return self._execute_command(command)
        
    def verify_workspace(self, remote_config: RemoteConfig, project_config: ProjectConfig) -> OperationResult:
        """验证工作空间和项目设置"""
        # 检查工作目录存在
        workspace_check = ["test", "-d", remote_config.workspace_path]
        workspace_result = self._execute_command(workspace_check)
        if not workspace_result.success:
            return OperationResult(success=False, message="Workspace directory not found")
            
        # 检查是否为git仓库
        git_check = ["git", "-C", remote_config.workspace_path, "rev-parse", "--git-dir"]
        return self._execute_command(git_check)
        
    def diagnose_environment(self, remote_config: RemoteConfig) -> OperationResult:
        """诊断远程环境状态"""
        # 检查必要工具
        tools_to_check = [
            ["git", "--version"],
            ["code", "--version"],
            ["ssh", "-V"]
        ]
        
        results = []
        for tool_cmd in tools_to_check:
            result = self._execute_command(tool_cmd)
            results.append({
                "tool": tool_cmd[0],
                "status": result.success,
                "output": result.data.get("output") if result.success else result.message
            })
            
        return OperationResult(
            success=all(r["status"] for r in results),
            message="Environment diagnosis complete",
            data={"tools": results}
        )
remote_config = RemoteConfig(
    hostname="dev-server",
    username="dev",
    workspace_path="~/projects/my-project"
)

project_config = ProjectConfig(
    repo_url="https://github.com/org/repo.git",
    branch="develop"
)

devops_tools = DevOpsTools()
result = devops_tools.setup_workspace(remote_config, project_config)