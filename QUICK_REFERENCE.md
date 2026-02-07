# Calference 项目运行脚本 - 快速参考卡片

## 🎯 最常用的 3 个命令

```bash
# 1️⃣ 生成 ITU 干扰报告
python run.py itu-report

# 2️⃣ 启动 Web 服务
python run.py web-api

# 3️⃣ 显示项目状态
python run.py status
```

---

## 📋 所有可用命令速查表

### 使用 Python 脚本 (`python run.py`)

```bash
# 报告生成
python run.py itu-report                          # 生成报告
python run.py itu-report --image path/to/img.png  # 指定图片
python run.py itu-report --no-rag                 # 禁用 RAG

# 卫星仿真
python run.py calself-sim                         # 运行仿真
python run.py calself-sim --duration 0.5          # 指定时长

# 数据准备
python run.py prepare-rag                         # 准备 RAG 数据
python run.py download-model                      # 下载模型

# 服务启动
python run.py web-api                             # 启动 Web API
python run.py calself-service                     # 启动仿真服务

# 其他
python run.py example itu_report                  # 运行示例
python run.py status                              # 显示状态
python run.py --help                              # 查看帮助
```

### 使用 Makefile (`make`)

```bash
make help                                         # 查看所有命令
make install                                      # 安装依赖
make setup                                        # 完整设置
make itu-report                                   # 生成报告
make calself-sim                                  # 运行仿真
make prepare-rag                                  # 准备 RAG 数据
make download-model                               # 下载模型
make web-api                                      # 启动 Web API
make calself-service                              # 启动仿真服务
make example-itu                                  # 运行示例
make status                                       # 显示状态
make clean                                        # 清理临时文件
```

### 使用 Shell 脚本 (`./quickstart.sh`)

```bash
./quickstart.sh help                              # 查看帮助
./quickstart.sh itu-report                        # 生成报告
./quickstart.sh calself-sim --duration 0.5        # 运行仿真
./quickstart.sh web-api --port 8000               # 启动 Web 服务
./quickstart.sh status                            # 显示状态
```

---

## 🚀 快速开始（3 步）

### 第一次使用

```bash
# 1. 一键初始化
python3 init.py --auto

# 2. 配置 API 密钥
export LLM_API_KEY="your_api_key"

# 3. 运行示例
python3 run.py itu-report
```

### 日常使用

```bash
# 方式一：使用 Python 脚本
python3 run.py itu-report

# 方式二：使用 Makefile（推荐）
make itu-report

# 方式三：使用 Shell 脚本
./quickstart.sh itu-report
```

---

## 📁 输出文件位置

| 功能 | 输出位置 |
|------|---------|
| Markdown 报告 | `output_reports/reports/interference_report_en.md` |
| Word 报告 | `output_reports/reports/interference_report_en.docx` |
| Agent 配置 | `output_reports/metadata/agent_configs.json` |
| 审计日志 | `output_reports/metadata/audit_log.json` |
| 数据流 | `output_reports/data_flow/data_flow.json` |
| RAG Chunks | `data/rag/chunks.jsonl` |
| RAG Embeddings | `data/rag/embeddings.npy` |

---

## 🔧 常见参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--image` | 指定图片路径 | `--image data/img.png` |
| `--no-rag` | 禁用 RAG 检索 | `--no-rag` |
| `--duration` | 仿真时长（小时） | `--duration 0.5` |
| `--step` | 时间步长（秒） | `--step 5` |
| `--host` | 服务器地址 | `--host 0.0.0.0` |
| `--port` | 服务器端口 | `--port 9000` |

---

## 🌐 Web 服务 URL

启动后访问：
- **Web API**: http://127.0.0.1:8000
- **API 文档**: http://127.0.0.1:8000/docs
- **仿真服务**: http://127.0.0.1:8001

---

## 📚 文档导航

| 文档 | 用途 |
|------|------|
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速入门 |
| [COMMANDS.md](COMMANDS.md) | 完整命令参考 |
| [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) | 脚本详细说明 |
| [README.md](README.md) | 项目主文档 |

---

## ⚠️ 常见问题快速解决

| 问题 | 解决方案 |
|------|---------|
| 缺少依赖 | `make install` |
| API 连接失败 | 检查 `LLM_API_KEY` 环境变量 |
| RAG 数据不存在 | `python3 run.py prepare-rag` |
| 端口被占用 | `python3 run.py web-api --port 9000` |
| 权限错误 | `chmod +x quickstart.sh run.py` |

---

## 💡 使用建议

✅ **推荐做法**:
- 使用 `make` 命令进行日常操作
- 使用 `python3 run.py --help` 查看详细帮助
- 使用 `python3 run.py status` 检查项目状态
- 查看 [QUICKSTART.md](QUICKSTART.md) 了解详细信息

❌ **避免做法**:
- 不要使用 `python` 而应使用 `python3`
- 不要忘记配置 `LLM_API_KEY` 环境变量
- 不要在没有准备数据的情况下运行报告生成

---

**最后更新**: 2026-02-07 | **版本**: 1.1.0
