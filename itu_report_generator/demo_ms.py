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
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from PIL import Image
from autogen_core import Image as AutoGenImage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage

from flask import Flask, request, jsonify, send_file

from demo import build_prompt

app = Flask(__name__)

async def generate_report_async(image_path, image_info, current_date):
    """异步生成报告的核心逻辑"""
    api_key = "AIzaSyD2OboIM2cPVERwAETpfbRvkKfE3-6crZ4"
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    model_name = "gemini-2.0-flash"
    
    model_client = OpenAIChatCompletionClient(
        model=model_name,
        base_url=base_url,
        api_key=api_key,
        model_capabilities={
            "vision": True,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
        }
    )
    
    try:
        prompt_text = build_prompt(image_path, image_info, current_date)
        
        basic_info_analyzer = AssistantAgent(
            "basic_info_analyzer",
            model_client=model_client,
            description="Analyze basic context info from interference figure.",
            system_message="You only extract and structure the Basic Information section. Wait for others after finishing."
        )
        
        detailed_analyzer = AssistantAgent(
            "detailed_analyzer",
            model_client=model_client,
            description="Analyze interference patterns and numerical characteristics.",
            system_message="You only provide Data Analysis. Wait for others after finishing."
        )
        
        report_generator = AssistantAgent(
            "report_generator",
            model_client=model_client,
            description="Synthesize a complete interference analysis report.",
            system_message="""You must integrate the Basic Information from basic_info_analyzer and Data Analysis from detailed_analyzer into a complete report following the exact Markdown structure provided in the user's prompt. 

Do NOT just say TERMINATE. You must provide the full integrated report with all sections (Basic Information, Data Analysis, Evidence Summary, Conclusions, etc.) before saying TERMINATE."""
        )
        
        # Create group chat
        agents = [basic_info_analyzer, detailed_analyzer, report_generator]
        termination = TextMentionTermination("TERMINATE")
        group_chat = RoundRobinGroupChat(
            agents,
            termination_condition=termination
        )
        
        # Load image and create multimodal message
        pil_image = Image.open(image_path)
        autogen_image = AutoGenImage(pil_image)
        
        task = MultiModalMessage(
            content=[prompt_text, autogen_image],
            source="user"
        )
        
        # Run analysis
        result = await group_chat.run(task=task)
        final_text = result.messages[-1].content if result.messages else ""
        final_text = final_text.replace("```markdown", "").replace("```", "").strip()
        final_text = final_text.replace("TERMINATE", "").strip()
        
        return final_text
        
    finally:
        # 确保客户端被正确关闭
        await model_client.close()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'success': True,
        'service': 'multi_agent_report_service',
        'status': 'healthy'
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    """Generate interference analysis report using multi-agent system"""
    try:
        image_name = request.form.get('image_name')
        download = request.form.get('download', 'false').lower() == 'true'
        root = Path(__file__).parent
        out_dir = root / "data" / "output_reports"
        images_dir = root / "data" / "total"
        out_dir.mkdir(parents=True, exist_ok=True)
        images_dir.mkdir(parents=True, exist_ok=True)
        
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                dest = images_dir / file.filename
                if dest.exists():
                    image_path = str(dest)
                else:
                    file.save(str(dest))
                    image_path = str(dest)
        else:
            if not image_name:
                return jsonify({
                    'success': False,
                    'error': 'Provide image_name or upload a file'
                }), 400
            dest = images_dir / image_name
            if dest.exists():
                image_path = str(dest)
            else:
                return jsonify({
                    'success': False,
                    'error': f'File not found in images directory: {image_name}'
                }), 404

        filename = os.path.basename(image_path)
        constellation = filename.split('_')[0].capitalize() if filename else "Unknown"
        terminal_type = "Ground Terminal System" if "earth" in filename.lower() else ("Satellite System" if "satellite" in filename.lower() else "Unknown Terminal Type")
        metric_map = {"cinr": "CINR", "cir": "CIR", "cnr": "CNR", "epfd": "EPFD", "inr": "INR", "link_count": "Link Count", "pfd": "PFD", "temp": "ΔT/T"}
        analysis_type = next((v for k, v in metric_map.items() if k in filename.lower()), "Unknown")
        image_info = {"constellation": constellation, "terminal_type": terminal_type, "analysis_type": analysis_type, "filename": filename}

        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 调用异步函数生成报告
        final_text = asyncio.run(generate_report_async(image_path, image_info, current_date))
        
        # 添加图片插入逻辑
        try:
            image_filename = os.path.basename(image_path)
            image_dest = os.path.join(str(images_dir), image_filename).replace("\\", "/")
            if not os.path.exists(image_dest):
                shutil.copy2(image_path, image_dest)
            figure_block = f"\n\n## Figure\n\n![Interference figure]({image_dest})\n\n"
            
            marker = "## 2. Data Analysis"
            if marker in final_text:
                final_text = final_text.replace(marker, figure_block + marker, 1)
            else:
                final_text = final_text + figure_block
        except Exception as e:
            print(f"Error inserting image: {str(e)}")
        
        md_path = out_dir / f"interference_report_en.md"
        md_path.write_text(final_text, encoding="utf-8")
        docx_path = out_dir / "interference_report_en.docx"
        pandoc_exe = shutil.which("pandoc")
        if pandoc_exe:
            cmd = [pandoc_exe, "--from", "gfm", "--to", "docx", str(md_path), "-o", str(docx_path)]
            subprocess.run(cmd, check=False)
            if docx_path.exists():
                print(f"Word saved (pandoc): {docx_path}")
            else:
                print("Pandoc did not produce a DOCX file. Check pandoc installation or try pypandoc.")
        else:
            print(f"DOCX conversion error")

        return jsonify({
            'success': True,
            'data': {
                'markdown_path': str(md_path),
                'docx_path': str(docx_path),
                'metric': analysis_type,
                'constellation': constellation,
                'terminal_type': terminal_type,
                'filename': filename,
            },
            'message': 'Report generated successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("Starting Multi-Agent ITU Report Generator Service on http://localhost:5005")
    app.run(host='0.0.0.0', port=5005, debug=True)