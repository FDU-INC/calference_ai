import json
import random
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

chunks_file = Path("test_output_step2_chunks.jsonl")
embeddings_file = Path("test_output_step3_embeddings.npy")
metadata_file = Path("test_output_step3_metadata.json")

# 1) 读取部分块
chunks = []
with chunks_file.open("r", encoding="utf-8") as f:
    for line in f:
        chunks.append(json.loads(line))
# 可选择只保留前 1000 块或随机采样
sampled = chunks[:1000]

# 2) 生成嵌入
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
texts = [item["text"] for item in sampled]
embeds = model.encode(texts, batch_size=32, show_progress_bar=True)
np.save(embeddings_file, embeds)
with metadata_file.open("w", encoding="utf-8") as f:
    json.dump(sampled, f, ensure_ascii=False, indent=2)

# 3) 简单检索测试
query = "EPFD limit requirements"
q_vec = model.encode([query])
sims = cosine_similarity(q_vec, embeds)[0]
top_idx = sims.argsort()[::-1][:3]
for rank, idx in enumerate(top_idx, 1):
    info = sampled[idx]
    print(f"Rank {rank} | Score {sims[idx]:.3f} | Source {info['source']} | Chunk {info['chunk_id']}")
    print(info["text"][:200].replace("\n", " "), "...\n")