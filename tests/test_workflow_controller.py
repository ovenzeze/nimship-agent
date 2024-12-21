import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from workflows.workflow_controller import WorkflowController
from workflows.models import WorkflowStateData

@pytest.fixture
def workflow_controller():
    return WorkflowController(
        workflow_name="junior_developer",
        session_id="test-session"
    )

def test_workflow_initialization(workflow_controller):
    assert workflow_controller.current_state == "init"
    print(f"✓ Initial state: {workflow_controller.current_state}")

def test_valid_transition(workflow_controller):
    valid_data = WorkflowStateData(
        project_name="Test Project",
        project_description="A test project",
        user_stories=["As a user, I want to test"],
        acceptance_criteria=["Test passes"]
    )
    
    success = workflow_controller.try_transition("requirement", valid_data.model_dump())
    print(f"✓ Valid transition result: {success}")
    assert success

def test_invalid_transition(workflow_controller):
    invalid_success = workflow_controller.try_transition("testing", {})
    print(f"✓ Invalid transition blocked: {not invalid_success}")
    assert not invalid_success

def test_invalid_data(workflow_controller):
    invalid_data = {"project_name": "Test Project"}
    invalid_data_success = workflow_controller.try_transition("requirement", invalid_data)
    print(f"✓ Invalid data blocked: {not invalid_data_success}")
    assert not invalid_data_success

def test_agent_execution():
    print("\nTesting Agent Execution...")
    
    test_data = WorkflowStateData(
        project_name="Test Project",
        project_description="A test automation project",
        user_stories=["As a developer, I want to automate testing"],
        acceptance_criteria=["All tests should pass"]
    )
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-agent-execution"
    )
    
    success = controller.try_transition("requirement", test_data.model_dump())
    print(f"✓ Requirement transition: {success}")
    print(f"✓ Current state: {controller.current_state}")
    
    if success:
        result_data = controller.session_state.get("state_data", {})
        assert result_data.get("content") is not None
        assert result_data.get("status") in ["success", "pending", "error"]
        print("✓ Agent execution test passed")

if __name__ == "__main__":
    pytest.main([__file__])
