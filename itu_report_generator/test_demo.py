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
import os

def test_service():
    base_url = "http://localhost:5005"
    
    # 1. 健康检查
    print("🔍 Testing health...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Service is running")
        else:
            print("❌ Service not responding")
            return
    except:
        print("❌ Service not running. Start with: python demo_ms.py")
        return
    
    # # 2. 测试分析
    # print("📸 Testing analysis...")
    # test_images = [
    #     "oneweb_total_earth_cinr.png",
    #     "oneweb_total_earth_epfd.png",
    #     "oneweb_total_earth_cir.png"
    # ]
    
    # for image_name in test_images:
    #     import pdb;pdb.set_trace()
    #     print(f"   Testing: {image_name}")
    #     try:
    #         data = {'image_name': image_name, 'download': 'false'}
    #         response = requests.post(f"{base_url}/analyze", data=data, timeout=60)
            
    #         if response.status_code == 200:
    #             result = response.json()
    #             print(f"   ✅ Success: {result['data']['constellation']} - {result['data']['metric']}")
    #             break  # 成功一个就够了
    #         else:
    #             print(f"   ❌ Failed: {response.status_code}")
    #     except Exception as e:
    #         print(f"   ❌ Error: {str(e)}")
    
    # 3. 测试文件上传
    print("📤 Testing file upload...")
    image_path = "./data/total/oneweb_total_earth_epfd.png"
    if os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                files = {'file': f}
                data = {'download': 'false'}
                response = requests.post(f"{base_url}/analyze", files=files, data=data, timeout=600)
            
            if response.status_code == 200:
                print("   ✅ Upload successful")
            else:
                print(f"   ❌ Upload failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Upload error: {str(e)}")
    else:
        print("   ⚠️  Test image not found")
    
    print("✅ Test completed!")

if __name__ == "__main__":
    test_service()