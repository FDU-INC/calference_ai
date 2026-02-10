# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
#
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
#
# Author: yjh
# Date: 2026-02-08

"""
Calself 服务接口定义

定义了 Calself 服务的抽象接口，可以有多种实现：
- REST API 客户端实现
- 本地直接调用实现
- gRPC 客户端实现等
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict


class ICalselfService(ABC):
    """
    Calself 服务抽象接口

    定义了卫星干扰仿真服务的标准接口
    """

    @abstractmethod
    def run_simulation(
        self,
        start_time: datetime,
        duration_hours: float = 0.1,
        step: int = 2,
        **kwargs
    ) -> Dict:
        """
        运行卫星干扰仿真

        Args:
            start_time: 仿真开始时间
            duration_hours: 仿真时长（小时）
            step: 时间步长（秒）
            **kwargs: 其他参数

        Returns:
            仿真结果字典
        """
        pass

    @abstractmethod
    def get_inference_files(
        self,
        company_id: Optional[int] = None
    ) -> Dict:
        """
        获取干扰分析结果文件列表

        Args:
            company_id: 公司ID（可选，用于过滤）

        Returns:
            文件列表字典
        """
        pass

    @abstractmethod
    def load_inference_file(
        self,
        company_id: int,
        timestamp: str
    ) -> Dict:
        """
        加载指定的干扰分析结果文件

        Args:
            company_id: 公司ID
            timestamp: 时间戳（文件名）

        Returns:
            结果数据字典
        """
        pass
