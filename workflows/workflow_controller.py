import json
from datetime import datetime
from typing import Dict, Any, Optional
from phi.workflow import Workflow
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from pydantic import Field
from phi.utils.log import logger
from .workflow_loader import WorkflowConfigLoader
from agents.base_agent import NimshipAgent
from .models import WorkflowStateData, AgentResponse

class WorkflowController(Workflow):
    config_loader: WorkflowConfigLoader = Field(default_factory=WorkflowConfigLoader)
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    current_state: str = Field(default="init")

    def __init__(self, workflow_name: str, session_id: str, storage: Optional[SqlWorkflowStorage] = None):
        super().__init__(
            session_id=session_id,
            storage=storage or SqlWorkflowStorage(
                table_name=f"{workflow_name}_workflows",
                db_file="tmp/workflows.db"
            )
        )
        
        self.workflow_config = self.config_loader.load_workflow(workflow_name)
        self.current_state = self.workflow_config["initial_state"]
        logger.info(f"Workflow initialized in state: {self.current_state}")

    def get_valid_transitions(self):
        return [
            t for t in self.workflow_config["transitions"] 
            if t["from_state"] == self.current_state
        ]

    def validate_transition(self, to_state: str) -> Optional[Dict[str, Any]]:
        valid_transitions = self.get_valid_transitions()
        for transition in valid_transitions:
            if transition["to_state"] == to_state:
                logger.info(f"Found valid transition: {self.current_state} -> {to_state}")
                return transition
        logger.error(f"Invalid transition: {self.current_state} -> {to_state}")
        return None

    def validate_state_data(self, state: str, data: Dict[str, Any]) -> bool:
        state_requirements = self.workflow_config["state_data"].get(state, {})
        required_fields = state_requirements.get("required_fields", [])
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field for state {state}: {field}")
                return False
            
        logger.info(f"State data validation passed for state: {state}")
        return True

    def load_agent(self, agent_id: str) -> NimshipAgent:
        agent_config = next(
            (a for a in self.workflow_config["agents"] if a["id"] == agent_id),
            None
        )
        if not agent_config:
            logger.error(f"Agent not found: {agent_id}")
            raise ValueError(f"Agent {agent_id} not found in workflow config")
            
        return NimshipAgent(config_path=agent_config["config_path"])

    def execute_agent_task(self, agent_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing agent task: {agent_id}")
        try:
            agent = self.load_agent(agent_id)
            base_data = {
                "status": "pending",
                "metadata": {},
                "content": None
            }
            task_data.update({k: v for k, v in base_data.items() if k not in task_data})
            
            state_data = WorkflowStateData(**task_data)
            formatted_input = {
                "role": "user",
                "content": state_data.model_dump_json()
            }
            
            agent_result = agent.run(formatted_input)
            
            # Handle different response types
            if isinstance(agent_result, dict):
                content = agent_result.get("content", "")
            else:
                content = str(agent_result)
                
            updated_data = state_data.model_copy(update={
                "content": content,
                "status": "success",
                "last_updated": datetime.now().isoformat()
            })

            return updated_data.model_dump()            
        except Exception as e:
            logger.error(f"Agent task failed: {str(e)}")
            # Return original data with error status instead of raising
            return {
                **task_data,
                "content": str(e),
                "status": "error",
                "last_updated": datetime.now().isoformat()
            }

    def try_transition(self, to_state: str, data: Dict[str, Any]) -> bool:
        transition = self.validate_transition(to_state)
        if not transition:
            return False

        if not self.validate_state_data(to_state, data):
            return False

        old_state = self.current_state
        try:
            agent_result = self.execute_agent_task(transition["agent_id"], data)
            
            self.current_state = to_state
            self.session_state["current_state"] = to_state
            self.session_state["state_data"] = agent_result
            
            logger.info(f"State transition successful: {old_state} -> {to_state}")
            return True
            
        except Exception as e:
            self.current_state = old_state
            logger.error(f"State transition failed: {str(e)}")
            return False