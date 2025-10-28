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

def get_fixed_report_structure():
    return """
# Report Structure and Content Instructions
Strictly follow the structure below and focus on analyzing the specified image:

## 1. Background
### 1.1 Overview of {system_name} Satellite System
Briefly describe the basic information of the {system_name} system, including its general characteristics as a LEO communication constellation (e.g., global broadband service), and basic constellation parameters (orbital altitude, inclination, etc.).

### 1.2 Analysis Scenario
Clarify that the purpose of this analysis is to evaluate the self-performance of the `{system_name}` system over a 24-hour simulation period, especially focusing on the **{terminal_type}** and the **{analysis_type}** indicator.

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

## 3. Simulation Results Analysis

### 3.1 Indicator Definition
- Clearly define **{analysis_type}** (e.g., CINR, CIR, etc.) and explain its significance in satellite communications.
- Briefly describe how this indicator is measured and what it represents for system performance.

### 3.2 Data Description
- Summarize the key features of the plot:
    - **Value Range:** State the minimum, maximum, and average values observed.
    - **Trend:** Describe the overall trend (e.g., stable, increasing, fluctuating).
    - **Key Features:** Highlight any peaks, troughs, or notable patterns.
- If possible, present the value range and statistics in a small markdown table.

### 3.3 Cause Analysis
- Analyze the possible reasons for the observed data characteristics, such as:
    - Satellite movement and handover events
    - Interference from other satellites or terrestrial sources
    - Atmospheric or environmental effects
    - Ground terminal configuration or operational changes
- Use bullet points for clarity.

### 3.4 Standard Comparison
- Compare the observed values to relevant ITU or industry standards (e.g., ITU-R S.1503 for CINR).
- Clearly state whether the observed performance meets, exceeds, or falls short of the required thresholds.
- If applicable, discuss the implications of any deviations from the standard.

> **Note:** Ensure each sub-section is clearly labeled and formatted for readability. Use concise, professional language.

## 4. Interference Simulation Conclusion
### 4.1 Summary
Based on the analysis, fill in a row in the summary table.
- **Analysis Dimension:** {terminal_type}
- **Key Indicator:** {analysis_type}
- **Simulation Result Range:** [Please fill in the analyzed value range]
- **ITU Standard Compliance:** [Yes/No/Partially/Not Applicable]

### 4.2 Conclusion
Based on the analysis of the current chart, provide a clear and concise final conclusion. The conclusion should cover:
1.  **Link Quality Assessment:** The performance of the `{system_name}` system under this indicator (e.g., stable link, high quality/periodic degradation, etc.).
2.  **Preliminary Compatibility Judgment:** Based on this indicator, preliminarily judge whether the `{system_name}` system meets ITU interference protection standards and whether there are risks that require further attention.

When generating tables, use standard markdown syntax: only one line of `| --- | ... |` should appear below the header row. Do not output `---` as a separator in the table content or anywhere else in the report.
""".strip()

def create_aisofc_agents(model_client):
    """Create four AISOF agents with fixed report structure for professional satellite interference analysis collaboration."""
    from autogen_agentchat.agents import AssistantAgent

    fixed_structure = get_fixed_report_structure()

    parser_agent = AssistantAgent(
        "parser_agent",
        model_client=model_client,
        description="Responsible for ITU data parsing and parameter recognition, outputs structured data.",
        system_message="""
You are the Parser Agent. Extract system_name, terminal_type, analysis_type, filename, and all basic parameters from the input. Output structured data for the other agents. Do NOT generate any report sections.
Please output your content in markdown format. Use bold, bullet points, headings, and paragraphs to make the content clear and visually appealing. Do not wrap your output in code blocks (do not use triple backticks).
"""
    )

    analysis_agent = AssistantAgent(
        "analysis_agent",
        model_client=model_client,
        description="Responsible for data analysis and pattern recognition, outputs analytical conclusions.",
        system_message="""
You are the Analysis Agent. Based on the structured data, perform detailed analysis (indicator definition, data description, cause analysis, standard comparison). Output only the analysis content for the Report Agent. Do NOT generate the full report or section headers.
Please output your content in markdown format. Use bold, bullet points, headings, and paragraphs to make the content clear and visually appealing. Do not wrap your output in code blocks (do not use triple backticks).
"""
    )

    review_agent = AssistantAgent(
        "review_agent",
        model_client=model_client,
        description="Responsible for ITU compliance checking, error detection, and logic verification, outputs compliance status.",
        system_message="""
You are the Review Agent. Review the outputs for ITU compliance and logic. Output only compliance and review content for the Report Agent. Do NOT generate the full report or section headers.
Please output your content in markdown format. Use bold, bullet points, headings, and paragraphs to make the content clear and visually appealing. Do not wrap your output in code blocks (do not use triple backticks).
"""
    )

    report_agent = AssistantAgent(
        "report_agent",
        model_client=model_client,
        description="Responsible for report generation, template adaptation, and multi-format export, outputs the final report.",
        system_message=f"""
You are the Report Agent. Integrate the outputs from the Parser, Analysis, and Review Agents. 
You MUST generate the final report strictly following this fixed structure and content requirements (do not change section titles, order, or formatting):

{fixed_structure}

Fill in all sections with the information provided by the other agents. When all content is integrated and finalized, reply TERMINATE.

The report title (and any section titles that refer to the system or analysis) MUST be automatically adapted to match the actual system, constellation, or analysis type in the provided image and data. For example, if the image is about Oneweb, the title should be 'Oneweb Satellite Network Performance Simulation Analysis Report' or similar, not a generic or fixed title. All titles and references in the report should accurately reflect the actual content and context of the image and analysis.

You MUST output ONLY the final report in markdown format, with NO extra explanations, confirmations, greetings, or any other text before or after the report. Do NOT say anything like 'Okay', 'Here is the report', 'I will now generate...', etc. Only output the report content itself.
"""
    )

    return [parser_agent, analysis_agent, review_agent, report_agent] 