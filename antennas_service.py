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
from antennas import (
    add_antenna, get_antenna, list_antennas,
    update_antenna, delete_antenna
)

app = Flask(__name__)

@app.route('/antennas', methods=['GET'])
def get_all_antennas():
    """Get all antennas"""
    try:
        antennas = list_antennas()
        return jsonify({
            'success': True,
            'data': antennas,
            'message': f'Retrieved {len(antennas)} antennas'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/antennas/<antenna_id>', methods=['GET'])
def get_antenna_by_id(antenna_id):
    """Get antenna by ID"""
    try:
        antenna = get_antenna(antenna_id)
        if antenna is None:
            return jsonify({
                'success': False,
                'error': f'Antenna {antenna_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': antenna,
            'message': f'Retrieved antenna {antenna_id}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/antennas', methods=['POST'])
def create_antenna():
    """Create new antenna"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        antenna_id = data.get('antenna_id')
        if not antenna_id:
            return jsonify({
                'success': False,
                'error': 'antenna_id is required'
            }), 400
        
        antenna_info = {k: v for k, v in data.items() if k != 'antenna_id'}
        add_antenna(antenna_id, antenna_info)
        
        return jsonify({
            'success': True,
            'data': {'antenna_id': antenna_id},
            'message': f'Created antenna {antenna_id}'
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

@app.route('/antennas/<antenna_id>', methods=['PUT'])
def update_antenna_by_id(antenna_id):
    """Update antenna information"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body cannot be empty'
            }), 400
        
        update_antenna(antenna_id, data)
        
        return jsonify({
            'success': True,
            'data': {'antenna_id': antenna_id},
            'message': f'Updated antenna {antenna_id}'
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

@app.route('/antennas/<antenna_id>', methods=['DELETE'])
def delete_antenna_by_id(antenna_id):
    """Delete antenna"""
    try:
        delete_antenna(antenna_id)
        
        return jsonify({
            'success': True,
            'data': {'antenna_id': antenna_id},
            'message': f'Deleted antenna {antenna_id}'
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
        'service': 'antennas_service',
        'status': 'healthy'
    })

if __name__ == '__main__':
    print("Starting Antenna Microservice on http://localhost:5003")
    app.run(host='0.0.0.0', port=5003, debug=True)
