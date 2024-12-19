import json

# 文件路径
MODEL_CONFIG_FILE = "/Users/clayzhang/Code/nimship-agent/bedrock_models.json"

def update_model_ids(file_path):
    """更新模型的 modelId 字段，对 inferenceTypesSupported 包含 'INFERENCE_PROFILE' 的模型添加 'us.' 前缀"""
    try:
        # 读取配置文件
        with open(file_path, "r") as file:
            models = json.load(file)

        # 遍历模型列表并更新 modelId
        for model in models:
            if "INFERENCE_PROFILE" in model.get("inferenceTypesSupported", []):
                if not model["modelId"].startswith("us."):
                    old_model_id = model["modelId"]
                    model["modelId"] = f"us.{old_model_id}"
                    print(f"[UPDATED] {old_model_id} -> {model['modelId']}")

        # 写回更新后的文件
        with open(file_path, "w") as file:
            json.dump(models, file, indent=4)
        print(f"\n更新完成，文件已保存到 {file_path}")

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到！请确保文件路径正确。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 格式无效！请检查文件内容是否为有效 JSON。")
    except Exception as e:
        print(f"处理文件时发生错误: {str(e)}")

if __name__ == "__main__":
    update_model_ids(MODEL_CONFIG_FILE)