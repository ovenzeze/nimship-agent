import sys
import os
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from workflows.workflow_controller import WorkflowController
from workflows.workflow_loader import WorkflowConfigLoader
from workflows.models import WorkflowStateData
from phi.utils.log import logger

@pytest.fixture
def workflow_config():
    config_dir = Path("config/workflows")
    workflow_path = config_dir / "junior_developer.workflow.json"
    loader = WorkflowConfigLoader(config_dir)
    return loader.load_workflow(workflow_path)

def test_qa_validation(workflow_config):
    """测试QA验证功能"""
    print("\nTesting QA Validation...")
    
    controller = WorkflowController(
        workflow_config=workflow_config,
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
    
    states = ["requirement", "technical", "development"]
    for state in states:
        success = controller.try_transition(state, test_data.model_dump())
        print(f"✓ {state.capitalize()} transition: {success}")
        assert success
    
    print("\n→ 执行QA测试阶段")
    success = controller.try_transition("testing", test_data.model_dump())
    print(f"✓ QA测试结果: {success}")
    
    result_data = controller.session_state.get("state_data", {})
    print("\n→ QA测试数据验证:")
    print(f"- 测试结果: {result_data.get('test_results')}")
    print(f"- 缺陷报告: {result_data.get('bug_report')}")
    
    assert result_data.get("test_results") is not None
    assert result_data.get("bug_report") is not None
    assert controller.current_state == "testing"
