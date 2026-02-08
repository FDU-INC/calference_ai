# Calference 快速入门指南

## 📋 目录

1. [5分钟快速开始](#5分钟快速开始)
2. [命令参考](#命令参考)
3. [常见问题](#常见问题)
4. [故障排除](#故障排除)

---

## 5分钟快速开始

### 第一步：安装依赖

```bash
# 方式一：使用 Makefile（推荐）
make install

# 方式二：直接使用 pip
pip install -r requirements.txt
```

### 第二步：准备数据（可选但推荐）

```bash
# 方式一：使用 Makefile
make setup

# 方式二：分步执行
python run.py download-model      # 下载 embedding 模型
python run.py prepare-rag         # 准备 RAG 数据
```

### 第三步：运行示例

```bash
# 生成 ITU 干扰报告
python run.py itu-report

# 或使用 Makefile
make itu-report
```

### 第四步：查看结果

报告生成完成后，输出文件位置：
- **Markdown 报告**: `output_reports/reports/interference_report_en.md`
- **Word 报告**: `output_reports/reports/interference_report_en.docx`
- **元数据**: `output_reports/metadata/`
- **数据流**: `output_reports/data_flow/`

---

## 命令参考

### 使用 Python 脚本（`python run.py`）

#### 报告生成

```bash
# 生成 ITU 干扰报告（使用默认图片）
python run.py itu-report

# 指定自定义图片
python run.py itu-report --image path/to/image.png

# 禁用 RAG 检索
python run.py itu-report --no-rag
```

#### 卫星仿真

```bash
# 运行仿真（默认0.1小时）
python run.py calself-sim

# 指定仿真时长（小时）
python run.py calself-sim --duration 0.5

# 指定时间步长（秒）
python run.py calself-sim --duration 1.0 --step 5
```

#### 数据准备

```bash
# 准备 RAG 数据（生成 chunks 和 embeddings）
python run.py prepare-rag

# 下载 embedding 模型
python run.py download-model
```

#### 服务启动

```bash
# 启动 Web API 服务
python run.py web-api

# 指定主机和端口
python run.py web-api --host 0.0.0.0 --port 8000

# 启动 Calself 仿真服务
python run.py calself-service --host 127.0.0.1 --port 8001
```

#### 示例和状态

```bash
# 运行 ITU 报告示例
python run.py example itu_report

# 运行 Calself 仿真示例
python run.py example calself_usage

# 显示项目状态
python run.py status
```

### 使用 Makefile（`make`）

```bash
# 查看所有命令
make help

# 安装依赖
make install

# 完整设置（安装+准备数据）
make setup

# 生成报告
make itu-report

# 运行仿真
make calself-sim

# 准备数据
make prepare-rag
make download-model

# 启动服务
make web-api
make calself-service

# 运行示例
make example-itu
make example-calself

# 显示状态
make status

# 清理临时文件
make clean
```

### 使用快速启动脚本（`./quickstart.sh`）

```bash
# 添加执行权限
chmod +x quickstart.sh

# 查看帮助
./quickstart.sh help

# 生成报告
./quickstart.sh itu-report

# 运行仿真
./quickstart.sh calself-sim --duration 0.5

# 启动服务
./quickstart.sh web-api --port 8000

# 显示状态
./quickstart.sh status
```

---

## 常见问题

### Q1: 如何配置 LLM API？

**A:** 编辑 `itu_report_generator/config.py` 或设置环境变量：

```bash
# Gemini 配置（推荐）
export LLM_MODEL_NAME="gemini-2.0-flash"
export LLM_BASE_URL="https://api.aicodemirror.com/api/gemini"
export LLM_API_KEY="your_api_key_here"

# 或 Claude 配置
export LLM_MODEL_NAME="claude-3-7-sonnet-20250219"
export LLM_BASE_URL="http://your-proxy:8000"
export LLM_API_KEY="your_api_key_here"
```

### Q2: 如何使用自定义图片生成报告？

**A:** 使用 `--image` 参数指定图片路径：

```bash
python run.py itu-report --image /path/to/your/image.png
```

### Q3: 如何禁用 RAG 检索？

**A:** 使用 `--no-rag` 参数：

```bash
python run.py itu-report --no-rag
```

### Q4: 如何修改 Web 服务的端口？

**A:** 使用 `--port` 参数：

```bash
python run.py web-api --port 9000
```

### Q5: 如何查看项目的完整状态？

**A:** 运行状态命令：

```bash
python run.py status
```

### Q6: 如何清理临时文件？

**A:** 使用 Makefile 的 clean 命令：

```bash
make clean
```

### Q7: 仿真需要多长时间？

**A:** 取决于仿真时长和时间步长：
- 默认（0.1小时，步长2秒）：约 1-2 分钟
- 完整仿真（1小时，步长2秒）：约 10-20 分钟

### Q8: 报告生成需要多长时间？

**A:** 取决于 LLM 响应速度：
- 无 RAG：约 2-5 分钟
- 有 RAG：约 3-8 分钟

---

## 故障排除

### 问题 1: 缺少依赖包

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```bash
# 重新安装依赖
pip install -r requirements.txt

# 或使用 Makefile
make install
```

### 问题 2: LLM API 连接失败

**症状**: `Connection error` 或 `API key invalid`

**解决方案**:
1. 检查 API 密钥是否正确
2. 检查网络连接
3. 检查 API 端点是否可访问
4. 查看 `itu_report_generator/config.py` 中的配置

### 问题 3: RAG 数据不存在

**症状**: `FileNotFoundError: chunks.jsonl not found`

**解决方案**:
```bash
# 准备 RAG 数据
python run.py prepare-rag

# 或使用 Makefile
make prepare-rag
```

### 问题 4: Embedding 模型下载失败

**症状**: `Connection timeout` 或 `Download failed`

**解决方案**:
```bash
# 检查网络连接
# 尝试使用代理
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 重新下载
python run.py download-model

# 或使用 HuggingFace 镜像
export HF_ENDPOINT="https://hf-mirror.com"
python run.py download-model
```

### 问题 5: Web 服务启动失败

**症状**: `Address already in use` 或 `Permission denied`

**解决方案**:
```bash
# 使用不同的端口
python run.py web-api --port 8001

# 或检查占用的进程
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

### 问题 6: 仿真服务无法连接

**症状**: `Connection refused` 或 `Service unavailable`

**解决方案**:
1. 确保仿真服务已启动
2. 检查服务地址和端口
3. 检查防火墙设置

```bash
# 启动仿真服务
python run.py calself-service --host 127.0.0.1 --port 8001
```

### 问题 7: 权限错误

**症状**: `Permission denied` 或 `Access denied`

**解决方案**:
```bash
# 添加执行权限
chmod +x quickstart.sh run.py

# 或使用 Python 直接运行
python run.py [command]
```

### 问题 8: 内存不足

**症状**: `MemoryError` 或 `Out of memory`

**解决方案**:
1. 减少仿真时长
2. 增加系统内存
3. 关闭其他应用程序

```bash
# 运行较短的仿真
python run.py calself-sim --duration 0.05
```

---

## 高级用法

### 自定义配置

编辑 `itu_report_generator/config.py` 修改：

```python
# LLM 配置
LLM_MODEL_NAME = "your-model"
LLM_BASE_URL = "your-api-endpoint"
LLM_API_KEY = "your-api-key"

# RAG 配置
RAG_TOP_K = 5  # 检索结果数量
RAG_EMBEDDING_MODEL = "your-embedding-model"

# 输出配置
OUTPUT_REPORT_DIR = "custom/output/path"
```

### 批量处理

创建脚本处理多个图片：

```python
from pathlib import Path
from itu_report_generator.itu_interference_analyzer import main

image_dir = Path("data/images")
for image_path in image_dir.glob("*.png"):
    print(f"处理: {image_path}")
    main(image_path=str(image_path), use_rag=True)
```

### 集成到其他项目

```python
from itu_report_generator.report_service import generate_report_segmented
from pathlib import Path

# 生成报告
result = await generate_report_segmented(
    image_path=Path("data/image.png"),
    use_rag=True
)

# 获取结果
print(f"Markdown: {result['markdown_path']}")
print(f"Word: {result['docx_path']}")
```

---

## 获取帮助

- **查看脚本帮助**: `python run.py --help`
- **查看 Makefile 命令**: `make help`
- **查看快速启动脚本**: `./quickstart.sh help`
- **查看项目状态**: `python run.py status`

---

**最后更新**: 2026-02-07
**版本**: 1.1.0
