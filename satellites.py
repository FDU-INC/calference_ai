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

def load_satellites(filename='satellites.json'):
    """Load all satellite data from JSON file"""
    if not os.path.exists(filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_satellites(data, filename='satellites.json'):
    """Save satellite data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_satellite(sat_id, info, filename='satellites.json'):
    """Add new satellite record"""
    data = load_satellites(filename)
    if sat_id in data:
        raise ValueError(f"Satellite '{sat_id}' already exists.")
    data[sat_id] = info
    save_satellites(data, filename)


def get_satellite(sat_id, filename='satellites.json'):
    """Get single satellite information by ID"""
    data = load_satellites(filename)
    return data.get(sat_id, None)


def list_satellites(filename='satellites.json'):
    """List all satellite IDs"""
    data = load_satellites(filename)
    return list(data.keys())


def update_satellite(sat_id, updates, filename='satellites.json'):
    """
    Update satellite information.
    Updates can contain nested fields, e.g.:
    {"tx_eirp_dBW": 47.0, "tx_losses_dB": 1.2}
    """
    data = load_satellites(filename)
    if sat_id not in data:
        raise ValueError(f"Satellite '{sat_id}' not found.")

    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(data[sat_id].get(key), dict):
            data[sat_id][key].update(value)
        else:
            data[sat_id][key] = value

    save_satellites(data, filename)


def delete_satellite(sat_id, filename='satellites.json'):
    """Delete satellite by ID"""
    data = load_satellites(filename)
    if sat_id not in data:
        raise ValueError(f"Satellite '{sat_id}' not found.")
    del data[sat_id]
    save_satellites(data, filename)
