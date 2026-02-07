#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calference 项目初始化脚本

用于首次设置项目，包括：
- 检查 Python 版本
- 创建必要的目录
- 安装依赖
- 下载模型
- 准备 RAG 数据
- 验证配置

使用方法：
    python init.py                  # 交互式初始化
    python init.py --auto           # 自动初始化（无需确认）
    python init.py --check          # 仅检查环境
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple


class ProjectInitializer:
    """项目初始化器"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.python_version = sys.version_info
        self.errors = []
        self.warnings = []

    def check_python_version(self) -> bool:
        """检查 Python 版本"""
        print("🔍 检查 Python 版本...")

        if self.python_version < (3, 10):
            msg = f"Python 版本过低: {self.python_version.major}.{self.python_version.minor} (需要 3.10+)"
            self.errors.append(msg)
            print(f"  ❌ {msg}")
            return False

        print(f"  ✅ Python {self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}")
        return True

    def check_directories(self) -> bool:
        """检查必要的目录"""
        print("\n🔍 检查项目目录...")

        required_dirs = [
            "itu_report_generator",
            "Calself",
            "calself_client",
            "data",
            "output_reports",
        ]

        all_exist = True
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"  ✅ {dir_name}/")
            else:
                print(f"  ⚠️  {dir_name}/ (不存在)")
                all_exist = False

        return all_exist

    def create_directories(self) -> bool:
        """创建必要的目录"""
        print("\n📁 创建必要的目录...")

        dirs_to_create = [
            "data/input",
            "data/rag",
            "data/models",
            "output_reports/reports",
            "output_reports/metadata",
            "output_reports/data_flow",
        ]

        try:
            for dir_name in dirs_to_create:
                dir_path = self.project_root / dir_name
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ {dir_name}/")
            return True
        except Exception as e:
            self.errors.append(f"创建目录失败: {e}")
            print(f"  ❌ 创建目录失败: {e}")
            return False

    def check_dependencies(self) -> Tuple[bool, list]:
        """检查依赖包"""
        print("\n🔍 检查依赖包...")

        required_packages = [
            "numpy",
            "scipy",
            "sgp4",
            "autogen",
            "openai",
            "sentence_transformers",
            "fastapi",
            "uvicorn",
            "python_docx",
            "PIL",
        ]

        missing = []
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package}")
                missing.append(package)

        return len(missing) == 0, missing

    def install_dependencies(self) -> bool:
        """安装依赖"""
        print("\n📦 安装依赖包...")

        try:
            requirements_file = self.project_root / "requirements.txt"
            if not requirements_file.exists():
                self.errors.append("requirements.txt 不存在")
                print(f"  ❌ requirements.txt 不存在")
                return False

            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                cwd=str(self.project_root),
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("  ✅ 依赖安装完成")
                return True
            else:
                self.errors.append(f"依赖安装失败: {result.stderr}")
                print(f"  ❌ 依赖安装失败")
                print(f"     {result.stderr}")
                return False
        except Exception as e:
            self.errors.append(f"安装依赖时出错: {e}")
            print(f"  ❌ 安装依赖时出错: {e}")
            return False

    def download_model(self) -> bool:
        """下载 embedding 模型"""
        print("\n📥 下载 embedding 模型...")

        try:
            result = subprocess.run(
                [sys.executable, "run.py", "download-model"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                print("  ✅ 模型下载完成")
                return True
            else:
                self.warnings.append(f"模型下载失败: {result.stderr}")
                print(f"  ⚠️  模型下载失败（可稍后手动下载）")
                return False
        except subprocess.TimeoutExpired:
            self.warnings.append("模型下载超时")
            print(f"  ⚠️  模型下载超时（可稍后手动下载）")
            return False
        except Exception as e:
            self.warnings.append(f"模型下载出错: {e}")
            print(f"  ⚠️  模型下载出错: {e}")
            return False

    def prepare_rag_data(self) -> bool:
        """准备 RAG 数据"""
        print("\n📚 准备 RAG 数据...")

        try:
            result = subprocess.run(
                [sys.executable, "run.py", "prepare-rag"],
                cwd=str(self.project_root),
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                print("  ✅ RAG 数据准备完成")
                return True
            else:
                self.warnings.append(f"RAG 数据准备失败: {result.stderr}")
                print(f"  ⚠️  RAG 数据准备失败（可稍后手动准备）")
                return False
        except subprocess.TimeoutExpired:
            self.warnings.append("RAG 数据准备超时")
            print(f"  ⚠️  RAG 数据准备超时（可稍后手动准备）")
            return False
        except Exception as e:
            self.warnings.append(f"RAG 数据准备出错: {e}")
            print(f"  ⚠️  RAG 数据准备出错: {e}")
            return False

    def check_config(self) -> bool:
        """检查配置"""
        print("\n🔍 检查配置...")

        config_file = self.project_root / "itu_report_generator" / "config.py"
        if not config_file.exists():
            self.errors.append("config.py 不存在")
            print(f"  ❌ config.py 不存在")
            return False

        # 检查 LLM 配置
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            self.warnings.append("LLM_API_KEY 环境变量未设置")
            print(f"  ⚠️  LLM_API_KEY 环境变量未设置")
            print(f"     请运行: export LLM_API_KEY='your_api_key'")
        else:
            print(f"  ✅ LLM_API_KEY 已配置")

        print(f"  ✅ config.py 存在")
        return True

    def show_summary(self) -> None:
        """显示总结"""
        print("\n" + "=" * 70)
        print("📊 初始化总结")
        print("=" * 70)

        if self.errors:
            print("\n❌ 错误:")
            for error in self.errors:
                print(f"  - {error}")

        if self.warnings:
            print("\n⚠️  警告:")
            for warning in self.warnings:
                print(f"  - {warning}")

        if not self.errors:
            print("\n✅ 初始化成功！")
            print("\n下一步:")
            print("  1. 配置 LLM API 密钥:")
            print("     export LLM_API_KEY='your_api_key'")
            print("\n  2. 运行示例:")
            print("     python run.py example itu_report")
            print("\n  3. 启动服务:")
            print("     python run.py web-api")
        else:
            print("\n❌ 初始化失败，请解决上述错误后重试")

        print()

    def run(self, auto: bool = False, check_only: bool = False) -> int:
        """运行初始化"""
        print("=" * 70)
        print("🚀 Calference 项目初始化")
        print("=" * 70)
        print()

        # 检查 Python 版本
        if not self.check_python_version():
            self.show_summary()
            return 1

        # 检查目录
        self.check_directories()

        # 创建目录
        if not self.create_directories():
            self.show_summary()
            return 1

        # 检查依赖
        deps_ok, missing = self.check_dependencies()

        if not deps_ok:
            if check_only:
                self.show_summary()
                return 1

            if not auto:
                response = input("\n缺少依赖包，是否安装? (y/n): ")
                if response.lower() != 'y':
                    print("跳过依赖安装")
                    self.show_summary()
                    return 1

            if not self.install_dependencies():
                self.show_summary()
                return 1

        if check_only:
            self.show_summary()
            return 0

        # 下载模型
        if not auto:
            response = input("\n是否下载 embedding 模型? (y/n): ")
            if response.lower() == 'y':
                self.download_model()
        else:
            self.download_model()

        # 准备 RAG 数据
        if not auto:
            response = input("\n是否准备 RAG 数据? (y/n): ")
            if response.lower() == 'y':
                self.prepare_rag_data()
        else:
            self.prepare_rag_data()

        # 检查配置
        self.check_config()

        # 显示总结
        self.show_summary()

        return 0 if not self.errors else 1


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Calference 项目初始化脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  python init.py                  # 交互式初始化
  python init.py --auto           # 自动初始化
  python init.py --check          # 仅检查环境
        """
    )

    parser.add_argument(
        "--auto",
        action="store_true",
        help="自动初始化（无需确认）"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="仅检查环境"
    )

    args = parser.parse_args()

    initializer = ProjectInitializer()
    return initializer.run(auto=args.auto, check_only=args.check)


if __name__ == "__main__":
    sys.exit(main())
