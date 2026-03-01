import requests
from datetime import datetime

# 服务地址
base_url = "http://localhost:8000"

# 1. 健康检查
response = requests.get(f"{base_url}/api/v1/health")
print("健康检查:", response.json())

# 2. 运行仿真
sim_request = {
    "start_time": "2024-12-16T00:00:00",
    "duration_hours": 0.1,
    "step": 2
}
response = requests.post(f"{base_url}/api/v1/simulate", json=sim_request)
print("仿真结果:", response.json())

# 3. 获取文件列表
response = requests.get(f"{base_url}/api/v1/inference/files")
print("文件列表:", response.json())

# 4. 获取具体数据
response = requests.get(f"{base_url}/api/v1/inference/data/1/20241216000002.json")
print("结果数据:", response.json())