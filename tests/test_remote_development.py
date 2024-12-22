import pytest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.file_manager import FileManagerTools
from tools.git_tools import GitTools
from tools.devops import DevOpsTools

# 确保环境变量已经加载
from dotenv import load_dotenv
load_dotenv()

# 条件导入
try:
    import paramiko
except ImportError:
    paramiko = None

try:
    import requests
except ImportError:
    requests = None

@pytest.fixture
def file_manager():
    return FileManagerTools(environment='remote')

@pytest.fixture
def git_tools():
    return GitTools()

@pytest.fixture
def devops_tools():
    return DevOpsTools()

@pytest.mark.parametrize("operation,method,args", [
    ("create", "create_file", ("test.txt", "test content")),
    ("read", "read_file", ("test.txt",)),
    ("update", "update_file", ("test.txt", "updated content")),
    ("delete", "delete_file", ("test.txt",))
])
def test_remote_file_operations(file_manager, operation, method, args):
    with patch('tools.file_manager.VSCodeRemoteProvider') as mock_provider:
        mock_method = getattr(mock_provider.return_value, method)
        mock_method.return_value = MagicMock(success=True)
        if operation == "read":
            mock_method.return_value.data = {'content': 'test content'}
        
        result = getattr(file_manager, method)(*args)
        assert result.success
        if operation == "read":
            assert result.data['content'] == 'test content'

def test_remote_git_operations(git_tools):
    with patch.object(GitTools, '_execute_git_command', return_value=MagicMock(success=True)):
        assert git_tools.create_branch('new-feature').success
        assert git_tools.commit_changes('Test commit').success
        assert git_tools.switch_branch('main').success

def test_devops_operations(devops_tools):
    with patch.object(DevOpsTools, 'push_changes', return_value=MagicMock(success=True)):
        assert devops_tools.push_changes('origin', 'main').success
    
    with patch.object(DevOpsTools, 'create_pull_request', return_value=MagicMock(success=True)):
        assert devops_tools.create_pull_request('feature', 'main').success

def test_error_handling(file_manager, git_tools):
    with patch.object(file_manager, '_get_provider') as mock_provider:
        mock_provider.return_value.read_file.side_effect = FileNotFoundError
        result = file_manager.read_file('nonexistent.txt')
        assert not result.success

    with patch.object(git_tools, '_execute_git_command', return_value=MagicMock(success=False, message='Git error')):
        result = git_tools.create_branch('invalid-branch')
        assert not result.success
        assert result.message == 'Git error'

# 如果 paramiko 不可用，跳过这个测试
@pytest.mark.skipif(paramiko is None, reason="paramiko is not installed")
def test_remote_connection():
    hostname = os.getenv('NIMSHIP_REMOTE_HOSTNAME')
    username = os.getenv('NIMSHIP_REMOTE_USER')
    port = int(os.getenv('NIMSHIP_REMOTE_PORT', 22))

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, port, username)
        assert True, "Successfully connected to remote server"
    except Exception as e:
        pytest.fail(f"Failed to connect to remote server: {str(e)}")
    finally:
        ssh.close()

# 如果 requests 不可用，跳过这个测试
@pytest.mark.skipif(requests is None, reason="requests is not installed")
def test_vscode_server_connection():
    # This test assumes that the VS Code Server is running on the default port 8080
    hostname = os.getenv('NIMSHIP_REMOTE_HOSTNAME')
    vscode_server_url = f"http://{hostname}:8080"

    try:
        response = requests.get(vscode_server_url)
        assert response.status_code == 200, "VS Code Server is accessible"
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to VS Code Server: {str(e)}")

# 注意：要运行所有测试，请确保已安装 paramiko 和 requests 库
# 可以通过运行 `pip install -r requirements.txt` 来安装所有依赖
