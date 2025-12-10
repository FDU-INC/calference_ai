"""
步骤2：文本清洗与分块
目标：把 data/itu_standards_txt 中的标准文本拆成可用于向量化的文本块
"""

from pathlib import Path
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter


def clean_text(text: str) -> str:
    """基础清洗：去掉多余空行、分页符、不可见字符"""
    text = text.replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = text.replace("…", "...")
    text = text.replace("***", "")
    # 只保留有内容的行
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def main():
    base_dir = Path(__file__).parent
    txt_dir = base_dir / "data" / "itu_standards_txt"
    output_path = base_dir / "test_output_step2_chunks.jsonl"

    if not txt_dir.exists():
        print(f"✗ 文本目录不存在: {txt_dir}")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    all_chunks = []
    total_files = 0

    print("=" * 60)
    print("步骤2：文本清洗与分块")
    print("=" * 60)
    print(f"输入目录: {txt_dir}")
    print(f"输出文件: {output_path}\n")

    for txt_file in sorted(txt_dir.glob("*.txt")):
        total_files += 1
        raw_text = txt_file.read_text(encoding="utf-8")
        cleaned = clean_text(raw_text)
        chunks = splitter.split_text(cleaned)

        print(f"{txt_file.name}: {len(chunks)} 块")

        for idx, chunk in enumerate(chunks):
            all_chunks.append({
                "source": txt_file.name,
                "chunk_id": idx,
                "text": chunk,
            })

    if not all_chunks:
        print("✗ 没有生成任何文本块，检查输入文件是否为空")
        return

    with output_path.open("w", encoding="utf-8") as f:
        for item in all_chunks:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\n共处理 {total_files} 个文件，生成 {len(all_chunks)} 个文本块")
    print(f"详情已写入: {output_path}")


if __name__ == "__main__":
    main()