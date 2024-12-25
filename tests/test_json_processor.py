import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from datetime import datetime
from pydantic import BaseModel
from utils.json_processor import JsonProcessor
from workflows.models import WorkflowStateData


class TestModel(BaseModel):
    name: str
    value: int


class TestJsonProcessor:
    def test_clean_content_basic(self):
        """测试基础content清理"""
        data = {
            "content": '{"key": "value"}'
        }
        cleaned = JsonProcessor.clean_content(data)
        assert isinstance(cleaned["content"], dict)
        assert cleaned["content"]["key"] == "value"

    def test_clean_content_nested(self):
        """测试嵌套content清理"""
        data = {
            "content": '{"level1": {"level2": {"level3": "value"}}}'
        }
        cleaned = JsonProcessor.clean_content(data)
        assert cleaned["content"]["level1"]["level2"]["level3"] == "value"

    def test_clean_content_invalid_json(self):
        """测试无效JSON的content处理"""
        data = {
            "content": "Invalid JSON {key: value}"
        }
        cleaned = JsonProcessor.clean_content(data)
        assert "raw_content" in cleaned["content"]
        assert cleaned["content"]["raw_content"] == data["content"]

    def test_clean_content_empty(self):
        """测试空数据处理"""
        assert JsonProcessor.clean_content({}) == {}
        assert JsonProcessor.clean_content(None) is None

    def test_safe_serialize_datetime(self):
        """测试datetime序列化"""
        now = datetime.now()
        data = {"timestamp": now}
        serialized = JsonProcessor.safe_serialize(data)
        assert now.isoformat() in serialized

    def test_safe_serialize_pydantic(self):
        """测试Pydantic模型序列化"""
        model = TestModel(name="test", value=123)
        data = {"model": model}
        serialized = JsonProcessor.safe_serialize(data)
        assert '"name":"test"' in serialized.replace(" ", "")
        assert '"value":123' in serialized.replace(" ", "")

    def test_safe_serialize_complex(self):
        """测试复杂对象序列化"""
        class CustomObject:
            def __str__(self):
                return "custom_object"

        data = {
            "custom": CustomObject(),
            "list": [1, "2", 3.0],
            "dict": {"key": "value"}
        }
        serialized = JsonProcessor.safe_serialize(data)
        assert "custom_object" in serialized
        assert "[1,\"2\",3.0]" in serialized.replace(" ", "")

    def test_safe_deserialize_valid(self):
        """测试有效JSON反序列化"""
        json_str = '{"key": "value", "number": 123}'
        data = JsonProcessor.safe_deserialize(json_str)
        assert data["key"] == "value"
        assert data["number"] == 123

    def test_safe_deserialize_invalid(self):
        """测试无效JSON反序列化"""
        invalid_json = '{key: value}'
        data = JsonProcessor.safe_deserialize(invalid_json)
        assert "raw_data" in data
        assert data["raw_data"] == invalid_json

    def test_integration_workflow_data(self):
        """测试工作流数据集成场景"""
        workflow_data = {
            "project_name": "Test Project",
            "content": '''{
                "user_stories": ["Story 1", "Story 2"],
                "acceptance_criteria": ["Criteria 1"],
                "metadata": {"version": "1.0"}
            }''',
            "status": "pending"
        }
        
        # 清理数据
        cleaned = JsonProcessor.clean_content(workflow_data)
        assert isinstance(cleaned["content"], dict)
        assert len(cleaned["content"]["user_stories"]) == 2
        
        # 序列化
        serialized = JsonProcessor.safe_serialize(cleaned)
        assert isinstance(serialized, str)
        
        # 反序列化
        deserialized = JsonProcessor.safe_deserialize(serialized)
        assert deserialized["project_name"] == "Test Project"
        assert len(deserialized["content"]["user_stories"]) == 2

    @pytest.mark.parametrize("input_data,expected_type", [
        ('{"key": "value"}', dict),
        ('["item1", "item2"]', list),
        ('123', int),
        ('"string"', str),
        ('true', bool),
        ('null', type(None))
    ])
    def test_safe_deserialize_types(self, input_data, expected_type):
        """测试不同类型数据的反序列化"""
        result = JsonProcessor.safe_deserialize(input_data)
        assert isinstance(result, expected_type)


if __name__ == "__main__":
    pytest.main([__file__])


def test_agent_response_processing():
    """测试Agent响应数据处理"""
    agent_response = {
        "content": {
            "markdown": """
            ## Technical Analysis
            1. Architecture Review
            2. Performance Analysis
            """,
            "recommendations": [
                {"priority": "high", "item": "Improve error handling"},
                {"priority": "medium", "item": "Add monitoring"}
            ],
            "metrics": {
                "latencyMs": 1500,
                "tokenCount": 250
            }
        },
        "metadata": {
            "agent_id": "tech_leader",
            "timestamp": "2024-01-01T10:00:00Z"
        }
    }
    
    cleaned = JsonProcessor.clean_content(agent_response)
    assert isinstance(cleaned["content"], dict)
    assert "recommendations" in cleaned["content"]
    assert isinstance(cleaned["content"]["recommendations"], list)


def test_nested_workflow_state():
    """测试嵌套的工作流状态数据"""
    workflow_data = {
        "current_state": "technical_review",
        "state_data": {
            "project_name": "Test Project",
            "content": {
                "review_comments": [
                    {"reviewer": "tech_lead", "comment": "Need more details"},
                    {"reviewer": "architect", "comment": "Approved with notes"}
                ],
                "technical_specs": {
                    "architecture": "microservices",
                    "deployment": "kubernetes",
                    "monitoring": {
                        "tools": ["prometheus", "grafana"],
                        "metrics": ["latency", "throughput"]
                    }
                }
            }
        }
    }
    
    cleaned = JsonProcessor.clean_content(workflow_data)
    assert isinstance(cleaned["state_data"]["content"], dict)
    assert isinstance(cleaned["state_data"]["content"]["technical_specs"], dict)


def test_error_recovery():
    """测试错误数据恢复处理"""
    invalid_data = {
        "content": "Invalid JSON: {key: value}",
        "metadata": {
            "valid_key": "valid_value",
            "invalid_json": "{broken: json}",
            "nested": {
                "array": "[1, 2, invalid]"
            }
        }
    }
    
    cleaned = JsonProcessor.clean_content(invalid_data)
    assert "content" in cleaned
    assert cleaned["metadata"]["valid_key"] == "valid_value"
    assert isinstance(cleaned["metadata"]["invalid_json"], str)


def test_special_characters():
    """测试特殊字符处理"""
    special_data = {
        "content": """
        ## Code Review
        
        def test():
            print("Hello \"World\"")
            # Comments with special chars: @#$%^&*
        """,
        "metadata": {
            "path": "C:\\Project\\test.py",
            "unicode": "测试中文",
            "symbols": "!@#$%^&*()"
        }
    }
    
    cleaned = JsonProcessor.clean_content(special_data)
    serialized = JsonProcessor.safe_serialize(cleaned)
    deserialized = JsonProcessor.safe_deserialize(serialized)
    
    assert isinstance(deserialized, dict)
    assert "content" in deserialized
    assert "metadata" in deserialized


test_data = [
    ({"content": None}, {"content": {}}),  # None转换为空字典
    ({"content": ""}, {"content": {"raw_content": ""}}),
    ({"content": []}, {"content": []}),
    ({"content": {}}, {"content": {}}),
    ({"content": 123}, {"content": 123}),  # 保持数字类型
    ({"content": True}, {"content": True})  # 保持布尔类型
]

@pytest.mark.parametrize("input_data,expected", test_data)
def test_content_type_handling(input_data, expected):
    """测试不同类型content处理"""
    cleaned = JsonProcessor.clean_content(input_data)
    assert cleaned == expected




def test_workflow_state_validation():
    """测试工作流状态数据验证"""
    state_data = {
        "project_name": "Test Project",
        "project_description": "Test Description",
        "user_stories": ["Story 1"],
        "acceptance_criteria": ["Criteria 1"],
        "content": {
            "technical_review": {
                "status": "approved",
                "comments": ["Good design"]
            }
        }
    }
    
    workflow_state = WorkflowStateData(**state_data)
    cleaned = JsonProcessor.clean_content(workflow_state.model_dump())
    
    assert "project_name" in cleaned
    assert cleaned["project_name"] == "Test Project"