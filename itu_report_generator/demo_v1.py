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
from typing import Tuple, List, Dict
from PIL import Image
from autogen_core import Image as AutoGenImage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import MultiModalMessage
import shutil, subprocess
from src.aisofc_agents import create_aisofc_agents

def build_prompt(image_path: str, image_info: dict, current_date: str, use_rag: bool = True) -> Tuple[str, List[Dict]]:
    """
    Build a STRICT, Word-friendly Markdown prompt for interference analysis reporting.
    The model MUST return Markdown only (no code fences, no extraneous text).
    
    Args:
        image_path: 图片路径
        image_info: 图片信息字典
        current_date: 当前日期
        use_rag: 是否使用RAG检索ITU标准信息
    
    Returns:
        (prompt_text, rag_results): prompt文本和RAG检索结果列表
    """
    itu_refs_section = ""
    rag_results = []
    
    if use_rag:
        from src.itu_word_rag import get_itu_word_rag_instance
        
        rag = get_itu_word_rag_instance()
        if rag:
            analysis_type = image_info.get('analysis_type')
            query = f"{analysis_type} limit threshold requirement standard"
            rag_results = rag.search(query, top_k=3)
            
            if rag_results:
                itu_refs_section = rag.format_references_for_prompt(rag_results, max_length=250)
                itu_refs_section = "\n\n" + itu_refs_section + "\n"
    
    prompt_text = f"""You are a professional analyst specializing in interference analysis.
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

### 5.1 ITU Standard Compliance
- Based on the ITU standards referenced below, provide a clear assessment:
  - **Compliance Status**: **Compliant** / **Non-Compliant** / **Partially Compliant** / **Not Applicable**
  - **Key Findings**: Summarize how the observed values compare to ITU standard limits
  - **Specific Thresholds**: If applicable, cite the specific ITU limit values (e.g., EPFD limit of **-XX dB(W/m²)**)
  - **Risk Assessment**: Evaluate the risk level (Low/Moderate/High) based on compliance status
{itu_refs_section}

### 5.2 Additional Considerations
- If applicable, discuss potential threshold exceedance qualitatively (e.g., cinr/cir/EPFD/PFD etc) and uncertainty.
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
    
    return prompt_text, rag_results

async def main():
    image_path = "./data/total/oneweb_total_earth_cinr.png"
    filename = os.path.basename(image_path)
    use_rag = True
    api_key = "sk-poVFrR7aculYhRKykwkuLuHcDlSBjjfRzBYqu4xoNqpIGZFz"
    base_url = "https://api.aikeji.vip/v1"
    model_name = "gemini-2.5-flash"

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
    
    prompt_text, rag_results = build_prompt(image_path, image_info, current_date, use_rag=use_rag)
    
    if use_rag and rag_results:
        print("\n" + "=" * 60)
        print("ITU RAG 检索结果 (Top {}):".format(len(rag_results)))
        print("=" * 60)
        for i, result in enumerate(rag_results, 1):
            source = result.get('source', 'Unknown')
            score = result.get('score', 0.0)
            text = result.get('text', '')
            
            print(f"\n[{i}] {source} (相似度: {score:.4f})")
            print(f"    内容: {text.replace(chr(10), ' ')}...")
        print("=" * 60 + "\n")  

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


    agents = create_aisofc_agents(model_client)
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

    final_text = result.messages[-1].content
    final_text = final_text.replace("```markdown", "").replace("```", "").strip()
    final_text = final_text.replace("TERMINATE", "").strip()

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
    cmd = [pandoc_exe, "--from", "gfm", "--to", "docx", str(md_path), "-o", str(docx_path)]
    subprocess.run(cmd, check=True)
    print(f"Word saved (pandoc): {docx_path}")
if __name__ == "__main__":
    asyncio.run(main())