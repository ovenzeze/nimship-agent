from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class OperationResult:
    success: bool
    message: str
    data: Dict[str, Any] = None

class Tool:
    pass
