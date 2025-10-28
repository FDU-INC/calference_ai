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
from PIL import Image
import asyncio
from datetime import datetime
from autogen_core import Image as AutoGenImage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
from src.utils import parse_image_path
from src.proxy_setup import enable_proxy

def create_model_client():
    """创建模型客户端"""
    return OpenAIChatCompletionClient(
        model="gemini-2.0-flash",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key="AIzaSyA_NEbwL2Ur4XPNjEg1eHdGfoL66sjeY5o",
        model_capabilities={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
        }
    )

def parse_image_path(image_path):
    """解析图片路径，提取星座名称和终端类型信息"""
    filename = os.path.basename(image_path)
    parts = filename.split('_')
    
    # 提取星座名称
    constellation = parts[0].capitalize()  # OneWeb, Omni
    
    # 提取终端类型
    if 'earth' in filename:
        terminal_type = "地面终端系统"
    elif 'satellite' in filename:
        terminal_type = "卫星系统"
    else:
        terminal_type = "未知终端类型"
    
    # 提取分析类型
    analysis_types = {
        'cinr': 'CINR（载干噪比）',
        'cir': 'CIR（载干比）',
        'cnr': 'CNR（载噪比）',
        'epfd': 'EPFD（等效功率通量密度）',
        'inr': 'INR（干扰噪声比）',
        'link_count': '链路数量',
        'pfd': 'PFD（功率通量密度）',
        'temp': 'ΔT/T'
    }
    
    analysis_type = "未知分析类型"
    for key, value in analysis_types.items():
        if key in filename.lower():
            analysis_type = value
            break
    
    return {
        'constellation': constellation,
        'terminal_type': terminal_type,
        'analysis_type': analysis_type,
        'filename': filename
    }

def create_agents(model_client):
    """创建专门用于干扰分析的AI助手"""
    basic_info_analyzer = AssistantAgent(
        "basic_info_analyzer",
        model_client=model_client,
        description="专门负责分析干扰分析图的基本信息和上下文",
        system_message="""你是一位专业的干扰分析基本信息分析专家。你的职责仅限于提取和整理基本信息部分：

1. 基本信息部分必须包含：
   - 报告日期
   - 时间范围
   - 图表名称
   - 图表文件名
   - 系统类型
   - 监测指标

请只提供这部分信息，不要涉及数据分析或结论建议。完成后请等待其他分析员的意见。""",
    )

    detailed_analyzer = AssistantAgent(
        "detailed_analyzer",
        model_client=model_client,
        description="专门负责深入分析干扰模式和数值特征",
        system_message="""你是一位专业的干扰分析详细分析专家。你的职责仅限于数据分析部分：

1. 干扰情况判断（是/否存在明显干扰）
2. 干扰数值分析：
   - 典型值范围
   - 最小值
   - 最大值
   - 平均值
3. 时间特征分析：
   - 异常时间段
   - 干扰持续时间
   - 干扰幅度
4. 波动特性描述
5. 潜在干扰源分析

请只提供这部分分析内容，不要涉及基本信息或结论建议。完成后请等待其他分析员的意见。""",
    )

    report_generator = AssistantAgent(
        "report_generator",
        model_client=model_client,
        description="专门负责生成综合性的干扰分析报告",
        system_message="""你是一位专业的干扰分析报告生成专家。你的职责是：

1. 等待并整合其他分析员的信息：
   - 基本信息分析员提供的基本信息
   - 详细分析员提供的数据分析结果

2. 基于以上信息，生成结论与建议部分：
   - 总体结论
   - 具体建议措施
   - 后续行动建议

3. 将三部分内容整合成一份完整的报告

当分析完成且所有观点都已整合时，请回复TERMINATE。""",
    )

    return [basic_info_analyzer, detailed_analyzer, report_generator]

def create_group_chat(agents):
    """创建群聊"""
    termination = TextMentionTermination("TERMINATE")
    return RoundRobinGroupChat(
        agents,
        termination_condition=termination
    )

def create_task(image_path):
    """创建干扰分析任务"""
    pil_image = Image.open(image_path)
    autogen_image = AutoGenImage(pil_image)
    image_info = parse_image_path(image_path)
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    return MultiModalMessage(
        content=[
            f"""请根据提供的干扰分析图，生成一份专业的中文干扰分析报告。

图片信息：
- 图片路径：{image_path}
- 图片类型：干扰分析图
- 图片描述：{image_info['constellation']}星座{image_info['terminal_type']}干扰分析图

报告需要包含以下关键信息：

1. 基本信息
- 报告日期：{current_date}
- 时间范围：00:00 - 24:00 (24小时制)
- 图表名称：{image_info['constellation']}星座{image_info['terminal_type']}干扰分析
- 图表文件名：{image_info['filename']}
- 系统类型：{image_info['terminal_type']}
- 监测指标：{image_info['analysis_type']}

2. 数据分析
- 干扰情况判断（是/否存在明显干扰）
- 干扰数值分析：
  * 典型值范围
  * 最小值
  * 最大值
  * 平均值
- 时间特征分析：
  * 异常时间段
  * 干扰持续时间
  * 干扰幅度
- 波动特性描述
- 潜在干扰源分析

3. 结论与建议
- 总体结论
- 具体建议措施
- 后续行动建议

请确保报告内容专业、准确，重点突出干扰特征和关键数据。""",
            autogen_image
        ],
        source="user"
    )

async def run_chat(group_chat, task):
    """运行群聊"""
    console = Console(group_chat.run_stream(task=task))
    await console

async def main():
    """主函数"""
    # 开启代理
    enable_proxy()
    
    # 创建客户端和助手
    model_client = create_model_client()
    agents = create_agents(model_client)
    group_chat = create_group_chat(agents)
    
    # 创建并运行任务
    task = create_task("./data/total/oneweb_total_earth_cinr.png")
    await run_chat(group_chat, task)
    
    # 清理资源
    await model_client.close()

if __name__ == "__main__":
    asyncio.run(main()) 