.PHONY: help install setup prepare-rag download-model itu-report calself-sim web-api calself-service example-itu example-calself status clean

# 项目根目录
PROJECT_ROOT := $(shell pwd)
PYTHON := python3

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║           Calference 项目 - 快速命令参考                       ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 环境设置:"
	@echo "  make install          - 安装项目依赖"
	@echo "  make setup            - 完整项目设置（安装+准备数据）"
	@echo ""
	@echo "📚 数据准备:"
	@echo "  make prepare-rag      - 准备 RAG 数据（生成 chunks 和 embeddings）"
	@echo "  make download-model   - 下载 embedding 模型到本地"
	@echo ""
	@echo "🚀 主要功能:"
	@echo "  make itu-report       - 生成 ITU 干扰报告"
	@echo "  make calself-sim      - 运行 Calself 卫星仿真"
	@echo ""
	@echo "🌐 服务启动:"
	@echo "  make web-api          - 启动 Web API 服务 (http://127.0.0.1:8000)"
	@echo "  make calself-service  - 启动 Calself 仿真服务 (http://127.0.0.1:8001)"
	@echo ""
	@echo "📚 示例:"
	@echo "  make example-itu      - 运行 ITU 报告生成示例"
	@echo "  make example-calself  - 运行 Calself 仿真示例"
	@echo ""
	@echo "📊 其他:"
	@echo "  make status           - 显示项目状态"
	@echo "  make clean            - 清理临时文件"
	@echo ""

install:
	@echo "📦 安装项目依赖..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@echo "✅ 依赖安装完成"

setup: install prepare-rag download-model
	@echo "✅ 项目设置完成！"
	@echo ""
	@echo "下一步："
	@echo "  1. 配置 LLM API 密钥: export LLM_API_KEY='your_key'"
	@echo "  2. 运行示例: make example-itu"
	@echo "  3. 启动服务: make web-api"

prepare-rag:
	@echo "📚 准备 RAG 数据..."
	$(PYTHON) run.py prepare-rag

download-model:
	@echo "📥 下载 embedding 模型..."
	$(PYTHON) run.py download-model

itu-report:
	@echo "📊 生成 ITU 干扰报告..."
	$(PYTHON) run.py itu-report

calself-sim:
	@echo "🛰️  运行 Calself 卫星仿真..."
	$(PYTHON) run.py calself-sim --duration 0.1

web-api:
	@echo "🌐 启动 Web API 服务..."
	$(PYTHON) run.py web-api --host 127.0.0.1 --port 8000

calself-service:
	@echo "🛰️  启动 Calself 仿真服务..."
	$(PYTHON) run.py calself-service --host 127.0.0.1 --port 8001

example-itu:
	@echo "📚 运行 ITU 报告生成示例..."
	$(PYTHON) run.py example itu_report

example-calself:
	@echo "📚 运行 Calself 仿真示例..."
	$(PYTHON) run.py example calself_usage

status:
	@echo "📊 显示项目状态..."
	$(PYTHON) run.py status

clean:
	@echo "🧹 清理临时文件..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "✅ 清理完成"

.DEFAULT_GOAL := help
