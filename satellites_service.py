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
from satellites import (
    add_satellite, get_satellite, list_satellites,
    update_satellite, delete_satellite
)

app = Flask(__name__)

@app.route('/satellites', methods=['GET'])
def get_all_satellites():
    """Get all satellites"""
    try:
        satellites = list_satellites()
        return jsonify({
            'success': True,
            'data': satellites,
            'message': f'Retrieved {len(satellites)} satellites'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/satellites/<satellite_id>', methods=['GET'])
def get_satellite_by_id(satellite_id):
    """Get satellite by ID"""
    try:
        satellite = get_satellite(satellite_id)
        if satellite is None:
            return jsonify({
                'success': False,
                'error': f'Satellite {satellite_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': satellite,
            'message': f'Retrieved satellite {satellite_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/satellites', methods=['POST'])
def create_satellite():
    """Create new satellite"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        satellite_id = data.get('satellite_id')
        if not satellite_id:
            return jsonify({
                'success': False,
                'error': 'satellite_id is required'
            }), 400
        
        satellite_info = {k: v for k, v in data.items() if k != 'satellite_id'}
        add_satellite(satellite_id, satellite_info)
        
        return jsonify({
            'success': True,
            'data': {'satellite_id': satellite_id},
            'message': f'Created satellite {satellite_id}'
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

@app.route('/satellites/<satellite_id>', methods=['PUT'])
def update_satellite_by_id(satellite_id):
    """Update satellite information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        update_satellite(satellite_id, data)
        
        return jsonify({
            'success': True,
            'data': {'satellite_id': satellite_id},
            'message': f'Updated satellite {satellite_id}'
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

@app.route('/satellites/<satellite_id>', methods=['DELETE'])
def delete_satellite_by_id(satellite_id):
    """Delete satellite"""
    try:
        delete_satellite(satellite_id)
        
        return jsonify({
            'success': True,
            'data': {'satellite_id': satellite_id},
            'message': f'Deleted satellite {satellite_id}'
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
        'service': 'satellites_service',
        'status': 'healthy'
    })

if __name__ == '__main__':
    print("Starting Satellite Microservice on http://localhost:5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
