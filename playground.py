from phi.agent import Agent
from phi.storage.agent.sqlite import SqlAgentStorage
from phi.playground import Playground, serve_playground_app
from agents.base_agent import NimshipAgent
from utils.model_factory import load_agent_config

def create_agent(config_path):
    config = load_agent_config(config_path)
    return NimshipAgent(config_path)

web_agent = create_agent("/Users/clayzhang/Code/nimship-agent/config/web.agent.json")

app = Playground(agents=[web_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
