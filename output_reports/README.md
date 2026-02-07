# 输出文件目录结构说明

## 目录组织

```
output_reports/
├── reports/          # 最终报告文件
│   ├── interference_report_en.md      # Markdown 格式报告
│   └── interference_report_en.docx    # Word 格式报告
├── metadata/         # 元数据和配置文件
│   ├── agent_configs.json             # Agent 配置信息
│   └── audit_log.json                 # 审计日志
└── data_flow/        # 数据流转记录
    ├── data_flow.json                 # 详细的数据流转记录
    └── data_flow_summary.json         # 数据流转摘要
```

## 文件说明

### reports/ - 最终报告
- **interference_report_en.md**: 使用 Markdown 格式的干扰分析报告，包含完整的分析结果、合规性评估和建议
- **interference_report_en.docx**: 使用 Word 格式的报告，集成了原始干扰图像，便于打印和分享

### metadata/ - 元数据
- **agent_configs.json**: 记录所有 Agent 的配置信息，包括：
  - Agent 名称、角色、描述
  - 系统提示词（system_message）
  - 输入/输出格式、Token 限制、温度参数
  - 终止标记（termination_marker）

- **audit_log.json**: 完整的审计日志，记录：
  - 每个事件的类型（input_recorded / output_recorded）
  - 涉及的 Agent 名称
  - 数据来源/格式
  - 精确的时间戳

### data_flow/ - 数据流转
- **data_flow.json**: 详细的数据流转记录，包含：
  - 每个 Agent 的输入数据来源和时间戳
  - 每个 Agent 的输出数据格式和时间戳
  - 数据预览（前 200 字符）

- **data_flow_summary.json**: 简化版的数据流转摘要，包含：
  - 每个 Agent 是否有输入/输出
  - 输入来源和输出格式
  - 用于快速检查流程完整性

## 使用场景

| 文件 | 主要用途 | 使用场景 |
|------|--------|--------|
| **interference_report_en.md** | 最终报告 | 提交给客户、发布到网站 |
| **interference_report_en.docx** | 最终报告 | 打印、邮件分享、正式文档 |
| **agent_configs.json** | 配置管理 | 重现实验、对比不同配置 |
| **audit_log.json** | 审计记录 | 合规性检查、性能分析 |
| **data_flow.json** | 详细追踪 | 调试数据流转问题 |
| **data_flow_summary.json** | 快速检查 | 验证流程完整性 |

## 数据流转过程

```
输入图像
   ↓
[Parser Agent] → 提取结构化数据 (JSON)
   ↓
[Analysis Agent] → 分析干扰特征 (Text)
   ↓
[Review Agent] → 合规性评估 (Text)
   ↓
[Report Agent] → 生成最终报告 (Markdown)
   ↓
输出报告 + 元数据 + 数据流转记录
```

## 配置说明

在 `config.py` 中定义了以下输出目录：

```python
OUTPUT_REPORTS_DIR = str(BASE_DIR / "data" / "output_reports" / "reports")
OUTPUT_METADATA_DIR = str(BASE_DIR / "data" / "output_reports" / "metadata")
OUTPUT_DATAFLOW_DIR = str(BASE_DIR / "data" / "output_reports" / "data_flow")
```

这些配置在 `itu_interference_analyzer.py` 中被使用，确保所有输出文件都保存到正确的位置。
