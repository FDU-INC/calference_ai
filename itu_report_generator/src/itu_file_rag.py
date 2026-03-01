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
# Date: 2025-02-07
# Description: ITU File RAG - Simple RAG system based on JSONL and NumPy

"""
ITU 文件系统 RAG检索模块
基于JSONL和NumPy的简单RAG系统，无需数据库
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

# 代理设置：用于下载/加载 HuggingFace 模型（SentenceTransformer）
# 注意：同时设置大小写环境变量，兼容不同库/系统读取方式
DEFAULT_PROXY_URL = "http://10.192.54.148:7897"
os.environ.setdefault("http_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("https_proxy", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTP_PROXY", DEFAULT_PROXY_URL)
os.environ.setdefault("HTTPS_PROXY", DEFAULT_PROXY_URL)

from sentence_transformers import SentenceTransformer


class ITUFileRAG:
    """基于文件系统的简单 RAG 检索系统。

    数据来源：`chunks.jsonl` + `embeddings.npy`，无需数据库。
    """
    
    def __init__(self, 
                 data_dir: str = "data",
                 chunks_file: str = "chunks.jsonl",
                 embeddings_file: str = "embeddings.npy",
                 embedding_model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        初始化文件RAG系统
        
        Args:
            data_dir: 数据目录路径
            chunks_file: chunks文件名
            embeddings_file: embeddings文件名
            embedding_model_name: Embedding模型名称
        """
        self.data_dir = Path(data_dir)
        self.chunks_file = self.data_dir / chunks_file
        self.embeddings_file = self.data_dir / embeddings_file
        self.embedding_model_name = embedding_model_name
        
        self.chunks = []           # 文本数据列表
        self.embeddings = None     # NumPy数组 (num_chunks, embedding_dim)
        self.model = None          # Embedding模型
        
        # 加载数据
        self._load_data()
    
    def _load_data(self) -> None:
        """加载chunks和embeddings数据"""
        print("📥 正在加载RAG数据...")
        
        # 1. 加载chunks
        if self.chunks_file.exists():
            print(f"📖 加载chunks文件: {self.chunks_file}")
            with open(self.chunks_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            self.chunks.append(json.loads(line.strip()))
                        except json.JSONDecodeError as e:
                            print(f"⚠️ 解析JSON失败: {e}")
            print(f"✅ 成功加载 {len(self.chunks)} 个chunks")
        else:
            print(f"⚠️ chunks文件不存在: {self.chunks_file}")
            print("💡 提示: 请先运行 prepare_data.py 生成数据文件")
        
        # 2. 加载embeddings
        if self.embeddings_file.exists():
            print(f"📖 加载embeddings文件: {self.embeddings_file}")
            try:
                self.embeddings = np.load(self.embeddings_file)
                print(f"✅ 成功加载 {len(self.embeddings)} 个embeddings，维度: {self.embeddings.shape[1]}")
            except Exception as e:
                print(f"❌ 加载embeddings失败: {e}")
        else:
            print(f"⚠️ embeddings文件不存在: {self.embeddings_file}")
        
        # 3. 加载embedding模型（用于查询）
        # 加载策略与 download_embedding_model.py 保持一致：
        # - 使用 SentenceTransformer 的 cache_folder 参数，将模型缓存到
        #   <data_dir>/models/<embedding_model_name>
        # - 如果目录中已有模型，则直接复用，不再重新下载
        print(f"📥 正在加载embedding模型: {self.embedding_model_name}")
        try:
            model_root = self.data_dir / "models"
            model_dir = model_root / self.embedding_model_name
            print(f"📁 使用本地/缓存模型目录: {model_dir}")
            
            model_root.mkdir(parents=True, exist_ok=True)
            # 如有需要会自动从远端下载到 model_dir；若已存在则直接复用
            self.model = SentenceTransformer(self.embedding_model_name, cache_folder=str(model_dir))
            print("✅ embedding模型加载完成！")
        except Exception as e:
            print(f"❌ 模型加载失败: {e}")
            self.model = None
        
        # 验证数据一致性
        if self.chunks and self.embeddings is not None:
            if len(self.chunks) != len(self.embeddings):
                print(f"⚠️ 警告: chunks数量({len(self.chunks)})与embeddings数量({len(self.embeddings)})不匹配")
        
        print("✅ ITU 文件RAG系统初始化完成\n")
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        生成文本的embedding向量
        
        Args:
            text: 输入文本
        
        Returns:
            embedding向量（NumPy数组）
        """
        if self.model is None:
            raise RuntimeError("Embedding模型未加载")
        
        return self.model.encode(text)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        搜索相关ITU标准内容
        
        Args:
            query: 查询文本
            top_k: 返回前k个结果
        
        Returns:
            包含文本块信息的字典列表，每个字典包含：
            - text: 文本内容
            - source: 来源文件
            - chunk_id: 块ID
            - score: 相似度分数
            - doc_id: 文档ID
        """
        if not self.chunks or self.embeddings is None:
            print("⚠️ 数据未加载，无法搜索")
            return []
        
        if self.model is None:
            print("⚠️ Embedding模型未加载，无法搜索")
            return []
        
        # 1. 生成查询向量
        query_embedding = self.generate_embedding(query)
        
        # 2. 计算所有chunks的相似度（向量化计算）
        similarities = self._cosine_similarity_batch(query_embedding, self.embeddings)
        
        # 3. 获取Top-K索引
        top_k_indices = np.argsort(similarities)[::-1][:top_k]
        
        # 4. 构建结果
        results = []
        for idx in top_k_indices:
            chunk = self.chunks[idx]
            results.append({
                'doc_id': chunk.get('doc_id', ''),
                'filename': chunk.get('source', ''),
                'source': chunk.get('source', 'Unknown'),
                'text': chunk.get('text', ''),
                'chunk_id': chunk.get('chunk_id', 0),
                'score': float(similarities[idx])
            })
        
        print(f"🔍 找到 {len(results)} 个最相关chunk")
        return results
    
    def _cosine_similarity_batch(
        self, query_vec: np.ndarray, all_vecs: np.ndarray
    ) -> np.ndarray:
        """
        批量计算余弦相似度（向量化）
        
        Args:
            query_vec: 查询向量 (embedding_dim,)
            all_vecs: 所有向量 (num_chunks, embedding_dim)
        
        Returns:
            相似度数组 (num_chunks,)
        """
        # 归一化
        query_norm = query_vec / (np.linalg.norm(query_vec) + 1e-10)
        all_norms = all_vecs / (np.linalg.norm(all_vecs, axis=1, keepdims=True) + 1e-10)
        
        # 计算余弦相似度（点积）
        similarities = np.dot(all_norms, query_norm)
        
        return similarities
    
    def format_references_for_prompt(
        self, results: List[Dict], max_length: int = 300
    ) -> str:
        """
        格式化检索结果用于prompt
        
        Args:
            results: 检索结果列表
            max_length: 每个结果的最大文本长度
        
        Returns:
            格式化的文本
        """
        if not results:
            return ""
        
        lines = ["## ITU Standard Reference Information"]
        lines.append("Based on ITU recommendations, the following standards are relevant:\n")
        
        for i, result in enumerate(results, 1):
            source = result.get('source', 'Unknown')
            score = result.get('score', 0.0)
            text = result.get('text', '')
            
            # 截断文本
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            lines.append(f"### {i}. {source} (相似度: {score:.3f})")
            lines.append(f"{text}\n")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict[str, object]:
        """获取当前 RAG 状态的统计信息。"""
        stats = {
            "chunks_count": len(self.chunks),
            "embeddings_count": len(self.embeddings) if self.embeddings is not None else 0,
            "embedding_dim": self.embeddings.shape[1] if self.embeddings is not None else 0,
            "model_loaded": self.model is not None,
            "status": "ready" if (self.chunks and self.embeddings is not None and self.model) else "not_ready"
        }
        
        # 统计文档数量
        if self.chunks:
            doc_ids = set(chunk.get('doc_id', '') for chunk in self.chunks)
            stats["documents_count"] = len(doc_ids)
        
        return stats


# 全局单例
_rag_instance: Optional[ITUFileRAG] = None


def get_itu_file_rag_instance(data_dir: Optional[str] = None) -> Optional[ITUFileRAG]:
    """
    获取ITU文件RAG单例实例
    
    Args:
        data_dir: 数据目录，如果为None则使用配置文件中的设置
    
    Returns:
        ITUFileRAG实例，如果初始化失败则返回None
    """
    global _rag_instance
    
    if _rag_instance is None:
        try:
            # 尝试从配置文件导入
            if data_dir is None:
                try:
                    # 优先使用包内绝对导入（用于 Web API/作为库调用）
                    try:
                        from itu_report_generator.config import RAG_DATA_DIR
                    except Exception:
                        # 兼容脚本直接运行场景（python itu_file_rag.py）
                        from config import RAG_DATA_DIR
                    data_dir = RAG_DATA_DIR
                except (ImportError, AttributeError):
                    # 如果配置文件中没有，使用默认值
                    data_dir = "data"
            
            _rag_instance = ITUFileRAG(data_dir=data_dir)
        except Exception as e:
            print(f"❌ RAG系统初始化失败: {e}")
            return None
    
    return _rag_instance


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("ITU 文件RAG系统测试")
    print("=" * 60)
    
    # 初始化
    rag = ITUFileRAG(data_dir="../data")
    
    # 显示统计信息
    stats = rag.get_stats()
    print("\n📊 统计信息:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # 测试搜索
    if stats['status'] == 'ready':
        print("\n🔍 测试搜索:")
        query = "EPFD limit requirements"
        results = rag.search(query, top_k=3)
        
        print(f"\n查询: {query}")
        print(f"结果数量: {len(results)}\n")
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['source']} (相似度: {result['score']:.3f})")
            print(f"   {result['text'][:100]}...\n")

