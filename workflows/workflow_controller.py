from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import os
import json
from phi.workflow import Workflow
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from pydantic import Field
from phi.utils.log import logger
from .workflow_loader import WorkflowConfigLoader
from agents.base_agent import NimshipAgent
from utils.json_processor import JsonProcessor


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


class WorkflowController(Workflow):
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    current_state: str = Field(default="init")
    input_data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, workflow_path: str, session_id: str, storage: Optional[SqlWorkflowStorage] = None):
        # Initialize parent class first
        super().__init__(
            session_id=session_id,
            storage=storage
        )
        
        # Load configuration
        config_dir = os.path.dirname(workflow_path)
        loader = WorkflowConfigLoader(config_dir)
        self.workflow_config = loader.load_workflow(Path(workflow_path))
        
        # Set up storage
        if not storage:
            self.storage = SqlWorkflowStorage(
                table_name=f"{self.workflow_config['name']}_workflows",
                db_file="tmp/workflows.db"
            )
        
        # Load input data
        self.input_data = self._load_workflow_input(config_dir)
        self.current_state = self.workflow_config["initial_state"]
        logger.info(f"Workflow initialized in state: {self.current_state}")

    def _load_workflow_input(self, config_dir: str) -> Dict[str, Any]:
        """Load workflow input data"""
        input_path = os.path.join(
            config_dir,
            self.workflow_config['input_file']
        )
        with open(input_path, 'r') as f:
            return json.load(f)

    def get_valid_transitions(self):
        """Get valid transitions for current state"""
        return [
            t for t in self.workflow_config["transitions"]
            if t["from_state"] == self.current_state
        ]

    def validate_transition(self, to_state: str) -> Optional[Dict[str, Any]]:
        """Validate if state transition is allowed"""
        valid_transitions = self.get_valid_transitions()
        for transition in valid_transitions:
            if transition["to_state"] == to_state:
                logger.info(f"Found valid transition: {self.current_state} -> {to_state}")
                return transition
        logger.error(f"Invalid transition: {self.current_state} -> {to_state}")
        return None

    def validate_state_data(self, state: str, data: Dict[str, Any]) -> bool:
        """Validate if state data meets requirements"""
        state_requirements = self.workflow_config["state_data"].get(state, {})
        required_fields = state_requirements.get("required_fields", [])

        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field for state {state}: {field}")
                return False

        logger.info(f"State data validation passed for state: {state}")
        return True

    def load_agent(self, agent_id: str) -> NimshipAgent:
        """Load agent instance"""
        agent_config = next(
            (a for a in self.workflow_config["agents"] if a["id"] == agent_id),
            None
        )
        if not agent_config:
            logger.error(f"Agent not found: {agent_id}")
            raise ValueError(f"Agent {agent_id} not found in workflow config")

        return NimshipAgent(config_path=agent_config["config_path"])

    def _serialize_run_response(self, response):
        """Convert RunResponse to a serializable dictionary"""
        if hasattr(response, 'model_dump'):
            return response.model_dump()
        elif hasattr(response, '__dict__'):
            return {k: str(v) for k, v in response.__dict__.items()}
        else:
            return str(response)

    def execute_agent_task(self, agent_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent task"""
        logger.info(f"Executing agent task: {agent_id}")
        try:
            agent = self.load_agent(agent_id)
            
            # Keep original data
            current_data = task_data.copy()
            
            # Format input
            formatted_input = {
                "role": "user",
                "content": JsonProcessor.safe_serialize(current_data)
            }
            
            # Log agent input
            logger.info(f"Agent {agent_id} input: {json.dumps(formatted_input, indent=2, default=json_serial)}")
            
            # Execute agent
            result = agent.run(formatted_input)
            
            # Log raw agent output
            serialized_result = self._serialize_run_response(result)
            logger.info(f"Agent {agent_id} raw output: {json.dumps(serialized_result, indent=2, default=json_serial)}")
            
            # Process return result
            if isinstance(serialized_result, dict):
                # Merge instead of replace
                cleaned_result = JsonProcessor.clean_content(serialized_result)
                logger.info(f"Agent {agent_id} cleaned output: {json.dumps(cleaned_result, indent=2, default=json_serial)}")
                
                # Log the exact content of cleaned_result
                logger.info(f"Cleaned result keys: {cleaned_result.keys()}")
                if 'content' in cleaned_result:
                    logger.info(f"Content in cleaned result: {cleaned_result['content']}")
                    
                    # Check if technical_design is nested in content
                    if isinstance(cleaned_result['content'], dict) and 'technical_design' in cleaned_result['content']:
                        current_data['technical_design'] = cleaned_result['content']['technical_design']
                        logger.info(f"Found technical_design in content: {current_data['technical_design']}")
                
                current_data.update(cleaned_result)
                
                # Check for required fields
                required_fields = self.workflow_config["state_data"].get(self.current_state, {}).get("required_fields", [])
                missing_fields = [field for field in required_fields if field not in current_data]
                
                if missing_fields:
                    logger.warning(f"Missing required fields: {missing_fields}")
                    formatter_agent = self.load_agent("formatter")
                    formatter_input = {
                        "role": "user",
                        "content": JsonProcessor.safe_serialize({
                            "original_data": current_data,
                            "missing_fields": missing_fields
                        })
                    }
                    logger.info(f"Formatter agent input: {json.dumps(formatter_input, indent=2, default=json_serial)}")
                    formatter_result = formatter_agent.run(formatter_input)
                    formatted_result = self._serialize_run_response(formatter_result)
                    logger.info(f"Formatter agent raw output: {json.dumps(formatted_result, indent=2, default=json_serial)}")
                    if isinstance(formatted_result, dict):
                        cleaned_formatted_result = JsonProcessor.clean_content(formatted_result)
                        logger.info(f"Formatter agent cleaned output: {json.dumps(cleaned_formatted_result, indent=2, default=json_serial)}")
                        current_data.update(cleaned_formatted_result)
                    else:
                        logger.error("Formatter agent did not return a dictionary")
            else:
                current_data["content"] = str(serialized_result)
                logger.info(f"Agent {agent_id} output (non-dict): {serialized_result}")
            
            # Add status information
            current_data.update({
                "status": "success",
                "last_updated": datetime.now().isoformat()
            })
            
            # Log final state data
            logger.info(f"Final state data after {agent_id} task: {json.dumps(current_data, indent=2, default=json_serial)}")
            
            return current_data
                
        except Exception as e:
            logger.error(f"Agent task failed: {str(e)}")
            return {
                **task_data,
                "content": str(e),
                "status": "error",
                "last_updated": datetime.now().isoformat()
            }

    def try_transition(self, to_state: str, data: Dict[str, Any]) -> bool:
        """Try to transition to new state"""
        transition = self.validate_transition(to_state)
        if not transition:
            return False

        logger.info(f"State data before validation: {json.dumps(data, indent=2, default=json_serial)}")
        logger.info(f"Required fields for state {to_state}: {self.workflow_config['state_data'][to_state]['required_fields']}")
        
        # Check for missing fields before validation
        required_fields = self.workflow_config["state_data"].get(to_state, {}).get("required_fields", [])
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            logger.warning(f"Missing required fields: {missing_fields}")
            formatter_agent = self.load_agent("formatter")
            formatter_input = {
                "role": "user",
                "content": JsonProcessor.safe_serialize({
                    "original_data": data,
                    "missing_fields": missing_fields,
                    "current_state": self.current_state,
                    "target_state": to_state
                })
            }
            logger.info(f"Formatter agent input: {json.dumps(formatter_input, indent=2, default=json_serial)}")
            formatter_result = formatter_agent.run(formatter_input)
            formatted_result = self._serialize_run_response(formatter_result)
            logger.info(f"Formatter agent raw output: {json.dumps(formatted_result, indent=2, default=json_serial)}")
            if isinstance(formatted_result, dict):
                cleaned_formatted_result = JsonProcessor.clean_content(formatted_result)
                logger.info(f"Formatter agent cleaned output: {json.dumps(cleaned_formatted_result, indent=2, default=json_serial)}")
                data.update(cleaned_formatted_result)
            else:
                logger.error("Formatter agent did not return a dictionary")

        if not self.validate_state_data(to_state, data):
            logger.error(f"State data validation failed for {to_state}")
            return False

        logger.info(f"State data validation passed for {to_state}")

        old_state = self.current_state
        try:
            agent_result = self.execute_agent_task(transition["agent_id"], data)

            self.current_state = to_state
            self.session_state["current_state"] = to_state
            self.session_state["state_data"] = agent_result

            logger.info(f"State transition successful: {old_state} -> {to_state}")
            logger.info(f"Final state data after transition: {json.dumps(agent_result, indent=2, default=json_serial)}")
            return True

        except Exception as e:
            self.current_state = old_state
            logger.error(f"State transition failed: {str(e)}")
            return False
