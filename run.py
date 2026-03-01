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


class CalferenceRunner:
    """Calference 项目运行器"""

    # 常量定义：默认仿真参数（与 main_ms.py 保持一致）
    DEFAULT_START_TIME = "2024-12-16T00:00:00"
    DEFAULT_DURATION_HOURS = 0.1
    DEFAULT_STEP = 2
    DEFAULT_NEIGH_K = 8
    DEFAULT_NEIGH_METHOD = 2
    DEFAULT_UPDATE_VIS_METHOD = 3
    DEFAULT_BUILD_NEIGH_METHOD = 1
    DEFAULT_UPDATE_INFERENCE_METHOD = 0
    DEFAULT_SERVICE_URL = "http://localhost:8000"
    CALSELF_DATA_DIR = Path("/mnt/data/yjh/projects/Calference11.3/Calself/data")

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.itu_module = self.project_root / "itu_report_generator"
        self.calself_module = self.project_root / "Calself"

    def run_itu_report(self, image_path=None, use_rag=True):
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

    def _check_service_health(self, client, service_url):
        """
        检查 Calself 微服务健康状态

        Args:
            client: CalselfClient 实例
            service_url: 服务地址

        Returns:
            bool: 服务是否可用
        """
        print("🔍 检查 Calself 微服务状态...")
        try:
            health = client._request("GET", "/api/v1/health")
            print(f"✅ 服务状态: {health.get('status', 'unknown')}")
            print()
            return True
        except Exception as e:
            print(f"❌ 无法连接到 Calself 微服务: {e}")
            print("💡 提示: 请确认 Calself 微服务已启动且端口正确（默认 8000）")
            print("   运行: python /mnt/data/yjh/projects/Calference11.3/Calself/server.py")
            return False

    def _parse_start_time(self, start_time_str):
        """
        解析仿真开始时间

        Args:
            start_time_str: ISO 格式时间字符串，如果为 None 则使用默认值

        Returns:
            datetime 对象
        """
        from datetime import datetime

        if start_time_str:
            return datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
        else:
            # 与 main_ms.py 保持一致：datetime(2024, 12, 16, 0, 0, 0)
            return datetime(2024, 12, 16, 0, 0, 0)

    def _print_simulation_config(self, service_url, start_time, duration_hours, step, **kwargs):
        """
        打印仿真配置信息

        Args:
            service_url: 服务地址
            start_time: 开始时间
            duration_hours: 仿真时长
            step: 时间步长
            **kwargs: 其他配置参数
        """
        print("=" * 70)
        print("🛰️  运行 Calself 卫星干扰仿真（服务端执行）")
        print("=" * 70)
        print(f"🌐 服务地址: {service_url}")
        print(f"📅 开始时间: {start_time.isoformat()}")
        print(f"⏱️  仿真时长: {duration_hours} 小时")
        print(f"⏱️  时间步长: {step} 秒")
        
        # 显示其他高级参数（如果提供）
        if kwargs.get('neigh_k'):
            print(f"🔧 邻居数量: {kwargs['neigh_k']}")
        if kwargs.get('neigh_method'):
            print(f"🔧 邻居更新方法: {kwargs['neigh_method']}")
        if kwargs.get('update_vis_method'):
            print(f"🔧 可见性更新方法: {kwargs['update_vis_method']}")
        
        print()

    def _run_simulation_request(self, client, start_time, duration_hours, step, **kwargs):
        """
        发送仿真请求到服务端

        Args:
            client: CalselfClient 实例
            start_time: 开始时间
            duration_hours: 仿真时长
            step: 时间步长
            **kwargs: 其他仿真参数
                - analyse_company: 分析公司配置（字典格式）
                - cellular_dict: 蜂窝网络配置（字典格式）
                注意：neigh_k, neigh_method 等高级参数目前需要服务端支持

        Returns:
            仿真结果字典
        """
        print("📡 发送仿真请求到微服务...")
        
        # 构建请求参数（基础参数）
        sim_params = {
            'start_time': start_time,
            'duration_hours': duration_hours,
            'step': step,
        }
        
        # 添加可选的高级参数（如果服务端支持）
        if kwargs.get('analyse_company'):
            sim_params['analyse_company'] = kwargs['analyse_company']
        if kwargs.get('cellular_dict'):
            sim_params['cellular_dict'] = kwargs['cellular_dict']
        
        # 注意：neigh_k, neigh_method, update_vis_method 等参数
        # 需要服务端 SimRequest 模型支持后才能传递
        # 目前这些参数仅用于显示配置信息
        
        result = client.run_simulation(**sim_params)
        
        print("\n" + "=" * 70)
        print("✅ 仿真请求完成（结果由服务端返回）")
        print("=" * 70)
        print(f"📊 结果状态: {result.get('status', 'unknown')}")

        # 显示仿真统计信息
        if "result" in result and isinstance(result["result"], dict):
            sim_result = result["result"]
            total_time = sim_result.get("total_execution_time")
            if total_time is not None:
                print(f"⏱️  总执行时间: {total_time:.2f} 秒")
            if 'steps' in sim_result:
                print(f"📊 完成步数: {len(sim_result['steps'])}")

        print()
        return result

    def _load_inference_file(self, company_id, timestamp):
        """
        加载指定的推理结果文件

        Args:
            company_id: 公司ID（目录名）
            timestamp: 时间戳文件名

        Returns:
            加载的数据，如果失败返回 None
        """
        import json
        
        inference_dir = self.CALSELF_DATA_DIR / "inference"
        
        # 确保文件名以 .json 结尾
        if not timestamp.endswith('.json'):
            timestamp = f"{timestamp}.json"
        
        file_path = inference_dir / str(company_id) / timestamp
        
        if not file_path.exists():
            print(f"❌ 错误: 文件不存在: {file_path}")
            return None

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 显示加载信息
        if isinstance(data, dict):
            print(f"✅ 已加载 {company_id}/{timestamp}（字段数: {len(data)}）")
        elif isinstance(data, list):
            print(f"✅ 已加载 {company_id}/{timestamp}（条目数: {len(data)}）")
        else:
            print(f"✅ 已加载 {company_id}/{timestamp}（类型: {type(data).__name__}）")
        
        print(f"📁 文件路径: {file_path}")
        return data

    def _get_file_info(self, file_path):
        """
        获取文件的详细信息

        Args:
            file_path: 文件路径

        Returns:
            文件信息字典
        """
        import os
        from datetime import datetime

        stat = file_path.stat()
        file_size_mb = stat.st_size / 1024 / 1024
        
        # 尝试从文件名解析时间戳
        timestamp_str = file_path.stem
        time_info = {}
        try:
            # 假设文件名格式为 YYYYMMDDHHMMSS
            if len(timestamp_str) >= 14:
                dt = datetime.strptime(timestamp_str[:14], "%Y%m%d%H%M%S")
                time_info['parsed_time'] = dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass

        return {
            'size_mb': file_size_mb,
            'modified': datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            **time_info
        }

    def _list_inference_files(self, company_id=None, show_details=False):
        """
        列出推理结果缓存文件

        Args:
            company_id: 如果指定，只列出该目录的文件
            show_details: 是否显示详细信息（文件大小、时间等）

        Returns:
            文件字典，键为目录名，值为文件列表
        """
        inference_dir = self.CALSELF_DATA_DIR / "inference"

        if not inference_dir.exists():
            print(f"❌ 错误: 推理结果目录不存在: {inference_dir}")
            print("💡 提示: 可以使用 --run 运行一次新仿真以生成缓存")
            return None

        # 扫描所有目录
        files = {}
        for subdir in sorted(inference_dir.iterdir()):
            if subdir.is_dir():
                json_files = sorted([f.name for f in subdir.glob("*.json")])
                if json_files:
                    files[subdir.name] = json_files

        if not files:
            print("❌ 没有找到任何推理结果缓存文件")
            print("💡 提示: 可以使用 --run 运行一次新仿真以生成缓存")
            return None

        # 如果指定了 company_id，只显示该目录
        if company_id:
            company_key = str(company_id)
            if company_key in files:
                file_list = files[company_key]
                latest = file_list[-1] if file_list else None
                earliest = file_list[0] if file_list else None
                
                print(f"  {company_key}: {len(file_list)} 个文件")
                if latest:
                    print(f"    最新: {latest}")
                if earliest and earliest != latest:
                    print(f"    最早: {earliest}")
                
                # 显示详细信息
                if show_details and latest:
                    latest_path = inference_dir / company_key / latest
                    if latest_path.exists():
                        info = self._get_file_info(latest_path)
                        print(f"    大小: {info['size_mb']:.2f} MB")
                        if 'parsed_time' in info:
                            print(f"    时间: {info['parsed_time']}")
            else:
                print(f"❌ 错误: 目录 {company_key} 不存在")
                return None
        else:
            # 显示所有目录
            for company_key, file_list in files.items():
                latest = file_list[-1] if file_list else None
                earliest = file_list[0] if file_list else None
                
                print(f"  {company_key}: {len(file_list)} 个文件")
                if latest:
                    print(f"    最新: {latest}")
                if earliest and earliest != latest:
                    print(f"    最早: {earliest}")
                
                # 显示详细信息
                if show_details and latest:
                    latest_path = inference_dir / company_key / latest
                    if latest_path.exists():
                        info = self._get_file_info(latest_path)
                        print(f"    大小: {info['size_mb']:.2f} MB")

        return files

    def _get_file_statistics(self, company_id, timestamp):
        """
        获取推理结果文件的统计信息

        Args:
            company_id: 公司ID
            timestamp: 时间戳文件名

        Returns:
            统计信息字典
        """
        data = self._load_inference_file(company_id, timestamp)
        if data is None:
            return None

        stats = {
            'company_id': company_id,
            'timestamp': timestamp,
            'data_type': type(data).__name__,
        }

        if isinstance(data, dict):
            stats['keys'] = list(data.keys())
            stats['key_count'] = len(data.keys())
            # 尝试获取更多统计信息
            for key, value in data.items():
                if isinstance(value, (list, dict)):
                    stats[f'{key}_count'] = len(value)
        elif isinstance(data, list):
            stats['item_count'] = len(data)
            if data and isinstance(data[0], dict):
                stats['sample_keys'] = list(data[0].keys()) if data[0] else []

        return stats

    def _print_usage_hints(self):
        """打印使用提示"""
        print()
        print("💡 提示:")
        print("  - 列出全部缓存: python run.py calself-sim")
        print("  - 指定目录: python run.py calself-sim --company-id 1")
        print("  - 加载具体文件: python run.py calself-sim --company-id 1 --timestamp 20241216000002")
        print("  - 运行新仿真: python run.py calself-sim --run")
        print("  - 高级参数: python run.py calself-sim --run --neigh-k 10 --neigh-method 2")
        print()

    def run_calself_sim(
        self,
        company_id=None,
        timestamp=None,
        run_simulation=False,
        start_time=None,
        duration_hours=None,
        step=None,
        service_url=None,
        neigh_k=None,
        neigh_method=None,
        update_vis_method=None,
        analyse_company=None,
        cellular_dict=None,
        show_details=False,
        **kwargs
    ):
        """
        Calself 仿真：run.py 仅发出指令，实际执行在 Calself 微服务上完成

        Args:
            company_id: 推理结果目录名（例如 1 / 3 / total）
            timestamp: 推理结果文件名（例如 20241216000002.json 或 20241216000002）
            run_simulation: 是否运行新仿真（默认 False，读取缓存）
            start_time: 仿真开始时间（ISO 字符串，如 2024-12-16T00:00:00；不传则使用默认值）
            duration_hours: 仿真时长（小时，默认 0.1）
            step: 时间步长（秒，默认 2）
            service_url: Calself 微服务地址（默认 http://localhost:8000）
            neigh_k: 邻居数量（默认 8）
            neigh_method: 邻居更新方法（默认 2）
            update_vis_method: 可见性更新方法（默认 3）
            analyse_company: 分析公司配置（字典格式）
            cellular_dict: 蜂窝网络配置（字典格式）
            show_details: 是否显示缓存文件的详细信息（大小、时间等）
            **kwargs: 其他仿真参数

        Returns:
            返回码
        """
        try:
            # 检查依赖
            self._check_dependencies(["requests"])

            sys.path.insert(0, str(self.project_root))
            from calself_client.client import CalselfClient, CalselfAPIError

            # 使用默认值
            duration_hours = duration_hours or self.DEFAULT_DURATION_HOURS
            step = step or self.DEFAULT_STEP
            service_url = service_url or self.DEFAULT_SERVICE_URL

            # 运行新仿真
            if run_simulation:
                client = CalselfClient(base_url=service_url)
                
                # 健康检查
                if not self._check_service_health(client, service_url):
                    return 1

                # 解析开始时间
                sim_start_time = self._parse_start_time(start_time)

                # 打印配置信息
                self._print_simulation_config(
                    service_url, sim_start_time, duration_hours, step,
                    neigh_k=neigh_k or self.DEFAULT_NEIGH_K,
                    neigh_method=neigh_method or self.DEFAULT_NEIGH_METHOD,
                    update_vis_method=update_vis_method or self.DEFAULT_UPDATE_VIS_METHOD
                )

                # 发送仿真请求
                result = self._run_simulation_request(
                    client, sim_start_time, duration_hours, step,
                    analyse_company=analyse_company,
                    cellular_dict=cellular_dict
                )

            # 读取缓存数据（默认行为）
            # 注意：直接读取本地文件系统，避免触发服务端初始化，实现快速访问
            print("=" * 70)
            print("🛰️  读取 Calself 推理结果缓存（本地文件）")
            print("=" * 70)

            # 如果指定了 company_id 和 timestamp，加载具体文件
            if company_id and timestamp:
                print("=" * 70)
                print("🛰️  读取 Calself 推理结果缓存（本地文件）")
                print("=" * 70)
                
                data = self._load_inference_file(company_id, timestamp)
                if data is None:
                    return 1
                
                # 显示统计信息
                stats = self._get_file_statistics(company_id, timestamp)
                if stats:
                    print("\n📊 文件统计信息:")
                    for key, value in stats.items():
                        if key not in ['company_id', 'timestamp']:
                            print(f"  - {key}: {value}")
                
                return 0

            # 列出缓存文件
            files = self._list_inference_files(company_id, show_details=show_details)
            if files is None:
                return 1

            # 打印使用提示和路径信息
            self._print_usage_hints()
            print(f"📁 数据目录: {self.CALSELF_DATA_DIR}")
            print(f"📁 推理结果目录: {self.CALSELF_DATA_DIR / 'inference'}")
            print()
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            print("💡 提示: 请确认 Calself 微服务已启动且端口正确（默认 8000）")
            return 1

    def prepare_rag_data(self):
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

    def download_embedding_model(self):
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

    def start_web_api(self, host="127.0.0.1", port=8001):
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
            # FastAPI 的 Form/File 依赖 python-multipart（import 名为 multipart）
            self._check_dependencies(["fastapi", "uvicorn", "multipart"])

            # 启动 uvicorn 服务
            api_file = self.itu_module / "frontend" / "api.py"

            if not api_file.exists():
                print(f"❌ 错误: API 文件不存在: {api_file}")
                return 1

            print(f"🚀 服务启动在 http://{host}:{port}")
            print(f"📖 API 文档: http://{host}:{port}/docs")
            print()

            # 重要：必须使用当前 Python 环境启动 uvicorn
            # 避免调用到系统/用户目录下的 uvicorn（例如 Python3.6），导致依赖与导入路径错乱
            cmd = [
                sys.executable,
                "-m",
                "uvicorn",
                "itu_report_generator.frontend.api:app",
                "--host",
                host,
                "--port",
                str(port),
                "--reload",
            ]

            subprocess.run(cmd, cwd=str(self.project_root))
            return 0

        except Exception as e:
            print(f"\n❌ 错误: {e}")
            return 1

    def start_calself_service(self, host="127.0.0.1", port=8001):
        """
        启动 Calself 仿真微服务（仅限开发者使用）

        注意：Calself 模块不开源，此命令仅供开发者/管理员使用。
        普通用户应假设 Calself 服务已在后台运行。

        Args:
            host: 服务器地址
            port: 服务器端口

        Returns:
            返回码
        """
        print("=" * 70)
        print("⚠️  警告: 此命令仅供开发者/管理员使用")
        print("🛰️  启动 Calself 仿真微服务")
        print("=" * 70)
        print()
        print("💡 注意: Calself 模块不开源，普通用户应假设服务已运行")
        print("   如果服务未运行，请联系系统管理员")
        print()

        try:
            # 检查依赖
            # FastAPI 的 Form/File 依赖 python-multipart（import 名为 multipart）
            self._check_dependencies(["fastapi", "uvicorn", "multipart"])

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

    def run_example(self, example_name):
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

    def show_status(self):
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
    def _check_dependencies(packages):
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

【Calself 仿真（默认加载缓存数据）】
  python run.py calself-sim                    # 列出所有可用的缓存数据
  python run.py calself-sim --company-id 1     # 列出指定目录的缓存数据
  python run.py calself-sim --company-id 1 --timestamp 20241216000002  # 加载具体文件
  python run.py calself-sim --show-details     # 显示缓存文件的详细信息（大小、时间等）

【Calself 运行新仿真】
  python run.py calself-sim --run              # 运行新仿真（默认参数：2024-12-16T00:00:00, 0.1小时, 2秒）
  python run.py calself-sim --run --duration 0.5 --step 2  # 自定义基础参数
  python run.py calself-sim --run --start-time 2024-12-16T00:00:00  # 指定开始时间
  
【Calself 高级仿真参数】
  python run.py calself-sim --run --neigh-k 10           # 设置邻居数量为 10
  python run.py calself-sim --run --neigh-method 2       # 设置邻居更新方法（2=双向）
  python run.py calself-sim --run --update-vis-method 3  # 设置可见性更新方法（3=对比三种方法）
  python run.py calself-sim --run --neigh-k 10 --neigh-method 2  # 组合使用多个参数

【RAG 数据准备】
  python run.py prepare-rag                   # 准备RAG数据
  python run.py download-model                # 下载embedding模型

【Web 服务】
  python run.py web-api --port 8001           # 启动Web API服务
  python run.py web-api --host 0.0.0.0 --port 8001  # 指定主机和端口

【示例和状态】
  python run.py example itu_report            # 运行示例
  python run.py status                        # 显示项目状态

【架构说明】
  Calself 采用微服务架构：
  - Calself 模块（本地部署，不开源，默认在端口 8000 运行）
  - 通过 FastAPI 微服务暴露接口（默认端口 8000）
  - run.py 仅提供缓存数据加载功能，不直接调用服务
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

    # Calself 仿真（默认加载缓存，可选运行新仿真）
    calself_parser = subparsers.add_parser("calself-sim", help="Calself 仿真：默认加载缓存数据，使用 --run 运行新仿真")
    calself_parser.add_argument(
        "--run",
        action="store_true",
        help="运行新仿真（默认是加载缓存数据）"
    )
    calself_parser.add_argument(
        "--company-id",
        type=str,
        default=None,
        help="指定推理结果目录名（加载缓存时使用，例如 1 / 3 / total）"
    )
    calself_parser.add_argument(
        "--timestamp",
        type=str,
        default=None,
        help="指定要加载的推理结果文件（例如 20241216000002 或 20241216000002.json）"
    )
    calself_parser.add_argument(
        "--start-time",
        type=str,
        default=None,
        help="仿真开始时间（ISO 格式，仅在 --run 时有效；不传则使用默认值 2024-12-16T00:00:00，与 main_ms.py 一致）"
    )
    calself_parser.add_argument(
        "--duration",
        type=float,
        default=0.1,
        help="仿真时长（小时，仅在 --run 时有效，默认0.1）"
    )
    calself_parser.add_argument(
        "--step",
        type=int,
        default=2,
        help="时间步长（秒，仅在 --run 时有效，默认2）"
    )
    calself_parser.add_argument(
        "--service-url",
        type=str,
        default="http://localhost:8000",
        help="Calself 服务地址（仅在 --run 时有效，默认 http://localhost:8000）"
    )
    # 高级仿真参数
    calself_parser.add_argument(
        "--neigh-k",
        type=int,
        default=None,
        help="邻居数量（仅在 --run 时有效，默认 8）"
    )
    calself_parser.add_argument(
        "--neigh-method",
        type=int,
        default=None,
        help="邻居更新方法（仅在 --run 时有效，默认 2：双向）"
    )
    calself_parser.add_argument(
        "--update-vis-method",
        type=int,
        default=None,
        help="可见性更新方法（仅在 --run 时有效，默认 3：对比三种方法）"
    )
    calself_parser.add_argument(
        "--show-details",
        action="store_true",
        help="显示缓存文件的详细信息（大小、时间等）"
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
        default=8001,
        help="服务器端口（默认8001）"
    )

    # Calself 服务（仅限开发者）
    calself_service_parser = subparsers.add_parser(
        "calself-service",
        help="启动 Calself 仿真微服务（仅限开发者/管理员，Calself 不开源，普通用户应假设服务已运行）"
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
        default=8000,
        help="服务器端口（默认8000）"
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
            company_id=args.company_id,
            timestamp=args.timestamp,
            run_simulation=args.run,
            start_time=args.start_time,
            duration_hours=args.duration,
            step=args.step,
            service_url=args.service_url,
            neigh_k=args.neigh_k if hasattr(args, 'neigh_k') else None,
            neigh_method=args.neigh_method if hasattr(args, 'neigh_method') else None,
            update_vis_method=args.update_vis_method if hasattr(args, 'update_vis_method') else None,
            show_details=args.show_details if hasattr(args, 'show_details') else False
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
