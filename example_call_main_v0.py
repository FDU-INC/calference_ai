"""
调用 Calself/main_v0 并返回 data/inference 中文件的示例

这个脚本演示了如何：
1. 运行 main_v0 进行推理计算
2. 获取并返回 data/inference 目录中的结果文件
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 添加 Calself 到 Python 路径
sys.path.insert(0, str(Path(__file__).parent / "Calself"))


def run_main_v0() -> bool:
    """
    运行 main_v0.py 脚本
    
    Returns:
        bool: 是否成功运行
    """
    main_v0_path = Path(__file__).parent / "Calself" / "main_v0.py"
    
    try:
        print(f"正在运行 main_v0.py...")
        # 使用 subprocess 运行脚本
        result = subprocess.run(
            [sys.executable, str(main_v0_path)],
            cwd=str(main_v0_path.parent),
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("main_v0 运行成功")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"运行出错: {result.stderr}")
            if result.stdout:
                print(f"输出: {result.stdout}")
            return False
    except Exception as e:
        print(f"运行 main_v0 时发生错误: {e}")
        return False


def get_inference_files(company_id: Optional[int] = None) -> Dict[str, List[str]]:
    """
    获取 data/inference 目录中的文件
    
    Args:
        company_id: 可选的公司ID（1, 3等），如果提供则只返回该公司的文件
    
    Returns:
        Dict: 包含文件路径的字典，键为目录名，值为文件列表
    """
    inference_base = Path(__file__).parent / "Calself" / "data" / "inference"
    
    result = {}
    
    # 如果指定了公司ID，只查看该目录
    if company_id:
        company_dir = inference_base / str(company_id)
        if company_dir.exists():
            files = sorted([f.name for f in company_dir.glob("*.json")])
            result[str(company_id)] = files
    else:
        # 遍历所有子目录
        if inference_base.exists():
            for subdir in inference_base.iterdir():
                if subdir.is_dir():
                    files = sorted([f.name for f in subdir.glob("*.json")])
                    result[subdir.name] = files
    
    return result


def load_inference_file(company_id: int, timestamp: str) -> Optional[Dict]:
    """
    加载指定的推理结果文件
    
    Args:
        company_id: 公司ID（1, 3等）
        timestamp: 时间戳文件名（如 "20241216000002.json"）
    
    Returns:
        Dict: JSON 文件内容，如果文件不存在返回 None
    """
    file_path = Path(__file__).parent / "Calself" / "data" / "inference" / str(company_id) / timestamp
    
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None


def get_latest_inference_files(company_id: Optional[int] = None, limit: int = 5) -> Dict[str, List[str]]:
    """
    获取最新的推理结果文件
    
    Args:
        company_id: 可选的公司ID
        limit: 每个目录返回的文件数量
    
    Returns:
        Dict: 包含最新文件路径的字典
    """
    all_files = get_inference_files(company_id)
    
    result = {}
    for dir_name, files in all_files.items():
        # 按文件名（时间戳）排序，取最新的
        result[dir_name] = files[-limit:] if len(files) > limit else files
    
    return result


def get_all_inference_file_paths(company_id: Optional[int] = None) -> List[str]:
    """
    获取所有推理文件的完整路径列表
    
    Args:
        company_id: 可选的公司ID
    
    Returns:
        List[str]: 完整文件路径列表
    """
    inference_base = Path(__file__).parent / "Calself" / "data" / "inference"
    file_paths = []
    
    if company_id:
        company_dir = inference_base / str(company_id)
        if company_dir.exists():
            file_paths = [str(f) for f in sorted(company_dir.glob("*.json"))]
    else:
        if inference_base.exists():
            for subdir in inference_base.iterdir():
                if subdir.is_dir():
                    file_paths.extend([str(f) for f in sorted(subdir.glob("*.json"))])
    
    return file_paths


def main(run_calculation: bool = True):
    """
    主函数：运行 main_v0 并返回结果文件
    
    Args:
        run_calculation: 是否运行 main_v0 进行计算，默认为 True（每次运行都会执行计算）
    """
    print("=" * 60)
    print("Calself main_v0 调用示例")
    print("=" * 60)
    
    # 1. 运行 main_v0
    if run_calculation:
        print("\n正在运行 main_v0...")
        success = run_main_v0()
        if not success:
            print("警告: main_v0 运行失败，将使用现有结果文件")
    else:
        print("\n跳过 main_v0 运行，使用已有结果文件")
    
    # 2. 获取所有推理文件
    print("\n1. 获取所有推理文件:")
    all_files = get_inference_files()
    for dir_name, files in all_files.items():
        print(f"  {dir_name}/: {len(files)} 个文件")
        if files:
            print(f"    最新文件: {files[-1]}")
            print(f"    最早文件: {files[0]}")
    
    # 3. 获取特定公司的文件
    print("\n2. 获取公司 1 的推理文件:")
    company_1_files = get_inference_files(company_id=1)
    print(f"  文件数量: {len(company_1_files.get('1', []))}")
    if company_1_files.get('1'):
        print(f"  示例文件: {company_1_files['1'][:3]}...")  # 显示前3个
    
    # 4. 获取最新的文件
    print("\n3. 获取最新的 5 个文件:")
    latest_files = get_latest_inference_files(limit=5)
    for dir_name, files in latest_files.items():
        print(f"  {dir_name}/: {files}")
    
    # 5. 加载并显示一个示例文件
    print("\n4. 加载示例文件内容:")
    if company_1_files.get('1'):
        example_file = company_1_files['1'][0]
        data = load_inference_file(1, example_file)
        if data:
            print(f"  文件: {example_file}")
            print(f"  数据键: {list(data.keys())}")
            # 只显示部分内容，避免输出过长
            if '1' in data:
                print(f"  公司 1 的数据结构: {list(data['1'].keys()) if isinstance(data['1'], dict) else 'N/A'}")
    
    # 6. 获取所有文件的完整路径
    print("\n5. 获取所有推理文件的完整路径:")
    all_paths = get_all_inference_file_paths()
    print(f"  总文件数: {len(all_paths)}")
    if all_paths:
        print(f"  示例路径: {all_paths[0]}")
    
    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)
    
    return all_files


if __name__ == "__main__":
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="调用 Calself/main_v0 并返回结果文件")
    parser.add_argument(
        "--skip-run",
        action="store_true",
        dest="skip_run",
        help="跳过运行 main_v0，只读取已有结果文件（默认每次都会运行计算）"
    )
    args = parser.parse_args()
    
    # 返回结果文件（默认运行计算，除非指定 --skip-run）
    result_files = main(run_calculation=not args.skip_run)
    
    # 如果需要返回给调用者使用
    print(f"\n返回的文件字典包含 {len(result_files)} 个目录")

