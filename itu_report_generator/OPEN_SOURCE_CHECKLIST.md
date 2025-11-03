# 开源准备检查清单

本文档用于确保项目已准备好进行开源发布。

## ✅ 已完成项目

- [x] 创建 `.gitignore` 文件，确保 `Calself/` 目录被忽略
- [x] 更新 `config.py`，移除硬编码路径，使用环境变量和相对路径
- [x] 创建 `config.py.example` 配置模板文件
- [x] 创建 `requirements.txt` 依赖列表
- [x] 创建 `LICENSE` 文件（GPL-3.0）
- [x] 更新 `README.md`，补充安装和配置说明
- [x] 创建根目录 `README.md`
- [x] 检查所有文件的许可证声明（已确认均为 GPL-3.0）

## 📋 发布前检查清单

在正式发布到 GitHub/Gitee 之前，请确认：

### 代码检查
- [ ] 所有敏感信息（API密钥、个人路径、IP地址等）已移除
- [ ] 硬编码路径已替换为配置文件或环境变量
- [ ] 所有 `itu_report_generator/` 目录下的文件都有 GPL-3.0 许可证声明
- [ ] 没有对 `Calself/` 目录的引用或依赖

### 文档检查
- [ ] README.md 文档完整、清晰
- [ ] 配置文件示例（config.py.example）已创建
- [ ] 安装和使用说明清晰易懂

### Git 检查
- [ ] 确认 `.gitignore` 正确排除 `Calself/` 目录
- [ ] 检查 Git 历史记录中是否包含敏感信息（如有，需要清理）
- [ ] 确认要提交的文件列表：
  ```bash
  git status
  ```

### 功能检查
- [ ] 测试开源模块可以独立运行（不依赖 Calself）
- [ ] 测试使用环境变量配置是否正常工作
- [ ] 测试使用配置文件是否正常工作

## 🚀 发布步骤

1. **初始化 Git 仓库**（如果还没有）
   ```bash
   git init
   ```

2. **添加文件到 Git**
   ```bash
   git add itu_report_generator/
   git add .gitignore
   git add README.md
   ```

3. **检查要提交的文件**
   ```bash
   git status
   # 确认 Calself/ 不在列表中
   ```

4. **提交更改**
   ```bash
   git commit -m "Initial open source release: itu_report_generator"
   ```

5. **创建 GitHub/Gitee 仓库并推送**
   ```bash
   git remote add origin <repository-url>
   git branch -M main
   git push -u origin main
   ```

6. **添加标签（可选）**
   ```bash
   git tag -a v1.0.0 -m "First open source release"
   git push origin v1.0.0
   ```

## 📝 后续维护建议

- [ ] 设置 GitHub Actions 进行 CI/CD（可选）
- [ ] 添加代码贡献指南（CONTRIBUTING.md）
- [ ] 设置 Issue 模板
- [ ] 定期更新依赖包版本
- [ ] 维护 CHANGELOG.md 记录版本更新

## ⚠️ 注意事项

1. **不要提交敏感信息**：确保 `config.py` 在 `.gitignore` 中
2. **检查大文件**：模型文件（.bin, .pt 等）不应提交
3. **数据文件**：确认是否需要提交示例数据或数据文件模板
4. **许可证一致性**：确保所有文件头部声明与 LICENSE 文件一致

## 📞 需要帮助？

如有问题，请检查：
- `.gitignore` 是否正确配置
- `config.py.example` 是否包含所有必要配置项
- 所有路径是否使用相对路径或环境变量

---

**最后更新**：2025-01-XX

