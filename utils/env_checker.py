import os
from typing import List, Dict

def check_required_env_vars() -> Dict[str, bool]:
    """检查必需的环境变量"""
    required_vars = {
        'AWS_ACCESS_KEY_ID': False,
        'AWS_SECRET_ACCESS_KEY': False,
        'AWS_REGION': False,
        'PHI_API_KEY': False
    }
    
    for var in required_vars:
        if os.getenv(var):
            required_vars[var] = True
            
    return required_vars