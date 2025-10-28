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

import subprocess
import time
import sys
import os

services = [
    ("earth_station_service.py", 5001),
    ("satellites_service.py", 5002),
    ("antennas_service.py", 5003),
    ("interference_service.py", 5004),
    ("itu_report_generator/demo_ms.py", 5005)
]

processes = []

# Start all services
for script, port in services:
    if os.path.exists(script):
        print(f"Starting {script} on port {port}")
        process = subprocess.Popen([sys.executable, script])
        processes.append((script, process))
        time.sleep(1)
    else:
        print(f"Error: {script} not found")

print("All services started")
print("Press Ctrl+C to stop all services")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopping all services...")
    for script, process in processes:
        print(f"Stopping {script}")
        process.terminate()
        process.wait()
    print("All services stopped")