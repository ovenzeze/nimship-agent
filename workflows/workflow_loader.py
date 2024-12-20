import json
from typing import Dict, Any
from pathlib import Path
from phi.utils.log import logger

class WorkflowConfigLoader:
    def __init__(self, config_dir: str = "/Users/clayzhang/Code/nimship-agent/config/workflows"):
        self.config_dir = Path(config_dir)

    
    def load_workflow(self, workflow_name: str) -> Dict[str, Any]:
        """Load workflow configuration from json file
        
        Args:
            workflow_name: Name of the workflow file without extension
            
        Returns:
            Dict containing the workflow configuration
            
        Raises:
            FileNotFoundError: If workflow file doesn't exist
            JSONDecodeError: If workflow file is not valid JSON
        """
        workflow_path = self.config_dir / f"{workflow_name}.workflow.json"
        
        try:
            with open(workflow_path) as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Workflow config not found: {workflow_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in workflow config: {workflow_path}")
            raise