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
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage



def build_prompt(image_path: str, image_info: dict, current_date: str) -> str:
    """
    Build a STRICT, Word-friendly Markdown prompt for interference analysis reporting.
    The model MUST return Markdown only (no code fences, no extraneous text).
    """
    return f"""You are a professional analyst specializing in interference analysis.
Your task: produce a clean, Word-ready report in STRICT GitHub-Flavored Markdown (GFM).

Output rules (VERY IMPORTANT):
- Markdown ONLY. Do NOT use code fences, XML/HTML, or backticks.
- Use these constructs only: headings (#, ##, ###), bold (**text**), tables, bullet lists (- ...), numbered lists (1. ...), and plain paragraphs.
- **BOLD FORMATTING**: Use **bold** for all important values, key findings, critical numbers, and significant conclusions. Examples:
  - **Yes/No** for interference presence
  - **xx dB** for specific measurements
  - **00:00–24:00** for time ranges
  - **High/Moderate/Low** for severity levels
  - **Terrestrial microwave links** for interference sources 
  - **Adaptive filtering** for recommendations
- Be concise and professional; no speculation beyond evidence.

Structure and formatting requirements (use EXACT headings and order):

# Interference Analysis Report

## 1. Basic Information
- Use a 2-column table with bold labels on the left.
- Table must include at least: Report date, Time range, Chart title, File name, System type, Monitoring metric, Image path, Image description.

| **Field** | **Value** |
| --- | --- |
| **Report date** | {current_date} |
| **Time range** | 00:00–24:00 (24-hour format) |
| **Research institution** | **Institute of Space Internet, Fudan University** 
| **Chart title** | {image_info.get('constellation', 'Unknown')} constellation {image_info.get('terminal_type', 'Unknown')} interference analysis |
| **File name** | {image_info.get('filename', 'Unknown')} |
| **System type** | {image_info.get('terminal_type', 'Unknown')} |
| **Monitoring metric** | {image_info.get('analysis_type', 'Unknown')} |
| **Image path** | {image_path} |
| **Image description** | {image_info.get('constellation', 'Unknown')} constellation – {image_info.get('terminal_type', 'Unknown')} |

## 2. Data Analysis
- Start with a single bold line stating presence of interference.
- Then provide a metrics table and bullet explanations.

**Interference presence**: Yes/No (choose one)

### 2.1 Numerical Analysis
- Provide the table below; use N/A if unknown.
- **Note**: CINR/CIR/CNR should be positive values (dB), EPFD/PFD/INR should be negative values (dB).

| **Metric** | **Typical range** | **Minimum** | **Maximum** | **Average** |
| --- | --- | --- | --- | --- |
| **{image_info.get('analysis_type', 'Metric')}** | **[min, max] dB** | **min_value dB** | **max_value dB** | **avg_value dB** |

### 2.2 Temporal Characteristics
- Bullet the items below; be concise and specific.

- Abnormal time periods: list ranges like HH:MM–HH:MM; if none, write N/A.
- Interference duration: short-lived / sustained (estimate).
- Interference magnitude: qualitative descriptor (e.g., low/moderate/high) and rationale.

### 2.3 Variability Description
- 1–2 short paragraphs on fluctuation patterns (e.g., spikes vs stable).

### 2.4 Potential Interference Sources
- Provide 3–5 bullet hypotheses with brief rationale each.
- Link hypotheses to evidence observed in the figure.

## 3. Evidence Summary
- 3–5 bullets pointing to concrete visual cues (peaks, bands, time clusters, etc.).
- Keep each bullet one sentence.

## 4. Conclusions and Recommendations
- Write in two subsections.

### 4.1 Overall Conclusion
- 1–2 concise paragraphs summarizing impact and risk.

### 4.2 Actionable Recommendations
1. Action item with purpose and expected effect.
2. Action item with purpose and expected effect.
3. Action item with purpose and expected effect.

## 5. Compliance Considerations
- If applicable, discuss potential threshold exceedance qualitatively (e.g., cinr/cir/EPFD/PFD ect) and uncertainty.
- Note any required follow-up measurements.

## 6. Appendix: Metadata
- Bullet list with the following items (fill if known, else N/A):
- Constellation: {image_info.get('constellation', 'Unknown')}
- Terminal type: {image_info.get('terminal_type', 'Unknown')}
- Monitoring metric: {image_info.get('analysis_type', 'Unknown')}
- Source file: {image_info.get('filename', 'Unknown')}
- Path: {image_path}

Final constraints:
- Do not include any code blocks or backticks.
- Do not include any headings other than those specified above.
- Keep the report ready for direct conversion to Word without cleanup.
"""


async def main():


    image_path = "./data/total/oneweb_total_earth_cir.png"

    filename = os.path.basename(image_path)
    parts = filename.split('_')
    constellation = parts[0].capitalize() if parts else "Unknown"

    if 'earth' in filename.lower():
        terminal_type = "Ground Terminal System"
    elif 'satellite' in filename.lower():
        terminal_type = "Satellite System"
    else:
        terminal_type = "Unknown Terminal Type"

    analysis_types_map = {
        'cinr': 'CINR',
        'cir': 'CIR',
        'cnr': 'CNR',
        'epfd': 'EPFD',
        'inr': 'INR',
        'link_count': 'Link Count',
        'pfd': 'PFD',
        'temp': 'ΔT/T'
    }
    analysis_type = "Unknown"
    for k, v in analysis_types_map.items():
        if k in filename.lower():
            analysis_type = v
            break

    image_info = {
        'constellation': constellation,
        'terminal_type': terminal_type,
        'analysis_type': analysis_type,
        'filename': filename
    }
    # 4) 构造英文 Prompt（唯一封装的函数）
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt_text = build_prompt(image_path, image_info, current_date)
    # 5) 构造模型客户端（读取环境变量）
    # - 使用 OpenAI 兼容端点：从环境变量读取，默认指向 Google 兼容端点（如不需要请自行改为 OpenAI 默认）
    api_key = os.environ.get("OPENAI_API_KEY", "AIzaSyD2OboIM2cPVERwAETpfbRvkKfE3-6crZ4")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = os.environ.get("OPENAI_MODEL", "gemini-2.0-flash")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is empty. Please set a valid key in environment variables.")

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

    # 6) 构造代理们与群聊（过程式）
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
    agents = [basic_info_analyzer, detailed_analyzer, report_generator]

    termination = TextMentionTermination("TERMINATE")
    group_chat = RoundRobinGroupChat(
        agents,
        termination_condition=termination
    )

    # 7) 读取图片并构造多模态消息
    pil_image = Image.open(image_path)
    autogen_image = AutoGenImage(pil_image)

    task = MultiModalMessage(
        content=[prompt_text, autogen_image],
        source="user"
    )

    # 8) 运行并在控制台打印
    # console = Console(group_chat.run_stream(task=task))
    # await console
    from pathlib import Path
    out_dir = Path(__file__).parent / "data" / "output_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    result = await group_chat.run(task=task)
    final_text = result.messages[-1].content if result.messages else ""
    final_text = final_text.replace("```markdown", "").replace("```", "").strip()
    final_text = final_text.replace("TERMINATE", "").strip()
    # Inject figure into Markdown before section "## 2. Data Analysis"
    try:
        image_filename = os.path.basename(image_path)
        image_dest = out_dir / image_filename
        shutil.copy2(image_path, str(image_dest))

        figure_block = f"\n\n## Figure\n\n![Interference figure]({image_filename})\n\n"

        marker = "## 2. Data Analysis"
        if marker in final_text:
            final_text = final_text.replace(marker, figure_block + marker, 1)
        else:
            final_text = final_text + figure_block
    except Exception:
        pass
    md_path = out_dir / f"interference_report_en.md"
    md_path.write_text(final_text, encoding="utf-8")
    print(f"Markdown saved: {md_path}")
    # Convert to Word (.docx) if possible
    try:
        import shutil, subprocess
        docx_path = out_dir / "interference_report_en.docx"
        pandoc_exe = shutil.which("pandoc")
        if pandoc_exe:
            cmd = [pandoc_exe, "--from", "gfm", "--to", "docx", str(md_path), "-o", str(docx_path)]
            subprocess.run(cmd, check=False)
            if docx_path.exists():
                print(f"Word saved (pandoc): {docx_path}")
            else:
                print("Pandoc did not produce a DOCX file. Check pandoc installation or try pypandoc.")
    except Exception as e:
        print(f"DOCX conversion error: {e}")
    # 9) 清理资源
    await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())

#pandoc "./data/output_reports/interference_report_en.md" -o interference_report_en.docx