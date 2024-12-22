import pytest
from tools.file_manager import FileManagerTools, VSCodeRemoteProvider, ContentMatch
import tempfile
import os

class TestFileManager:
    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield tmpdirname
            
    @pytest.fixture
    def file_manager(self):
        return FileManagerTools()

    def test_file_operations(self, temp_dir):
        file_manager = FileManagerTools()
        test_file = os.path.join(temp_dir, "test.txt")
        
        # 创建文件
        result = file_manager.create_file(test_file, "test content")
        assert result.success
        
        # 读取文件
        result = file_manager.read_file(test_file)
        assert result.success
        assert result.data["content"] == "test content"

    def test_directory_operations(self, file_manager, temp_dir):
        # 测试目录创建
        test_dir = os.path.join(temp_dir, "test_dir")
        result = file_manager.create_directory(test_dir)
        assert result.success

        # 测试目录移动
        new_dir = os.path.join(temp_dir, "new_dir")
        result = file_manager.move_directory(test_dir, new_dir)
        assert result.success

    def test_search_operations(self, file_manager, temp_dir):
        # 创建测试文件
        test_file = os.path.join(temp_dir, "test.txt")
        file_manager.create_file(test_file, "test content")

        # 测试文件搜索
        results = file_manager.search_files(os.path.join(temp_dir, "*.txt"))
        assert len(results) > 0

        # 测试内容搜索
        matches = file_manager.search_in_files("test", os.path.join(temp_dir, "*.txt"))
        assert len(matches) > 0