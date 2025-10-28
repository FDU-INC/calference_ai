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
from earth_station import (
    add_station, get_station, list_stations,
    update_station, delete_station
)

app = Flask(__name__)

@app.route('/stations', methods=['GET'])
def get_all_stations():
    """Get all earth stations"""
    try:
        stations = list_stations()
        return jsonify({
            'success': True,
            'data': stations,
            'message': f'Retrieved {len(stations)} earth stations'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stations/<station_id>', methods=['GET'])
def get_station_by_id(station_id):
    """Get earth station by ID"""
    try:
        station = get_station(station_id)
        if station is None:
            return jsonify({
                'success': False,
                'error': f'Earth station {station_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': station,
            'message': f'Retrieved earth station {station_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stations', methods=['POST'])
def create_station():
    """Create new earth station"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        station_id = data.get('station_id')
        if not station_id:
            return jsonify({
                'success': False,
                'error': 'station_id is required'
            }), 400
        
        station_info = {k: v for k, v in data.items() if k != 'station_id'}
        add_station(station_id, station_info)
        
        return jsonify({
            'success': True,
            'data': {'station_id': station_id},
            'message': f'Created earth station {station_id}'
        }), 201
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 409
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stations/<station_id>', methods=['PUT'])
def update_station_by_id(station_id):
    """Update earth station information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        update_station(station_id, data)
        
        return jsonify({
            'success': True,
            'data': {'station_id': station_id},
            'message': f'Updated earth station {station_id}'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stations/<station_id>', methods=['DELETE'])
def delete_station_by_id(station_id):
    """Delete earth station"""
    try:
        delete_station(station_id)
        
        return jsonify({
            'success': True,
            'data': {'station_id': station_id},
            'message': f'Deleted earth station {station_id}'
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
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
        'service': 'earth_station_service',
        'status': 'healthy'
    })

if __name__ == '__main__':
    print("Starting Earth Station Microservice on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
