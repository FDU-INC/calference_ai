"""
测试RAG集成到demo.py
验证RAG功能是否正常工作
"""

from pathlib import Path
from datetime import datetime
import sys

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from demo import build_prompt

def test_rag_integration():
    """测试RAG集成"""
    print("=" * 60)
    print("测试RAG集成到demo.py")
    print("=" * 60)
    
    # 模拟图片信息
    image_info = {
        'constellation': 'OneWeb',
        'terminal_type': 'Ground Terminal System',
        'analysis_type': 'EPFD',
        'filename': 'oneweb_total_earth_epfd.png'
    }
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 测试启用RAG
    print("\n1. 测试启用RAG:")
    print("-" * 60)
    prompt_with_rag = build_prompt(
        image_path="./data/total/test.png",
        image_info=image_info,
        current_date=current_date,
        use_rag=True
    )
    
    # 检查prompt中是否包含ITU标准引用
    if "ITU Standard Reference Information" in prompt_with_rag:
        print("✓ RAG功能正常工作，已找到ITU标准引用")
        # 显示引用部分
        start_idx = prompt_with_rag.find("## ITU Standard Reference Information")
        if start_idx != -1:
            ref_section = prompt_with_rag[start_idx:start_idx+500]
            print("\n引用部分预览:")
            print(ref_section)
    else:
        print("⚠ 未找到ITU标准引用，可能RAG未正确初始化或未找到相关结果")
    
    # 测试禁用RAG
    print("\n\n2. 测试禁用RAG:")
    print("-" * 60)
    prompt_without_rag = build_prompt(
        image_path="./data/total/test.png",
        image_info=image_info,
        current_date=current_date,
        use_rag=False
    )
    
    if "ITU Standard Reference Information" not in prompt_without_rag:
        print("✓ RAG功能已正确禁用")
    else:
        print("✗ RAG功能未正确禁用")
    
    print("\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_rag_integration()

