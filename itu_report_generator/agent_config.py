# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
#
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
#
# Author: yjh
# Date: 2026-02-07
# Description: Agent Configuration - Role definitions and data flow management

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AgentRole(Enum):
    """Agent角色定义"""
    PARSER = "parser"
    ANALYSIS = "analysis"
    REVIEW = "review"
    REPORT = "report"


@dataclass
class AgentConfig:
    """Agent配置"""
    name: str
    role: AgentRole
    description: str
    max_tokens: int
    temperature: float
    system_message: str
    input_source: Optional[str] = None  # 数据来源：'image', 'parser', 'analysis', 'review'
    output_format: str = "text"  # 'json', 'text', 'markdown'
    termination_marker: str = ""  # 完成标记


class DataFlowManager:
    """
    管理agent间的数据流转

    特点：
    1. 追踪每个agent的输入和输出
    2. 支持数据验证和转换
    3. 支持中间结果缓存
    4. 支持流程审计日志
    """

    def __init__(self):
        self.data_flow = {}  # {agent_name: {"input": ..., "output": ...}}
        self.audit_log = []  # 审计日志

    def record_input(self, agent_name: str, input_data: Any, source: str) -> None:
        """记录agent的输入"""
        if agent_name not in self.data_flow:
            self.data_flow[agent_name] = {}

        self.data_flow[agent_name]["input"] = {
            "data": input_data,
            "source": source,
            "timestamp": self._get_timestamp(),
        }

        self.audit_log.append({
            "event": "input_recorded",
            "agent": agent_name,
            "source": source,
            "timestamp": self._get_timestamp(),
        })

    def record_output(self, agent_name: str, output_data: Any, format_type: str = "text") -> None:
        """记录agent的输出"""
        if agent_name not in self.data_flow:
            self.data_flow[agent_name] = {}

        self.data_flow[agent_name]["output"] = {
            "data": output_data,
            "format": format_type,
            "timestamp": self._get_timestamp(),
        }

        self.audit_log.append({
            "event": "output_recorded",
            "agent": agent_name,
            "format": format_type,
            "timestamp": self._get_timestamp(),
        })

    def get_agent_output(self, agent_name: str) -> Optional[Any]:
        """获取agent的输出"""
        if agent_name in self.data_flow and "output" in self.data_flow[agent_name]:
            return self.data_flow[agent_name]["output"]["data"]
        return None

    def get_data_flow_summary(self) -> Dict[str, Any]:
        """获取数据流转摘要"""
        summary = {}
        for agent_name, flow in self.data_flow.items():
            summary[agent_name] = {
                "has_input": "input" in flow,
                "has_output": "output" in flow,
                "input_source": flow.get("input", {}).get("source"),
                "output_format": flow.get("output", {}).get("format"),
            }
        return summary

    def export_audit_log(self, filepath: str) -> None:
        """导出审计日志"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.audit_log, f, indent=2, ensure_ascii=False)

    def export_data_flow(self, filepath: str) -> None:
        """导出数据流转记录"""
        # 转换为可序列化的格式
        serializable_flow = {}
        for agent_name, flow in self.data_flow.items():
            serializable_flow[agent_name] = {
                "input": {
                    "source": flow.get("input", {}).get("source"),
                    "timestamp": flow.get("input", {}).get("timestamp"),
                    "data_preview": str(flow.get("input", {}).get("data"))[:200],
                } if "input" in flow else None,
                "output": {
                    "format": flow.get("output", {}).get("format"),
                    "timestamp": flow.get("output", {}).get("timestamp"),
                    "data_preview": str(flow.get("output", {}).get("data"))[:200],
                } if "output" in flow else None,
            }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable_flow, f, indent=2, ensure_ascii=False)

    @staticmethod
    def _get_timestamp() -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


class AgentConfigBuilder:
    """Agent配置构建器"""

    @staticmethod
    def build_parser_config() -> AgentConfig:
        """构建Parser Agent配置"""
        return AgentConfig(
            name="parser_agent",
            role=AgentRole.PARSER,
            description="Parse ITU interference map and extract structured data",
            max_tokens=1024,
            temperature=0.2,
            system_message=(
                "You are the Parser Agent. Your ONLY job is to analyze the interference map image and extract structured data.\n\n"
                "CRITICAL: Output ONLY valid JSON (no markdown, no explanations). The JSON must contain:\n"
                "{\n"
                '  "basic_info": {\n'
                '    "report_date": "YYYY-MM-DD",\n'
                '    "time_range": "HH:MM-HH:MM or description",\n'
                '    "system_type": "Ground Terminal System or Satellite System",\n'
                '    "monitoring_metric": "CINR/CIR/CNR/EPFD/PFD/INR/etc",\n'
                '    "filename": "extracted from image or context"\n'
                "  },\n"
                '  "numerical_data": {\n'
                '    "metric_name": "extracted metric",\n'
                '    "min_value": number,\n'
                '    "max_value": number,\n'
                '    "avg_value": number,\n'
                '    "range": number,\n'
                '    "unit": "dB or other"\n'
                "  },\n"
                '  "temporal_characteristics": {\n'
                '    "abnormal_periods": ["period1", "period2"],\n'
                '    "duration_type": "short-lived/intermittent/sustained",\n'
                '    "magnitude": "low/moderate/high"\n'
                "  },\n"
                '  "visual_patterns": [\n'
                '    "pattern1 with specifics",\n'
                '    "pattern2 with specifics"\n'
                "  ]\n"
                "}\n\n"
                "INSTRUCTIONS:\n"
                "1. Look for COLORBAR on the right side - read MIN and MAX values\n"
                "2. Calculate AVG = (Min + Max) / 2\n"
                "3. Calculate RANGE = Max - Min\n"
                "4. Identify temporal anomalies from the heatmap\n"
                "5. List visual patterns observed\n\n"
                "Output ONLY the JSON, nothing else. End with: [PARSER_DONE]"
            ),
            input_source="image",
            output_format="json",
            termination_marker="[PARSER_DONE]",
        )

    @staticmethod
    def build_analysis_config() -> AgentConfig:
        """构建Analysis Agent配置"""
        return AgentConfig(
            name="analysis_agent",
            role=AgentRole.ANALYSIS,
            description="Analyze parsed data and identify patterns and interference",
            max_tokens=1536,
            temperature=0.3,
            system_message=(
                "You are the Analysis Agent. Your job is to analyze the structured data from Parser Agent.\n\n"
                "INPUT: You will receive JSON data from Parser Agent containing numerical data and visual patterns.\n"
                "OUTPUT: Generate analysis in this format:\n\n"
                "## Data Analysis Results\n\n"
                "**Interference Presence**: [Yes/No/Uncertain] - [reason based on data]\n\n"
                "### Numerical Analysis\n"
                "- Min Value: [value] dB\n"
                "- Max Value: [value] dB\n"
                "- Average: [value] dB\n"
                "- Range: [value] dB\n"
                "- Assessment: [Are values typical? Any concerning patterns?]\n\n"
                "### Temporal Characteristics\n"
                "- Abnormal Periods: [specific times/regions]\n"
                "- Duration: [short-lived/intermittent/sustained]\n"
                "- Magnitude: [low/moderate/high]\n\n"
                "### Pattern Analysis\n"
                "[2-3 paragraphs analyzing visual patterns, variability, and potential sources]\n\n"
                "### Potential Interference Sources\n"
                "1. [hypothesis with evidence from figure, e.g., 'peaks at HH:MM suggest...']\n"
                "2. [hypothesis with evidence]\n"
                "3. [hypothesis with evidence]\n\n"
                "IMPORTANT: Do NOT re-analyze the image. Use ONLY the data provided by Parser Agent.\n"
                "End with: [ANALYSIS_DONE]"
            ),
            input_source="parser",
            output_format="text",
            termination_marker="[ANALYSIS_DONE]",
        )

    @staticmethod
    def build_review_config() -> AgentConfig:
        """构建Review Agent配置"""
        return AgentConfig(
            name="review_agent",
            role=AgentRole.REVIEW,
            description="Review analysis for ITU compliance and logical consistency",
            max_tokens=1024,
            temperature=0.3,
            system_message=(
                "You are the Review Agent. Your job is to verify the analysis from Analysis Agent.\n\n"
                "INPUT: You will receive analysis results from Analysis Agent.\n"
                "OUTPUT: Generate review in this format:\n\n"
                "## Compliance Review\n\n"
                "### ITU Standard Compliance\n"
                "- **Compliance Status**: [Compliant/Non-Compliant/Partially Compliant/Marginal]\n"
                "- **Key Findings**: [summary of compliance assessment]\n"
                "- **Risk Level**: [High/Moderate/Low]\n\n"
                "[1 paragraph explaining compliance assessment based on ITU standards]\n\n"
                "### Evidence Summary\n"
                "- [Visual cue 1 with specifics]\n"
                "- [Visual cue 2 with specifics]\n"
                "- [Visual cue 3 with specifics]\n"
                "- [Visual cue 4 with specifics]\n\n"
                "### Logical Consistency Check\n"
                "[Assessment of whether analysis is logically consistent and well-supported]\n\n"
                "### Recommendations\n"
                "1. **[Action 1]**: [Purpose and expected impact]\n"
                "2. **[Action 2]**: [Purpose and expected impact]\n"
                "3. **[Action 3]**: [Purpose and expected impact]\n\n"
                "End with: [REVIEW_DONE]"
            ),
            input_source="analysis",
            output_format="text",
            termination_marker="[REVIEW_DONE]",
        )

    @staticmethod
    def build_report_config() -> AgentConfig:
        """构建Report Agent配置"""
        return AgentConfig(
            name="report_agent",
            role=AgentRole.REPORT,
            description="Generate final formatted report",
            max_tokens=1536,
            temperature=0.2,
            system_message=(
                "You are the Report Agent. Your job is to generate the final formatted report.\n\n"
                "INPUT: You will receive review results from Review Agent.\n"
                "OUTPUT: Generate the complete report in markdown format:\n\n"
                "# Interference Analysis Report\n\n"
                "## 1. Basic Information\n"
                "| Field | Value |\n"
                "|-------|-------|\n"
                "| Report date | [date] |\n"
                "| System type | [type] |\n"
                "| Monitoring metric | [metric] |\n"
                "| Research institution | Institute of Space Internet, Fudan University |\n\n"
                "## 2. Data Analysis\n"
                "[Include analysis results from Review Agent]\n\n"
                "## 3. Compliance Assessment\n"
                "[Include compliance review from Review Agent]\n\n"
                "## 4. Conclusions and Recommendations\n"
                "[Include recommendations from Review Agent]\n\n"
                "## 5. Appendix: Metadata\n"
                "- Constellation: [constellation]\n"
                "- Terminal type: [terminal_type]\n"
                "- Analysis type: [analysis_type]\n"
                "- Date: [date]\n\n"
                "IMPORTANT: Integrate all previous agent outputs into a cohesive, well-formatted report.\n"
                "Use **bold** for key values and statuses.\n"
                "End with: [REPORT_DONE]"
            ),
            input_source="review",
            output_format="markdown",
            termination_marker="[REPORT_DONE]",
        )

    @staticmethod
    def build_all_configs() -> Dict[str, AgentConfig]:
        """构建所有agent配置"""
        return {
            "parser": AgentConfigBuilder.build_parser_config(),
            "analysis": AgentConfigBuilder.build_analysis_config(),
            "review": AgentConfigBuilder.build_review_config(),
            "report": AgentConfigBuilder.build_report_config(),
        }

    @staticmethod
    def export_configs(filepath: str) -> None:
        """导出所有配置到JSON文件"""
        configs = AgentConfigBuilder.build_all_configs()
        serializable_configs = {}
        for name, config in configs.items():
            config_dict = asdict(config)
            config_dict["role"] = config_dict["role"].value
            serializable_configs[name] = config_dict

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(serializable_configs, f, indent=2, ensure_ascii=False)


class AgentSequenceValidator:
    """
    验证agent序列的有效性

    规则：
    1. Parser必须是第一个agent
    2. 后续agent的input_source必须匹配前一个agent的role
    3. 最后一个agent必须是Report
    """

    @staticmethod
    def validate_sequence(configs: List[AgentConfig]) -> bool:
        """验证agent序列"""
        if not configs:
            print("[ERROR] Agent sequence is empty")
            return False

        # 检查第一个agent是否是Parser
        if configs[0].role != AgentRole.PARSER:
            print("[ERROR] First agent must be Parser")
            return False

        # 检查最后一个agent是否是Report
        if configs[-1].role != AgentRole.REPORT:
            print("[ERROR] Last agent must be Report")
            return False

        # 检查agent间的数据流转
        for i in range(1, len(configs)):
            prev_agent = configs[i - 1]
            curr_agent = configs[i]

            # 验证input_source
            expected_source = prev_agent.role.value
            if curr_agent.input_source != expected_source:
                print(
                    f"[ERROR] Agent {curr_agent.name} expects input from {curr_agent.input_source}, "
                    f"but previous agent {prev_agent.name} is {expected_source}"
                )
                return False

        print("[INFO] Agent sequence validation passed")
        return True

    @staticmethod
    def print_sequence_info(configs: List[AgentConfig]) -> None:
        """打印agent序列信息"""
        print("\n=== Agent Sequence Information ===")
        for i, config in enumerate(configs):
            print(f"\n[{i + 1}] {config.name}")
            print(f"    Role: {config.role.value}")
            print(f"    Input Source: {config.input_source}")
            print(f"    Output Format: {config.output_format}")
            print(f"    Max Tokens: {config.max_tokens}")
            print(f"    Temperature: {config.temperature}")
            print(f"    Termination Marker: {config.termination_marker}")
