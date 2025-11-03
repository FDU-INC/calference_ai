# ITU 干扰图智能分析报告生成程序

本项目用于自动化生成符合国际电信联盟（ITU）标准的卫星网络干扰仿真分析报告。通过大模型（LLM）智能分析仿真图片，自动撰写结构化、专业的 Word 报告，极大提升卫星通信干扰分析的效率和规范性。

## 功能特性

- **单图分析**：对单张仿真图片自动生成详细分析报告。
- **多图批量分析**：对同一星座/终端类型的多张图片，生成结构化的合并分析报告。
- **专业 Prompt 构建**：自动生成符合 ITU 专业术语和结构的分析提示词。
- **Word 报告输出**：自动插入图片与分析内容，输出高质量 docx 格式报告。
- **可扩展性强**：支持自定义模型、图片解析规则和报告结构。
- **多语言支持**：支持中文和英文报告生成。

## 目录结构

```
.
├── main.py                  # 项目主入口，命令行批量/单图分析
├── config.py                # 配置文件（需自定义模型路径、输入输出目录等）
├── config.py.example        # 配置文件模板
├── LICENSE                  # GPL-3.0 许可证
├── requirements.txt         # Python 依赖包列表
├── src/
│   ├── orchestrator.py      # 核心流程协调器，调度 LLM、报告生成等
│   ├── prompt_builder.py    # 专业分析 Prompt 构建
│   ├── utils.py             # 工具函数（如图片名解析、日期等）
│   ├── llm_inference.py     # 大模型推理接口
│   └── report_writer.py     # Word 报告生成
├── data/
│   ├── total/               # 输入图片目录
│   └── output_reports/      # 输出报告目录
└── README.md                # 项目说明文档
```

## 安装

### 1. 克隆项目

```bash
git clone <repository-url>
cd itu_report_generator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**：本项目需要 PyTorch 和 CUDA 支持（用于运行 Qwen2.5-VL 模型）。请根据你的系统安装对应版本的 PyTorch。

### 3. 准备模型

下载并配置 Qwen2.5-VL-7B-Instruct 模型。你可以从 [Hugging Face](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) 下载。

### 4. 配置

复制配置文件模板：

```bash
cp config.py.example config.py
```

编辑 `config.py` 并设置以下配置：

- `MODEL_PATH`：Qwen2.5-VL 模型的本地路径
- `INPUT_IMAGE_DIR`：仿真图片输入目录
- `OUTPUT_REPORT_DIR`：报告输出目录
- `ORGANIZATION_NAME`：分析机构名称
- `PROXY`：代理服务器（可选，如不需要则设置为 `None`）

**或者使用环境变量配置**（推荐用于生产环境）：

```bash
export QWEN_MODEL_PATH="/path/to/your/model"
export INPUT_IMAGE_DIR="/path/to/images"
export OUTPUT_REPORT_DIR="/path/to/output"
export ORGANIZATION_NAME="Your Organization"
export PROXY="http://proxy:port"  # 可选
```

## 使用方法

### 1. 单张图片分析

```bash
python main.py --single IMAGE_NAME [--lang en/zh]
```
- 例（中文报告，默认）：`python main.py --single oneweb_total_earth_cinr.png`
- 例（英文报告）：`python main.py --single oneweb_total_earth_cinr.png --lang en`

### 2. 批量分析（多图合并报告）

```bash
python main.py --batch CONSTELLATION TERMINAL_TYPE [--max N] [--lang en/zh]
```
- 例（中文报告，默认）：`python main.py --batch oneweb earth --max 8`
- 例（英文报告）：`python main.py --batch oneweb earth --max 8 --lang en`
- 会自动筛选包含关键词的图片，合成一份结构化多图分析报告。

### 3. 默认处理全部图片（无参数）

```bash
python main.py [--lang en/zh]
```
- 会对输入目录下所有图片逐一生成单独报告。
- 例（英文报告）：`python main.py --lang en`

## 多语言支持说明

- 通过 `--lang en` 参数可生成**全英文**版 Word 分析报告，适用于国际交流、英文材料需求。
- 不加 `--lang` 或 `--lang zh`，则生成**中文**报告。
- 报告结构、专业术语均自动适配目标语言。

## 主要流程说明

- **图片信息解析**：自动从图片文件名中提取星座、终端类型、分析指标等信息。
- **Prompt 构建**：根据图片信息自动生成专业分析提示词，适配单图/多图场景。
- **大模型分析**：调用 LLM 对图片及 prompt 进行分析，输出结构化文本。
- **Word 报告生成**：插入图片、分析内容，自动生成 docx 报告。

## 注意事项

- **图片命名规范**：需保证输入图片命名规范，便于自动解析关键信息。格式建议：`{constellation}_{terminal_type}_{analysis_type}.png`
- **模型要求**：需要 Qwen2.5-VL-7B-Instruct 模型，确保有足够的 GPU 内存（推荐 16GB+）
- **依赖独立性**：本项目是独立的报告生成工具，不依赖其他闭源模块
- **自定义扩展**：若需自定义报告结构或分析维度，可修改 `src/prompt_builder.py`

## 常见问题

### Q: 如何在没有 GPU 的环境下运行？
A: 可以将模型路径设置为支持 CPU 推理的模型，但运行速度会较慢。也可以考虑使用远程 API 调用。

### Q: 支持其他 LLM 模型吗？
A: 当前版本主要针对 Qwen2.5-VL 优化。如需支持其他模型，需要修改 `src/llm_inference.py`。

### Q: 如何处理大批量图片？
A: 使用 `--batch` 参数可以批量处理同类图片，生成合并报告。对于大量不同类别的图片，建议分别处理。

## 许可证

本项目采用 **GNU General Public License v3.0 (GPL-3.0)** 许可证。

详细许可证信息请查看 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 联系方式

如有问题或建议，请通过 Issue 联系我们。

## 致谢

感谢复旦大学空间互联网研究院的支持。


