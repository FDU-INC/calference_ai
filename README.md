# Calference Project

本项目是一个卫星干扰仿真分析系统，包含核心仿真计算模块和自动化报告生成工具。

## 项目结构

本项目采用**部分开源**策略：

- **`itu_report_generator/`** - ITU干扰图智能分析报告生成工具（**开源，GPL-3.0许可证**）
- **`Calself/`** - 核心仿真计算系统（**闭源，不包含在公开仓库中**）

## 开源组件

### ITU Report Generator

一个基于大语言模型（LLM）的自动化报告生成工具，用于分析卫星网络干扰仿真图片并生成符合ITU标准的专业Word报告。

**主要功能：**
- 单图/多图智能分析
- 自动生成结构化Word报告
- 支持中英文双语
- 符合ITU专业术语标准

**详见：** [itu_report_generator/README.md](itu_report_generator/README.md)

## 快速开始

### 使用开源组件（ITU Report Generator）

```bash
cd itu_report_generator
pip install -r requirements.txt
cp config.py.example config.py
# 编辑 config.py 设置你的配置
python main.py --single your_image.png
```

详细使用说明请参考 [itu_report_generator/README.md](itu_report_generator/README.md)。

### 闭源组件（Calself）

`Calself/` 目录包含核心仿真计算系统，该部分为专有软件，不在公开仓库中提供。

## 许可证

本项目采用**混合许可证**模式：

- **`itu_report_generator/`** - [GNU General Public License v3.0 (GPL-3.0)](itu_report_generator/LICENSE)
- **`Calself/`** - 专有许可证（闭源）

## 项目状态

- ✅ `itu_report_generator` - 开源可用
- 🔒 `Calself` - 闭源专有软件

## 贡献指南

本项目仅接受对开源组件 `itu_report_generator/` 的贡献。请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支
3. 提交更改（仅限 `itu_report_generator/` 目录）
4. 开启 Pull Request

## 联系方式

如有问题或建议，请通过 Issue 联系我们。

---

**注意**：本项目仓库仅包含开源组件。闭源组件 `Calself/` 不在本仓库中，且不会出现在公开的 Git 历史记录中。

