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
import sys

# Service endpoints
EARTH_STATION_SERVICE = "http://localhost:5001"
SATELLITES_SERVICE = "http://localhost:5002"
ANTENNAS_SERVICE = "http://localhost:5003"
INTERFERENCE_SERVICE = "http://localhost:5004"
MULTI_AGENT_REPORT_SERVICE = "http://localhost:5005"

def check_services():
    """Check if all services are running"""
    services = [
        EARTH_STATION_SERVICE,
        SATELLITES_SERVICE,
        ANTENNAS_SERVICE,
        INTERFERENCE_SERVICE,
        MULTI_AGENT_REPORT_SERVICE
    ]
    
    for url in services:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code != 200:
                return False
        except Exception:
            return False
    return True

def load_data(earth_file, satellites_file, antennas_file):
    """Load initial data to services"""
    # Load earth stations
    try:
        with open(earth_file, 'r') as f:
            earth_stations = __import__('json').load(f)
        for station_id, data in earth_stations.items():
            requests.post(f"{EARTH_STATION_SERVICE}/stations", 
                         json={'station_id': station_id, **data})
    except Exception:
        pass
    
    # Load satellites
    try:
        with open(satellites_file, 'r') as f:
            satellites = __import__('json').load(f)
        for satellite_id, data in satellites.items():
            requests.post(f"{SATELLITES_SERVICE}/satellites", 
                         json={'satellite_id': satellite_id, **data})
    except Exception:
        pass
    
    # Load antennas
    try:
        with open(antennas_file, 'r') as f:
            antennas = __import__('json').load(f)
        for antenna_id, data in antennas.items():
            requests.post(f"{ANTENNAS_SERVICE}/antennas", 
                         json={'antenna_id': antenna_id, **data})
    except Exception:
        pass

def run_analysis(filename, ground_file, step=1, duration=86400):
    """Run NGSO interference analysis"""
    try:
        data = {'filename': filename, 'ground_file': ground_file, 'step': step, 'duration': duration}
        response = requests.post(f"{INTERFERENCE_SERVICE}/update_ngso_interference", json=data)
        if response.status_code == 200:
            result = response.json()['data']['interference_over_time']
            print(f"Analysis Results: {len(result)} points, Max: {max(result):.2f} dB")
    except Exception:
        pass

def generate_report(image_name='oneweb_total_earth_cinr.png'):
    """Generate AI report"""
    try:
        data = {'image_name': image_name, 'download': 'false'}
        response = requests.post(f"{MULTI_AGENT_REPORT_SERVICE}/analyze", data=data, timeout=600)
        if response.status_code == 200:
            result = response.json()
            print(f"Report: {result['data']['constellation']} - {result['data']['metric']}")
            print(f"Markdown: {result['data']['markdown_path']}")
            print(f"Word: {result['data']['docx_path']}")
            return True
    except Exception as e:
        print(f"Report error: {str(e)}")
    return False

def main():
    print("=== Satellite Interference Analysis ===")
    
    # Check services
    if not check_services():
        print("❌ Services not ready. Run: python start_services.py")
        sys.exit(1)
    print("✅ Services ready")
    
    # Load data (optional)
    load_data('earth_stations_ngso.json', 'satellites_ngso.json', 'antennas.json')
    
    # Run analysis (optional)
    run_analysis('satellites_ngso.json', 'earth_stations_ngso.json')
    
    # Generate report
    print("🤖 Generating AI report...")
    if generate_report('oneweb_total_earth_cinr.png'):
        print("✅ Report completed")
    else:
        print("⚠️ Report failed")
    
    print("🎉 Done!")

if __name__ == "__main__":
    main()