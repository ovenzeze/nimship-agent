from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class AgentResponse(BaseModel):
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    last_updated: Optional[str] = None

class WorkflowStateData(BaseModel):
    project_name: str
    project_description: str
    user_stories: List[str]
    acceptance_criteria: List[str]
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    last_updated: Optional[str] = None
    
    # 可选技术字段
    technical_design: Optional[str] = None
    implementation_plan: Optional[str] = None
    code_complete: Optional[bool] = None
    unit_tests: Optional[str] = None
    test_results: Optional[str] = None
    bug_report: Optional[str] = None
