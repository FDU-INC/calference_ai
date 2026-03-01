"""
报告生成服务封装（供 Web API 调用）。

设计目标：
- `run.py web-api` 只是启动 Web 服务
- 真正的报告生成逻辑复用 `itu_interference_analyzer.py` 的管道
- 允许通过参数覆盖 LLM 配置（model/base_url/api_key）
"""

import importlib
import os
from datetime import datetime
from pathlib import Path


async def generate_report(
    image_path,
    use_rag=True,
    model_name=None,
    base_url=None,
    api_key=None,
    output_dir=None,
):
    """
    生成干扰分析报告（Markdown + DOCX）。

    Args:
        image_path: 图片路径（Path 或 str）。
        use_rag: 是否启用 RAG（目前由分析管道内部逻辑决定，参数保留兼容）。
        model_name: 覆盖 LLM_MODEL_NAME（可选）。
        base_url: 覆盖 LLM_BASE_URL（可选）。
        api_key: 覆盖 LLM_API_KEY（可选）。
        output_dir: 输出目录（可选）。注意：当前管道默认写入项目根目录的 `output_reports/`，
            该参数主要用于 API 返回信息兼容。

    Returns:
        dict: 包含 markdown 内容、输出文件路径等信息。
    """
    # 1) 统一转 Path
    image_path = Path(image_path).resolve()
    if not image_path.exists():
        raise FileNotFoundError(f"图片不存在: {image_path}")

    # 2) 通过环境变量覆盖配置（config.py 在 import 时读取环境变量）
    if model_name:
        os.environ["LLM_MODEL_NAME"] = str(model_name)
    if base_url:
        os.environ["LLM_BASE_URL"] = str(base_url)
    if api_key:
        os.environ["LLM_API_KEY"] = str(api_key)

    # 3) 重新加载 config 与 analyzer，确保覆盖配置生效
    import itu_report_generator.config as config

    importlib.reload(config)

    import itu_report_generator.itu_interference_analyzer as analyzer

    importlib.reload(analyzer)

    # 4) 配置代理（如有需要）
    # 注意：该函数会设置 HTTP_PROXY/HTTPS_PROXY
    analyzer.configure_proxies()

    # 5) 运行管道（返回 Markdown 文本）
    filename = image_path.name
    image_info = analyzer.parse_image_info(filename)
    current_date = datetime.now().strftime("%Y-%m-%d")

    pipeline = analyzer.ConfigurableDialoguePipeline(
        image_info=image_info,
        current_date=current_date,
        image_path=str(image_path),
    )

    markdown = await pipeline.run(image_path=str(image_path), compress_img=False)

    # 6) 输出路径（当前管道内部固定输出到 config.OUTPUT_REPORTS_DIR）
    md_path = Path(config.OUTPUT_REPORTS_DIR) / "interference_report_en.md"
    docx_path = Path(config.OUTPUT_REPORTS_DIR) / "interference_report_en.docx"

    # 7) 返回结果（保持与 frontend/api.py 的预期字段一致）
    return {
        "markdown": markdown,
        "markdown_path": str(md_path),
        "docx_path": str(docx_path) if docx_path.exists() else None,
        "image_path": str(image_path),
        "rag_results": [],
        "output_dir": str(output_dir) if output_dir else None,
        "use_rag": bool(use_rag),
    }



