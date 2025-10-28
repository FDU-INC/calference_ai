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
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
import shutil, subprocess

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
    image_path = os.environ.get("IMAGE_PATH", "./data/total/oneweb_total_earth_cinr.png")
    filename = os.path.basename(image_path)
    parts = filename.split('_')
    assert len(parts) > 0
    constellation = parts[0]
    teminal_type = "Ground Terminal System" if "earth" in filename.lower() else "Satellite System"
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
    analysis_type = next((v for k, v in analysis_types_map.items() if k in filename.lower()), "Unknown")
    image_info = {
        'constellation': constellation,
        'terminal_type': teminal_type,
        'analysis_type': analysis_type,
        'filename': filename
    }
    current_date = datetime.now().strftime("%Y-%m-%d")
    prompt_text = build_prompt(image_path, image_info, current_date)

    api_key = os.environ.get("OPENAI_API_KEY", "AIzaSyD2OboIM2cPVERwAETpfbRvkKfE3-6crZ4")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    model_name = os.environ.get("OPENAI_MODEL", "gemini-2.0-flash")

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

    pil_image = Image.open(image_path)
    autogen_image = AutoGenImage(pil_image)

    task = MultiModalMessage(
        content=[prompt_text, autogen_image],
        source="user"
    )

    out_dir = './data/output_reports'
    image_dir = './data/total'
    os.makedirs(out_dir, exist_ok=True)
    result = await group_chat.run(task=task)
    final_text = result.messages[-1].content if result.messages else ""
    final_text = result.messages[-1].content if result.messages else ""
    final_text = final_text.replace("```markdown", "").replace("```", "").strip()
    final_text = final_text.replace("TERMINATE", "").strip()
    import pdb;pdb.set_trace()
    # Inject figure into Markdown before section "## 2. Data Analysis"
    try:
        
        image_filename = os.path.basename(image_path)
        image_dest = os.path.join(image_dir, image_filename).replace("\\", "/")
        if not os.path.exists(image_dest):
            shutil.copy2(image_path, image_dest)
        figure_block = f"\n\n## Figure\n\n![Interference figure]({image_dest})\n\n"

        
        marker = "## 2. Data Analysis"
        if marker in final_text:
            final_text = final_text.replace(marker, figure_block + marker, 1)
        else:
            final_text = final_text + figure_block
    except Exception:
        pass
    
    md_path = os.path.join(out_dir, "interference_report_en.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(final_text)
    print(f"Markdown saved: {md_path}")
    # Convert to Word (.docx) if possible


    docx_path = os.path.join(out_dir, "interference_report_en.docx")
    pandoc_exe = shutil.which("pandoc")
    print(f"Current dir: {os.getcwd()}")
    print(f"Files here: {os.listdir('.')}")
    if not pandoc_exe:
        raise RuntimeError("Pandoc 未找到，请先安装并加入 PATH（如：conda install -c conda-forge pandoc 或 choco install pandoc -y）。")

    cmd = [pandoc_exe, "--from", "gfm", "--to", "docx", str(md_path), "-o", str(docx_path)]
    subprocess.run(cmd, check=True)
    print(f"Word saved (pandoc): {docx_path}")
if __name__ == "__main__":
    asyncio.run(main())