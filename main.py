import os
import sys
import json
import time
import logging
from pathlib import Path  # Unused import
from typing import List, Dict
from workflows.workflow_controller import WorkflowController
from workflows.models import WorkflowStateData

# Configure logging
logging.basicConfig(filename='workflow.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def load_system_config(config_file: str = "config/system.config.json") -> dict:
    """加载系统配置"""
    with open(config_file, 'r') as f:
        return json.load(f)


def get_input(prompt: str) -> str:
    """持续等待用户输入直到得到有效值"""
    while True:
        print(prompt, end='', flush=True)
        user_input = sys.stdin.readline().strip()
        if user_input:
            return user_input
        print("Please provide input")


def parse_args():
    """处理命令行参数"""
    import argparse
    parser = argparse.ArgumentParser(description='Nimship Agent CLI')
    parser.add_argument('--workflow', type=str, help='Workflow name to run')
    parser.add_argument('--mode', choices=['cli', 'ui'], default='cli', help='Running mode')
    parser.add_argument('--silent', action='store_true', help='Run in silent mode')
    return parser.parse_args()


def get_available_workflows(workflow_dir: str) -> List[Dict]:
    """获取可用的workflows及其详细信息"""
    workflows = []
    for file in os.listdir(workflow_dir):
        if file.endswith(".workflow.json"):
            workflow_path = os.path.join(workflow_dir, file)
            try:
                with open(workflow_path, 'r') as f:
                    config = json.load(f)
                    workflows.append({
                        'filename': file,
                        'path': workflow_path,
                        'name': config.get('name', ''),
                        'description': config.get('description', ''),
                        'agents': [agent['name'] for agent in config.get('agents', [])]
                    })
            except Exception as e:
                print(f"Error loading workflow {file}: {str(e)}")
    return workflows


def display_workflows(workflows: List[Dict]):
    """展示workflow信息"""
    print("\nAvailable Workflows:")
    for idx, workflow in enumerate(workflows, 1):
        print(f"\n{idx}. {workflow['name']}")
        print(f"   Description: {workflow['description']}")
        print(f"   Collaborating Agents: {', '.join(workflow['agents'])}")


def load_workflow_input(config_dir: str, input_file: str) -> dict:
    """加载workflow输入数据"""
    input_path = os.path.join(config_dir, input_file)
    with open(input_path, 'r') as f:
        return json.load(f)


def run_workflow(workflow_path: str, mode: str):
    """运行workflow"""
    # 创建工作流实例 - 一次性完成所有初始化
    controller = WorkflowController(
        workflow_path=workflow_path,
        session_id=f"session-{int(time.time())}"
    )
    
    # 执行工作流程
    workflow_states = [
        ("requirement", "product_manager"),
        ("technical", "tech_leader"),
        ("development", "engineer"),
        ("testing", "qa_engineer")
    ]
    
    state_data = WorkflowStateData(**controller.input_data)
    
    for state, agent in workflow_states:
        print(f"\n→ Transitioning to {state}")
        print(f"→ Agent: {agent}")
        
        success = controller.try_transition(state, state_data.model_dump())
        if not success:
            print(f"! Workflow stopped at {state}")
            return False
            
        print(f"✓ Completed state: {state}")
        if controller.session_state.get("state_data"):
            state_data = WorkflowStateData(**controller.session_state["state_data"])
    
    print("\n✓ Workflow completed successfully")
    return True


def main():
    args = parse_args()
    
    # 加载系统配置
    system_config = load_system_config()
    workflow_dir = os.path.join(".", system_config['paths']['workflow_config_dir'])
    
    if args.workflow:
        workflow_path = os.path.join(workflow_dir, f"{args.workflow}.workflow.json")
        if os.path.exists(workflow_path):
            return run_workflow(workflow_path, args.mode)
        else:
            print(f"Workflow not found: {args.workflow}")
            return False
    
    print("Welcome to Nimship Agent!")
    
    workflows = get_available_workflows(workflow_dir)
    if not workflows:
        print("No workflows available")
        return
        
    display_workflows(workflows)
    
    workflow_idx = int(get_input("\nSelect a Workflow by number: ")) - 1
    if 0 <= workflow_idx < len(workflows):
        selected_workflow = workflows[workflow_idx]
        mode = get_input("Choose mode (cli/ui): ")
        run_workflow(selected_workflow['path'], mode)
    else:
        print("Invalid workflow selection")


if __name__ == "__main__":
    main()
