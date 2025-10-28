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

import sys
sys.path.append('/mnt/data/yjh/projects/ITU/itu_report_generator')
# ----------------- 模型配置 -----------------
# 指定你的Qwen2.5-VL模型的存放路径
MODEL_PATH = "/mnt/data/yjh/model/Qwen2.5-VL-7B-Instruct/qwen/Qwen2.5-VL-7B-Instruct"

# ----------------- 路径配置 -----------------
# 输入的干扰图存放目录
INPUT_IMAGE_DIR = "/mnt/data/yjh/projects/ITU/itu_report_generator/data/total"

# 生成的Word报告输出目录
OUTPUT_REPORT_DIR = "/mnt/data/yjh/projects/ITU/itu_report_generator/data/output_reports"

# ----------------- 报告元数据 -----------------
# 在报告中显示的公司或机构名称
ORGANIZATION_NAME = "复旦大学空间互联网研究院"

# ----------------- 网络配置 -----------------
# 代理服务器配置
PROXY = "http://10.192.54.148:7897"  # 可根据实际情况修改
