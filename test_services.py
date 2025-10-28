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

import requests
import json
import time

# 微服务地址
SERVICES = {
    'earth_station': 'http://localhost:5001',
    'satellites': 'http://localhost:5002',
    'antennas': 'http://localhost:5003',
    'interference': 'http://localhost:5004'
}

def test_service_health():
    """测试服务健康状态"""
    print("=== 测试服务健康状态 ===")
    
    for name, url in SERVICES.items():
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print(f"✅ {name} 服务正常")
            else:
                print(f"❌ {name} 服务异常: {response.status_code}")
        except Exception as e:
            print(f"❌ {name} 服务连接失败: {str(e)}")

def test_earth_station_service():
    """测试地面站服务"""
    print("\n=== 测试地面站服务 ===")
    
    url = SERVICES['earth_station']
    
    # 测试创建地面站
    station_data = {
        'station_id': 'TEST_GS',
        'name': '测试地面站',
        'lat_deg': 39.9042,
        'lon_deg': 116.4074,
        'alt_m': 50,
        'rx_system': {
            'T_sys_K': 500,
            'bandwidth_Hz': 36000000,
            'rx_losses_dB': 1.5
        },
        'rx_antenna_id': 'ANT_RX_1'
    }
    
    try:
        # 创建地面站
        response = requests.post(f"{url}/stations", json=station_data)
        if response.status_code == 201:
            print("✅ 创建地面站成功")
        else:
            print(f"⚠️ 创建地面站: {response.json().get('error', '未知错误')}")
        
        # 获取地面站
        response = requests.get(f"{url}/stations/TEST_GS")
        if response.status_code == 200:
            print("✅ 获取地面站成功")
        else:
            print(f"❌ 获取地面站失败: {response.json().get('error', '未知错误')}")
        
        # 更新地面站
        update_data = {'alt_m': 100}
        response = requests.put(f"{url}/stations/TEST_GS", json=update_data)
        if response.status_code == 200:
            print("✅ 更新地面站成功")
        else:
            print(f"❌ 更新地面站失败: {response.json().get('error', '未知错误')}")
        
        # 删除地面站
        response = requests.delete(f"{url}/stations/TEST_GS")
        if response.status_code == 200:
            print("✅ 删除地面站成功")
        else:
            print(f"❌ 删除地面站失败: {response.json().get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 地面站服务测试失败: {str(e)}")

def test_satellites_service():
    """测试卫星服务"""
    print("\n=== 测试卫星服务 ===")
    
    url = SERVICES['satellites']
    
    # 测试创建卫星
    satellite_data = {
        'satellite_id': 'TEST_SAT',
        'name': '测试卫星',
        'lon_deg': 123.0,
        'tx_eirp_dBW': 45.0,
        'tx_losses_dB': 1.0,
        'frequency_Hz': 12000000000
    }
    
    try:
        # 创建卫星
        response = requests.post(f"{url}/satellites", json=satellite_data)
        if response.status_code == 201:
            print("✅ 创建卫星成功")
        else:
            print(f"⚠️ 创建卫星: {response.json().get('error', '未知错误')}")
        
        # 获取卫星
        response = requests.get(f"{url}/satellites/TEST_SAT")
        if response.status_code == 200:
            print("✅ 获取卫星成功")
        else:
            print(f"❌ 获取卫星失败: {response.json().get('error', '未知错误')}")
        
        # 更新卫星
        update_data = {'tx_eirp_dBW': 50.0}
        response = requests.put(f"{url}/satellites/TEST_SAT", json=update_data)
        if response.status_code == 200:
            print("✅ 更新卫星成功")
        else:
            print(f"❌ 更新卫星失败: {response.json().get('error', '未知错误')}")
        
        # 删除卫星
        response = requests.delete(f"{url}/satellites/TEST_SAT")
        if response.status_code == 200:
            print("✅ 删除卫星成功")
        else:
            print(f"❌ 删除卫星失败: {response.json().get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 卫星服务测试失败: {str(e)}")

def test_antennas_service():
    """测试天线服务"""
    print("\n=== 测试天线服务 ===")
    
    url = SERVICES['antennas']
    
    # 测试创建天线
    antenna_data = {
        'antenna_id': 'TEST_ANT',
        'name': '测试天线',
        'diameter_m': 2.4,
        'efficiency': 0.6,
        'pattern_file': None
    }
    
    try:
        # 创建天线
        response = requests.post(f"{url}/antennas", json=antenna_data)
        if response.status_code == 201:
            print("✅ 创建天线成功")
        else:
            print(f"⚠️ 创建天线: {response.json().get('error', '未知错误')}")
        
        # 获取天线
        response = requests.get(f"{url}/antennas/TEST_ANT")
        if response.status_code == 200:
            print("✅ 获取天线成功")
        else:
            print(f"❌ 获取天线失败: {response.json().get('error', '未知错误')}")
        
        # 更新天线
        update_data = {'efficiency': 0.65}
        response = requests.put(f"{url}/antennas/TEST_ANT", json=update_data)
        if response.status_code == 200:
            print("✅ 更新天线成功")
        else:
            print(f"❌ 更新天线失败: {response.json().get('error', '未知错误')}")
        
        # 删除天线
        response = requests.delete(f"{url}/antennas/TEST_ANT")
        if response.status_code == 200:
            print("✅ 删除天线成功")
        else:
            print(f"❌ 删除天线失败: {response.json().get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 天线服务测试失败: {str(e)}")

def test_interference_service():
    """测试干扰计算服务"""
    print("\n=== 测试干扰计算服务 ===")
    
    url = SERVICES['interference']
    
    try:
        # 测试依赖服务状态
        response = requests.get(f"{url}/services/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 依赖服务状态检查成功")
            print(f"  所有服务正常: {data.get('all_healthy', False)}")
        else:
            print(f"❌ 依赖服务状态检查失败: {response.json().get('error', '未知错误')}")
        
        # 测试ITU标准检查
        itu_data = {
            'results': {
                'I_over_N_dB': -8.0
            },
            'reuse': False
        }
        
        response = requests.post(f"{url}/check_itu_thresholds", json=itu_data)
        if response.status_code == 200:
            print("✅ ITU标准检查成功")
        else:
            print(f"❌ ITU标准检查失败: {response.json().get('error', '未知错误')}")
            
    except Exception as e:
        print(f"❌ 干扰计算服务测试失败: {str(e)}")

def main():
    """主测试函数"""
    print("=== 微服务系统测试 ===")
    print("请确保所有微服务已启动")
    print("启动命令: python start_services.py")
    print()
    
    # 等待用户确认
    input("按回车键开始测试...")
    
    # 测试服务健康状态
    test_service_health()
    
    # 测试各个服务
    test_earth_station_service()
    test_satellites_service()
    test_antennas_service()
    test_interference_service()
    
    print("\n=== 测试完成 ===")
    print("如果所有测试都显示 ✅，说明微服务系统运行正常")

if __name__ == "__main__":
    main()
