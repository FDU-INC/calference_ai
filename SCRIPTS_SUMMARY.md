# Calference 运行脚本总结

## 📋 新增文件清单

本次更新为项目添加了以下文件，用于简化项目的运行和管理：

### 核心运行脚本

| 文件 | 大小 | 说明 |
|------|------|------|
| `run.py` | 16KB | 统一运行脚本，支持所有项目功能 |
| `init.py` | 11KB | 项目初始化脚本，一键设置环境 |
| `quickstart.sh` | 4.1KB | Shell 快速启动脚本（Linux/macOS） |
| `Makefile` | 3.3KB | Makefile 快速命令集 |
| `examples_comprehensive.py` | 9.5KB | 综合使用示例脚本 |

### 文档文件

| 文件 | 说明 |
|------|------|
| `QUICKSTART.md` | 5分钟快速入门指南 |
| `COMMANDS.md` | 完整命令参考卡片 |
| `README.md` (更新) | 添加了新脚本说明 |

---

## 🚀 快速使用指南

### 第一次使用（推荐）

```bash
# 1. 一键初始化
python init.py --auto

# 2. 配置 API 密钥
export LLM_API_KEY="your_api_key"

# 3. 运行示例
python run.py itu-report
```

### 日常使用

```bash
# 生成报告
python run.py itu-report

# 或使用 Makefile
make itu-report

# 或使用 Shell 脚本
./quickstart.sh itu-report
```

---

## 📚 脚本详细说明

### 1. `run.py` - 统一运行脚本

**功能**: 项目的主要入口点，支持所有功能

**主要命令**:
```bash
python run.py itu-report              # 生成 ITU 报告
python run.py calself-sim             # 运行卫星仿真
python run.py prepare-rag             # 准备 RAG 数据
python run.py download-model          # 下载 embedding 模型
python run.py web-api                 # 启动 Web API
python run.py calself-service         # 启动仿真服务
python run.py example itu_report      # 运行示例
python run.py status                  # 显示项目状态
```

**特点**:
- ✅ 完整的命令行接口
- ✅ 详细的帮助信息
- ✅ 参数验证和错误处理
- ✅ 依赖检查

**使用场景**: 需要完整功能和详细控制时

---

### 2. `init.py` - 项目初始化脚本

**功能**: 一键初始化项目环境

**主要命令**:
```bash
python init.py                        # 交互式初始化
python init.py --auto                 # 自动初始化（无需确认）
python init.py --check                # 仅检查环境
```

**初始化步骤**:
1. ✅ 检查 Python 版本（需要 3.10+）
2. ✅ 创建必要的目录
3. ✅ 安装依赖包
4. ✅ 下载 embedding 模型
5. ✅ 准备 RAG 数据
6. ✅ 验证配置

**特点**:
- ✅ 自动化程度高
- ✅ 交互式和自动两种模式
- ✅ 详细的进度反馈
- ✅ 错误和警告提示

**使用场景**: 第一次使用项目时

---

### 3. `Makefile` - 快速命令集

**功能**: 提供简洁的 Makefile 命令

**主要命令**:
```bash
make help                             # 查看所有命令
make install                          # 安装依赖
make setup                            # 完整设置
make itu-report                       # 生成报告
make calself-sim                      # 运行仿真
make prepare-rag                      # 准备 RAG 数据
make download-model                   # 下载模型
make web-api                          # 启动 Web 服务
make calself-service                  # 启动仿真服务
make example-itu                      # 运行示例
make status                           # 显示状态
make clean                            # 清理临时文件
```

**特点**:
- ✅ 命令简洁易记
- ✅ 支持 Tab 自动补全
- ✅ 详细的帮助信息
- ✅ 适合频繁使用

**使用场景**: 日常开发和测试

---

### 4. `quickstart.sh` - Shell 快速启动脚本

**功能**: Shell 脚本版本的快速启动工具

**主要命令**:
```bash
./quickstart.sh help                  # 查看帮助
./quickstart.sh itu-report            # 生成报告
./quickstart.sh calself-sim           # 运行仿真
./quickstart.sh web-api               # 启动 Web 服务
./quickstart.sh status                # 显示状态
```

**特点**:
- ✅ 支持 Linux/macOS
- ✅ 彩色输出
- ✅ 自动环境检查
- ✅ 错误处理

**使用场景**: Linux/macOS 用户的快速启动

---

### 5. `examples_comprehensive.py` - 综合使用示例

**功能**: 交互式示例脚本，演示所有主要功能

**使用方法**:
```bash
python examples_comprehensive.py
```

**包含的示例**:
1. 生成 ITU 干扰报告
2. 运行 Calself 卫星仿真
3. 启动 Web 服务
4. RAG 检索增强
5. 批量处理多个图片
6. 自定义配置
7. 查看项目状态
8. 故障排除

**特点**:
- ✅ 交互式菜单
- ✅ 详细的代码示例
- ✅ 常见问题解答
- ✅ 故障排除指南

**使用场景**: 学习项目功能和最佳实践

---

## 📖 文档文件

### `QUICKSTART.md` - 快速入门指南

**内容**:
- 5分钟快速开始
- 完整命令参考
- 常见问题解答
- 故障排除指南
- 高级用法

**适合**: 新用户快速上手

### `COMMANDS.md` - 命令参考卡片

**内容**:
- 快速命令速查表
- 完整命令列表
- 参数详解
- 输出文件位置
- 常用场景
- 常见错误

**适合**: 快速查找命令和参数

---

## 🎯 使用场景指南

### 场景 1: 第一次使用项目

```bash
# 步骤 1: 一键初始化
python init.py --auto

# 步骤 2: 配置 API
export LLM_API_KEY="your_key"

# 步骤 3: 运行示例
python run.py itu-report

# 步骤 4: 查看结果
cat output_reports/reports/interference_report_en.md
```

### 场景 2: 日常开发

```bash
# 使用 Makefile 快速命令
make itu-report
make calself-sim
make web-api
make status
```

### 场景 3: 学习项目功能

```bash
# 运行综合示例
python examples_comprehensive.py

# 查看快速入门
cat QUICKSTART.md

# 查看命令参考
cat COMMANDS.md
```

### 场景 4: 故障排除

```bash
# 检查项目状态
python run.py status

# 查看快速入门中的故障排除
grep -A 5 "问题" QUICKSTART.md

# 查看综合示例中的故障排除
python examples_comprehensive.py  # 选择选项 8
```

### 场景 5: 自动化脚本

```bash
# 批量处理多个图片
for img in data/input/*.png; do
    python run.py itu-report --image "$img"
done

# 或使用 Makefile
for img in data/input/*.png; do
    make itu-report
done
```

---

## 🔧 脚本功能对比

| 功能 | run.py | init.py | Makefile | quickstart.sh | examples_comprehensive.py |
|------|--------|---------|----------|---------------|---------------------------|
| 生成报告 | ✅ | ❌ | ✅ | ✅ | 📚 |
| 运行仿真 | ✅ | ❌ | ✅ | ✅ | 📚 |
| 启动服务 | ✅ | ❌ | ✅ | ✅ | 📚 |
| 初始化环境 | ❌ | ✅ | ❌ | ❌ | ❌ |
| 准备数据 | ✅ | ✅ | ✅ | ✅ | 📚 |
| 显示状态 | ✅ | ✅ | ✅ | ✅ | 📚 |
| 交互式菜单 | ❌ | ✅ | ❌ | ❌ | ✅ |
| 示例代码 | ❌ | ❌ | ❌ | ❌ | ✅ |

**图例**: ✅ 支持 | ❌ 不支持 | 📚 包含示例

---

## 📊 文件大小和性能

| 文件 | 大小 | 加载时间 | 说明 |
|------|------|---------|------|
| `run.py` | 16KB | <100ms | 功能完整，启动快 |
| `init.py` | 11KB | <100ms | 初始化脚本，启动快 |
| `Makefile` | 3.3KB | 即时 | 无需加载，最快 |
| `quickstart.sh` | 4.1KB | <50ms | Shell 脚本，很快 |
| `examples_comprehensive.py` | 9.5KB | <100ms | 示例脚本，启动快 |

---

## 🎓 学习路径

### 初级用户

1. 阅读 `QUICKSTART.md` 的"5分钟快速开始"
2. 运行 `python init.py --auto`
3. 运行 `python run.py itu-report`
4. 查看生成的报告

### 中级用户

1. 学习 `COMMANDS.md` 中的命令参考
2. 使用 `make` 命令进行日常操作
3. 运行 `python examples_comprehensive.py` 学习高级功能
4. 自定义配置和参数

### 高级用户

1. 研究 `run.py` 的源代码
2. 修改 `itu_report_generator/config.py` 进行自定义
3. 集成到其他项目
4. 贡献改进和新功能

---

## 🔍 故障排除快速指南

| 问题 | 解决方案 |
|------|---------|
| 缺少依赖 | `python init.py` 或 `make install` |
| API 连接失败 | 检查 `LLM_API_KEY` 环境变量 |
| RAG 数据不存在 | `python run.py prepare-rag` |
| 端口被占用 | `python run.py web-api --port 9000` |
| 权限错误 | `chmod +x quickstart.sh run.py` |
| 查看帮助 | `python run.py --help` 或 `make help` |

---

## 📞 获取帮助

1. **查看脚本帮助**:
   ```bash
   python run.py --help
   make help
   ./quickstart.sh help
   ```

2. **查看文档**:
   ```bash
   cat QUICKSTART.md
   cat COMMANDS.md
   cat PROJECT_STRUCTURE.md
   ```

3. **运行示例**:
   ```bash
   python examples_comprehensive.py
   ```

4. **检查项目状态**:
   ```bash
   python run.py status
   ```

---

## ✅ 检查清单

使用以下检查清单验证项目设置：

- [ ] Python 版本 >= 3.10
- [ ] 依赖已安装 (`pip install -r requirements.txt`)
- [ ] LLM API 密钥已配置 (`export LLM_API_KEY=...`)
- [ ] 项目初始化完成 (`python init.py --auto`)
- [ ] 可以生成报告 (`python run.py itu-report`)
- [ ] 可以启动服务 (`python run.py web-api`)
- [ ] 项目状态正常 (`python run.py status`)

---

## 📝 版本信息

- **创建日期**: 2026-02-07
- **项目版本**: 1.1.0
- **Python 版本**: 3.10+
- **脚本总数**: 5 个
- **文档总数**: 3 个（新增）

---

## 🎉 总结

本次更新为 Calference 项目添加了完整的运行脚本和文档系统，包括：

✅ **5 个运行脚本**，支持多种使用场景
✅ **3 文档文件**，提供详细的使用指南
✅ **完整的命令参考**，方便快速查找
✅ **交互式示例**，帮助用户学习功能
✅ **一键初始化**，简化项目设置

现在用户可以通过多种方式快速运行项目，无论是第一次使用还是日常开发，都能找到合适的工具和文档。

---

**Made with ❤️ by Calference Team**
