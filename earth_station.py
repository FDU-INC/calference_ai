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

import json
import os

def load_ground_stations(filename='earth_stations.json'):
    """Load all earth station data from JSON file"""
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_ground_stations(data, filename='ground_stations.json'):
    """Save earth station data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
def add_station(station_id, info, filename='ground_stations.json'):
    """Add new earth station"""
    data = load_ground_stations(filename)
    if station_id in data:
        raise ValueError(f"Station '{station_id}' already exists.")
    data[station_id] = info
    save_ground_stations(data, filename)


def get_station(station_id, filename='ground_stations.json'):
    """Get single earth station by ID"""
    data = load_ground_stations(filename)
    return data.get(station_id, None)


def list_stations(filename='ground_stations.json'):
    """List all earth station IDs"""
    data = load_ground_stations(filename)
    return list(data.keys())


def update_station(station_id, updates, filename='ground_stations.json'):
    """
    Update earth station information.
    Updates can contain nested fields, e.g.:
    {"alt_m": 120, "rx_system": {"T_sys_K": 480}}
    """
    data = load_ground_stations(filename)
    if station_id not in data:
        raise ValueError(f"Station '{station_id}' not found.")

    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(data[station_id].get(key), dict):
            data[station_id][key].update(value)
        else:
            data[station_id][key] = value

    save_ground_stations(data, filename)


def delete_station(station_id, filename='ground_stations.json'):
    """Delete earth station by ID"""
    data = load_ground_stations(filename)
    if station_id not in data:
        raise ValueError(f"Station '{station_id}' not found.")
    del data[station_id]
    save_ground_stations(data, filename)
