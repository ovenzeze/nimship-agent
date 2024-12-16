def _validate_model_config(self, model_config: Dict) -> bool:
    """验证模型配置"""
    if model_config.get("type") != "bedrock":
        raise ValueError("只支持 bedrock 类型的模型")
    
    supported_models = [
        "anthropic.claude-3-sonnet-20240229-v1:0",
        "anthropic.claude-instant-v1"
    ]
    if model_config.get("name") not in supported_models:
        raise ValueError(f"不支持的模型: {model_config.get('name')}")
    
    return True