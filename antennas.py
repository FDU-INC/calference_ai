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

def load_antennas(filename='antennas.json'):
    """Load all antenna data from JSON file"""
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_antennas(data, filename='antennas.json'):
    """Save antenna data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_antenna(ant_id, info, filename='antennas.json'):
    """Add new antenna record"""
    data = load_antennas(filename)
    if ant_id in data:
        raise ValueError(f"Antenna '{ant_id}' already exists.")
    data[ant_id] = info
    save_antennas(data, filename)


def get_antenna(ant_id, filename='antennas.json'):
    """Get single antenna information by ID"""
    data = load_antennas(filename)
    return data.get(ant_id, None)


def list_antennas(filename='antennas.json'):
    """List all antenna IDs"""
    data = load_antennas(filename)
    return list(data.keys())


def update_antenna(ant_id, updates, filename='antennas.json'):
    """
    Update antenna information.
    Updates can contain nested fields, e.g.:
    {"efficiency": 0.65, "pattern_file": "pattern_ANT1.json"}
    """
    data = load_antennas(filename)
    if ant_id not in data:
        raise ValueError(f"Antenna '{ant_id}' not found.")

    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(data[ant_id].get(key), dict):
            data[ant_id][key].update(value)
        else:
            data[ant_id][key] = value

    save_antennas(data, filename)


def delete_antenna(ant_id, filename='antennas.json'):
    """Delete antenna by ID"""
    data = load_antennas(filename)
    if ant_id not in data:
        raise ValueError(f"Antenna '{ant_id}' not found.")
    del data[ant_id]
    save_antennas(data, filename)
