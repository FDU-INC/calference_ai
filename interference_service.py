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

from flask import Flask, request, jsonify
import json
import os
import requests
from interference import (
    compute_ci_for_es, check_against_itu_thresholds, update_ngso_interference
)

app = Flask(__name__)

# Microservice endpoint configuration
EARTH_STATION_SERVICE = "http://localhost:5001"
SATELLITES_SERVICE = "http://localhost:5002"
ANTENNAS_SERVICE = "http://localhost:5003"

def get_earth_station(station_id):
    """Get earth station data from earth station microservice"""
    try:
        response = requests.get(f"{EARTH_STATION_SERVICE}/stations/{station_id}")
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to get earth station: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Failed to connect to earth station service: {str(e)}")

def get_satellite(satellite_id):
    """Get satellite data from satellite microservice"""
    try:
        response = requests.get(f"{SATELLITES_SERVICE}/satellites/{satellite_id}")
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to get satellite: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Failed to connect to satellite service: {str(e)}")

def get_antenna(antenna_id):
    """Get antenna data from antenna microservice"""
    try:
        response = requests.get(f"{ANTENNAS_SERVICE}/antennas/{antenna_id}")
        if response.status_code == 200:
            return response.json()['data']
        else:
            raise Exception(f"Failed to get antenna: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Failed to connect to antenna service: {str(e)}")

def get_all_antennas():
    """Get all antenna data"""
    try:
        response = requests.get(f"{ANTENNAS_SERVICE}/antennas")
        if response.status_code == 200:
            antenna_ids = response.json()['data']
            antennas = {}
            for antenna_id in antenna_ids:
                antenna_data = get_antenna(antenna_id)
                antennas[antenna_id] = antenna_data
            return antennas
        else:
            raise Exception(f"Failed to get antenna list: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        raise Exception(f"Failed to connect to antenna service: {str(e)}")

@app.route('/compute_ci', methods=['POST'])
def compute_ci():
    """Calculate Carrier-to-Interference ratio (C/I)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        # Get required parameters
        station_id = data.get('station_id')
        main_satellite_id = data.get('main_satellite_id')
        interf_satellite_id = data.get('interf_satellite_id')
        verbose = data.get('verbose', False)
        
        if not all([station_id, main_satellite_id, interf_satellite_id]):
            return jsonify({
                'success': False,
                'error': 'station_id, main_satellite_id, interf_satellite_id are required'
            }), 400
        
        # Get data from microservices
        es = get_earth_station(station_id)
        sat_main = get_satellite(main_satellite_id)
        sat_interf = get_satellite(interf_satellite_id)
        antennas = get_all_antennas()
        
        # Calculate C/I ratio
        result = compute_ci_for_es(es, sat_main, sat_interf, antennas, verbose)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'C/I calculation completed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/check_itu_thresholds', methods=['POST'])
def check_itu():
    """Check ITU standard thresholds"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        # Get parameters
        results = data.get('results')
        reuse = data.get('reuse', False)
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'results parameter is required'
            }), 400
        
        # Check ITU standards
        check_result = check_against_itu_thresholds(results, reuse)
        
        return jsonify({
            'success': True,
            'data': check_result,
            'message': 'ITU standard check completed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/update_ngso_interference', methods=['POST'])
def update_ngso():
    """Update NGSO interference analysis"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        # Get parameters
        filename = data.get('filename', 'satellites_ngso.json')
        ground_file = data.get('ground_file', 'earth_stations_ngso.json')
        step = data.get('step', 1)
        duration = data.get('duration', 86400)
        
        # Execute NGSO interference analysis
        interference_data = update_ngso_interference(filename, ground_file, step, duration)
        
        return jsonify({
            'success': True,
            'data': {
                'interference_over_time': interference_data,
                'duration': duration,
                'step': step
            },
            'message': 'NGSO interference analysis completed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'interference_service',
        'status': 'healthy'
    })

@app.route('/services/health', methods=['GET'])
def check_dependencies():
    """Check dependency service status"""
    services_status = {}
    
    # Check earth station service
    try:
        response = requests.get(f"{EARTH_STATION_SERVICE}/health", timeout=5)
        services_status['earth_station'] = response.status_code == 200
    except:
        services_status['earth_station'] = False
    
    # Check satellite service
    try:
        response = requests.get(f"{SATELLITES_SERVICE}/health", timeout=5)
        services_status['satellites'] = response.status_code == 200
    except:
        services_status['satellites'] = False
    
    # Check antenna service
    try:
        response = requests.get(f"{ANTENNAS_SERVICE}/health", timeout=5)
        services_status['antennas'] = response.status_code == 200
    except:
        services_status['antennas'] = False
    
    all_healthy = all(services_status.values())
    
    return jsonify({
        'success': True,
        'service': 'interference_service',
        'dependencies': services_status,
        'all_healthy': all_healthy,
        'status': 'healthy' if all_healthy else 'degraded'
    })

if __name__ == '__main__':
    print("Starting Interference Calculation Microservice on http://localhost:5004")
    app.run(host='0.0.0.0', port=5004, debug=True)
