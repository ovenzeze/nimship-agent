import json
from typing import Dict, Any
from phi.model.aws.claude import Claude as BedrockClaude

def load_model_from_config(config: Dict[str, Any]):
    model_type = config.get("type", "bedrock").lower()
    model_name = config.get("name", "anthropic.claude-instant-v1")
    
    if model_type == "bedrock":
        return BedrockClaude(id=model_name)
    else:
        raise ValueError(f"Unsupported model type: {model_type}. Only 'bedrock' is supported.")

def load_agent_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r') as f:
        return json.load(f)
