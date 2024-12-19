# LiteLLM Docker 部署报告

## 引言
- 本报告旨在分析和总结 LiteLLM 的 Docker 部署方案和最佳实践
- LiteLLM 作为一个 LLM 代理服务，提供了多种部署选项，包括基础部署、数据库集成部署以及高可用集群部署

## 第1部分：快速部署方案
### 基础部署步骤
1. 克隆代码并配置环境
```bash
# 获取代码
git clone https://github.com/BerriAI/litellm
cd litellm

# 配置环境变量
echo 'LITELLM_MASTER_KEY="sk-1234"' > .env
echo 'LITELLM_SALT_KEY="sk-1234"' >> .env
source .env

# 启动服务
docker-compose up
```

2. 创建配置文件 `litellm_config.yaml`
```yaml
model_list:
  - model_name: azure-gpt-3.5
    litellm_params:
      model: azure/<your-azure-model-deployment>
      api_base: os.environ/AZURE_API_BASE
      api_key: os.environ/AZURE_API_KEY
      api_version: "2023-07-01-preview"
```

3. 运行 Docker 镜像
```bash
docker run \
  -v $(pwd)/litellm_config.yaml:/app/config.yaml \
  -e AZURE_API_KEY=d6*********** \
  -e AZURE_API_BASE=https://openai-***********/ \
  -p 4000:4000 \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml --detailed_debug
```

## 第2部分：高级部署方案
### 数据库集成部署
1. 前置要求：
   - PostgreSQL 数据库（如 Supabase、Neon 等）
   - 设置 `DATABASE_URL` 环境变量
   - 配置 `LITELLM_MASTER_KEY`（必须以 sk- 开头）

2. 使用专用数据库镜像
```bash
docker pull ghcr.io/berriai/litellm-database:main-latest

docker run \
  -v $(pwd)/litellm_config.yaml:/app/config.yaml \
  -e LITELLM_MASTER_KEY=sk-1234 \
  -e DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname> \
  -e AZURE_API_KEY=d6*********** \
  -e AZURE_API_BASE=https://openai-***********/ \
  -p 4000:4000 \
  ghcr.io/berriai/litellm-database:main-latest \
  --config /app/config.yaml --detailed_debug
```

## 第3部分：集群部署方案
### Redis 集成部署
1. 配置 Redis 支持的 `config.yaml`
```yaml
model_list:
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: azure/<your-deployment-name>
      api_base: <your-azure-endpoint>
      api_key: <your-azure-api-key>
      rpm: 6

router_settings:
  redis_host: <your redis host>
  redis_password: <your redis password>
  redis_port: 1992
```

### Kubernetes 部署
1. 创建 EKS 集群
```bash
eksctl create cluster --name=litellm-cluster --region=us-west-2 --node-type=t2.small
```

2. 配置文件挂载
```bash
kubectl create configmap litellm-config --from-file=proxy_config.yaml
kubectl apply -f kub.yaml
kubectl apply -f service.yaml
```

## 第4部分：高级配置选项
### SSL 证书配置
```bash
docker run ghcr.io/berriai/litellm:main-latest \
  --ssl_keyfile_path ssl_test/keyfile.key \
  --ssl_certfile_path ssl_test/certfile.crt
```

### HTTP/2 支持
1. 创建支持 HTTP/2 的 Dockerfile
```dockerfile
FROM ghcr.io/berriai/litellm:main-latest
WORKDIR /app
COPY config.yaml .
RUN chmod +x ./docker/entrypoint.sh
EXPOSE 4000/tcp
RUN pip install hypercorn
CMD ["--port", "4000", "--config", "config.yaml"]
```

## 结论
- LiteLLM 提供了灵活多样的部署方案，从简单的单容器部署到复杂的集群部署
- 支持多种高级特性，如数据库集成、Redis 集群、SSL 证书等
- 通过 Docker 和 Kubernetes 的支持，可以轻松实现容器化和集群化部署
- 配置方式灵活，支持环境变量和配置文件两种方式