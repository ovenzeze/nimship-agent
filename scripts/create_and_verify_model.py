import requests
import os
import json
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中读取 AWS 凭据
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # 默认区域为 us-east-1

# API endpoints and headers
BASE_URL = "http://localhost:4000"
CREATE_URL = f"{BASE_URL}/model/new"
HEADERS = {
    "Authorization": "Bearer sk-cVek69kBvShIm0DjXPomJQ",  # 替换为您的 API Key
    "Content-Type": "application/json"
}

# 配置文件路径
MODEL_CONFIG_FILE = "bedrock_models.json"

def load_model_config():
    """从配置文件中加载模型数据"""
    try:
        with open(MODEL_CONFIG_FILE, "r") as file:
            models = json.load(file)
            if not models or not isinstance(models, list):
                raise ValueError("配置文件内容无效或未包含模型列表")
            return models
    except FileNotFoundError:
        print(f"配置文件 {MODEL_CONFIG_FILE} 未找到！请确保文件存在。")
        return []
    except json.JSONDecodeError:
        print(f"配置文件 {MODEL_CONFIG_FILE} 格式无效！请检查文件内容是否为有效 JSON。")
        return []
    except Exception as e:
        print(f"加载配置文件时出错: {str(e)}")
        return []

def create_model(model_data):
    """调用创建模型接口"""
    payload = {
        "model_name": model_data["modelName"],
        "litellm_params": {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "aws_region_name": AWS_REGION,
            "model": f"bedrock/{model_data['modelId']}",
            "timeout": 60,
            "max_retries": 3
        },
        "model": f"{model_data['modelId']}",
        "model_info": {
            "id": model_data["modelId"],
            "db_model": True,
            "base_model": model_data["modelName"],
            "providerName": model_data["providerName"],
            "modelARN": model_data["modelArn"],
            "key": model_data["modelId"]
        }
    }

    try:
        response = requests.post(CREATE_URL, headers=HEADERS, json=payload)
        if response.status_code in [200, 201]:
            print(f"[SUCCESS] 模型 '{model_data['modelId']}' 创建成功")
        else:
            print(f"[ERROR] 模型 '{model_data['modelId']}' 创建失败 - 状态码: {response.status_code}")
    except Exception as e:
        print(f"[EXCEPTION] 模型 '{model_data['modelId']}' 创建时出错: {str(e)}")

def process_models(models, batch_size=5):
    """批量处理模型创建，按批次暂停等待用户确认"""
    total_models = len(models)
    print(f"共加载 {total_models} 个模型，开始创建...")

    for i in range(0, total_models, batch_size):
        batch = models[i:i + batch_size]
        print(f"\n正在创建第 {i + 1} 到第 {i + len(batch)} 个模型...")

        for model in batch:
            create_model(model)

        if i + batch_size < total_models:
            input("\n已完成一批模型创建。按回车键继续创建下一批...")

if __name__ == "__main__":
    # 加载配置文件
    model_config = load_model_config()

    if model_config:
        # 按批次处理模型
        process_models(model_config)
    else:
        print("未加载到有效的模型配置，程序终止。")
