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
import numpy as np
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt

from interference import compute_ci_for_es, check_against_itu_thresholds, load_json, kepler_to_eci, update_ngso_interference
from earth_station import (
    add_station, get_station, list_stations,
    update_station, delete_station
) 
from satellites import (
    add_satellite, get_satellite, list_satellites,
    update_satellite, delete_satellite
)
from antennas import (
    add_antenna, get_antenna, list_antennas,
    update_antenna, delete_antenna
)

if __name__ == "__main__":
    # # GSO干扰计算
    # gs = load_json('earth_stations.json')
    # sats = load_json('satellites.json')
    # ants = load_json('antennas.json')

    # # 假设我们要评估 ground station ES1, 主卫星 GSO_A, 干扰卫星 GSO_B
    # es = gs['ES1']
    # satA = sats['GSO_A']
    # satB = sats['GSO_B']

    # res = compute_ci_for_es(es, satA, satB, ants, verbose=True)
    # check = check_against_itu_thresholds(res, reuse=False)
    # print("\nITU S.1323 threshold check:", check)

    # NGSO干扰计算
    # --- ngso轨道位置计算示例 ---
    # 载入NGSO卫星数据
    # sats = load_json("satellites_ngso.json")

    # # 获取某颗卫星的轨道六根数
    # kep = sats["NGSO_SAT_01"]["keplerian"]

    # # 计算当前时刻卫星ECI坐标
    # pos = kepler_to_eci(
    #     a=kep["a_km"],
    #     e=kep["e"],
    #     i=kep["i_deg"],
    #     raan=kep["raan_deg"],
    #     argp=kep["argp_deg"],
    #     M0=kep["M0_deg"],
    #     epoch=kep["epoch"]
    # )
    # print("当前卫星ECI坐标 (km)：", pos)

    # 设置时间跨度为1小时，步长为1秒，计算干扰
    update_ngso_interference(filename='satellites_ngso.json', ground_file='earth_stations_ngso.json', step=1, duration=86400)
