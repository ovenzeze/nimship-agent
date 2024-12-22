import logging
from phi.agent import Agent
from phi.tools.phi import PhiTools

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_phi_agent():
    try:
        # Create an Agent with the Phi tool, explicitly using bedrock model
        agent = Agent(tools=[PhiTools()], name="Phi Workspace Manager", model="bedrock")
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
        response = agent.print_response(operation, markdown=True)
        logger.info(f"Operation executed: {operation}")
        return response
    except Exception as e:
        logger.error(f"Failed to execute operation '{operation}': {str(e)}")

def main():
    agent = create_phi_agent()
    if agent:
        # Example 1: Create a new agent app
        execute_agent_operation(agent, "Create a new agent-app called agent-app-turing")

        # Example 2: Start a workspace
        execute_agent_operation(agent, "Start the workspace agent-app-turing")

if __name__ == "__main__":
    main()
