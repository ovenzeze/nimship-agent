import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from workflows.workflow_controller import WorkflowController
from workflows.models import WorkflowStateData
from phi.utils.log import logger

@pytest.fixture
def qa_workflow_controller():
    return WorkflowController(
        workflow_name="junior_developer",
        session_id="test-qa-workflow"
    )

def test_qa_basic_flow(qa_workflow_controller):
    """测试QA基础工作流"""
    print("\nTesting QA Basic Flow...")
    
    test_data = WorkflowStateData(
        project_name="Test Project",
        project_description="A test automation project",
        user_stories=["As a developer, I want to automate testing"],
        acceptance_criteria=["All tests should pass"],
        technical_design="Microservices Architecture",
        implementation_plan="Agile Development",
        code_complete=True,
        unit_tests="All unit tests implemented"
    )
    
    states = ["requirement", "technical", "development", "testing"]
    for state in states:
        success = qa_workflow_controller.try_transition(state, test_data.model_dump())
        print(f"✓ {state.capitalize()} transition: {success}")
        assert success

def test_qa_validation():
    """测试QA验证功能"""
    print("\nTesting QA Validation...")
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-qa-validation"
    )
    
    test_data = WorkflowStateData(
        project_name="Test Project",
        project_description="A test automation project",
        user_stories=["As a developer, I want to automate testing"],
        acceptance_criteria=["All tests should pass"],
        technical_design="Microservices Architecture",
        implementation_plan="Agile Development",
        code_complete=True,
        unit_tests="All unit tests implemented",
        test_results="All tests passed",
        bug_report="No critical bugs found"
    )
    
    # 执行状态转换
    for state in ["requirement", "technical", "development", "testing"]:
        success = controller.try_transition(state, test_data.model_dump())
        print(f"✓ {state.capitalize()} transition: {success}")
        print(f"✓ Current state: {controller.current_state}")
        
        if state == "testing":
            result_data = controller.session_state.get("state_data", {})
            assert result_data.get("test_results") is not None
            assert result_data.get("bug_report") is not None

if __name__ == "__main__":
    pytest.main([__file__])
