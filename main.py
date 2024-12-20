import os
import sys
import json
import select
from typing import List, Dict
from agents.base_agent import NimshipAgent
from utils.model_factory import load_agent_config
from phi.playground import Playground, serve_playground_app

def get_input(prompt, default=None):
    print(prompt, end='', flush=True)
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        return sys.stdin.readline().strip()
    else:
        print(f"\nNo input provided. Using default: {default}")
        return default

def get_agent_config_suffix(config_file: str = "config/system.config.json") -> str:
    """从 system.config.json 中加载 agent 配置文件后缀"""
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config.get("agent_config_suffix", ".agent.json")
    except FileNotFoundError:
        print(f"Warning: {config_file} not found. Using default suffix '.agent.json'")
        return ".agent.json"
def get_available_agents(config_dir: str, suffix: str) -> List[str]:
    """获取指定后缀的 Agent 配置文件"""
    agents = []
    for file in os.listdir(config_dir):
        if file.endswith(suffix):
            agents.append(file)
    return agents

# 列出所有可用的 Workflows (假定存储在 workflows 目录中)
def get_available_workflows(workflow_dir: str) -> List[str]:
    workflows = []
    for file in os.listdir(workflow_dir):
        if file.endswith(".py"):
            workflows.append(file)
    return workflows

# 运行指定的 Agent
def run_agent(config_path: str, prompt: str, mode: str):
    if mode == "cli":
        # 无头模式运行
        agent = NimshipAgent(config_path)
        response = agent.run(prompt)
        print("Agent Response:", response)
    elif mode == "ui":
        # Web UI 模式运行
        agent = NimshipAgent(config_path)
        app = Playground(agents=[agent]).get_app()
        serve_playground_app("playground:app", reload=True)
    else:
        print("Invalid mode selected. Please choose 'cli' or 'ui'.")

# 主函数
def main():
    print("Starting main function")
    config_dir = "./config"  # 假定所有 Agent 配置文件存储在 config 目录中
    workflow_dir = "./workflows"  # 假定所有 Workflows 存储在 workflows 目录中
    
    print("Welcome to Nimship Agent!")
    
    try:
        print("Getting agent config suffix")
        agent_config_suffix = get_agent_config_suffix()
        print(f"Agent config suffix: {agent_config_suffix}")
        
        print("Getting available agents")
        agents = get_available_agents(config_dir, agent_config_suffix)
        print("Available Agents:")
        if agents:
            for idx, agent in enumerate(agents):
                print(f"{idx + 1}. {agent}")
        else:
            print("No agents found.")
        
        print("Getting available workflows")
        workflows = get_available_workflows(workflow_dir)
        print("\nAvailable Workflows:")
        if workflows:
            for idx, workflow in enumerate(workflows):
                print(f"{idx + 1}. {workflow}")
        else:
            print("No workflows found.")
        
        if not agents and not workflows:
            print("No agents or workflows available. Exiting.")
            return
        
        print("\nWhat would you like to do?")
        if agents:
            print("1. Run an Agent")
        if workflows:
            print("2. Run a Workflow")
        print("Waiting for user input...")
        choice = get_input("Enter your choice (1/2): ", "1")
        print(f"User chose: {choice}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return

    if choice == "1" and agents:
        agent_idx = int(get_input("Select an Agent by number: ", "1")) - 1
        if agent_idx < 0 or agent_idx >= len(agents):
            print("Invalid Agent selection. Selecting the first agent.")
            agent_idx = 0
        config_path = os.path.join(config_dir, agents[agent_idx])
        prompt = get_input("Enter a prompt for the Agent: ", "Hello, Agent!")
        mode = get_input("Choose mode (cli/ui): ", "cli")
        run_agent(config_path, prompt, mode)
    elif choice == "2" and workflows:
        workflow_idx = int(get_input("Select a Workflow by number: ", "1")) - 1
        if workflow_idx < 0 or workflow_idx >= len(workflows):
            print("Invalid Workflow selection. Selecting the first workflow.")
            workflow_idx = 0
        workflow_path = os.path.join(workflow_dir, workflows[workflow_idx])
        print(f"Running Workflow: {workflow_path}")
        os.system(f"python {workflow_path}")
    else:
        print("Invalid choice or no agents/workflows available. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
