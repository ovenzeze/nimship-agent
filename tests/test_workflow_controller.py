import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController

def test_agent_execution():
    print("\nTesting Agent Execution...")
    
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-agent-execution"
    )
    
    # 准备完整的初始状态数据
    init_data = {
        "project_name": "Test Project",
        "project_description": "A test automation project",
        "user_stories": [
            "As a developer, I want to automate testing",
            "As a user, I want reliable software"
        ],
        "acceptance_criteria": [
            "All tests should pass",
            "Code coverage > 80%"
        ]
    }
    
    # 测试Product Manager的需求分析任务
    success = controller.try_transition("requirement", init_data)
    print(f"✓ Product Manager task execution: {success}")
    print(f"✓ New state: {controller.current_state}")
    print(f"✓ Updated data: {controller.session_state.get('state_data')}")

def main():
    print("Testing WorkflowController...")
    
    # 基础功能测试
    controller = WorkflowController(
        workflow_name="junior_developer",
        session_id="test-session"
    )
    
    print(f"✓ Initial state: {controller.current_state}")
    
    # 测试有效转换
    valid_data = {
        "project_name": "Test Project",
        "project_description": "A test project"
    }
    success = controller.try_transition("requirement", valid_data)
    print(f"✓ Valid transition result: {success}")
    
    # 测试无效转换
    invalid_success = controller.try_transition("testing", {})
    print(f"✓ Invalid transition blocked: {not invalid_success}")
    
    # 测试数据验证
    invalid_data = {"project_name": "Test Project"}
    invalid_data_success = controller.try_transition("requirement", invalid_data)
    print(f"✓ Invalid data blocked: {not invalid_data_success}")
    
    # 执行Agent测试
    test_agent_execution()

if __name__ == "__main__":
    main()
