#!/mnt/data/yjh/anaconda3/envs/itu/bin/python3.10
# -*- coding: utf-8 -*-
"""
Calference 项目主运行脚本

这是项目的统一入口点，提供了所有主要功能的CLI接口：
- ITU 干扰报告生成
- Calself 卫星仿真
- RAG 数据准备
- 模型下载
- Web 服务启动

使用方法：
    python run.py --help                    # 查看帮助
    python run.py itu-report                # 生成ITU报告
    python run.py calself-sim               # 运行卫星仿真
    python run.py prepare-rag               # 准备RAG数据
    python run.py download-model            # 下载embedding模型
    python run.py web-api                   # 启动Web服务
"""

import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional


class CalferenceRunner:
    """Calference 项目运行器"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.itu_module = self.project_root / "itu_report_generator"
        self.calself_module = self.project_root / "Calself"

    def run_itu_report(self, image_path: Optional[str] = None, use_rag: bool = True) -> int:
        """
        生成 ITU 干扰报告

        Args:
            image_path: 干扰图表路径（可选）
            use_rag: 是否使用 RAG 检索

        Returns:
            返回码
        """
        print("=" * 70)
        print("🚀 启动 ITU 干扰报告生成")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["autogen_core", "autogen_agentchat", "sentence_transformers"])

            # 导入并运行
            sys.path.insert(0, str(self.itu_module))
            from itu_interference_analyzer import main
            import asyncio

            # 调用异步主函数
            asyncio.run(main(image_path=image_path, use_rag=use_rag))

            print("\n" + "=" * 70)
            print("✅ 报告生成完成！")
            print("=" * 70)
            print(f"📁 输出目录: {self.project_root / 'output_reports'}")
            print()
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def run_calself_sim(
        self,
        duration_hours: float = 0.1,
        step: int = 2,
        service_url: str = "http://localhost:8001",
        use_cache: bool = False,
        company_id: int = None
    ) -> int:
        """
        运行 Calself 卫星仿真（通过 REST API）或加载缓存数据

        Args:
            duration_hours: 仿真时长（小时）
            step: 时间步长（秒）
            service_url: Calself 服务地址
            use_cache: 是否使用缓存的静态数据而不运行新仿真
            company_id: 指定公司ID（仅在use_cache=True时有效）

        Returns:
            返回码
        """
        print("=" * 70)
        print("🛰️  启动 Calself 卫星干扰仿真")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["requests"])

            # 导入客户端
            sys.path.insert(0, str(self.project_root))
            from calself_client.client import CalselfClient, CalselfAPIError
            from datetime import datetime
            import json
            from pathlib import Path

            # 如果使用缓存数据
            if use_cache:
                print("📦 使用缓存的静态数据")
                print()

                # 使用 Calself/data 目录
                data_dir = Path(self.project_root) / "Calself" / "data"

                if company_id is not None:
                    # 加载特定公司的数据
                    company_data_dir = data_dir / "earth_station" / str(company_id)
                    if not company_data_dir.exists():
                        print(f"❌ 错误: 公司 {company_id} 的数据目录不存在: {company_data_dir}")
                        return 1

                    # 获取最新的数据文件
                    json_files = sorted(company_data_dir.glob("*.json"), reverse=True)
                    if not json_files:
                        print(f"❌ 错误: 公司 {company_id} 的数据目录中没有JSON文件")
                        return 1

                    latest_file = json_files[0]
                    print(f"📂 加载公司 {company_id} 的最新数据")
                    print(f"📄 文件: {latest_file.name}")

                    with open(latest_file) as f:
                        data = json.load(f)

                    print(f"✅ 成功加载 {len(data)} 个地球站的数据")
                    print()

                else:
                    # 列出所有可用的公司数据
                    print("📂 可用的缓存数据:")
                    earth_station_dir = data_dir / "earth_station"

                    if not earth_station_dir.exists():
                        print(f"❌ 错误: 数据目录不存在: {earth_station_dir}")
                        return 1

                    companies = {}
                    for company_dir in sorted(earth_station_dir.iterdir()):
                        if company_dir.is_dir():
                            json_files = list(company_dir.glob("*.json"))
                            if json_files:
                                latest_file = sorted(json_files, reverse=True)[0]
                                companies[company_dir.name] = {
                                    'path': company_dir,
                                    'file_count': len(json_files),
                                    'latest': latest_file.name
                                }

                    if not companies:
                        print("❌ 错误: 没有找到任何缓存数据")
                        return 1

                    for company_id_str, info in companies.items():
                        print(f"  公司 {company_id_str}: {info['file_count']} 个文件")
                        print(f"    最新: {info['latest']}")

                    print()
                    print("💡 提示: 使用 --company-id 参数指定要加载的公司")
                    print(f"   例如: python run.py calself-sim --use-cache --company-id 0")
                    print()

                print("=" * 70)
                print("✅ 缓存数据加载完成！")
                print("=" * 70)
                print(f"📁 数据目录: {data_dir}")
                print()
                return 0

            # 否则调用微服务运行仿真
            print(f"🌐 连接 Calself 微服务: {service_url}")
            print(f"⏱️  仿真时长: {duration_hours} 小时")
            print(f"⏱️  时间步长: {step} 秒")
            print()

            # 创建客户端
            client = CalselfClient(base_url=service_url)

            # 检查服务健康状态
            print("🔍 检查服务健康状态...")
            try:
                health_response = client._request("GET", "/api/v1/health")
                print(f"✅ 服务状态: {health_response.get('status', 'unknown')}")
            except Exception as e:
                print(f"⚠️  无法检查服务状态: {e}")
                print(f"💡 请确保 Calself 微服务已启动")
                print(f"   运行: python run.py calself-service --port 8001")
                print()
                print("💡 或者使用缓存数据:")
                print(f"   python run.py calself-sim --use-cache")
                return 1

            print()

            # 使用当前时间作为仿真开始时间
            start_time = datetime.now()

            print("📡 发送仿真请求到微服务...")
            print(f"   开始时间: {start_time.isoformat()}")
            result = client.run_simulation(
                start_time=start_time,
                duration_hours=duration_hours,
                step=step
            )

            print("\n" + "=" * 70)
            print("✅ 仿真完成！")
            print("=" * 70)
            print(f"📊 结果状态: {result.get('status', 'unknown')}")

            # 显示仿真统计信息
            if 'result' in result and isinstance(result['result'], dict):
                sim_result = result['result']
                if 'total_execution_time' in sim_result:
                    print(f"⏱️  总执行时间: {sim_result['total_execution_time']:.2f} 秒")
                if 'steps' in sim_result:
                    print(f"📊 完成步数: {len(sim_result['steps'])}")

            print(f"📁 数据保存位置: {Path(self.project_root) / 'Calself' / 'data'}")
            print()
            return 0

        except Exception as e:
            error_msg = str(e)
            print(f"\n❌ 错误: {error_msg}")

            # 检查是否是连接错误
            if "无法连接" in error_msg or "Connection" in error_msg:
                print(f"💡 提示: 请先启动 Calself 微服务")
                print(f"   运行: python run.py calself-service --port 8001")
                print()
                print("💡 或者使用缓存数据:")
                print(f"   python run.py calself-sim --use-cache")

            return 1

    def prepare_rag_data(self) -> int:
        """
        准备 RAG 数据（生成 chunks 和 embeddings）

        Returns:
            返回码
        """
        print("=" * 70)
        print("📚 准备 RAG 数据")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["sentence_transformers", "numpy"])

            # 运行数据准备脚本
            sys.path.insert(0, str(self.itu_module))
            from src.prepare_data import main

            main(auto_overwrite=True)

            print("\n" + "=" * 70)
            print("✅ RAG 数据准备完成！")
            print("=" * 70)
            print(f"📁 输出目录: {self.project_root / 'data' / 'rag'}")
            print()
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def download_embedding_model(self) -> int:
        """
        下载 embedding 模型到本地

        Returns:
            返回码
        """
        print("=" * 70)
        print("📥 下载 Embedding 模型")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["sentence_transformers"])

            # 运行模型下载脚本
            sys.path.insert(0, str(self.itu_module))
            from src.download_embedding_model import main

            main()

            print("\n" + "=" * 70)
            print("✅ 模型下载完成！")
            print("=" * 70)
            print(f"📁 模型目录: {self.project_root / 'data' / 'models'}")
            print()
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def start_web_api(self, host: str = "127.0.0.1", port: int = 8000) -> int:
        """
        启动 Web API 服务

        Args:
            host: 服务器地址
            port: 服务器端口

        Returns:
            返回码
        """
        print("=" * 70)
        print("🌐 启动 Web API 服务")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["fastapi", "uvicorn"])

            # 启动 uvicorn 服务
            api_file = self.itu_module / "frontend" / "api.py"

            if not api_file.exists():
                print(f"❌ 错误: API 文件不存在: {api_file}")
                return 1

            print(f"🚀 服务启动在 http://{host}:{port}")
            print(f"📖 API 文档: http://{host}:{port}/docs")
            print()

            cmd = [
                "uvicorn",
                f"itu_report_generator.frontend.api:app",
                "--host", host,
                "--port", str(port),
                "--reload"
            ]

            subprocess.run(cmd, cwd=str(self.project_root))
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def start_calself_service(self, host: str = "127.0.0.1", port: int = 8001) -> int:
        """
        启动 Calself 仿真微服务

        Args:
            host: 服务器地址
            port: 服务器端口

        Returns:
            返回码
        """
        print("=" * 70)
        print("🛰️  启动 Calself 仿真微服务")
        print("=" * 70)

        try:
            # 检查依赖
            self._check_dependencies(["fastapi", "uvicorn"])

            # 检查服务文件
            server_file = self.calself_module / "server.py"

            if not server_file.exists():
                print(f"❌ 错误: 服务文件不存在: {server_file}")
                return 1

            print(f"🚀 微服务启动在 http://{host}:{port}")
            print(f"📖 API 文档: http://{host}:{port}/docs")
            print(f"🔍 健康检查: http://{host}:{port}/api/v1/health")
            print()
            print("💡 提示: 在另一个终端运行以下命令来调用仿真:")
            print(f"   python run.py calself-sim --service-url http://{host}:{port}")
            print()

            cmd = [
                sys.executable,
                "-m", "uvicorn",
                "Calself.server:app",
                "--host", host,
                "--port", str(port)
            ]

            subprocess.run(cmd, cwd=str(self.project_root))
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def run_example(self, example_name: str) -> int:
        """
        运行示例脚本

        Args:
            example_name: 示例名称 (itu_report, calself_usage)

        Returns:
            返回码
        """
        print("=" * 70)
        print(f"📚 运行示例: {example_name}")
        print("=" * 70)

        try:
            examples_dir = self.project_root / "examples"

            if example_name == "itu_report":
                script = examples_dir / "example_itu_report.py"
            elif example_name == "calself_usage":
                script = examples_dir / "example_calself_usage.py"
            else:
                print(f"❌ 未知的示例: {example_name}")
                return 1

            if not script.exists():
                print(f"❌ 错误: 示例文件不存在: {script}")
                return 1

            print(f"🚀 运行: {script.name}")
            print()

            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(self.project_root)
            )

            return result.returncode

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def show_status(self) -> int:
        """
        显示项目状态信息

        Returns:
            返回码
        """
        print("=" * 70)
        print("📊 Calference 项目状态")
        print("=" * 70)
        print()

        # 检查目录
        print("📁 项目结构:")
        dirs = {
            "ITU 报告生成器": self.itu_module,
            "Calself 仿真": self.calself_module,
            "数据目录": self.project_root / "data",
            "输出报告": self.project_root / "output_reports",
        }

        for name, path in dirs.items():
            status = "✅" if path.exists() else "❌"
            print(f"  {status} {name}: {path}")

        print()

        # 检查关键文件
        print("📄 关键文件:")
        files = {
            "配置文件": self.itu_module / "config.py",
            "主程序": self.itu_module / "itu_interference_analyzer.py",
            "RAG 模块": self.itu_module / "src" / "itu_file_rag.py",
            "Web API": self.itu_module / "frontend" / "api.py",
        }

        for name, path in files.items():
            status = "✅" if path.exists() else "❌"
            print(f"  {status} {name}: {path.name}")

        print()

        # 检查数据文件
        print("💾 数据文件:")
        data_files = {
            "Chunks": self.project_root / "data" / "rag" / "chunks.jsonl",
            "Embeddings": self.project_root / "data" / "rag" / "embeddings.npy",
            "元数据": self.project_root / "data" / "rag" / "metadata.json",
        }

        for name, path in data_files.items():
            if path.exists():
                size = path.stat().st_size / 1024 / 1024
                print(f"  ✅ {name}: {size:.2f} MB")
            else:
                print(f"  ❌ {name}: 不存在")

        print()
        return 0

    @staticmethod
    def _check_dependencies(packages: list) -> None:
        """
        检查依赖包是否已安装

        Args:
            packages: 包名列表

        Raises:
            ImportError: 如果缺少依赖
        """
        missing = []
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)

        if missing:
            print(f"❌ 缺少依赖包: {', '.join(missing)}")
            print(f"   请运行: pip install {' '.join(missing)}")
            raise ImportError(f"缺少依赖: {missing}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Calference 项目运行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：

【ITU 干扰报告生成】
  python run.py itu-report                    # 生成ITU报告
  python run.py itu-report --image path/to/image.png  # 指定图片
  python run.py itu-report --no-rag           # 禁用RAG检索

【Calself 卫星仿真（微服务模式）】
  # 终端1: 启动 Calself 微服务
  python run.py calself-service --port 8001

  # 终端2: 调用仿真服务
  python run.py calself-sim --duration 0.5   # 运行仿真（0.5小时）
  python run.py calself-sim --service-url http://localhost:8001  # 指定服务地址

【Calself 卫星仿真（使用缓存数据）】
  python run.py calself-sim --use-cache                # 列出所有可用的缓存数据
  python run.py calself-sim --use-cache --company-id 0 # 加载 Starlink 的缓存数据
  python run.py calself-sim --use-cache --company-id 1 # 加载 OneWeb 的缓存数据

【RAG 数据准备】
  python run.py prepare-rag                   # 准备RAG数据
  python run.py download-model                # 下载embedding模型

【Web 服务】
  python run.py web-api --port 8000           # 启动Web API服务
  python run.py web-api --host 0.0.0.0 --port 8000  # 指定主机和端口

【示例和状态】
  python run.py example itu_report            # 运行示例
  python run.py status                        # 显示项目状态

【架构说明】
  Calself 采用微服务架构：
  - Calself 模块（本地部署，不开源）
  - 通过 FastAPI 微服务暴露接口
  - 开源部分通过 REST API 调用 Calself 服务
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="命令")

    # ITU 报告生成
    itu_parser = subparsers.add_parser("itu-report", help="生成 ITU 干扰报告")
    itu_parser.add_argument(
        "--image",
        type=str,
        default=None,
        help="干扰图表路径（可选）"
    )
    itu_parser.add_argument(
        "--no-rag",
        action="store_true",
        help="禁用 RAG 检索"
    )

    # Calself 仿真
    calself_parser = subparsers.add_parser("calself-sim", help="运行 Calself 卫星仿真或加载缓存数据")
    calself_parser.add_argument(
        "--duration",
        type=float,
        default=0.1,
        help="仿真时长（小时，默认0.1）"
    )
    calself_parser.add_argument(
        "--step",
        type=int,
        default=2,
        help="时间步长（秒，默认2）"
    )
    calself_parser.add_argument(
        "--service-url",
        type=str,
        default="http://localhost:8001",
        help="Calself 服务地址（默认 http://localhost:8001）"
    )
    calself_parser.add_argument(
        "--use-cache",
        action="store_true",
        help="使用缓存的静态数据而不运行新仿真"
    )
    calself_parser.add_argument(
        "--company-id",
        type=int,
        default=None,
        help="指定公司ID（仅在--use-cache时有效）"
    )

    # RAG 数据准备
    subparsers.add_parser("prepare-rag", help="准备 RAG 数据")

    # 模型下载
    subparsers.add_parser("download-model", help="下载 embedding 模型")

    # Web API
    web_parser = subparsers.add_parser("web-api", help="启动 Web API 服务")
    web_parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="服务器地址（默认127.0.0.1）"
    )
    web_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口（默认8000）"
    )

    # Calself 服务
    calself_service_parser = subparsers.add_parser(
        "calself-service",
        help="启动 Calself 仿真微服务（本地部署，不开源）"
    )
    calself_service_parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="服务器地址（默认127.0.0.1）"
    )
    calself_service_parser.add_argument(
        "--port",
        type=int,
        default=8001,
        help="服务器端口（默认8001）"
    )

    # 示例
    example_parser = subparsers.add_parser("example", help="运行示例脚本")
    example_parser.add_argument(
        "name",
        choices=["itu_report", "calself_usage"],
        help="示例名称"
    )

    # 状态
    subparsers.add_parser("status", help="显示项目状态")

    args = parser.parse_args()

    runner = CalferenceRunner()

    # 执行命令
    if args.command == "itu-report":
        return runner.run_itu_report(
            image_path=args.image,
            use_rag=not args.no_rag
        )
    elif args.command == "calself-sim":
        return runner.run_calself_sim(
            duration_hours=args.duration,
            step=args.step,
            service_url=args.service_url,
            use_cache=args.use_cache,
            company_id=args.company_id
        )
    elif args.command == "prepare-rag":
        return runner.prepare_rag_data()
    elif args.command == "download-model":
        return runner.download_embedding_model()
    elif args.command == "web-api":
        return runner.start_web_api(host=args.host, port=args.port)
    elif args.command == "calself-service":
        return runner.start_calself_service(host=args.host, port=args.port)
    elif args.command == "example":
        return runner.run_example(args.name)
    elif args.command == "status":
        return runner.show_status()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
