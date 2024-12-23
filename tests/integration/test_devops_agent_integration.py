import os
import json
import pytest
from pathlib import Path
from dotenv import load_dotenv
from tools.file_manager import FileManagerTools
from tools.devops import DevOpsTools
from agents.base_agent import NimshipAgent

load_dotenv()

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
# 工作流配置目录
WORKFLOW_DIR = PROJECT_ROOT / "config" / "workflows"
# 测试配置目录
TEST_CONFIG_DIR = Path(__file__).parent / "test_configs"
TEST_CONFIG_DIR.mkdir(exist_ok=True)

@pytest.fixture(scope="module")
def devops_agent() -> NimshipAgent:
    """初始化DevOps Agent"""
    agent_config_path = PROJECT_ROOT / "config" / "agents" / "devops_engineer.agent.json"
    return NimshipAgent(config_path=str(agent_config_path))
@pytest.fixture(scope="module")
def file_manager():
    return FileManagerTools(environment='remote')

@pytest.fixture(scope="module")
def devops_tools():
    return DevOpsTools()

def test_devops_agent_setup(devops_agent):
    """测试DevOps Agent环境配置"""
    setup_prompt = {
        "role": "user",
        "content": json.dumps({
            "task": "environment_setup",
            "config": {
                "vscode_server": {
                    "host": os.getenv("VSCODE_SERVER_HOST"),
                    "port": int(os.getenv("VSCODE_SERVER_PORT", "8080")),
                },
                "workspace": {
                    "path": os.getenv("WORKSPACE_PATH"),
                    "project": os.getenv("PROJECT_NAME")
                }
            }
        })
    }
    
    response = devops_agent.run(setup_prompt)
    print(f"Setup response: {response}")  # 添加调试输出
    assert response.get("status") == "success", "DevOps Agent setup failed"

def test_vscode_connection(devops_agent, devops_tools):
    """测试VSCode Server连接"""
    # 使用DevOpsTools进行实际连接测试
    connection_result = devops_tools.check_connection_status(
        remote_config={
            "hostname": os.getenv("VSCODE_SERVER_HOST"),
            "port": int(os.getenv("VSCODE_SERVER_PORT", "8080"))
        }
    )
    assert connection_result.success, "VSCode Server connection failed"
    
    # 让Agent验证连接
    verify_prompt = {
        "role": "user",
        "content": json.dumps({
            "task": "verify_connection",
            "params": {
                "check_items": ["vscode_server", "workspace_access"]
            }
        })
    }
    
    response = devops_agent.run(verify_prompt)
    print(f"Connection verification response: {response}")  # 添加调试输出
    assert response.get("status") == "success"

def test_project_operations(devops_agent, file_manager, devops_tools):
    """测试项目操作流程"""
    workspace_path = os.getenv("WORKSPACE_PATH")
    test_branch = f"test-integration-{os.urandom(4).hex()}"
    
    try:
        # 1. 创建测试分支
        branch_result = devops_tools.create_branch(test_branch)
        assert branch_result.success, f"Failed to create branch: {branch_result.message}"
        
        # 2. 创建测试文件
        test_file = os.path.join(workspace_path, "test_integration.py")
        create_result = file_manager.create_file(
            test_file,
            "def test_function():\n    return 'Integration test'"
        )
        assert create_result.success, f"Failed to create test file: {create_result.message}"
        
        # 3. 让Agent处理提交
        commit_prompt = {
            "role": "user",
            "content": json.dumps({
                "task": "commit_changes",
                "params": {
                    "files": [test_file],
                    "message": "test: add integration test file",
                    "branch": test_branch
                }
            })
        }
        response = devops_agent.run(commit_prompt)
        print(f"Commit response: {response}")  # 添加调试输出
        assert response.get("status") == "success"
        
    finally:
        # 清理：切换回主分支
        devops_tools.switch_branch("main")
        # 删除测试文件
        if os.path.exists(test_file):
            file_manager.delete_file(test_file)

def test_cleanup(devops_agent, file_manager):
    """清理测试环境"""
    cleanup_prompt = {
        "role": "user",
        "content": json.dumps({
            "task": "cleanup_environment",
            "params": {
                "cleanup_items": ["test_files", "test_branches"]
            }
        })
    }
    
    response = devops_agent.run(cleanup_prompt)
    print(f"Cleanup response: {response}")  # 添加调试输出
    assert response.get("status") == "success"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])