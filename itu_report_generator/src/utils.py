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

import os
from datetime import datetime

def parse_image_path(image_path, lang='zh'):
    """解析图片路径，提取星座名称、终端类型和分析类型信息，支持中英文"""
    filename = os.path.basename(image_path)
    parts = filename.lower().split('_')
    constellation = parts[0].capitalize()
    if lang == 'en':
        terminal_type_map = {'earth': 'Ground Terminal', 'satellite': 'Satellite Terminal'}
        analysis_types = {
            'cinr': 'CINR', 'cir': 'CIR', 'cnr': 'CNR',
            'epfd': 'EPFD', 'inr': 'INR',
            'link_count': 'Link Count', 'pfd': 'PFD', 'temp': 'ΔT/T'
        }
    else:
        terminal_type_map = {'earth': '地面终端', 'satellite': '卫星端'}
        analysis_types = {
            'cinr': 'CINR（载干噪比）', 'cir': 'CIR（载干比）', 'cnr': 'CNR（载噪比）',
            'epfd': 'EPFD（等效功率通量密度）', 'inr': 'INR（干扰噪声比）',
            'link_count': '链路数量', 'pfd': 'PFD（功率通量密度）', 'temp': 'ΔT/T'
        }
    terminal_type = "未知终端" if lang == 'zh' else "Unknown Terminal"
    for k, v in terminal_type_map.items():
        if k in parts:
            terminal_type = v
            break
    analysis_type = "未知分析类型" if lang == 'zh' else "Unknown Analysis Type"
    for key, value in analysis_types.items():
        if key in filename:
            analysis_type = value
            break
    return {
        'constellation': constellation,
        'terminal_type': terminal_type,
        'analysis_type': analysis_type,
        'filename': os.path.basename(image_path)
    }

def get_current_report_date():
    """获取格式化的报告日期，例如：二〇二五年七月"""
    return datetime.now().strftime("二〇%y年%#m月")

class ProxyManager:
    """
    统一管理代理设置，可随时启用/关闭/切换代理。
    """
    def __init__(self, proxy_url=None, no_proxy="localhost,127.0.0.1"):
        self.proxy_url = proxy_url
        self.no_proxy = no_proxy
        self.env_keys = ["http_proxy", "https_proxy", "all_proxy"]

    def enable(self, proxy_url=None):
        """启用代理，可传入新的代理地址。"""
        if proxy_url:
            self.proxy_url = proxy_url
        if not self.proxy_url:
            raise ValueError("No proxy_url specified.")
        for key in self.env_keys:
            os.environ[key] = self.proxy_url
        os.environ["no_proxy"] = self.no_proxy

    def disable(self):
        """关闭代理。"""
        for key in self.env_keys:
            if key in os.environ:
                del os.environ[key]
        if "no_proxy" in os.environ:
            del os.environ["no_proxy"]

    def set_no_proxy(self, no_proxy):
        self.no_proxy = no_proxy
        os.environ["no_proxy"] = no_proxy
