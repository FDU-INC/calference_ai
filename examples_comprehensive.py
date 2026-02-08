#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calference 综合使用示例

演示项目的主要功能：
1. 生成 ITU 干扰报告
2. 运行 Calself 卫星仿真
3. 启动 Web 服务
4. 使用 RAG 检索

使用方法：
    python examples_comprehensive.py
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def print_section(title: str) -> None:
    """打印章节标题"""
    print("\n" + "=" * 70)
    print(f"📚 {title}")
    print("=" * 70 + "\n")


def example_1_itu_report() -> None:
    """示例 1: 生成 ITU 干扰报告"""
    print_section("示例 1: 生成 ITU 干扰报告")

    print("这个示例演示如何生成 ITU 干扰分析报告。\n")

    print("方式一：使用 run.py 脚本")
    print("  python run.py itu-report\n")

    print("方式二：使用 Makefile")
    print("  make itu-report\n")

    print("方式三：使用 Python 代码")
    print("""
from pathlib import Path
from itu_report_generator.itu_interference_analyzer import main

# 生成报告
main(image_path=None, use_rag=True)

# 查看结果
report_path = Path("output_reports/reports/interference_report_en.md")
if report_path.exists():
    with open(report_path) as f:
        print(f.read())
    """)

    print("\n📁 输出文件:")
    print("  - Markdown: output_reports/reports/interference_report_en.md")
    print("  - Word: output_reports/reports/interference_report_en.docx")
    print("  - 元数据: output_reports/metadata/")


def example_2_calself_simulation() -> None:
    """示例 2: 运行 Calself 卫星仿真"""
    print_section("示例 2: 运行 Calself 卫星仿真")

    print("这个示例演示如何运行卫星干扰仿真。\n")

    print("方式一：使用 run.py 脚本")
    print("  python run.py calself-sim --duration 0.1\n")

    print("方式二：使用 Makefile")
    print("  make calself-sim\n")

    print("方式三：使用 Python 代码")
    print("""
from datetime import datetime
from calself_client import CalselfClient

# 初始化客户端
client = CalselfClient("http://localhost:8000")

# 运行仿真
result = client.run_simulation(
    start_time=datetime(2024, 12, 16, 0, 0, 0),
    duration_hours=0.1,
    step=2
)

print(f"仿真完成: {result}")

# 获取结果文件
files = client.get_inference_files(company_id=1)
print(f"结果文件: {files}")
    """)

    print("\n⏱️  参数说明:")
    print("  - duration: 仿真时长（小时）")
    print("  - step: 时间步长（秒）")


def example_3_web_services() -> None:
    """示例 3: 启动 Web 服务"""
    print_section("示例 3: 启动 Web 服务")

    print("这个示例演示如何启动 Web 服务。\n")

    print("启动 Web API 服务:")
    print("  python run.py web-api --host 127.0.0.1 --port 8000\n")

    print("启动 Calself 仿真服务:")
    print("  python run.py calself-service --host 127.0.0.1 --port 8001\n")

    print("访问 API 文档:")
    print("  http://127.0.0.1:8000/docs\n")

    print("使用 Python 调用 API:")
    print("""
import requests

# 调用 Web API
response = requests.get("http://127.0.0.1:8000/health")
print(response.json())

# 生成报告
response = requests.post(
    "http://127.0.0.1:8000/generate-report",
    json={"use_rag": True}
)
print(response.json())
    """)


def example_4_rag_retrieval() -> None:
    """示例 4: RAG 检索增强"""
    print_section("示例 4: RAG 检索增强")

    print("这个示例演示如何使用 RAG 检索 ITU 标准文档。\n")

    print("准备 RAG 数据:")
    print("  python run.py prepare-rag\n")

    print("使用 RAG 检索:")
    print("""
from itu_report_generator.src.itu_file_rag import get_itu_file_rag_instance

# 获取 RAG 实例
rag = get_itu_file_rag_instance()

# 搜索相关文档
results = rag.search("CINR threshold limit", top_k=3)

# 显示结果
for result in results:
    print(f"文档: {result['document']}")
    print(f"相关度: {result['score']:.3f}")
    print(f"内容: {result['text'][:200]}...")
    print()
    """)

    print("📚 RAG 数据文件:")
    print("  - Chunks: data/rag/chunks.jsonl")
    print("  - Embeddings: data/rag/embeddings.npy")
    print("  - 元数据: data/rag/metadata.json")


def example_5_batch_processing() -> None:
    """示例 5: 批量处理"""
    print_section("示例 5: 批量处理多个图片")

    print("这个示例演示如何批量处理多个干扰图表。\n")

    print("Shell 脚本方式:")
    print("""
# 处理 data/input 目录下的所有 PNG 图片
for img in data/input/*.png; do
    echo "处理: $img"
    python run.py itu-report --image "$img"
done
    """)

    print("\nPython 脚本方式:")
    print("""
from pathlib import Path
from itu_report_generator.itu_interference_analyzer import main

# 处理所有图片
input_dir = Path("data/input")
for image_path in input_dir.glob("*.png"):
    print(f"处理: {image_path}")
    try:
        main(image_path=str(image_path), use_rag=True)
        print(f"✅ 完成: {image_path.name}")
    except Exception as e:
        print(f"❌ 失败: {e}")
    """)


def example_6_custom_configuration() -> None:
    """示例 6: 自定义配置"""
    print_section("示例 6: 自定义配置")

    print("这个示例演示如何自定义项目配置。\n")

    print("编辑配置件:")
    print("  nano itu_report_generator/config.py\n")

    print("主要配置项:")
    print("""
# LLM 配置
LLM_MODEL_NAME = "gemini-2.0-flash"
LLM_BASE_URL = "https://api.aicodemirror.com/api/gemini"
LLM_API_KEY = "your_api_key_here"

# RAG 配置
RAG_TOP_K = 3  # 检索结果数量
RAG_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# 输出配置
OUTPUT_REPORT_DIR = "output_reports"
    """)

    print("\n环境变量配置:")
    print("""
# 设置 LLM API 密钥
export LLM_API_KEY="your_api_key_here"

# 设置代理（可选）
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 设置 HuggingFace 镜像（可选）
export HF_ENDPOINT="https://hf-mirror.com"
    """)


def example_7_project_status() -> None:
    """示例 7: 查看项目状态"""
    print_section("示例 7: 查看项目状态")

    print("这个示例演示如何查看项目状态。\n")

    print("查看项目状态:")
    print("  python run.py status\n")

    print("或使用 Makefile:")
    print("  make status\n")

    print("或使用快速启动脚本:")
    print("  ./quickstart.sh status\n")

    print("输出示例:")
    print("""
📊 Calference 项目状态
════════════════════════════════════════════════════════════════

📁 项目结构:
  ✅ ITU 报告生成器: /path/to/itu_report_generator
  ✅ Calself 仿真: /path/to/Calself
  ✅ 数据目录: /path/to/data
  ✅ 输出报告: /path/to/output_reports

📄 关键文件:
  ✅ 配置文件: config.py
  ✅ 主程序: itu_interference_analyzer.py
  ✅ RAG 模块: itu_file_rag.py
  ✅ Web API: api.py

💾 数据文件:
  ✅ Chunks: 776.00 MB
  ✅ Embeddings: 2.00 MB
  ✅ 元数据: 0.50 MB
    """)


def example_8_troubleshooting() -> None:
    """示例 8: 故障排除"""
    print_section("示例 8: 常见问题和故障排除")

    print("问题 1: 缺少依赖包")
    print("  解决方案: make install\n")

    print("问题 2: LLM API 连接失败")
    print("  解决方案:")
    print("    1. 检查 API 密钥: echo $LLM_API_KEY")
    print("    2. 检查网络连接: ping api.example.com")
    print("    3. 检查配置: cat itu_report_generator/config.py\n")

    print("问题 3: RAG 数据不存在")
    print("  解决方案: python run.py prepare-rag\n")

    print("问题 4: 端口被占用")
    print("  解决方案: python run.py web-api --port 9000\n")

    print("问题 5: 权限错误")
    print("  解决方案: chmod +x quickstart.sh run.py\n")

    print("更多帮助:")
    print("  - 查看快速入门: cat QUICKSTART.md")
    print("  - 查看命令参考: cat COMMANDS.md")
    print("  - 查看项目结构: cat PROJECT_STRUCTURE.md")


def main():
    """主函数"""
    print("=" * 70)
    print("🚀 Calference 综合使用示例")
    print("=" * 70)

    examples = [
        ("1", "生成 ITU 干扰报告", example_1_itu_report),
        ("2", "运行 Calself 卫星仿真", example_2_calself_simulation),
        ("3", "启动 Web 服务", example_3_web_services),
        ("4", "RAG 检索增强", example_4_rag_retrieval),
        ("5", "批量处理多个图片", example_5_batch_processing),
        ("6", "自定义配置", example_6_custom_configuration),
        ("7", "查看项目状态", example_7_project_status),
        ("8", "故障排除", example_8_troubleshooting),
    ]

    print("\n请选择要查看的示例:\n")
    for num, title, _ in examples:
        print(f"  {num}. {title}")
    print("  0. 显示所有示例")
    print("  q. 退出\n")

    while True:
        choice = input("请输入选择 (0-8, q): ").strip().lower()

        if choice == 'q':
            print("\n👋 再见！")
            break
        elif choice == '0':
            for _, _, func in examples:
                func()
            print("\n" + "=" * 70)
            print("✅ 所有示例已显示")
            print("=" * 70)
            break
        elif choice in [str(i) for i in range(1, 9)]:
            for num, _, func in examples:
                if num == choice:
                    func()
                    break
        else:
            print("❌ 无效的选择，请重试\n")


if __name__ == "__main__":
    main()
