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

"""
ITU Word文档RAG检索模块
基于Word文档构建的RAG系统，用于检索ITU标准相关信息
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("警告: sentence-transformers 或 scikit-learn 未安装，RAG功能不可用")


class ITUWordRAG:
    """ITU Word文档RAG检索系统"""
    
    def __init__(self, base_dir: Optional[Path] = None):
        """
        初始化RAG系统
        
        Args:
            base_dir: 项目根目录，默认为脚本所在目录的父目录
        """
        if not RAG_AVAILABLE:
            raise ImportError("RAG依赖未安装，请运行: pip install sentence-transformers scikit-learn")
        
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        self.base_dir = Path(base_dir)
        self.chunks_file = self.base_dir / "test_output_step2_chunks.jsonl"
        self.embeddings_file = self.base_dir / "test_output_step3_embeddings.npy"
        self.metadata_file = self.base_dir / "test_output_step3_metadata.json"
        
        # 数据存储
        self.chunks: List[Dict] = []
        self.embeddings: Optional[np.ndarray] = None
        self.model: Optional[SentenceTransformer] = None
        
        # 加载数据
        self._load_data()
    
    def _load_data(self):
        """加载分块数据和向量"""
        # 检查文件是否存在
        if not self.chunks_file.exists():
            print(f"警告: 分块文件不存在: {self.chunks_file}")
            print("请先运行 test_step2_word_chunk.py 生成分块数据")
            return
        
        if not self.embeddings_file.exists() or not self.metadata_file.exists():
            print(f"警告: 向量或元数据文件不存在")
            print("请先运行 test_step3_word_embedding.py 生成向量数据")
            return
        
        # 加载分块数据
        print("加载文本块...")
        with self.chunks_file.open("r", encoding="utf-8") as f:
            for line in f:
                self.chunks.append(json.loads(line))
        
        # 加载向量（只加载前1000个，与test_step3一致）
        print("加载向量...")
        all_embeddings = np.load(self.embeddings_file)
        self.embeddings = all_embeddings[:len(self.chunks)]
        
        # 加载模型
        print("加载嵌入模型...")
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        
        print(f"✓ RAG系统初始化完成，包含 {len(self.chunks)} 个文本块")
    
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
        """
        if self.model is None or self.embeddings is None or len(self.chunks) == 0:
            print("警告: RAG系统未正确初始化")
            return []
        
        # 查询向量化
        query_embedding = self.model.encode([query])
        
        # 计算相似度
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # 排序并取前k个
        top_indices = similarities.argsort()[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            chunk_info = self.chunks[idx].copy()
            chunk_info['score'] = float(similarities[idx])
            results.append(chunk_info)
        
        return results
    
    def format_references_for_prompt(self, results: List[Dict], max_length: int = 300) -> str:
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


# 全局单例
_rag_instance: Optional[ITUWordRAG] = None


def get_itu_word_rag_instance(base_dir: Optional[Path] = None) -> Optional[ITUWordRAG]:
    """
    获取ITU Word RAG单例实例
    
    Args:
        base_dir: 项目根目录
    
    Returns:
        ITUWordRAG实例，如果初始化失败则返回None
    """
    global _rag_instance
    
    if _rag_instance is None:
        try:
            _rag_instance = ITUWordRAG(base_dir=base_dir)
        except Exception as e:
            print(f"RAG系统初始化失败: {e}")
            return None
    
    return _rag_instance

