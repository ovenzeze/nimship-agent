import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController
from phi.utils.log import logger

def test_engineer():
    print("\nTesting Engineer Agent...")
    logger.info("Starting Engineer test")
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-engineer"
    )
    
    # 1. 先执行requirement阶段
    requirement_data = {
        "project_name": "Test Project",
        "project_description": "A test automation project",
        "user_stories": ["As a developer, I want to automate testing"],
        "acceptance_criteria": ["All tests should pass"]
    }
    success = controller.try_transition("requirement", requirement_data)
    print(f"✓ Requirement transition: {success}")
    
    # 2. 执行technical阶段
    technical_data = {
        "technical_design": "Microservices Architecture",
        "implementation_plan": "Agile Development Process"
    }
    requirement_data.update(technical_data)
    success = controller.try_transition("technical", requirement_data)
    print(f"✓ Technical transition: {success}")
    
    # 3. 执行development阶段
    development_data = {
        "code_complete": True,
        "unit_tests": "All unit tests implemented"
    }
    requirement_data.update(development_data)
    success = controller.try_transition("development", requirement_data)
    print(f"✓ Development transition: {success}")
    print(f"✓ Current state: {controller.current_state}")

if __name__ == "__main__":
    test_engineer()
