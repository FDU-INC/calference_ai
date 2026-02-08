# Calference 命令参考卡片

## 🚀 快速命令速查表

### 最常用的命令

| 功能 | Python 脚本 | Makefile | Shell 脚本 |
|------|-----------|----------|-----------|
| 生成报告 | `python run.py itu-report` | `make itu-report` | `./quickstart.sh itu-report` |
| 运行仿真 | `python run.py calself-sim` | `make calself-sim` | `./quickstart.sh calself-sim` |
| 启动 Web | `python run.py web-api` | `make web-api` | `./quickstart.sh web-api` |
| 显示状态 | `python run.py status` | `make status` | `./quickstart.sh status` |
| 查看帮助 | `python run.py --help` | `make help` | `./quickstart.sh help` |

---

## 📊 完整命令列表

### 1️⃣ 环境设置

```bash
# 安装依赖
make install
python run.py --help  # 查看所有命令

# 完整项目设置
make setup
```

### 2️⃣ 数据准备

```bash
# 准备 RAG 数据（生成 chunks 和 embeddings）
make prepare-rag
python run.py prepare-rag

# 下载 embedding 模型
make download-model
python run.py download-model
```

### 3️⃣ 报告生成

```bash
# 基础用法
make itu-report
python run.py itu-report

# 指定图片
python run.py itu-report --image path/to/image.png

# 禁用 RAG
python run.py itu-report --no-rag
```

### 4️⃣ 卫星仿真

```bash
# 基础用法（0.1小时）
make calself-sim
python run.py calself-sim

# 自定义时长
python run.py calself-sim --duration 0.5

# 自定义步长
python run.py calself-sim --duration 1.0 --step 5
```

### 5️⃣ 服务启动

```bash
# Web API 服务
make web-api
python run.py web-api --host 127.0.0.1 --port 8000

# Calself 仿真服务
make calself-service
python run.py calself-service --host 127.0.0.1 --port 8001
```

### 6️⃣ 示例运行

```bash
# ITU 报告示例
make example-itu
python run.py example itu_report

# Calself 仿真示例
make example-calself
python run.py example calself_usage
```

### 7️⃣ 项目管理

```bash
# 显示项目状态
make status
python run.py status

# 清理临时文件
make clean
```

---

## 🔧 参数详解

### `python run.py itu-report`

| 参数 | 说明 | 示例 |
|------|------|------|
| `--image` | 干扰图表路径 | `--image data/image.png` |
| `--no-rag` | 禁用 RAG 检索 | `--no-rag` |

### `python run.py calself-sim`

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--duration` | 仿真时长（小时） | 0.1 | `--duration 0.5` |
| `--step` | 时间步长（秒） | 2 | `--step 5` |

### `python run.py web-api`

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--host` | 服务器地址 | 127.0.0.1 | `--host 0.0.0.0` |
| `--port` | 服务器端口 | 8000 | `--port 9000` |

### `python run.py calself-service`

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--host` | 服务器地址 | 127.0.0.1 | `--host 0.0.0.0` |
| `--port` | 服务器端口 | 8001 | `--port 9001` |

---

## 📁 输出文件位置

| 功能 | 输出位置 |
|------|---------|
| Markdown 报告 | `output_reports/reports/interference_report_en.md` |
| Word 报告 | `output_reports/reports/interference_report_en.docx` |
| Agent 配置 | `output_reports/metadata/agent_configs.json` |
| 审计日志 | `output_reports/metadata/audit_log.json` |
| 数据流 | `output_reports/data_flow/data_flow.json` |
| 数据流摘要 | `output_reports/data_flow/data_flow_summary.json` |
| RAG Chunks | `data/rag/chunks.jsonl` |
| RAG Embeddings | `data/rag/embeddings.npy` |
| RAG 元数据 | `data/rag/metadata.json` |

---

## 🌐 Web 服务 URL

### Web API 服务

启动后访问：
- **主页**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Calself 仿真服务

启动后访问：
- **主页**: http://127.0.0.1:8001
- **API 文档**: http://127.0.0.1:8001/docs

---

## 🔑 环境变量配置

```bash
# LLM 配置
export LLM_MODEL_NAME="gemini-2.0-flash"
export LLM_BASE_URL="https://api.aicodemirror.com/api/gemini"
export LLM_API_KEY="your_api_key_here"

# 代理配置（可选）
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# HuggingFace 镜像（可选）
export HF_ENDPOINT="https://hf-mirror.com"
```

---

## 💡 常用场景

### 场景 1: 第一次使用

```bash
# 1. 安装依赖
make install

# 2. 准备数据
make setup

# 3. 配置 API 密钥
export LLM_API_KEY="your_key"

# 4. 运行示例
make example-itu
```

### 场景 2: 生成自定义报告

```bash
# 1. 准备图片
cp your_image.png data/input/

# 2. 生成报告
python run.py itu-report --image data/input/your_image.png

# 3. 查看结果
cat output_reports/reports/interference_report_en.md
```

### 场景 3: 启动完整服务

```bash
# 终端 1: 启动 Web API
make web-api

# 终端 2: 启动仿真服务
make calself-service

# 终端 3: 访问服务
curl http://127.0.0.1:8000/docs
```

### 场景 4: 批量处理

```bash
# 处理多个图片
for img in data/input/*.png; do
    python run.py itu-report --image "$img"
done
```

---

## ⚠️ 常见错误及解决方案

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `ModuleNotFoundError` | 缺少依赖 | `make install` |
| `API key invalid` | API 密钥错误 | 检查 `LLM_API_KEY` 环境变量 |
| `FileNotFoundError` | 文件不存在 | `make prepare-rag` |
| `Connection refused` | 服务未启动 | 启动相应服务 |
| `Address already in use` | 端口被占用 | 使用 `--port` 指定其他端口 |

---

## 📚 更多信息

- **详细指南**: 查看 [QUICKSTART.md](QUICKSTART.md)
- **项目结构**: 查看 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **使用手册**: 查看 [docs/USER_MANUAL.md](docs/USER_MANUAL.md)
- **API 文档**: 启动 Web 服务后访问 `/docs`

---

**最后更新**: 2026-02-07
**版本**: 1.1.0
