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
# Date: 2026-02-07

"""
Calself 微服务封装
将 main_v0 封装为可调用的服务接口

@Name: yjh
@Date: 2025/11/03
"""

import requests
from datetime import datetime
from typing import Optional, Dict

from .calself_service import ICalselfService


class CalselfAPIError(Exception):
    """API 调用错误"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class CalselfClient(ICalselfService):
    """
    Calself REST API 客户端
    
    通过 HTTP RESTful API 访问 Calself 微服务
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        初始化客户端
        
        Args:
            base_url: Calself 微服务地址
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise CalselfAPIError(
                e.response.status_code,
                e.response.text if e.response.text else str(e)
            )
        except requests.exceptions.ConnectionError:
            raise CalselfAPIError(0, f"无法连接到服务: {self.base_url}")
    
    def run_simulation(
        self,
        start_time: datetime,
        duration_hours: float = 0.1,
        step: int = 2,
        **kwargs
    ) -> Dict:
        """运行仿真"""
        response = self._request(
            "POST",
            "/api/v1/simulate",
            json={
                "start_time": start_time.isoformat(),
                "duration_hours": duration_hours,
                "step": step,
                **kwargs
            }
        )
        return response
    
    def get_inference_files(
        self,
        company_id: Optional[int] = None
    ) -> Dict:
        """获取文件列表"""
        params = {"company_id": company_id} if company_id else {}
        response = self._request("GET", "/api/v1/inference/files", params=params)
        return response["files"]
    
    def load_inference_file(
        self,
        company_id: int,
        timestamp: str
    ) -> Dict:
        """加载结果文件"""
        if not timestamp.endswith('.json'):
            timestamp = f"{timestamp}.json"
        return self._request(
            "GET",
            f"/api/v1/inference/data/{company_id}/{timestamp}"
        )