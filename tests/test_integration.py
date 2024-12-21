import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController
from workflows.models import WorkflowStateData

def test_complete_workflow():
    """测试完整工作流程"""
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-integration"
    )
    
    test_data = WorkflowStateData(
        project_name="Integration Test Project",
        project_description="End-to-end workflow test",
        user_stories=["As a user, I want a complete system test"],
        acceptance_criteria=["All components work together"],
        technical_design="Full Stack Architecture",
        implementation_plan="Agile with CI/CD",
        code_complete=True,
        unit_tests="Comprehensive test suite",
        test_results="System validation complete",
        bug_report="Integration verified"
    )
    
    workflow_states = [
        ("requirement", "product_manager"),
        ("technical", "tech_leader"),
        ("development", "engineer"),
        ("testing", "qa_engineer")
    ]
    
    for state, agent in workflow_states:
        success = controller.try_transition(state, test_data.model_dump())
        print(f"✓ {state.capitalize()} phase with {agent}: {success}")
        assert success
        assert controller.current_state == state
