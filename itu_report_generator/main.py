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

import os
import sys
import config
from src.orchestrator import InterferenceReportOrchestrator

def main():
    """项目主函数"""
    print("--- 启动ITU干扰图智能分析报告生成程序 ---")

    # 确保输出目录存在
    if not os.path.exists(config.OUTPUT_REPORT_DIR):
        os.makedirs(config.OUTPUT_REPORT_DIR)
        print(f"已创建输出目录: {config.OUTPUT_REPORT_DIR}")

    # 初始化核心协调器
    orchestrator = InterferenceReportOrchestrator(
        model_path=config.MODEL_PATH,
        organization_name=config.ORGANIZATION_NAME
    )

    # 命令行参数解析
    args = sys.argv[1:]
    lang = 'zh'
    if '--lang' in args:
        try:
            lang = args[args.index('--lang')+1]
        except Exception:
            lang = 'zh'
    if not args:
        print("用法：\n  python main.py --single IMAGE_NAME  # 处理单张图片\n  python main.py --batch CONSTELLATION TERMINAL_TYPE [--max N] [--lang en/zh]  # 批量处理一类图片（如oneweb earth）\n  (不带参数则处理全部图片)")
        # 默认行为：处理全部图片
        image_files = [f for f in os.listdir(config.INPUT_IMAGE_DIR) if f.endswith('.png')]
        print(f"发现 {len(image_files)} 个图片文件，开始处理...")
        for image_file in image_files:
            image_path = os.path.join(config.INPUT_IMAGE_DIR, image_file)
            orchestrator.generate_single_report(image_path, config.OUTPUT_REPORT_DIR, lang=lang)
        print("--- 所有报告生成完毕 ---")
        return

    if args[0] == '--single' and len(args) > 1:
        image_name = args[1]
        image_path = os.path.join(config.INPUT_IMAGE_DIR, image_name)
        if not os.path.exists(image_path):
            print(f"未找到图片: {image_path}")
            return
        orchestrator.generate_single_report(image_path, config.OUTPUT_REPORT_DIR, lang=lang)
        print("--- 单张图片报告生成完毕 ---")
        return

    if args[0] == '--batch' and len(args) > 2:
        constellation = args[1].lower()
        terminal_type = args[2].lower()
        max_images = 8
        if '--max' in args:
            try:
                max_images = int(args[args.index('--max')+1])
            except Exception:
                pass
        # 直接调用新版多图分析接口，生成结构化多图报告
        orchestrator.generate_multi_image_report(
            image_dir=config.INPUT_IMAGE_DIR,
            output_dir=config.OUTPUT_REPORT_DIR,
            include_keywords=[constellation, terminal_type],
            max_images=max_images,
            lang=lang
        )
        print(f"--- {constellation} + {terminal_type} 批量图片报告生成完毕 ---")
        return

    print("参数错误。用法：\n  python main.py --single IMAGE_NAME [--lang en/zh]\n  python main.py --batch CONSTELLATION TERMINAL_TYPE [--max N] [--lang en/zh]")

if __name__ == "__main__":
    main()
