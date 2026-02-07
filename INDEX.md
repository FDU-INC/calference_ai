# Calference 项目文件索引

## 📑 项目文件导航

本文档提供了项目中所有重要文件的快速导航和说明。

---

## 🚀 快速开始文件

### 首先阅读

| 文件 | 说明 | 阅读时间 |
|------|------|---------|
| [README.md](README.md) | 项目主文档，包含项目简介和快速开始 | 5分钟 |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 最常用命令速查表 | 2分钟 |
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速入门指南 | 5分钟 |

### 然后运行

```bash
# 一键初始化
python3 init.py --auto

# 配置 API 密钥
export LLM_API_KEY="your_api_key"

# 运行示例
python3 run.py itu-report
```

---

## 📚 文档文件

### 快速参考

| 文件 | 大小 | 用途 | 适合人群 |
|------|------|------|---------|
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | 5.0KB | 最常用命令速查表 | 所有用户 |
| [COMMANDS.md](COMMANDS.md) | 5.7KB | 完整命令参考卡片 | 开发者 |
| [QUICKSTART.md](QUICKSTART.md) | 7.8KB | 5分钟快速入门 | 新用户 |

### 详细指南

| 文件 | 大小 | 用途 | 适合人群 |
|------|------|------|---------|
| [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) | 9.6KB | 所有脚本的详细说明 | 高级用户 |
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | 5.2KB | 项目设置验证清单 | 初始化用户 |
| [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) | 8.5KB | 本次更新的完整总结 | 所有用户 |

### 项目文档

| 文件 | 说明 |
|------|------|
| [README.md](README.md) | 项目主文档 |
| [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | 项目结构详解 |
| [docs/USER_MANUAL.md](docs/USER_MANUAL.md) | 详细使用手册 |
| [examples/README.md](examples/README.md) | 使用示例 |

---

## 🛠️ 运行脚本

### Python 脚本

| 文件 | 大小 | 说明 | 使用方式 |
|------|------|------|---------|
| [run.py](run.py) | 16KB | 统一运行脚本 | `python3 run.py --help` |
| [init.py](init.py) | 11KB | 项目初始化脚本 | `python3 init.py --auto` |
| [examples_comprehensive.py](examples_comprehensive.py) | 9.5KB | 综合使用示例 | `python3 examples_comprehensive.py` |

### Shell 脚本

| 文件 | 大小 | 说明 | 使用方式 |
|------|------|------|---------|
| [quickstart.sh](quickstart.sh) | 4.1KB | Shell 快速启动脚本 | `./quickstart.sh help` |

### Makefile

| 文件 | 大小 | 说明 | 使用方式 |
|------|------|------|---------|
| [Makefile](Makefile) | 3.3KB | Makefile 快速命令 | `make help` |

---

## ⚙️ 配置文件

| 文件 | 说明 | 操作 |
|------|------|------|
| [.env.example](.env.example) | 环境变量配置示例 | 复制为 `.env` 并编辑 |
| [itu_report_generator/config.py](itu_report_generator/config.py) | 项目配置文件 | 编辑以自定义配置 |

---

## 📂 项目结构

```
Calference11.3/
├── 📄 README.md                          # 项目主文档
├── 📄 QUICK_REFERENCE.md                 # 快速参考卡片
├── 📄 QUICKSTART.md                      # 快速入门指南
├── 📄 COMMANDS.md                        # 命令参考
├── 📄 SCRIPTS_SUMMARY.md                 # 脚本总结
├── 📄 SETUP_CHECKLIST.md                 # 设置检查清单
├── 📄 UPDATE_SUMMARY.md                  # 更新总结
├── 📄 INDEX.md                           # 本文件
│
├── 🐍 run.py                             # 统一运行脚本
├── 🐍 init.py                            # 初始化脚本
├── 🐍 examples_comprehensive.py          # 综合示例
├── 🔧 quickstart.sh                      # Shell 脚本
├── 📋 Makefile                           # Makefile 命令
├── ⚙️ .env.example                       # 环境变量示例
│
├── 📁 itu_report_generator/              # ITU 报告生成器
│   ├── config.py                         # 配置文件
│   ├── itu_interference_analyzer.py      # 主程序
│   ├── agent_config.py                   # Agent 配置
│   ├── src/                              # 源代码
│   │   ├── itu_file_rag.py              # RAG 模块
│   │   ├── prepare_data.py              # 数据准备
│   │   └── download_embedding_model.py  # 模型下载
│   ├── frontend/                         # Web 前端
│   │   ├── api.py                       # Web API
│   │   └── static/                      # 静态文件
│   └── data/                             # 数据目录
│
├── 📁 Calself/                           # 卫星仿真模块
│   ├── main.py                           # 主仿真程序
│   ├── server.py                         # 服务器
│   └── ...
│
├── 📁 calself_client/                    # API 客户端
│   ├── client.py                         # 客户端实现
│   └── __init__.py
│
├── 📁 data/                              # 数据目录
│   ├── rag/                              # RAG 数据
│   ├── models/                           # 本地模型
│   ├── input/                            # 输入数据
│   └── uploaded/                         # 上传文件
│
├── 📁 output_reports/                    # 输出报告
│   ├── reports/                          # 最终报告
│   ├── metadata/                         # 元数据
│   └── data_flow/                        # 数据流
│
├── 📁 examples/                          # 使用示例
│   ├── example_itu_report.py
│   ├── example_calself_usage.py
│   └── README.md
│
├── 📁 docs/                              # 文档
│   ├── USER_MANUAL.md
│   └── api.md
│
└── 📄 requirements.txt                   # Python 依赖
```

---

## 🎯 使用场景导航

### 场景 1: 第一次使用项目

**步骤**:
1. 阅读 [README.md](README.md)
2. 阅读 [QUICKSTART.md](QUICKSTART.md)
3. 运行 `python3 init.py --auto`
4. 查看 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)

**相关文件**:
- [README.md](README.md) - 项目简介
- [QUICKSTART.md](QUICKSTART.md) - 快速入门
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - 设置检查
- [init.py](init.py) - 初始化脚本

---

### 场景 2: 日常开发

**步骤**:
1. 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. 使用 `make` 命令或 `python3 run.py`
3. 查看 [COMMANDS.md](COMMANDS.md) 了解详细参数

**相关文件**:
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考
- [COMMANDS.md](COMMANDS.md) - 命令参考
- [Makefile](Makefile) - Makefile 命令
- [run.py](run.py) - 运行脚本

---

### 场景 3: 学习项目功能

**步骤**:
1. 运行 `python3 examples_comprehensive.py`
2. 查看 [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md)
3. 查看 [docs/USER_MANUAL.md](docs/USER_MANUAL.md)

**相关文件**:
- [examples_comprehensive.py](examples_comprehensive.py) - 综合示例
- [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) - 脚本说明
- [docs/USER_MANUAL.md](docs/USER_MANUAL.md) - 使用手册
- [examples/README.md](examples/README.md) - 示例代码

---

### 场景 4: 故障排除

**步骤**:
1. 运行 `python3 run.py status`
2. 查看 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) 的故障排除部分
3. 查看 [QUICKSTART.md](QUICKSTART.md) 的故障排除部分

**相关文件**:
- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - 设置检查
- [QUICKSTART.md](QUICKSTART.md) - 快速入门
- [run.py](run.py) - 状态检查

---

### 场景 5: 自定义配置

**步骤**:
1. 查看 [.env.example](.env.example)
2. 编辑 [itu_report_generator/config.py](itu_report_generator/config.py)
3. 查看 [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) 的自定义配置部分

**相关文件**:
- [.env.example](.env.example) - 环境变量示例
- [itu_report_generator/config.py](itu_report_generator/config.py) - 配置文件
- [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) - 脚本说明

---

## 📊 文件统计

### 新增文件

| 类型 | 数量 | 大小 |
|------|------|------|
| Python 脚本 | 3 | 36.5KB |
| Shell 脚本 | 1 | 4.1KB |
| Makefile | 1 | 3.3KB |
| 文档文件 | 6 | 46.0KB |
| 配置文件 | 1 | 2.0KB |
| **总计** | **12** | **91.9KB** |

### 更新文件

| 文件 | 更新内容 |
|------|---------|
| README.md | 添加新脚本工具说明和文档导航 |

---

## 🔍 快速查找

### 我想...

| 需求 | 查看文件 |
|------|---------|
| 快速开始 | [QUICKSTART.md](QUICKSTART.md) |
| 查找命令 | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) 或 [COMMANDS.md](COMMANDS.md) |
| 了解脚本 | [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) |
| 设置项目 | [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) |
| 学习功能 | [examples_comprehensive.py](examples_comprehensive.py) |
| 解决问题 | [QUICKSTART.md](QUICKSTART.md) 或 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) |
| 自定义配置 | [.env.example](.env.example) 或 [itu_report_generator/config.py](itu_report_generator/config.py) |
| 查看更新 | [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) |

---

## 🎓 推荐阅读顺序

### 初级用户（新手）

1. [README.md](README.md) - 了解项目
2. [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - 快速参考
3. [QUICKSTART.md](QUICKSTART.md) - 快速入门
4. [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - 设置检查

### 中级用户（开发者）

1. [COMMANDS.md](COMMANDS.md) - 完整命令参考
2. [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) - 脚本详解
3. [examples_comprehensive.py](examples_comprehensive.py) - 综合示例
4. [docs/USER_MANUAL.md](docs/USER_MANUAL.md) - 使用手册

### 高级用户（贡献者）

1. [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) - 脚本详解
2. [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构
3. [itu_report_generator/config.py](itu_report_generator/config.py) - 配置文件
4. 源代码文件

---

## 📞 获取帮助

| 问题 | 解决方案 |
|------|---------|
| 不知道从哪里开始 | 阅读 [README.md](README.md) |
| 需要快速命令 | 查看 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| 需要详细说明 | 查看 [COMMANDS.md](COMMANDS.md) |
| 需要设置帮助 | 查看 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) |
| 需要学习功能 | 运行 [examples_comprehensive.py](examples_comprehensive.py) |
| 需要故障排除 | 查看 [QUICKSTART.md](QUICKSTART.md) 的故障排除部分 |
| 需要了解更新 | 查看 [UPDATE_SUMMARY.md](UPDATE_SUMMARY.md) |

---

## ✨ 快速命令

```bash
# 查看帮助
python3 run.py --help
make help
./quickstart.sh help

# 快速开始
python3 init.py --auto
export LLM_API_KEY="your_key"
python3 run.py itu-report

# 日常使用
make itu-report
make web-api
make status

# 学习功能
python3 examples_comprehensive.py

# 检查状态
python3 run.py status
```

---

## 📝 版本信息

- **创建日期**: 2026-02-07
- **项目版本**: 1.1.0
- **文档版本**: 1.0.0
- **最后更新**: 2026-02-07

---

**Made with ❤️ by Calference Team**

**提示**: 使用 Ctrl+F 快速搜索本文档中的内容。
