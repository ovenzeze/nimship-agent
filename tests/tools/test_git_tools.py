import pytest
from tools.git_tools import GitTools
import tempfile
import os
import subprocess
import uuid

class TestGitTools:
    @pytest.fixture
    def git_repo(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            # 初始化Git仓库
            subprocess.run(["git", "init"], cwd=tmpdirname)
            # 创建并提交一个初始文件，确保有master分支
            test_file = os.path.join(tmpdirname, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")
            subprocess.run(["git", "add", "."], cwd=tmpdirname)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdirname)
            yield tmpdirname

    def test_git_operations(self, git_repo):
        git_tools = GitTools()
        
        # 使用唯一的分支名
        branch_name = f"test-branch-{uuid.uuid4().hex[:8]}"
        
        # 创建分支
        result = git_tools.create_branch(branch_name)
        assert result.success
        
        # 切换分支
        result = git_tools.switch_branch(branch_name)
        assert result.success
        
        # 提交更改
        test_file = os.path.join(git_repo, "new_file.txt")
        with open(test_file, "w") as f:
            f.write("new content")
        result = git_tools.commit_changes("Test commit")
        assert result.success