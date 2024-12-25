from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

class AgentResponse(BaseModel):
    content: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    last_updated: Optional[str] = None

class WorkflowStateData(BaseModel):
    project_name: str
    project_description: str
    user_stories: List[str] = Field(default_factory=list)
    acceptance_criteria: List[str] = Field(default_factory=list)
    content: Union[Dict[str, Any], str] = Field(default_factory=dict)
    status: str = Field(default="pending")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    last_updated: Optional[datetime] = None

    @field_validator('content', mode='before')
    @classmethod
    def validate_content(cls, v):
        if isinstance(v, str):
            return {
                'raw_content': v,
                'format': 'markdown' if '#' in v else 'text'
            }
        return v
