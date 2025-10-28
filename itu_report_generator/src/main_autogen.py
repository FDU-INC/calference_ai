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
import asyncio
from datetime import datetime
from PIL import Image
from autogen_core import Image as AutoGenImage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import MultiModalMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.aisofc_agents import create_aisofc_agents
from src.utils import parse_image_path
from src.report_writer import WordReportWriter
from src.dialogue_visualizer import save_dialogue_html
from src.proxy_setup import enable_proxy, setup_ssl
import glob

def create_model_client():
    return OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key="AIzaSyA2frMS99Kv6C9Es3aAKavo3JzVVaNGu1E",
        #api_key="AIzaSyCJ1jMNt0_9_IO0tPElbTLXeHxTkHuOvDI",
        #api_key = "AIzaSyBMJXjh39gek8uwgf25KRZkGzIc9ObxM-g",
        model_capabilities={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
        }
    )

def create_task(image_path, lang):
    pil_image = Image.open(image_path)
    autogen_image = AutoGenImage(pil_image)
    image_info = parse_image_path(image_path, lang=lang)
    return MultiModalMessage(
        content=[
            f"Image info: {image_info}",
            autogen_image
        ],
        source="user"
    )

async def run_chat(group_chat, task, output_html=None):
    dialogue_log = []
    async for message in group_chat.run_stream(task=task):
        agent_name = getattr(message, 'source', None)
        content = message.content if hasattr(message, 'content') else str(message)
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dialogue_log.append({'time': time_str, 'agent': agent_name, 'content': content})
        print(f"\n【{agent_name or 'Unknown Agent'}】")
        print(content)
        # 实时写入HTML气泡对话（仅在指定时）
        if output_html:
            save_dialogue_html(dialogue_log, output_html)
        await asyncio.sleep(5)
        # 增加终止条件，防止死循环
        if agent_name == "report_agent" and "TERMINATE" in content:
            break
    return dialogue_log

async def run_autogen(image_path, output_dir, lang='zh', output_html=None):
    enable_proxy()
    model_client = create_model_client()
    agents = create_aisofc_agents(model_client)
    group_chat = RoundRobinGroupChat(agents)
    task = create_task(image_path, lang)
    dialogue_log = await run_chat(group_chat, task, output_html)
    await model_client.close()
    return dialogue_log

# 保留原有main入口
if __name__ == "__main__":
    IMAGE_PATH = "/mnt/data/yjh/projects/ITU/itu_report_generator/data/total/oneweb_total_earth_cinr.png"
    OUTPUT_DIR = "/mnt/data/yjh/projects/ITU/itu_report_generator/data/output_reports"  # Word报告目录
    OUTPUT_HTML = "/mnt/data/yjh/projects/ITU/itu_report_generator/data/dialogue/dialogue_log.html"  # 新的HTML保存路径
    LANG = 'en'

    # 运行前清理旧的 HTML 和 Word 报告
    if os.path.exists(OUTPUT_DIR):
        for f in glob.glob(os.path.join(OUTPUT_DIR, "*.docx")):
            os.remove(f)
    # 确保 dialogue 目录存在
    dialogue_dir = os.path.dirname(OUTPUT_HTML)
    if not os.path.exists(dialogue_dir):
        os.makedirs(dialogue_dir)

    try:
        dialogue_log = asyncio.run(run_autogen(IMAGE_PATH, OUTPUT_DIR, LANG, OUTPUT_HTML))
    except asyncio.exceptions.CancelledError:
        print("[警告] 异步任务被主动终止（CancelledError），流程已正常结束。")
        dialogue_log = None
    print("\n最终报告文本如下:\n")
    print(dialogue_log if dialogue_log else "[无报告内容]")
    # 只在有报告时保存Word
    if dialogue_log:
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        writer = WordReportWriter()
        # 提取 report_agent 的最后一条消息内容
        report_content = None
        for entry in reversed(dialogue_log):
            if entry['agent'] == 'report_agent':
                report_content = entry['content']
                break
        if isinstance(report_content, list):
            report_content = next((x for x in report_content if isinstance(x, str)), "")
        if report_content is None:
            report_content = ""
        # 生成 Word 报告，并获取路径
        if LANG == 'en':
            word_path = writer.generate_report_en(IMAGE_PATH, report_content, OUTPUT_DIR)
        else:
            word_path = writer.generate_report(IMAGE_PATH, report_content, OUTPUT_DIR, lang=LANG)
        print("报告已保存到本地Word文件。")
        # 生成报告后，刷新HTML页面，带上下载链接
        word_rel_path = os.path.join("..", "output_reports", os.path.basename(word_path))
        save_dialogue_html(dialogue_log, OUTPUT_HTML, report_docx_path=word_rel_path)
    else:
        print("未能获取到最终报告内容，未生成Word文件。")
