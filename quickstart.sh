#!/bin/bash
# Calference 快速启动脚本
# 用于快速运行项目的各项功能

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_header() {
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# 显示帮助信息
show_help() {
    cat << EOF
${BLUE}Calference 快速启动脚本${NC}

用法: ./quickstart.sh [命令] [选项]

命令:
  itu-report              生成 ITU 干扰报告
  calself-sim             运行 Calself 卫星仿真
  prepare-rag             准备 RAG 数据
  download-model          下载 embedding 模型
  web-api                 启动 Web API 服务
  calself-service         启动 Calself 仿真服务
  example itu_report      运行 ITU 报告示例
  example calself_usage   运行 Calself 仿真示例
  status                  显示项目状态
  help                    显示此帮助信息

示例:
  ./quickstart.sh itu-report
  ./quickstart.sh calself-sim --duration 0.5
  ./quickstart.sh web-api --port 8000
  ./quickstart.sh status

EOF
}

# 检查 Python 环境
check_python() {
    if ! command -v $PYTHON &> /dev/null; then
        print_error "找不到 Python 解释器: $PYTHON"
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON --version 2>&1 | awk '{print $2}')
    print_info "使用 Python $PYTHON_VERSION"
}

# 检查依赖
check_dependencies() {
    print_info "检查依赖..."

    if ! $PYTHON -c "import pip" 2>/dev/null; then
        print_error "pip 未安装"
        exit 1
    fi

    print_success "依赖检查完成"
}

# 主函数
main() {
    local command=$1
    shift || true

    check_python

    case "$command" in
        itu-report)
            print_header "🚀 生成 ITU 干扰报告"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" itu-report "$@"
            ;;
        calself-sim)
            print_header "🛰️  运行 Calself 卫星仿真"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" calself-sim "$@"
            ;;
        prepare-rag)
            print_header "📚 准备 RAG 数据"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" prepare-rag "$@"
            ;;
        download-model)
            print_header "📥 下载 embedding 模型"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" download-model "$@"
            ;;
        web-api)
            print_header "🌐 启动 Web API 服务"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" web-api "$@"
            ;;
        calself-service)
            print_header "🛰️  启动 Calself 仿真服务"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" calself-service "$@"
            ;;
        example)
            print_header "📚 运行示例"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" example "$@"
            ;;
        status)
            print_header "📊 项目状态"
            check_dependencies
            $PYTHON "$PROJECT_ROOT/run.py" status "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            if [ -z "$command" ]; then
                show_help
            else
                print_error "未知命令: $command"
                echo ""
                show_help
                exit 1
            fi
            ;;
    esac
}

# 运行主函数
main "$@"
