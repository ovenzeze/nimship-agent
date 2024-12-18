from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class CodePatch:
    """代码更新补丁"""
    # 定位信息
    target_type: str  # 'function', 'class', 'block'
    target_name: Optional[str] = None  # 函数名/类名
    before_context: Optional[str] = None  # 更改位置之前的代码
    after_context: Optional[str] = None   # 更改位置之后的代码
    
    # 更新内容
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
