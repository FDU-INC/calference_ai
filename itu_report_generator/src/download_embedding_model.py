# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
#
# Copyright (C) 2025 FDU-INC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Author: yjh
# Date: 2026-02-07
# Description: Download Embedding Model - Utility script to download SentenceTransformer model

"""
Utility script to download the SentenceTransformer embedding model to a local folder.

Usage:
    (itu) python -m src.download_embedding_model
or:
    (itu) python src/download_embedding_model.py
"""

import os
import sys
from pathlib import Path

# 代理设置：用于下载/加载 HuggingFace 模型（SentenceTransformer）
# 注意：同时设置大小写环境变量，兼容不同库/系统读取方式
DEFAULT_PROXY_URL = "http://10.192.54.148:7897"
os.environ.setdefault("http_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("https_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTP_PROXY", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTPS_PROXY", DEFAULT_PROXY_URL)

# 将 itu_report_generator 目录添加到 Python 路径
current_dir = Path(__file__).resolve().parent
module_dir = current_dir.parent
repo_root = module_dir.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from sentence_transformers import SentenceTransformer

# 优先使用包内绝对导入；兼容脚本运行则回退到同目录导入
try:
    from itu_report_generator.config import LOCAL_MODELS_DIR, RAG_EMBEDDING_MODEL
except Exception:
    from config import LOCAL_MODELS_DIR, RAG_EMBEDDING_MODEL


def main() -> None:
    model_root = Path(LOCAL_MODELS_DIR)
    model_dir = model_root / RAG_EMBEDDING_MODEL

    print("=" * 60)
    print("Embedding model downloader")
    print("=" * 60)
    print(f"Target model name : {RAG_EMBEDDING_MODEL}")
    print(f"Target local path : {model_dir}")
    print(f"Proxy settings    : {os.environ.get('HTTP_PROXY', 'Not set')}")
    print()

    model_root.mkdir(parents=True, exist_ok=True)

    # 使用 SentenceTransformer 的 cache_folder 参数，将模型下载到指定目录
    print("📥 正在下载 / 准备本地模型（若已存在则直接复用）...")
    
    try:
        SentenceTransformer(RAG_EMBEDDING_MODEL, cache_folder=str(model_dir))
        print("✅ 模型已准备就绪。")
        print(f"   本地路径: {model_dir}")
        print()
        print("下一步：运行 demo 或前端时,将自动优先从该本地路径加载 embedding 模型。")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        print()
        print("可能的解决方案：")
        print("1. 检查代理设置是否正确")
        print("2. 检查网络连接")
        print("3. 尝试使用 HuggingFace 镜像: export HF_ENDPOINT=https://hf-mirror.com")
        raise


if __name__ == "__main__":
    main()
