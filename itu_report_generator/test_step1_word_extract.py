"""
步骤1：Word 文本提取（单文件单输出）
目标：将 data/itu_standards_word 中的 doc/docx 分别转换为 txt，保存在 data/itu_standards_txt
"""

from pathlib import Path
import shutil
import subprocess

try:
    import docx  # python-docx
    print("✓ python-docx 已安装")
except ImportError:
    print("✗ python-docx 未安装，请先执行: pip install python-docx")
    raise SystemExit(1)

PANDOC_PATH = shutil.which("pandoc")


def convert_doc_to_docx(doc_path: Path) -> Path | None:
    """使用 pandoc 将 .doc 转换为 .docx，返回转换后的路径"""
    if not PANDOC_PATH:
        print("  ✗ 未检测到 pandoc，无法转换 .doc -> .docx")
        return None

    tmp_dir = Path(__file__).parent / "tmp_converted_docx"
    tmp_dir.mkdir(exist_ok=True)
    output_path = tmp_dir / f"{doc_path.stem}.docx"

    cmd = [PANDOC_PATH, str(doc_path), "-o", str(output_path)]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"  ✗ pandoc 转换失败: {e.stderr.decode(errors='ignore')}")
        return None


def read_docx(path: Path) -> str:
    """读取 .docx 文本"""
    doc = docx.Document(str(path))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def read_doc(path: Path) -> str | None:
    """读取 .doc：自动转换为 .docx 后解析"""
    converted = convert_doc_to_docx(path)
    if not converted:
        return None
    return read_docx(converted).strip()


def main():
    base_dir = Path(__file__).parent
    word_dir = base_dir / "data" / "itu_standards_word"
    txt_dir = base_dir / "data" / "itu_standards_txt"
    txt_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("步骤1：Word 文本提取 -> 单独 TXT")
    print("=" * 60)
    print(f"源目录: {word_dir}")
    print(f"输出目录: {txt_dir}\n")

    if not word_dir.exists():
        print("✗ 源目录不存在")
        return

    files = sorted(word_dir.glob("*.*"))
    if not files:
        print("✗ 未找到任何 Word 文件")
        return

    success_count = 0

    for file_path in files:
        suffix = file_path.suffix.lower()
        print(f"处理: {file_path.name}")

        if suffix == ".docx":
            text = read_docx(file_path)
        elif suffix == ".doc":
            text = read_doc(file_path)
            if text is None:
                print(" ⚠ 跳过（pandoc 转换失败或未安装）")
                continue
        else:
            print(" ⚠ 非 doc/docx，跳过")
            continue

        if not text:
            print(" ⚠ 文本为空或提取失败")
            continue

        # 输出到独立 TXT
        txt_path = txt_dir / f"{file_path.stem}.txt"
        txt_path.write_text(text, encoding="utf-8")
        success_count += 1

        preview = text[:200].replace("\n", " ")
        print(f"  ✓ 输出: {txt_path.name} (长度: {len(text)} 字符)")
        print(f"  预览: {preview}...\n")

    print(f"\n完成！共生成 {success_count} 个 txt 文件。")

    # 清理临时转换目录
    tmp_dir = base_dir / "tmp_converted_docx"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()