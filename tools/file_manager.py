from dataclasses import dataclass
from typing import List, Optional
import re
import os
import glob


@dataclass
class ContentMatch:
    """文件内容匹配结果"""
    path: str
    line_number: int
    content: str


@dataclass
class CodePatch:
    """代码更新补丁"""
    target_type: str  # 'function', 'class', 'block'
    target_name: Optional[str] = None  # 函数名/类名
    before_context: Optional[str] = None  # 更改位置之前的代码
    after_context: Optional[str] = None  # 更改位置之后的代码
    change_type: str  # 'modify', 'insert', 'delete'
    new_content: Optional[str] = None 


class GitAwareFileManager:

    def apply_patch(self, file_path: str, patch: CodePatch) -> bool:
        with open(file_path, 'r') as f:
            content = f.read()

        if patch.target_type in ('function', 'class'):
            # 基于函数名/类名定位
            pattern = self._get_definition_pattern(patch.target_type, patch.target_name)
            match = re.search(pattern, content)
            if not match:
                raise ValueError(f"{patch.target_type} {patch.target_name} not found")
            start, end = self._find_block_bounds(content, match.start())

        elif patch.target_type == 'block':
            # 基于上下文定位
            if not (patch.before_context and patch.after_context):
                raise ValueError("Context required for block patches")
            start, end = self._find_with_context(
                content,
                patch.before_context,
                patch.after_context
            )

        # 应用更改
        if patch.change_type == 'modify':
            new_content = (
                content[:start] + 
                patch.new_content + 
                content[end:]
            )
        elif patch.change_type == 'insert':
            new_content = (
                content[:end] + 
                '\n' + patch.new_content + 
                content[end:]
            )
        elif patch.change_type == 'delete':
            new_content = content[:start] + content[end:]

        # 写入文件并提交
        with open(file_path, 'w') as f:
            f.write(new_content)

        return self._git_add_and_commit(
            file_path,
            f"Update {patch.target_type} {patch.target_name or 'block'}"
        )

    def _git_add_and_commit(self, file_path, message):
        #  此处应添加git操作，根据实际情况修改
        print(f"git add {file_path}")
        print(f"git commit -m \"{message}\"")
        return True

    def _get_definition_pattern(self, target_type: str, name: str) -> str:
        """生成函数或类定义的正则表达式"""
        if target_type == 'function':
            return rf'def\s+{name}\s*\('
        elif target_type == 'class':
            return rf'class\s+{name}\s*[:\(]'
        raise ValueError(f"Unsupported target type: {target_type}")

    def _find_block_bounds(self, content: str, start_pos: int) -> tuple[int, int]:
        """查找代码块的起止位置"""
        lines = content.splitlines(True)
        current_pos = 0
        block_start = -1
        
        # 找到包含起始位置的行
        for i, line in enumerate(lines):
            if current_pos <= start_pos < current_pos + len(line):
                block_start = i
                break
            current_pos += len(line)

        if block_start == -1:
            raise ValueError("Invalid start position")

        # 获取起始行的缩进级别
        indent = len(lines[block_start]) - len(lines[block_start].lstrip())
        
        # 查找块结束位置
        block_end = block_start + 1
        while block_end < len(lines):
            if lines[block_end].strip() and len(lines[block_end]) - len(lines[block_end].lstrip()) <= indent:
                break
            block_end += 1

        # 转换为字符位置
        start = sum(len(l) for l in lines[:block_start])
        end = sum(len(l) for l in lines[:block_end])
        
        return start, end

    def _find_with_context(self, content: str, before: str, after: str) -> tuple[int, int]:
        """基于上下文查找代码块的位置"""
        lines = content.splitlines()
        for i in range(len(lines)):
            if i > 0 and before in lines[i-1] and i < len(lines)-1 and after in lines[i+1]:
                start = sum(len(l) + 1 for l in lines[:i])
                end = start + len(lines[i]) + 1
                return start, end
        raise ValueError("Context not found")

    def search_files(self, pattern: str) -> List[str]:
        """搜索匹配模式的文件"""
        if not pattern:
            pattern = "*.*"
        return glob.glob(pattern, recursive=True)

    def create_directory(self, path: str) -> bool:
        """创建目录"""
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create directory {path}: {e}")
            return False

    def move_directory(self, src: str, dst: str) -> bool:
        """移动目录"""
        try:
            import shutil
            shutil.move(src, dst)
            self._git_add_and_commit([src, dst], f"Move directory from {src} to {dst}")
            return True
        except Exception as e:
            print(f"Failed to move directory: {e}")
            return False

    def search_in_files(self, content_pattern: str, file_pattern: Optional[str]=None) -> List[ContentMatch]:
        """在文件内容中搜索"""
        matches = []
        for file_path in self.search_files(file_pattern or ""):
            with open(file_path, 'r') as f:
                for i, line in enumerate(f, 1):
                    if re.search(content_pattern, line):
                        matches.append(ContentMatch(
                            path=file_path,
                            line_number=i,
                            content=line.strip()
                        ))
        return matches

from .base import Tool, OperationResult
from phi.tools.base import tool_response

class FileManagerTools(Tool):
    name: str = "FileManager"
    description: str = "Unified file operations for local and remote development"
    
    @tool_response
    def create_file(self, path: str, content: str) -> OperationResult:
        provider = self._get_provider()
        return provider.create_file(path, content)
        
    @tool_response
    def read_file(self, path: str) -> OperationResult:
        provider = self._get_provider()
        return provider.read_file(path)
