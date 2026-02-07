# Calference 项目初始化检查清单

## ✅ 项目设置检查清单

使用此清单验证项目是否正确设置。

### 第一步：环境检查

- [ ] Python 版本 >= 3.10
  ```bash
  python3 --version
  ```

- [ ] pip 已安装
  ```bash
  python3 -m pip --version
  ```

- [ ] Git 已安装（可选）
  ```bash
  git --version
  ```

### 第二步：项目结构检查

- [ ] 项目根目录存在
  ```bash
  ls -la | grep -E "(run.py|Makefile|init.py)"
  ```

- [ ] 主要模块存在
  ```bash
  ls -d itu_report_generator Calself calself_client data output_reports
  ```

- [ ] 关键文件存在
  ```bash
  ls itu_report_generator/config.py
  ls itu_report_generator/itu_interference_analyzer.py
  ```

### 第三步：依赖安装

- [ ] 安装项目依赖
  ```bash
  make install
  # 或
  python3 -m pip install -r requirements.txt
  ```

- [ ] 验证关键依赖
  ```bash
  python3 -c "import autogen; import sentence_transformers; print('✅ 依赖检查通过')"
  ```

### 第四步：数据准备

- [ ] 下载 embedding 模型
  ```bash
  python3 run.py download-model
  # 或
  make download-model
  ```

- [ ] 准备 RAG 数据
  ```bash
  python3 run.py prepare-rag
  # 或
  make prepare-rag
  ```

- [ ] 验证数据文件
  ```bash
  ls -lh data/rag/chunks.jsonl data/rag/embeddings.npy
  ```

### 第五步：配置设置

- [ ] 配置 LLM API 密钥
  ```bash
  export LLM_API_KEY="your_api_key_here"
  ```

- [ ] 验证配置
  ```bash
  echo $LLM_API_KEY
  ```

- [ ] （可选）编辑配置文件
  ```bash
  nano itu_report_generator/config.py
  ```

### 第六步：功能验证

- [ ] 显示项目状态
  ```bash
  python3 run.py status
  # 或
  make status
  ```

- [ ] 运行示例
  ```bash
  python3 run.py example itu_report
  # 或
  make example-itu
  ```

- [ ] 验证报告生成
  ```bash
  ls -lh output_reports/reports/
  ```

### 第七步：服务测试（可选）

- [ ] 启动 Web API 服务
  ```bash
  python3 run.py web-api --port 8000 &
  ```

- [ ] 访问 API 文档
  ```bash
  curl http://127.0.0.1:8000/docs
  ```

- [ ] 停止服务
  ```bash
  pkill -f "python3 run.py web-api"
  ```

---

## 📊 检查清单完成度

| 步骤 | 项目 | 状态 |
|------|------|------|
| 1 | 环境检查 | ⬜ |
| 2 | 项目结构 | ⬜ |
| 3 | 依赖安装 | ⬜ |
| 4 | 数据准备 | ⬜ |
| 5 | 配置设置 | ⬜ |
| 6 | 功能验证 | ⬜ |
| 7 | 服务测试 | ⬜ |

**总体进度**: 0/7 ✅

---

## 🚀 快速初始化（一键完成）

如果想跳过手动检查，可以使用一键初始化脚本：

```bash
# 自动完成所有步骤
python3 init.py --auto

# 或交互式初始化
python3 init.py
```

---

## 🆘 故障排除

### 问题 1: Python 版本过低

**症状**: `Python 版本过低: 3.6 (需要 3.10+)`

**解决方案**:
```bash
# 检查 Python 版本
python3 --version

# 如果版本过低，升级 Python
# Ubuntu/Debian:
sudo apt update && sudo apt install python3.10

# macOS:
brew install python@3.10

# 或使用 conda
conda create -n itu python=3.10
conda activate itu
```

### 问题 2: 缺少依赖

**症状**: `ModuleNotFoundError: No module named 'xxx'`

**解决方案**:
```bash
# 重新安装依赖
python3 -m pip install -r requirements.txt

# 或使用 Makefile
make install
```

### 问题 3: API 密钥未配置

**症状**: `API key invalid` 或 `Connection error`

**解决方案**:
```bash
# 设置 API 密钥
export LLM_API_KEY="your_api_key_here"

# 验证
echo $LLM_API_KEY

# 或编辑配置文件
nano itu_report_generator/config.py
```

### 问题 4: RAG 数据不存在

**症状**: `FileNotFoundError: chunks.jsonl not found`

**解决方案**:
```bash
# 准备 RAG 数据
python3 run.py prepare-rag

# 或使用 Makefile
make prepare-rag
```

### 问题 5: 模型下载失败

**症状**: `Connection timeout` 或 `Download failed`

**解决方案**:
```bash
# 检查网络连接
ping huggingface.co

# 使用代理
export HTTP_PROXY="http://proxy:port"
export HTTPS_PROXY="http://proxy:port"

# 使用 HuggingFace 镜像
export HF_ENDPOINT="https://hf-mirror.com"

# 重新下载
python3 run.py download-model
```

---

## 📞 获取帮助

1. **查看快速入门**:
   ```bash
   cat QUICKSTART.md
   ```

2. **查看命令参考**:
   ```bash
   cat COMMANDS.md
   ```

3. **查看脚本说明**:
   ```bash
   cat SCRIPTS_SUMMARY.md
   ```

4. **查看快速参考**:
   ```bash
   cat QUICK_REFERENCE.md
   ```

5. **查看脚本帮助**:
   ```bash
   python3 run.py --help
   make help
   ./quickstart.sh help
   ```

6. **显示项目状态**:
   ```bash
   python3 run.py status
   ```

---

## ✨ 初始化完成后

初始化完成后，你可以：

1. **生成报告**:
   ```bash
   python3 run.py itu-report
   ```

2. **启动服务**:
   ```bash
   python3 run.py web-api
   ```

3. **运行仿真**:
   ```bash
   python3 run.py calself-sim
   ```

4. **查看示例**:
   ```bash
   python3 examples_comprehensive.py
   ```

---

## 📝 记录

| 日期 | 操作 | 状态 |
|------|------|------|
| | 环境检查 | ⬜ |
| | 依赖安装 | ⬜ |
| | 数据准备 | ⬜ |
| | 配置设置 | ⬜ |
| | 功能验证 | ⬜ |

---

**最后更新**: 2026-02-07
**版本**: 1.1.0
