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
# Description: Configuration - LLM API settings and path configurations

import os
from pathlib import Path

# 获取项目根目录（Calference11.3）
BASE_DIR = Path(__file__).parent.parent
MODULE_DIR = Path(__file__).parent

# 项目级别的数据目录
PROJECT_DATA_DIR = str(BASE_DIR / "data")
PROJECT_OUTPUT_DIR = str(BASE_DIR / "output_reports")

# 输入数据目录
INPUT_IMAGE_DIR = str(BASE_DIR / "data" / "input")

# 输出报告目录（项目级别）
OUTPUT_REPORT_DIR = str(BASE_DIR / "output_reports")
OUTPUT_REPORTS_DIR = str(BASE_DIR / "output_reports" / "reports")
OUTPUT_METADATA_DIR = str(BASE_DIR / "output_reports" / "metadata")
OUTPUT_DATAFLOW_DIR = str(BASE_DIR / "output_reports" / "data_flow")

ORGANIZATION_NAME = "FDU-INC"

# 默认模型与密钥
# 使用智谱 GLM-4V（单智能体方案）
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4v-flash")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    os.getenv("OPENAI_API_KEY", "870846a4f1834fb8b0b5857cbbbe3080.uc16dTxZBl3YNnhZ"),
)

# 备选：Claude 中转（支持 200K context，但 AutoGen 集成可能有问题）
# LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "claude-3-7-sonnet-20250219")
# LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://43.160.240.127:8000")
# LLM_API_KEY = os.getenv("LLM_API_KEY", "sk-ad7ecae792396cdf908ed0d8373f8fc7ee5632c7f5b6d3d4")

# RAG配置：文件系统RAG（简化版本，无需MongoDB）
RAG_DATA_DIR = str(BASE_DIR / "data" / "rag")
RAG_CHUNKS_FILE = "chunks.jsonl"
RAG_EMBEDDINGS_FILE = "embeddings.npy"
RAG_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# 本地模型缓存目录（用于离线使用）
LOCAL_MODELS_DIR = str(BASE_DIR / "data" / "models")
# 设置HuggingFace缓存目录为本地模型目录
os.environ["HF_HOME"] = LOCAL_MODELS_DIR
os.environ["TRANSFORMERS_CACHE"] = LOCAL_MODELS_DIR
os.environ["SENTENCE_TRANSFORMERS_HOME"] = LOCAL_MODELS_DIR


