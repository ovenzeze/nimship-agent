import os
import sys
from typing import List

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.workflow_controller import WorkflowController, WorkflowState

def test_basic_workflow():
    """测试基本工作流程"""
    print("\n=== 测试基本工作流 ===")
    
    # 1. 初始化工作流
    controller = WorkflowController("config/test_workflow.json")
    print(f"初始状态: {controller.current_state}")
    
    # 2. 测试状态转换
    test_task = {
        "type": "code_review",
        "content": "Review test.py",
        "trigger_condition": "start_development"
    }
    
    # 3. 运行工作流
    responses = list(controller.run(test_task))
    
    # 4. 验证结果
    print(f"最终状态: {controller.current_state}")
    print(f"响应数量: {len(responses)}")
    for resp in responses:
        print(f"响应内容: {resp.content}")

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    
    controller = WorkflowController("config/test_workflow.json")
    
    # 测试无效状态转换
    invalid_task = {
        "type": "invalid",
        "content": "This should fail",
        "trigger_condition": "invalid_condition"
    }
    
    responses = list(controller.run(invalid_task))
    print(f"错误处理状态: {controller.current_state}")
    for resp in responses:
        print(f"错误响应: {resp.content}")

def main():
    """运行所有测试"""
    test_basic_workflow()
    test_error_handling()

if __name__ == "__main__":
    main()
