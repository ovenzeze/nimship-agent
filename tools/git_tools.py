from typing import List
import subprocess
from .base import Tool, OperationResult

class GitTools(Tool):
    name: str = "GitTools"
    description: str = "Git version control operations"

    def create_branch(self, name: str) -> OperationResult:
        return self._execute_git_command(['branch', name])

    def commit_changes(self, message: str) -> OperationResult:
        add_result = self._execute_git_command(['add', '.'])
        if not add_result.success:
            return add_result
        return self._execute_git_command(['commit', '-m', message])

    def switch_branch(self, name: str) -> OperationResult:
        return self._execute_git_command(['checkout', name])

    def view_history(self, path: str) -> List[dict]:
        result = self._execute_git_command(['log', '--pretty=format:%H|%an|%ad|%s', path])
        if not result.success:
            return []
        commits = []
        for line in result.data['output'].split('\n'):
            hash, author, date, message = line.split('|')
            commits.append({
                'hash': hash,
                'author': author,
                'date': date,
                'message': message
            })
        return commits

    def _execute_git_command(self, command: List[str]) -> OperationResult:
        try:
            output = subprocess.check_output(['git'] + command, stderr=subprocess.STDOUT, universal_newlines=True)
            return OperationResult(success=True, message="Git command executed successfully", data={'output': output})
        except subprocess.CalledProcessError as e:
            return OperationResult(success=False, message=f"Git command failed: {e.output}")
