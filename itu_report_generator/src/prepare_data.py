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
# Description: Data Preparation - Generate chunks and embeddings from ITU standard documents

"""
数据准备脚本
从ITU标准文档生成chunks和embeddings
读取 itu_report_generator/data/itu_standards_txt/ 中的ITU标准文档
生成 data/rag/chunks.jsonl 和 data/rag/embeddings.npy
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# 代理设置：用于下载/加载 HuggingFace 模型（SentenceTransformer）
# 注意：同时设置大小写环境变量，兼容不同库/系统读取方式
DEFAULT_PROXY_URL = "http://10.192.54.148:7897"
os.environ.setdefault("http_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("https_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTP_PROXY", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTPS_PROXY", DEFAULT_PROXY_URL)

from sentence_transformers import SentenceTransformer


# 配置
BASE_DIR = Path(__file__).parent.parent
PROJECT_ROOT = BASE_DIR.parent

# ITU 标准文档在模块内
INPUT_DIR = BASE_DIR / "data" / "itu_standards_txt"

# 输出到项目级别的 RAG 目录
OUTPUT_DIR = PROJECT_ROOT / "data" / "rag"
CHUNKS_FILE = OUTPUT_DIR / "chunks.jsonl"
EMBEDDINGS_FILE = OUTPUT_DIR / "embeddings.npy"
METADATA_FILE = OUTPUT_DIR / "metadata.json"

EMBEDDING_MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
CHUNK_SIZE = 500  # 每个chunk的字符数
CHUNK_OVERLAP = 50  # chunk之间的重叠字符数


def load_text_file(file_path: Path) -> str:
    """加载文本文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"⚠️ 读取文件失败 {file_path}: {e}")
        return ""


def split_text_into_chunks(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """
    将文本分割成chunks
    
    Args:
        text: 输入文本
        chunk_size: 每个chunk的大小
        overlap: chunk之间的重叠
    
    Returns:
        chunks列表
    """
    if not text:
        return []
    
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        
        # 如果不是最后一个chunk，尝试在句子边界处分割
        if end < text_length:
            # 查找最后一个句号、问号或换行符
            last_period = max(chunk.rfind('.'), chunk.rfind('。'), chunk.rfind('\n'))
            if last_period > chunk_size * 0.5:  # 至少保留一半的chunk
                chunk = chunk[:last_period + 1]
                end = start + last_period + 1
        
        chunks.append(chunk.strip())
        start = end - overlap
    
    return chunks


def process_documents(input_dir: Path) -> List[Dict]:
    """
    处理所有文档，生成chunks
    
    Args:
        input_dir: 输入目录
    
    Returns:
        chunks列表
    """
    all_chunks = []
    
    if not input_dir.exists():
        print(f"⚠️ 输入目录不存在: {input_dir}")
        return all_chunks
    
    # 获取所有txt文件
    txt_files = list(input_dir.glob("*.txt"))
    print(f"📁 找到 {len(txt_files)} 个文本文件")
    
    for file_path in txt_files:
        print(f"📖 处理文件: {file_path.name}")
        
        # 读取文本
        text = load_text_file(file_path)
        if not text:
            continue
        
        # 分割成chunks
        chunks = split_text_into_chunks(text)
        print(f"   生成 {len(chunks)} 个chunks")
        
        # 构建chunk数据
        doc_id = file_path.stem  # 文件名（不含扩展名）
        for chunk_id, chunk_text in enumerate(chunks):
            all_chunks.append({
                'doc_id': doc_id,
                'chunk_id': chunk_id,
                'text': chunk_text,
                'source': file_path.name
            })
    
    print(f"\n✅ 总共生成 {len(all_chunks)} 个chunks")
    return all_chunks


def generate_embeddings(chunks: List[Dict], model: SentenceTransformer) -> np.ndarray:
    """
    生成所有chunks的embeddings
    
    Args:
        chunks: chunks列表
        model: embedding模型
    
    Returns:
        embeddings数组 (num_chunks, embedding_dim)
    """
    print("\n📥 正在生成embeddings...")
    
    texts = [chunk['text'] for chunk in chunks]
    
    # 批量生成embeddings
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    print(f"✅ 生成完成，形状: {embeddings.shape}")
    return embeddings


def save_chunks(chunks: List[Dict], output_file: Path):
    """保存chunks到JSONL文件"""
    print(f"\n💾 保存chunks到: {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + '\n')
    
    print(f"✅ 保存完成")


def save_embeddings(embeddings: np.ndarray, output_file: Path):
    """保存embeddings到npy文件"""
    print(f"\n💾 保存embeddings到: {output_file}")
    
    np.save(output_file, embeddings)
    
    print(f"✅ 保存完成")


def save_metadata(chunks: List[Dict], embeddings: np.ndarray, output_file: Path):
    """保存元数据"""
    print(f"\n💾 保存元数据到: {output_file}")
    
    # 统计文档信息
    doc_stats = {}
    for chunk in chunks:
        doc_id = chunk['doc_id']
        if doc_id not in doc_stats:
            doc_stats[doc_id] = {'chunks_count': 0, 'source': chunk['source']}
        doc_stats[doc_id]['chunks_count'] += 1
    
    metadata = {
        'total_chunks': len(chunks),
        'embedding_dim': int(embeddings.shape[1]),
        'model_name': EMBEDDING_MODEL_NAME,
        'created_at': datetime.now().isoformat(),
        'chunk_size': CHUNK_SIZE,
        'chunk_overlap': CHUNK_OVERLAP,
        'documents': [
            {'doc_id': doc_id, **stats}
            for doc_id, stats in doc_stats.items()
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 保存完成")


def main(auto_overwrite: bool = False):
    """
    主函数

    Args:
        auto_overwrite: 是否自动覆盖现有文件
    """
    print("=" * 60)
    print("ITU 数据准备脚本")
    print("=" * 60)
    print(f"输入目录: {INPUT_DIR}")
    print(f"输出目录: {OUTPUT_DIR}")
    print()

    # 检查是否已有数据文件
    if CHUNKS_FILE.exists() or EMBEDDINGS_FILE.exists():
        print("⚠️ 警告: 数据文件已存在")
        print(f"  - {CHUNKS_FILE.name}: {'存在' if CHUNKS_FILE.exists() else '不存在'}")
        print(f"  - {EMBEDDINGS_FILE.name}: {'存在' if EMBEDDINGS_FILE.exists() else '不存在'}")

        if auto_overwrite:
            print("\n自动覆盖现有文件")
        else:
            response = input("\n是否覆盖现有文件? (y/n): ")
            if response.lower() != 'y':
                print("❌ 操作已取消")
                return
        print()

    # 1. 处理文档，生成chunks
    chunks = process_documents(INPUT_DIR)

    if not chunks:
        print("❌ 没有生成任何chunks，请检查输入目录")
        return

    # 2. 加载embedding模型
    print(f"\n📥 正在加载embedding模型: {EMBEDDING_MODEL_NAME}")
    try:
        model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        print("✅ 模型加载完成")
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return

    # 3. 生成embeddings
    embeddings = generate_embeddings(chunks, model)

    # 4. 保存数据
    save_chunks(chunks, CHUNKS_FILE)
    save_embeddings(embeddings, EMBEDDINGS_FILE)
    save_metadata(chunks, embeddings, METADATA_FILE)

    # 5. 显示统计信息
    print("\n" + "=" * 60)
    print("🎉 数据准备完成！")
    print("=" * 60)
    print(f"📊 统计信息:")
    print(f"  - 文档数量: {len(set(c['doc_id'] for c in chunks))}")
    print(f"  - Chunks数量: {len(chunks)}")
    print(f"  - Embeddings维度: {embeddings.shape[1]}")
    print(f"  - 文件大小:")
    print(f"    - {CHUNKS_FILE.name}: {CHUNKS_FILE.stat().st_size / 1024:.2f} KB")
    print(f"    - {EMBEDDINGS_FILE.name}: {EMBEDDINGS_FILE.stat().st_size / 1024:.2f} KB")
    print()
    print("💡 现在可以运行 demo_v1.py 或 demo_v2.py 测试RAG系统")


if __name__ == '__main__':
    main()


