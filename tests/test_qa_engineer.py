import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController
from phi.utils.log import logger

from workflows.models import WorkflowStateData

def test_qa_engineer():
    print("\nTesting QA Engineer Agent...")
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-qa"
    )
    
    # 准备初始状态数据
    state_data = WorkflowStateData(
        project_name="Test Project",
        project_description="A test automation project",
        user_stories=["As a developer, I want to automate testing"],
        acceptance_criteria=["All tests should pass"],
        technical_design="Microservices Architecture",
        implementation_plan="Agile Development Process",
        code_complete=True,
        unit_tests="All unit tests implemented",
        test_results="All tests passed",
        bug_report="No critical bugs found"
    )
    
    # 执行状态转换
    for state in ["requirement", "technical", "development", "testing"]:
        success = controller.try_transition(state, state_data.model_dump())
        print(f"✓ {state.capitalize()} transition: {success}")
        print(f"✓ Current state: {controller.current_state}")

if __name__ == "__main__":
    test_qa_engineer()
