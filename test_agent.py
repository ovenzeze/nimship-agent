import os
import sys
import json
import boto3
from agents.base_agent import NimshipAgent
from phi.utils.pprint import pprint_run_response

def test_aws_bedrock_credentials():
    """验证 AWS Bedrock 凭证"""
    try:
        bedrock = boto3.client('bedrock-runtime')
        print("✅ AWS Bedrock 凭证验证成功")
        return True
    except Exception as e:
        print(f"❌ AWS Bedrock 凭证验证失败: {str(e)}")
        print("请检查环境变量: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION")
        return False

def test_agent_initialization(config_path):
    """测试 Agent 初始化"""
    try:
        if not os.path.exists(config_path):
            print(f"❌ 配置文件不存在: {config_path}")
            return None
            
        agent = NimshipAgent(config_path)
        print(f"✅ Agent 初始化成功 (配置: {config_path})")
        return agent
    except Exception as e:
        print(f"❌ Agent 初始化失败 (配置: {config_path}): {str(e)}")
        return None

def test_agent_run(agent, prompt):
    """测试 Agent 运行"""
    try:
        response = agent.run(prompt)
        print("✅ Agent 运行成功")
        print(f"Response type: {type(response)}")
        
        if isinstance(response, dict):
            print("Response is a dictionary")
            print(f"Response keys: {response.keys()}")
            if 'content' in response:
                print(f"Response content: {response['content']}")
            elif 'text' in response:
                print(f"Response text: {response['text']}")
            else:
                print("Response does not have 'content' or 'text' key")
        elif hasattr(response, '__dict__'):
            print("Response is an object")
            if hasattr(response, 'content'):
                print(f"Response content: {response.content}")
            elif hasattr(response, 'text'):
                print(f"Response text: {response.text}")
            else:
                print("Response does not have 'content' or 'text' attribute")
        else:
            print(f"Unexpected response type: {type(response)}")
            print(f"Response: {response}")

        pprint_run_response(response, markdown=True)
        return True
    except Exception as e:
        print(f"❌ Agent 运行失败: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error attributes: {dir(e)}")
        return False

def test_team_agent():
    """测试团队 Agent 运行"""
    print("\n开始测试团队 Agent...")
    team_config = 'config/development_team.agent.json'
    
    # 检查所有必需的配置文件
    required_configs = [
        team_config,
        'config/product_manager.agent.json',
        'config/tech_leader.agent.json',
        'config/engineer.agent.json',
        'config/qa_engineer.agent.json'
    ]
    
    for config in required_configs:
        if not os.path.exists(config):
            print(f"❌ 缺少必需的配置文件: {config}")
            return False
            
        # 验证每个配置文件中的模型设置
        try:
            with open(config) as f:
                cfg = json.load(f)
                if cfg.get("model", {}).get("type") != "bedrock":
                    print(f"❌ {config} 中的模型类型不是 bedrock")
                    return False
        except Exception as e:
            print(f"❌ 读取配置文件失败 {config}: {str(e)}")
            return False
    
    team_agent = test_agent_initialization(team_config)
    if not team_agent:
        return False
    
    print("开始测试团队协作...")
    prompt = "开发一个简单的待办事项应用"
    return test_agent_run(team_agent, prompt)

def main():
    print("🚀 Nimship Agent 测试开始")
    
    # 检查 AWS 凭证
    if not test_aws_bedrock_credentials():
        sys.exit(1)
    
    # 测试单个 Agent
    single_agent_config = 'config/web.agent.json'
    single_agent = test_agent_initialization(single_agent_config)
    if not single_agent:
        sys.exit(1)
    
    if not test_agent_run(single_agent, "使用 DuckDuckGo 搜索最近的 AI 技术发展"):
        sys.exit(1)
    
    # 测试团队 Agent
    if not test_team_agent():
        sys.exit(1)
    
    print("🎉 Nimship Agent 测试全部通过")

if __name__ == '__main__':
    main()
