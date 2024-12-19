import json

# 文件路径
full_models_path = "/Users/clayzhang/Code/nimship-agent/bedrock_models_full.json"
filtered_models_path = "/Users/clayzhang/Code/nimship-agent/bedrock_models.json"

# 筛选逻辑
def filter_models(models):
    filtered = []

    # Anthropic: 保留更多版本
    for model in models:
        if model["providerName"] == "Anthropic":
            if "claude" in model["modelId"]:
                filtered.append(model)

    # Meta: 保留所有参数版本
    for model in models:
        if model["providerName"] == "Meta":
            if "llama3" in model["modelId"]:
                filtered.append(model)

    # Amazon: 常用模型
    for model in models:
        if model["providerName"] == "Amazon":
            if model["modelId"] in [
                "amazon.titan-tg1-large",
                "amazon.titan-image-generator-v2:0"
            ]:
                filtered.append(model)

    # Cohere: 常用模型
    for model in models:
        if model["providerName"] == "Cohere":
            if model["modelId"] in [
                "cohere.command-text-v14",
                "cohere.embed-multilingual-v3"
            ]:
                filtered.append(model)

    return filtered

# 读取完整模型文件
with open(full_models_path, "r") as f:
    full_models_data = json.load(f)

# 提取模型列表
full_models = full_models_data["modelSummaries"]

# 应用筛选逻辑
filtered_models = filter_models(full_models)

# 写入到新的文件
with open(filtered_models_path, "w") as f:
    json.dump(filtered_models, f, indent=4)

print(f"筛选完成，共保留 {len(filtered_models)} 个模型，已保存到 {filtered_models_path}")