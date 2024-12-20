import json
import os
from typing import Dict, Any, Optional, List
from phi.workflow import Workflow
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from pydantic import Field
from phi.utils.log import logger
from .workflow_loader import WorkflowConfigLoader
from agents.base_agent import NimshipAgent

class WorkflowController(Workflow):
    config_loader: WorkflowConfigLoader = Field(default_factory=WorkflowConfigLoader)
    workflow_config: Dict[str, Any] = Field(default_factory=dict)
    current_state: str = Field(default="init")

    def __init__(
        self, 
        workflow_name: str,
        session_id: str,
        storage: Optional[SqlWorkflowStorage] = None
    ):
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

    def get_valid_transitions(self) -> List[Dict[str, Any]]:
        """获取当前状态下的所有可能转换"""
        return [
            t for t in self.workflow_config["transitions"] 
            if t["from_state"] == self.current_state
        ]

    def validate_transition(self, to_state: str) -> Optional[Dict[str, Any]]:
        """验证状态转换是否允许"""
        valid_transitions = self.get_valid_transitions()
        for transition in valid_transitions:
            if transition["to_state"] == to_state:
                logger.info(f"Found valid transition: {self.current_state} -> {to_state}")
                return transition
        logger.error(f"Invalid transition: {self.current_state} -> {to_state}")
        return None

    def validate_state_data(self, state: str, data: Dict[str, Any]) -> bool:
        """验证状态数据的完整性"""
        state_requirements = self.workflow_config["state_data"].get(state, {})
        required_fields = state_requirements.get("required_fields", [])
        
        for field in required_fields:
            if field not in data:
                logger.error(f"Missing required field for state {state}: {field}")
                return False
            
        logger.info(f"State data validation passed for state: {state}")
        return True

    def try_transition(self, to_state: str, data: Dict[str, Any]) -> bool:
        """尝试执行状态转换"""
        # 验证转换是否允许
        transition = self.validate_transition(to_state)
        if not transition:
            return False

        # 验证状态数据
        if not self.validate_state_data(to_state, data):
            return False

        # 执行Agent任务
        try:
            agent_result = self.execute_agent_task(
                transition["agent_id"], 
                data
            )
            data.update(agent_result)
        except Exception as e:
            logger.error(f"Agent execution failed: {str(e)}")
            return False

        # 执行转换
        old_state = self.current_state
        try:
            self.current_state = to_state
            self.session_state["current_state"] = to_state
            self.session_state["state_data"] = data
            logger.info(f"State transition successful: {old_state} -> {to_state}")
            return True
        except Exception as e:
            self.current_state = old_state
            logger.error(f"State transition failed: {str(e)}")
            return False

    def load_agent(self, agent_id: str) -> NimshipAgent:
        """加载指定的Agent"""
        agent_config = next(
            (a for a in self.workflow_config["agents"] if a["id"] == agent_id),
            None
        )
        if not agent_config:
            logger.error(f"Agent not found: {agent_id}")
            raise ValueError(f"Agent {agent_id} not found in workflow config")
        
        # 从项目根目录解析配置路径    
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            agent_config["config_path"]
        )
        return NimshipAgent(config_path=config_path)

    def execute_agent_task(self, agent_id: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """执行Agent任务"""
        logger.info(f"Executing agent task: {agent_id}")
        try:
            agent = self.load_agent(agent_id)
            # Format task data as a user message
            formatted_input = {
                "role": "user",
                "content": json.dumps(task_data, indent=2)
            }
            result = agent.run(formatted_input)
            logger.info(f"Agent task completed: {agent_id}")
            return result
        except Exception as e:
            logger.error(f"Agent task failed: {str(e)}")
            raise