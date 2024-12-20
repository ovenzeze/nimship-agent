import sys
from agents.base_agent import NimshipAgent

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_agent.py <config_file> <prompt>")
        sys.exit(1)

    config_file = sys.argv[1]
    prompt = sys.argv[2]

    # 使用指定的配置文件初始化 agent
    agent = NimshipAgent(config_file)
    
    # 运行 agent，phiData 的监控和调试功能已内置
    response = agent.run(prompt)
    
    # 打印响应
    print("Agent Response:", response)

if __name__ == '__main__':
    main()
