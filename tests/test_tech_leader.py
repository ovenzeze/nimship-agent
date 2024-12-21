import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController
from phi.utils.log import logger

def test_tech_leader():
    print("\nTesting Tech Leader Agent...")
    logger.info("Starting Tech Leader test")
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-tech-leader"
    )
    print(f"✓ Controller initialized in state: {controller.current_state}")
    
    # 准备requirement阶段的数据
    requirement_data = {
        "project_name": "Test Project",
        "project_description": "A test automation project",
        "user_stories": [
            "As a developer, I want to automate testing"
        ],
        "acceptance_criteria": [
            "All tests should pass"
        ]
    }
    print("✓ Requirement data prepared")
    
    # 先转换到requirement状态
    success = controller.try_transition("requirement", requirement_data)
    print(f"✓ Requirement transition: {success}")
    
    # 准备technical阶段的数据
    technical_data = {
        "technical_design": "Microservices Architecture",
        "implementation_plan": "Agile Development Process"
    }
    requirement_data.update(technical_data)
    print("✓ Technical data prepared")
    
    # 执行到technical阶段的转换
    success = controller.try_transition("technical", requirement_data)
    print(f"✓ Technical transition: {success}")
    print(f"✓ Current state: {controller.current_state}")

if __name__ == "__main__":
    test_tech_leader()
