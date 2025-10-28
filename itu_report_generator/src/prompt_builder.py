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

def get_analysis_prompt(system_name, other_system_name, report_date, organization, image_info, image_list_str):
    """
    生成专业、结构化的分析提示词（Prompt）。
    """
    prompt = f"""
# 角色扮演
你是一名经验丰富的国际电信联盟（ITU）频轨协调专家，隶属于干扰分析任务组。你的核心任务是根据一系列复杂的仿真干扰图，撰写一份全面、严谨、专业的卫星网络性能分析报告。报告的格式、术语和分析深度必须严格遵循专业标准。

# 任务目标
基于以下提供的关于 **{system_name}** 星座的性能仿真图（本次分析聚焦于其中一张），生成一份完整的Word文档格式的分析报告。

# 报告基本信息
- **报告标题:** {system_name}卫星网络性能仿真分析报告
- **分析机构:** {organization}
- **报告日期:** {report_date}

---

# 报告正文结构与内容指令
请严格按照以下结构生成报告，并重点分析提供的 `{image_info['filename']}` 这张图：

## 1. 背景介绍
### 1.1 {system_name} 卫星系统概述
简要描述{system_name}系统的基本情况，包括其作为LEO通信星座的通用特性（如提供全球宽带服务）、星座基本参数（轨道高度、倾角等）。

### 1.2 分析场景说明
明确本次分析的目的在于评估`{system_name}`系统在24小时仿真周期内的自身性能，特别是分析 **{image_info['terminal_type']}** 的 **{image_info['analysis_type']}** 指标。

## 2. 仿真条件与分析依据
### 2.1 干扰保护标准
引用相关的ITU建议书或国际标准作为评判依据。例如：
- PFD/EPFD图表，需引用ITU-R S.1503等建议书的限值。
- ΔT/T图表，需引用ITU-R S.735等建议书的标准。
- CINR/CIR/CNR/INR是衡量链路质量的关键指标，数值越高代表性能越好。

### 2.2 仿真输入参数
*(请根据通用知识，创建两个表格填充典型参数，以保持报告结构的完整性)*
- **表1: {system_name} 地球站典型参数** (包含天线增益、波束宽度等)
- **表2: {system_name} 卫星链路典型参数** (包含频率范围、带宽、方向、EIRP等)

## 3. 仿真结果分析 (重点分析部分)
### 3.1 {system_name} {image_info['terminal_type']} 性能分析
请对提供的 **`{image_info['filename']}`** 这张图进行深入、详细的分析。分析必须包含以下几点：
1.  **指标定义:** 清晰解释 **{image_info['analysis_type']}** 的物理意义和在卫星通信中的作用。
2.  **数据描述:** 详细描述图表中曲线的**数值范围**（最大值、最小值、平均值）、**变化趋势**和**关键特征**（例如：峰值、谷值、波动性、周期性）。
3.  **原因分析:** 对观察到的现象进行专业解释。例如，`link_count`的变化与卫星过顶和切换有关；CINR的剧烈波动可能由卫星切换、波束边缘效应或来自`{other_system_name}`的瞬时干扰导致。
4.  **标准比对:** (如果适用) 将观测值（特别是PFD, EPFD, ΔT/T）与第2.1节中提到的ITU标准进行比较，判断是否超标。

## 4. 干扰仿真结论
### 4.1 结果汇总
基于对`{image_info['filename']}`的分析，在汇总表格中填写一行。
- **分析维度:** {image_info['terminal_type']}
- **关键指标:** {image_info['analysis_type']}
- **仿真结果范围:** [请填写分析出的数值范围]
- **是否满足ITU标准:** [是/否/部分满足/不适用]

### 4.2 结论
基于对当前图表的分析，给出一个明确、简洁的最终结论。结论应涵盖：
1.  **链路质量评估:** `{system_name}`系统在该指标下的性能表现（例如：链路稳定，质量较高/存在周期性恶化等）。
2.  **兼容性初步判断:** 基于该指标，初步判断`{system_name}`系统是否满足国际电联的干扰保护标准，是否存在需要进一步关注的风险。
"""
    return prompt.strip()

def get_multi_image_analysis_prompt(system_name, other_system_name, report_date, organization, image_infos, image_list_str):
    """
    生成适用于多张图片的专业、结构化分析提示词（Prompt），第3章开头插入所有图片，3.1为整体分析，3.2为结果汇总表。
    image_infos: List[dict]，每个dict包含 filename, terminal_type, analysis_type
    """
    # 构建图片文件名列表
    image_filenames = [img['filename'] for img in image_infos]
    image_list_md = '\n'.join([f"- {fn}" for fn in image_filenames])
    # 构建结论表格行
    summary_table_rows = ""
    for image_info in image_infos:
        summary_table_rows += f"| {image_info['filename']} | {image_info['terminal_type']} | {image_info['analysis_type']} | [请填写分析出的数值范围] | [是/否/部分满足/不适用] |\n"

    prompt = f"""
# 角色扮演
你是一名经验丰富的国际电信联盟（ITU）频轨协调专家，隶属于干扰分析任务组。你的核心任务是根据一系列复杂的仿真干扰图，撰写一份全面、严谨、专业的卫星网络性能分析报告。报告的格式、术语和分析深度必须严格遵循专业标准。

# 任务目标
基于以下提供的关于 **{system_name}** 星座的多张性能仿真图，生成一份完整的Word文档格式的分析报告。

# 报告基本信息
- **报告标题:** {system_name}卫星网络性能仿真分析报告
- **分析机构:** {organization}
- **报告日期:** {report_date}

---

# 报告正文结构与内容指令
请严格按照以下结构生成报告，并整体分析所有图片：

## 1. 背景介绍
### 1.1 {system_name} 卫星系统概述
简要描述{system_name}系统的基本情况，包括其作为LEO通信星座的通用特性（如提供全球宽带服务）、星座基本参数（轨道高度、倾角等）。

### 1.2 分析场景说明
明确本次分析的目的在于评估`{system_name}`系统在24小时仿真周期内的自身性能，特别是分析各类终端的关键指标。

## 2. 仿真条件与分析依据
### 2.1 干扰保护标准
引用相关的ITU建议书或国际标准作为评判依据。例如：
- PFD/EPFD图表，需引用ITU-R S.1503等建议书的限值。
- ΔT/T图表，需引用ITU-R S.735等建议书的标准。
- CINR/CIR/CNR/INR是衡量链路质量的关键指标，数值越高代表性能越好。

### 2.2 仿真输入参数
*(请根据通用知识，创建两个表格填充典型参数，以保持报告结构的完整性)*
- **表1: {system_name} 地球站典型参数** (包含天线增益、波束宽度等)
- **表2: {system_name} 卫星链路典型参数** (包含频率范围、带宽、方向、EIRP等)

### 2.3 分析图表清单
明确本次分析的数据来源是关于`{system_name}`系统的一系列仿真图，相关图表系列包括：
{image_list_str}

## 3. 仿真结果分析
请将下列所有仿真图片统一插入本章节开头：
{image_list_md}

### 3.1 性能分析（整体分析所有图片）
请对所有提供的图片进行整体、对比性分析，内容包括：
1. **共性与趋势**：描述所有图片数据的整体变化趋势、共性特征（如波动、峰值、周期性等）。
2. **关键特征与差异**：指出各图片之间的主要差异和各自的关键特征。
3. **原因分析**：对整体和个别现象进行专业解释（如卫星切换、干扰、波束边缘效应等）。
4. **标准比对**：将所有观测值与ITU标准进行对比，判断是否超标。

### 3.2 结果汇总表
请将所有图片的关键数据、数值范围、是否满足标准等信息汇总到下表：

| 图表 | 分析维度 | 关键指标 | 仿真结果范围 | 是否满足ITU标准 |
|------|----------|----------|--------------|-----------------|
{summary_table_rows}

## 4. 干扰仿真结论
### 4.1 结果汇总
基于上述多张图的分析，在下表中填写每张图的分析结论。

| 图表 | 分析维度 | 关键指标 | 仿真结果范围 | 是否满足ITU标准 |
|------|----------|----------|--------------|-----------------|
{summary_table_rows}

### 4.2 结论
基于所有图表的分析，给出一个明确、简洁的最终结论。结论应涵盖：
1.  **链路质量评估:** `{system_name}`系统在各项指标下的整体性能表现（例如：链路稳定，质量较高/存在周期性恶化等）。
2.  **兼容性初步判断:** 基于所有指标，初步判断`{system_name}`系统是否满足国际电联的干扰保护标准，是否存在需要进一步关注的风险。
"""
    return prompt.strip()

def get_analysis_prompt_en(system_name, other_system_name, report_date, organization, image_info, image_list_str):
    """
    Generate a professional, structured analysis prompt in English.
    """
    prompt = f"""
# Role Play
You are an experienced ITU (International Telecommunication Union) frequency coordination expert, part of the interference analysis task force. Your core task is to write a comprehensive, rigorous, and professional satellite network performance analysis report based on a series of complex simulation interference plots. The format, terminology, and analytical depth of the report must strictly adhere to professional standards.

# Task Objective
Based on the following performance simulation plots of the **{system_name}** constellation (focus on one specific image for this analysis), generate a complete analysis report in Word document format.

# Basic Report Information
- **Report Title:** {system_name} Satellite Network Performance Simulation Analysis Report
- **Organization:** {organization}
- **Report Date:** {report_date}

---

# Report Structure and Content Instructions
Strictly follow the structure below and focus on analyzing the image `{image_info['filename']}`:

## 1. Background
### 1.1 Overview of {system_name} Satellite System
Briefly describe the basic information of the {system_name} system, including its general characteristics as a LEO communication constellation (e.g., global broadband service), and basic constellation parameters (orbital altitude, inclination, etc.).

### 1.2 Analysis Scenario
Clarify that the purpose of this analysis is to evaluate the self-performance of the `{system_name}` system over a 24-hour simulation period, especially focusing on the **{image_info['terminal_type']}** and the **{image_info['analysis_type']}** indicator.

## 2. Simulation Conditions and Analytical Basis
### 2.1 Interference Protection Standards
List and cite the relevant ITU recommendations or international standards as evaluation criteria. For example:
- For CINR/CIR/CNR/INR, refer to **ITU-R S.1503** for minimum CINR requirements.
- For ΔT/T, refer to **ITU-R S.735** for time synchronization standards.
- Higher values of CINR/CIR/CNR/INR indicate better link quality.
Please explicitly list the standard numbers and their main requirements in the report.

### 2.2 Simulation Input Parameters
*(Please create two tables with typical parameters based on general knowledge to maintain report completeness)*
- **Table 1: Typical Parameters of {system_name} Earth Station** (including antenna gain, beamwidth, etc.)
- **Table 2: Typical Parameters of {system_name} Satellite Link** (including frequency range, bandwidth, direction, EIRP, etc.)

## 3. Simulation Results Analysis (Key Section)
### 3.1 Performance Analysis of {system_name} {image_info['terminal_type']}
Provide an in-depth and detailed analysis of the image **`{image_info['filename']}`**. The analysis must include:
1.  **Indicator Definition:** Clearly explain the physical meaning of **{image_info['analysis_type']}** and its role in satellite communications.
2.  **Data Description:** Describe in detail the **value range** (max, min, average), **trend**, and **key features** (e.g., peaks, troughs, volatility, periodicity) of the chart curves.
3.  **Cause Analysis:** Professionally explain the observed phenomena. For example, changes in `link_count` are related to satellite pass and handover; sharp CINR fluctuations may be caused by satellite handover, beam edge effects, or instantaneous interference from `{other_system_name}`.
4.  **Standard Comparison:** (If applicable) Compare observed values (especially PFD, EPFD, ΔT/T) with ITU standards mentioned in Section 2.1 to determine compliance.

## 4. Interference Simulation Conclusion
### 4.1 Summary
Based on the analysis of `{image_info['filename']}`, fill in a row in the summary table.
- **Analysis Dimension:** {image_info['terminal_type']}
- **Key Indicator:** {image_info['analysis_type']}
- **Simulation Result Range:** [Please fill in the analyzed value range]
- **ITU Standard Compliance:** [Yes/No/Partially/Not Applicable]

### 4.2 Conclusion
Based on the analysis of the current chart, provide a clear and concise final conclusion. The conclusion should cover:
1.  **Link Quality Assessment:** The performance of the `{system_name}` system under this indicator (e.g., stable link, high quality/periodic degradation, etc.).
2.  **Preliminary Compatibility Judgment:** Based on this indicator, preliminarily judge whether the `{system_name}` system meets ITU interference protection standards and whether there are risks that require further attention.

When generating tables, use standard markdown syntax: only one line of `| --- | ... |` should appear below the header row. Do not output `---` as a separator in the table content or anywhere else in the report.
"""
    return prompt.strip()


def get_multi_image_analysis_prompt_en(system_name, other_system_name, report_date, organization, image_infos, image_list_str):
    """
    Generate a professional, structured analysis prompt in English for multiple images.
    image_infos: List[dict] with filename, terminal_type, analysis_type
    """
    image_filenames = [img['filename'] for img in image_infos]
    image_list_md = '\n'.join([f"- {fn}" for fn in image_filenames])
    summary_table_rows = ""
    for image_info in image_infos:
        summary_table_rows += f"| {image_info['filename']} | {image_info['terminal_type']} | {image_info['analysis_type']} | [Please fill in the analyzed value range] | [Yes/No/Partially/Not Applicable] |\n"

    prompt = f"""
# Role Play
You are an experienced ITU (International Telecommunication Union) frequency coordination expert, part of the interference analysis task force. Your core task is to write a comprehensive, rigorous, and professional satellite network performance analysis report based on a series of complex simulation interference plots. The format, terminology, and analytical depth of the report must strictly adhere to professional standards.

# Task Objective
Based on the following multiple performance simulation plots of the **{system_name}** constellation, generate a complete analysis report in Word document format.

# Basic Report Information
- **Report Title:** {system_name} Satellite Network Performance Simulation Analysis Report
- **Organization:** {organization}
- **Report Date:** {report_date}

---

# Report Structure and Content Instructions
Strictly follow the structure below and analyze all images as a whole:

## 1. Background
### 1.1 Overview of {system_name} Satellite System
Briefly describe the basic information of the {system_name} system, including its general characteristics as a LEO communication constellation (e.g., global broadband service), and basic constellation parameters (orbital altitude, inclination, etc.).

### 1.2 Analysis Scenario
Clarify that the purpose of this analysis is to evaluate the self-performance of the `{system_name}` system over a 24-hour simulation period, especially focusing on key indicators for various terminals.

## 2. Simulation Conditions and Analytical Basis
### 2.1 Interference Protection Standards
Cite relevant ITU recommendations or international standards as evaluation criteria. For example:
- For PFD/EPFD charts, refer to ITU-R S.1503 limits.
- For ΔT/T charts, refer to ITU-R S.735 standards.
- CINR/CIR/CNR/INR are key indicators of link quality; higher values indicate better performance.

### 2.2 Simulation Input Parameters
*(Please create two tables with typical parameters based on general knowledge to maintain report completeness)*
- **Table 1: Typical Parameters of {system_name} Earth Station** (including antenna gain, beamwidth, etc.)
- **Table 2: Typical Parameters of {system_name} Satellite Link** (including frequency range, bandwidth, direction, EIRP, etc.)

### 2.3 List of Analytical Charts
Clarify that the data source for this analysis is a series of simulation plots of the `{system_name}` system. The related chart series include:
{image_list_str}

## 3. Simulation Results Analysis
Insert all the following simulation images at the beginning of this section:
{image_list_md}

### 3.1 Performance Analysis (Overall Analysis of All Images)
Provide an overall and comparative analysis of all provided images, including:
1. **Commonalities and Trends:** Describe the overall trends and common features (e.g., fluctuations, peaks, periodicity) of all image data.
2. **Key Features and Differences:** Point out the main differences and key features of each image.
3. **Cause Analysis:** Professionally explain overall and individual phenomena (e.g., satellite handover, interference, beam edge effects, etc.).
4. **Standard Comparison:** Compare all observed values with ITU standards to determine compliance.

### 3.2 Summary Table
Summarize the key data, value ranges, and ITU standard compliance for all images in the table below:

| Chart | Analysis Dimension | Key Indicator | Simulation Result Range | ITU Standard Compliance |
|-------|-------------------|---------------|------------------------|------------------------|
{summary_table_rows}

## 4. Interference Simulation Conclusion
### 4.1 Summary
Based on the above analysis of multiple images, fill in the analysis conclusion for each image in the table below.

| Chart | Analysis Dimension | Key Indicator | Simulation Result Range | ITU Standard Compliance |
|-------|-------------------|---------------|------------------------|------------------------|
{summary_table_rows}

### 4.2 Conclusion
Based on the analysis of all charts, provide a clear and concise final conclusion. The conclusion should cover:
1.  **Link Quality Assessment:** The overall performance of the `{system_name}` system under each indicator (e.g., stable link, high quality/periodic degradation, etc.).
2.  **Preliminary Compatibility Judgment:** Based on all indicators, preliminarily judge whether the `{system_name}` system meets ITU interference protection standards and whether there are risks that require further attention.
"""
    return prompt.strip()

def build_qwen_vl_multimodal_messages(image_paths, text_prompt):
    """
    构建Qwen2.5 VL多图推理的messages格式
    """
    content = []
    for img_path in image_paths:
        if not img_path.startswith("file://"):
            img_path = "file://" + os.path.abspath(img_path)
        content.append({
            "type": "image",
            "image": img_path,
            "resized_height": 512,
            "resized_width": 512
        })
    content.append({"type": "text", "text": text_prompt})
    return [{"role": "user", "content": content}]

