import logging
import os
from phi.agent import Agent
from phi.tools.phi import PhiTools
from phi.llm.openai import OpenAIChat

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MockLLM:
    def __init__(self):
        self.responses = {
            "Create a new agent-app called agent-app-turing": "New agent-app 'agent-app-turing' created successfully.",
            "Start the workspace agent-app-turing": "Workspace 'agent-app-turing' started successfully."
        }

    def complete(self, prompt, **kwargs):
        return self.responses.get(prompt, "Operation completed.")

def create_phi_agent():
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            model = OpenAIChat(model="gpt-3.5-turbo")
        else:
            logger.warning("No OpenAI API key found. Using mock LLM.")
            model = MockLLM()
        
        agent = Agent(tools=[PhiTools()], name="Phi Workspace Manager", llm=model, debug_mode=True)
        logger.info("Phi Workspace Manager agent created successfully")
        return agent
    except Exception as e:
        logger.error(f"Failed to create Phi Workspace Manager agent: {str(e)}")
        return None

def execute_agent_operation(agent, operation):
    if agent is None:
        logger.error("Agent is not initialized")
        return

    try:
        logger.debug(f"Executing operation: {operation}")
        if isinstance(agent.llm, MockLLM):
            response = agent.llm.complete(operation)
        else:
            response = agent.run(operation)
        logger.info(f"Operation executed: {operation}")
        logger.debug(f"Response: {response}")
        return response
    except Exception as e:
        logger.error(f"Failed to execute operation '{operation}': {str(e)}")

def main():
    print("Starting main function")
    logger.debug("Starting main function")
    agent = create_phi_agent()
    if agent:
        print("Agent created successfully")
        # Example 1: Create a new agent app
        print("Executing: Create a new agent-app called agent-app-turing")
        execute_agent_operation(agent, "Create a new agent-app called agent-app-turing")

        # Example 2: Start a workspace
        print("Executing: Start the workspace agent-app-turing")
        execute_agent_operation(agent, "Start the workspace agent-app-turing")
    else:
        print("Failed to create agent")
    print("Ending main function")
    logger.debug("Ending main function")

if __name__ == "__main__":
    main()
