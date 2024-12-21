from typing import Dict, Any
from phi.tools.base import Tool
from dataclasses import dataclass

@dataclass
class OperationResult:
    success: bool
    message: str
    data: Dict[str, Any] = None
