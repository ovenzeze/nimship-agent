import pytest
from tools.devops import DevOpsTools, RemoteConfig, ProjectConfig
from tools.base import OperationResult
from unittest.mock import patch


class TestDevOps:
    @pytest.fixture
    def devops_tools(self):
        return DevOpsTools()

    @pytest.fixture
    def remote_config(self):
        return RemoteConfig(
            hostname="test-host",
            username="test-user",
            port=22,
            workspace_path="/test/workspace"
        )

    @pytest.fixture
    def project_config(self):
        return ProjectConfig(
            repo_url="https://github.com/test/repo.git",
            branch="main"
        )

    def test_command_retry(self, devops_tools, remote_config):
        # Test retry mechanism for command execution
        with patch.object(devops_tools, '_execute_command') as mock_execute:
            mock_execute.side_effect = [
                OperationResult(success=False, message="First attempt failed"),
                OperationResult(success=True, data={"output": "success"})
            ]

            result = devops_tools._execute_command_with_retry(["test", "command"], max_retries=2)
            assert result.success
            assert mock_execute.call_count == 2

    def test_cleanup_workspace(self, devops_tools, remote_config):
        # Test workspace cleanup functionality
        with patch.object(devops_tools, '_execute_command') as mock_execute:
            mock_execute.side_effect = [
                OperationResult(success=True),
                OperationResult(success=True)
            ]

            result = devops_tools.cleanup_workspace(remote_config)
            assert result.success
            assert mock_execute.call_count == 2

    def check_connection_status(self, remote_config: RemoteConfig) -> OperationResult:
        """Check remote connection status"""
        command = ["code", "--status"]
        return self._execute_command(command)

    def verify_workspace(self, remote_config: RemoteConfig, project_config: ProjectConfig) -> OperationResult:
        """Verify workspace and project settings are correct"""
        workspace_check = self._execute_command(["ls", remote_config.workspace_path])
        if not workspace_check.success:
            return workspace_check

        git_check = self._execute_command(["git", "-C", remote_config.workspace_path, "status"])
        if not git_check.success:
            return git_check

        return OperationResult(success=True)

    def diagnose_environment(self, remote_config: RemoteConfig) -> OperationResult:
        """Diagnose remote environment status"""
        tools = ["git", "python", "node"]
        results = {}

        for tool in tools:
            result = self._execute_command([tool, "--version"])
            results[tool] = result.data["output"] if result.success else "Not found"

        return OperationResult(success=True, data={"tools": results})