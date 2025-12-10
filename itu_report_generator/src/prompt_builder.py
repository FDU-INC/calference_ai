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

from typing import Dict, List, Tuple


def _build_itu_refs(image_info: dict, use_rag: bool) -> Tuple[str, List[Dict]]:
    """Fetch ITU reference snippets via RAG (if available)."""
    if not use_rag:
        return "", []

    try:
        from .itu_word_rag import get_itu_word_rag_instance
    except Exception:
        return "", []

    rag_results: List[Dict] = []
    itu_refs_section = ""

    try:
        rag = get_itu_word_rag_instance()
        if rag:
            analysis_type = image_info.get("analysis_type")
            query = f"{analysis_type} limit threshold requirement standard"
            rag_results = rag.search(query, top_k=3)
            if rag_results:
                itu_refs_section = rag.format_references_for_prompt(
                    rag_results, max_length=250
                )
                itu_refs_section = "\n\n" + itu_refs_section + "\n"
    except Exception as e:
        print(f"RAG lookup failed: {e}")

    return itu_refs_section, rag_results


def build_prompt_en(
    image_path: str, image_info: dict, current_date: str, use_rag: bool = True
) -> Tuple[str, List[Dict]]:
    """English prompt (copied from demo) with optional ITU RAG references."""
    itu_refs_section, rag_results = _build_itu_refs(image_info, use_rag)

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


def build_prompt_zh(
    image_path: str, image_info: dict, current_date: str, use_rag: bool = True
) -> Tuple[str, List[Dict]]:
    """Chinese prompt aligned to the demo template (same structure,中文版)."""
    itu_refs_section, rag_results = _build_itu_refs(image_info, use_rag)

    prompt_text = f"""你是一名专业的干扰分析师。
你的任务：以严格的 Markdown（GitHub-Flavored Markdown）生成一份可直接用于 Word 的干扰分析报告。

输出规则（非常重要）：
- 只输出 Markdown，禁止代码块、HTML/XML、反引号。
- 只能使用：标题（#、##、###）、加粗（**text**）、表格、无序列表(- ...)、有序列表(1. ...)、普通段落。
- **加粗要求**：所有关键值/结论必须加粗，例如：
  - **是否存在干扰：Yes/No**
  - **具体数值：xx dB**
  - **时间范围：00:00–24:00**
  - **严重程度：高/中/低**
  - **干扰来源：地面微波链路** 等
- 保持简洁专业，基于证据，不要臆测。

结构与顺序（必须完全一致）：

# 干扰分析报告

## 1. 基本信息
- 使用2列表格，左列标签加粗。
- 至少包含：报告日期、时间范围、图表标题、文件名、系统类型、监测指标、图片路径、图片描述。

| **字段** | **取值** |
| --- | --- |
| **报告日期** | {current_date} |
| **时间范围** | 00:00–24:00 (24小时制) |
| **研究机构** | **复旦大学空间互联网研究院** |
| **图表标题** | {image_info.get('constellation', 'Unknown')} 星座 {image_info.get('terminal_type', 'Unknown')} 干扰分析 |
| **文件名** | {image_info.get('filename', 'Unknown')} |
| **系统类型** | {image_info.get('terminal_type', 'Unknown')} |
| **监测指标** | {image_info.get('analysis_type', 'Unknown')} |
| **图片路径** | {image_path} |
| **图片描述** | {image_info.get('constellation', 'Unknown')} 星座 – {image_info.get('terminal_type', 'Unknown')} |

## 2. 数据分析
- 先用单行加粗说明是否存在干扰。
- 然后给出指标表和要点说明。

**是否存在干扰**：Yes/No（二选一）

### 2.1 数值分析
- 提供下表，未知填 N/A。
- **注意**：CINR/CIR/CNR 应为正值(dB)，EPFD/PFD/INR 应为负值(dB)。

| **指标** | **典型范围** | **最小值** | **最大值** | **平均值** |
| --- | --- | --- | --- | --- |
| **{image_info.get('analysis_type', '指标')}** | **[min, max] dB** | **min_value dB** | **max_value dB** | **avg_value dB** |

### 2.2 时间特征
- 用要点列出，简洁具体。

- 异常时间段：如 HH:MM–HH:MM；无则写 N/A。
- 干扰持续性：短时 / 持续（估计）。
- 干扰强度：定性描述（低/中/高）并给出理由。

### 2.3 变化性描述
- 1–2 段简短文字说明波动模式（如尖峰/平稳）。

### 2.4 可能的干扰来源
- 给出 3–5 条假设及理由。
- 将假设与图中证据对应。

## 3. 证据总结
- 3–5 条要点，指向具体视觉证据（峰值、带状、时间簇等）。
- 每条保持一句话。

## 4. 结论与建议
- 分为两个小节。

### 4.1 总体结论
- 1–2 段，概述影响与风险。

### 4.2 可执行建议
1. 行动项，写明目的与预期效果。
2. 行动项，写明目的与预期效果。
3. 行动项，写明目的与预期效果。

## 5. 合规性考量

### 5.1 ITU 标准符合性
- 基于下方 ITU 参考，给出评估：
  - **符合性状态**：**Compliant/Non-Compliant/Partially/Not Applicable**
  - **关键结论**：观测值与ITU限值的比较
  - **具体阈值**：如 EPFD 限值 **-XX dB(W/m²)**
  - **风险评估**：Low / Moderate / High
{itu_refs_section}

### 5.2 其他考量
- 如适用，定性说明是否可能超阈值（CINR/CIR/EPFD/PFD 等）及不确定性。
- 备注需要的后续测量。

## 6. 附录：元数据
- 要点列出（未知填 N/A）：
- 星座：{image_info.get('constellation', 'Unknown')}
- 终端类型：{image_info.get('terminal_type', 'Unknown')}
- 监测指标：{image_info.get('analysis_type', 'Unknown')}
- 源文件：{image_info.get('filename', 'Unknown')}
- 路径：{image_path}

最终约束：
- 不要输出代码块或反引号。
- 只使用上述指定标题。
- 内容应可直接转为 Word，无需额外清理。
"""

    return prompt_text, rag_results


# Default alias for compatibility
build_prompt = build_prompt_en

__all__ = ["build_prompt", "build_prompt_en", "build_prompt_zh"]

