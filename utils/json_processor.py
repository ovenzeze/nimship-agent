import json
from typing import Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel
from phi.utils.log import logger
class JsonProcessor:
    @staticmethod
    def clean_content(data: Dict[str, Any]) -> Dict[str, Any]:
        """清理和规范化内容"""
        if not data:
            return {}
            
        result = data.copy()
        
        if 'content' in result:
            content = result['content']
            if isinstance(content, str):
                result['content'] = {
                    'raw_content': content,
                    'format': 'markdown' if '#' in content else 'text'
                }
        
        return result
    @staticmethod
    def safe_serialize(data: Any) -> str:
        """安全序列化为JSON字符串"""
        try:
            def serialize_item(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()
                if isinstance(obj, BaseModel):
                    return obj.model_dump()
                if hasattr(obj, '__str__'):
                    return str(obj)
                return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)
                
            return json.dumps(data, default=serialize_item, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Serialization error: {str(e)}")
            return str(data)
    @staticmethod
    def safe_deserialize(json_str: str) -> Union[Dict[str, Any], list, str, int, bool, None]:
        """安全反序列化JSON字符串"""
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            logger.error(f"Deserialization error for: {json_str}")
            return {"raw_data": json_str}
        except Exception as e:
            logger.error(f"Unexpected deserialization error: {str(e)}")
            return {"error": str(e), "raw_data": json_str}

    @staticmethod
    def merge_content(original: Dict[str, Any], update: Dict[str, Any]) -> Dict[str, Any]:
        """合并两个内容字典"""
        result = original.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = JsonProcessor.merge_content(result[key], value)
            else:
                result[key] = value
                
        return result

    @staticmethod
    def validate_structure(data: Dict[str, Any], required_fields: list = None) -> bool:
        """验证数据结构"""
        if required_fields is None:
            required_fields = ["content"]
            
        try:
            return all(field in data for field in required_fields)
        except Exception as e:
            logger.error(f"Validation error: {str(e)}")
            return False
