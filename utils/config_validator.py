import json
import os
from typing import Dict, Any

def validate_agent_config(config_path: str) -> bool:
    """验证 agent 配置文件的格式和必需字段"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        required_fields = ['name', 'description', 'model']
        for field in required_fields:
            if field not in config:
                print(f"❌ 配置缺少必需字段: {field}")
                return False
                
        if 'model' in config:
            if 'type' not in config['model'] or 'name' not in config['model']:
                print("❌ model 配置缺少 type 或 name 字段")
                return False
                
        return True
    except Exception as e:
        print(f"❌ 配置验证失败: {str(e)}")
        return False