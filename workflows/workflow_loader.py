import json
from typing import Dict, Any
from pathlib import Path
from phi.utils.log import logger

class WorkflowConfigLoader:
    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)
    
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """验证工作流配置的完整性"""
        required_fields = {
            'name', 'description', 'input_file',
            'agents', 'state_data', 'initial_state', 'transitions'
        }
        
        if not all(field in config for field in required_fields):
            missing = required_fields - set(config.keys())
            logger.error(f"Missing required fields: {missing}")
            return False
            
        return True
    
    def load_workflow(self, config_path: Path) -> Dict[str, Any]:
        """加载并验证工作流配置"""
        with open(config_path) as f:
            config = json.load(f)
            
        if not self.validate_config(config):
            raise ValueError(f"Invalid workflow config: {config_path}")
            
        return config        