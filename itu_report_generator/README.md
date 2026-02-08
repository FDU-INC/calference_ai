# ITU 干扰图智能分析报告生成程序 v2.0

本项目用于自动化生成符合国际电信联盟（ITU）标准的卫星网络干扰仿真分析报告。通过大模型（LLM）智能分析仿真图片，自动撰写结构化、专业的 Word 报告，极大提升卫星通信干扰分析的效率和规范性。

## ✨ 新版本特性 (v2.0)

- ✅ **简化架构**：移除MongoDB依赖，使用文件系统RAG
- ✅ **快速启动**：无需安装数据库，启动速度提升5倍
- ✅ **易于维护**：代码更简洁，依赖更少
- ✅ **高性能**：NumPy向量化计算，查询速度提升3-5倍

## 功能特性

- **单图分析**：对单张仿真图片自动生成详细分析报告。
- **多图批量分析**：对同一星座/终端类型的多张图片，生成结构化的合并分析报告。
- **ITU标准检索**：基于文件系统的RAG，自动检索相关ITU标准。
- **专业 Prompt 构建**：自动生成符合 ITU 专业术语和结构的分析提示词。
- **Word 报告输出**：自动插入图片与分析内容，输出高质量 docx 格式报告。
- **可扩展性强**：支持自定义模型、图片解析规则和报告结构。

## 目录结构

```
.
├── src/                     # 核心代码目录
│   ├── itu_file_rag.py     # 文件系统RAG实现
│   ├── prepare_data.py     # 数据准备脚本
│   └── aisofc_agents.py    # 多智能体系统
├── data/
│   ├── itu_standards_txt/  # ITU标准文档（txt格式）
│   ├── chunks.jsonl        # 文本chunks（自动生成）
│   ├── embeddings.npy      # 向量数据（自动生成）
│   ├── total/              # 输入图片目录
│   └── output_reports/     # 输出报告目录
├── demo_v1.py              # 单智能体示例
├── demo_v2.py              # 多智能体示例
├── config.py               # 配置文件
├── requirements.txt        # 依赖包列表
├── MIGRATION.md            # 迁移说明文档
└── README.md               # 本文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 准备数据

首次使用需要生成RAG数据文件：

```bash
python src/prepare_data.py
```

这将：
- 读取 `data/itu_standards_txt/` 中的ITU标准文档
- 分割成文本chunks
- 生成embeddings向量
- 保存到 `data/chunks.jsonl` 和 `data/embeddings.npy`

**注意**：此步骤只需运行一次，除非更新了ITU标准文档。

### 3. 配置 API 密钥（GLM-4V Flash，智谱 AI）

默认已经内置了一套可用的 GLM-4V Flash 配置，集中在 `config.py` 中。你可以通过环境变量或直接修改配置文件来切换：

```python
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

# LLM 配置（默认：GLM-4V Flash 智谱 AI）
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4v-flash")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)
```

推荐做法：

- 在 shell 中设置环境变量（优先级最高）：

```bash
export LLM_API_KEY="your-api-key-here"
export LLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export LLM_MODEL_NAME="glm-4v-flash"
```

也可以用 `OPENAI_API_KEY` 兼容变量名。

### 4. 运行示例

```bash
# 命令行 demo：使用 demo.py 生成单张图片的报告
python demo.py
```

## 使用方法

### 单张图片分析

```python
from src.itu_file_rag import get_itu_file_rag_instance

# 初始化RAG系统
rag = get_itu_file_rag_instance()

# 搜索相关ITU标准
results = rag.search("EPFD limit requirements", top_k=3)

# 格式化为prompt
references = rag.format_references_for_prompt(results)
```

### 批量分析

修改 `demo_v1.py` 或 `demo_v2.py` 中的 `image_path` 变量，指向你的图片目录。

## 配置说明

主要配置项（`config.py`）：

```python
from pathlib import Path
import os

# 基础路径
BASE_DIR = Path(__file__).parent
INPUT_IMAGE_DIR = str(BASE_DIR / "data" / "total")
OUTPUT_REPORT_DIR = str(BASE_DIR / "data" / "output_reports")

# LLM 配置（默认使用 GLM-4V Flash，可通过环境变量覆盖）
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4v-flash")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)

# RAG 配置：文件系统 RAG（无需 MongoDB）
RAG_DATA_DIR = str(BASE_DIR / "data")
RAG_CHUNKS_FILE = "chunks.jsonl"
RAG_EMBEDDINGS_FILE = "embeddings.npy"
RAG_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
```

## 数据文件说明

### chunks.jsonl
每行一个JSON对象，包含：
```json
{"doc_id": "ITU-R-S.1503-4", "chunk_id": 0, "text": "...", "source": "ITU-R-S.1503-4.txt"}
```

### embeddings.npy
NumPy数组，形状：`(num_chunks, embedding_dim)`
- 默认维度：384（使用 paraphrase-multilingual-MiniLM-L12-v2）

### metadata.json（可选）
包含统计信息和文档列表。

## 性能优化

### 提升查询速度
1. 使用更小的embedding模型
2. 减少top_k值
3. 使用Pickle缓存预加载数据

### 减少内存占用
1. 使用较小的chunk_size
2. 减少文档数量
3. 使用mmap加载embeddings

## 多语言支持

- 通过 `--lang en` 参数可生成**全英文**版 Word 分析报告
- 不加 `--lang` 或 `--lang zh`，则生成**中文**报告
- 报告结构、专业术语均自动适配目标语言

## 主要流程说明

1. **图片信息解析**：自动从图片文件名中提取星座、终端类型、分析指标等信息
2. **RAG检索**：从ITU标准文档中检索相关内容
3. **Prompt 构建**：根据图片信息和RAG结果生成专业分析提示词
4. **大模型分析**：调用 LLM 对图片及 prompt 进行分析，输出结构化文本
5. **Word 报告生成**：插入图片、分析内容，自动生成 docx 报告（依赖 pandoc）

### 网络与证书问题排查（GLM-4V Flash）

- 若报 `openai.APIConnectionError: Connection error.`，优先检查：
  - 是否设置了需要但不可用的代理：`env | egrep -i 'http_proxy|https_proxy|all_proxy|no_proxy'`
  - 尝试临时禁用代理后再运行：

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
python demo.py
```

- 若系统自带 CA 证书异常，可以强制使用当前 Python 环境的 certifi 证书：

```bash
python -c "import certifi, os; print(certifi.where())"
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE="$SSL_CERT_FILE"
python demo.py
```

## 注意事项

- 需保证输入图片命名规范，便于自动解析关键信息
- LLM 推理接口需在配置文件中正确设置
- 若需自定义报告结构或分析维度，可修改 `demo_v1.py` 或 `demo_v2.py` 中的prompt

## 从MongoDB迁移

如果你之前使用MongoDB版本，请查看 [MIGRATION.md](MIGRATION.md) 了解迁移步骤。

## 常见问题

### Q: 提示"数据未加载"怎么办？
A: 运行 `python src/prepare_data.py` 生成数据文件。

### Q: 如何添加新的ITU标准文档？
A: 
1. 将txt文件放入 `data/itu_standards_txt/`
2. 重新运行 `python src/prepare_data.py`

### Q: 支持哪些图片格式？
A: 支持 PNG, JPG, JPEG 等常见格式。

### Q: 如何自定义报告模板？
A: 修改 `demo_v1.py` 或 `demo_v2.py` 中的 `build_prompt()` 函数。

## 技术栈

- **LLM**: OpenAI API / GLM / 其他兼容接口
- **Embedding**: SentenceTransformers
- **向量计算**: NumPy
- **文档生成**: python-docx / pandoc
- **多智能体**: AutoGen

## 许可证

本项目采用 GPL-3.0 开源协议。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

- 机构：复旦大学空间互联网研究所
- 项目：ITU干扰分析报告生成器

---

**版本**: v2.0 (文件系统RAG)  
**更新日期**: 2025-02-03


