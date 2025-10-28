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
import ssl
import certifi
from src.utils import ProxyManager
import config

# 从配置文件获取代理配置
proxy_manager = ProxyManager(proxy_url=config.PROXY)

def setup_ssl():
    """配置SSL上下文"""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

def enable_proxy():
    """启用代理和SSL设置"""
    proxy_manager.enable()
    setup_ssl()

def disable_proxy():
    """禁用代理"""
    proxy_manager.disable()

def get_proxy_manager():
    """获取代理管理器实例"""
    return proxy_manager

def get_proxy_url():
    """获取代理URL"""
    return config.PROXY 