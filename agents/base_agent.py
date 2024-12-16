from typing import Dict, Any, List
from phi.agent import Agent
from utils.model_factory import load_model_from_config, load_agent_config
from phi.tools.duckduckgo import DuckDuckGo

class NimshipAgent(Agent):
    def __init__(self, config_path: str):
        # 加载配置
        config = load_agent_config(config_path)
        model = load_model_from_config(config.get("model", {}))
        
        # 初始化工具
        tools = self._initialize_tools(config.get("tools", []))
        
        # 启用更多 phidata 原生特性
        super().__init__(
            name=config.get("name", "Nimship Agent"),
            description=config.get("description", "A configurable AI agent"),
            role=config.get("role"),  # 添加角色支持
            instructions=config.get("instructions", []),  # 添加指令支持
            model=model,
            tools=tools,
            monitoring=True,
            debug_mode=True,
            markdown=True,  # 启用 markdown 支持
            structured_outputs=True,  # 启用结构化输出
            show_tool_calls=True  # 显示工具调用
        )

    def _initialize_tools(self, tool_configs: List[str]) -> List[Any]:
        """初始化工具，支持更灵活的工具配置"""
        tools = []
        for tool in tool_configs:
            if tool == "DuckDuckGo":
                tools.append(DuckDuckGo())
        return tools
