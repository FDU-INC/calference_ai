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
import math
import numpy as np
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import os

# Physical constants
C = 299792458.0  # Speed of light (m/s)
k_B = 1.38064852e-23  # Boltzmann constant (J/K)
# Earth constants (approximate, WGS84 equatorial radius/geocenter to GEO)
R_E = 6378.137e3  # m (WGS84 equatorial)
R_GEO = 42164e3   # m (approx geostationary orbit radius from Earth's center)

def load_json(fname):
    """Load JSON data from file"""
    with open(fname, 'r', encoding='utf-8') as f:
        return json.load(f)

def geodetic_to_ecef(lat_deg, lon_deg, alt_m):
    """Convert geodetic coordinates (degrees) + altitude (m) to ECEF (m)"""
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    # Use simplified spherical model (sufficient for this purpose), or replace with WGS84 precise conversion
    r = R_E + alt_m
    x = r * math.cos(lat) * math.cos(lon)
    y = r * math.cos(lat) * math.sin(lon)
    z = r * math.sin(lat)
    return np.array([x, y, z])

def geo_sat_position_ecef(lon_deg, incl_deg=0.0):
    """Simplified: GSO satellite as equatorial, zero inclination, lon_deg is sub-satellite longitude (degrees)"""
    lon = math.radians(lon_deg)
    lat = math.radians(0.0 + incl_deg)  # If inclination is non-zero, can be extended
    x = R_GEO * math.cos(lat) * math.cos(lon)
    y = R_GEO * math.cos(lat) * math.sin(lon)
    z = R_GEO * math.sin(lat)
    return np.array([x, y, z])

def vector_angle_deg(v1, v2):
    """Return angle between two vectors (degrees)"""
    dot = np.dot(v1, v2)
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    cosang = max(-1.0, min(1.0, dot / (n1 * n2)))
    return math.degrees(math.acos(cosang))

def slant_range_and_angles(es_ecef, sat_ecef):
    """Calculate slant range and vector between earth station and satellite"""
    vec = sat_ecef - es_ecef
    d = np.linalg.norm(vec)
    # Angle between geocenter vector and earth station to satellite vector (useful for some ITU formulas)
    return d, vec

def free_space_loss_dB(distance_m, freq_Hz):
    """Calculate free space path loss: FSL = 20 log10(4*pi*d*f / c)"""
    return 20.0 * math.log10(4.0 * math.pi * distance_m * freq_Hz / C)

def antenna_gain_parabolic_dBi(diameter_m, efficiency, freq_Hz, off_axis_deg=0.0):
    """Antenna pattern: main lobe gain approximation + off-axis attenuation (Gaussian approximation)"""
    wavelength = C / freq_Hz
    G0_lin = efficiency * (math.pi * diameter_m / wavelength) ** 2
    G0_dBi = 10.0 * math.log10(G0_lin) if G0_lin > 0 else -999.0
    # 3dB beamwidth approx: theta_3dB = 70 * lambda / D (deg) (common approximation)
    theta_3dB = 70.0 * wavelength / diameter_m  # deg
    if off_axis_deg <= 0:
        return G0_dBi
    # Simple approximation: Gaussian/quadratic attenuation
    # attenuation ≈ 12*(theta/theta_3dB)^2 dB (common parabolic antenna approximation)
    att = 12.0 * (off_axis_deg / theta_3dB) ** 2
    return G0_dBi - att

def antenna_gain_from_pattern(antenna_entry, off_axis_deg, freq_Hz):
    """If pattern_file is provided, read and interpolate (assumes user provides angle->gain)"""
    pf = antenna_entry.get('pattern_file')
    if pf:
        try:
            with open(pf, 'r') as f:
                data = json.load(f)
            # data expected {"angles_deg":[...], "gains_dBi":[...]}
            angs = np.array(data['angles_deg'])
            gains = np.array(data['gains_dBi'])
            return float(np.interp(off_axis_deg, angs, gains, left=gains[0], right=gains[-1]))
        except Exception:
            pass
    # Otherwise use parabolic approximation
    D = antenna_entry.get('diameter_m', 1.0)
    eta = antenna_entry.get('efficiency', 0.6)
    return antenna_gain_parabolic_dBi(D, eta, freq_Hz, off_axis_deg)

def compute_ci_for_es(es, sat_main, sat_interf, antennas, verbose=False):
    """
    Compute Carrier-to-Interference ratio for earth station
    
    Args:
        es: ground station dict
        sat_main: serving satellite dict
        sat_interf: interfering satellite dict
        antennas: dict of antenna definitions
        verbose: print detailed results
    """
    es_pos = geodetic_to_ecef(es['lat_deg'], es['lon_deg'], es.get('alt_m', 0.0))
    satA_pos = geo_sat_position_ecef(sat_main['lon_deg'])
    satB_pos = geo_sat_position_ecef(sat_interf['lon_deg'])

    # Line-of-sight vectors and angles
    vecA = satA_pos - es_pos
    vecB = satB_pos - es_pos
    ang_deg = vector_angle_deg(vecA, vecB)  # Angular separation between satellites from earth station (degrees)

    # Individual distances
    dA = np.linalg.norm(vecA)
    dB = np.linalg.norm(vecB)

    # Frequency (use main satellite frequency as reference, can be handled separately if different)
    freq = sat_main.get('frequency_Hz', sat_interf.get('frequency_Hz', 12e9))

    # Antenna pointing: assume receive antenna points to main satellite (off-axis for main = 0)
    # Receive antenna off-axis angle to interferer is ang_deg
    rx_ant = antennas[es['rx_antenna_id']]
    tx_ant_A = antennas.get(sat_main.get('tx_antenna_id'))
    tx_ant_B = antennas.get(sat_interf.get('tx_antenna_id'))

    # Get antenna gains
    G_rx_on_main = antenna_gain_from_pattern(rx_ant, 0.0, freq)  # dBi
    G_rx_off_interf = antenna_gain_from_pattern(rx_ant, ang_deg, freq)  # dBi

    # Transmit pattern: assume satellite points main lobe to earth station or provides EIRP
    # If tx_eirp_dBW is given, use directly; otherwise combine Pt + Gtx - tx_losses
    if 'tx_eirp_dBW' in sat_main:
        EIRP_A_dBW = sat_main['tx_eirp_dBW'] - sat_main.get('tx_losses_dB', 0.0)
    else:
        # fallback if Pt and Gtx available
        Pt_dBW = sat_main.get('tx_power_dBW', 0.0)
        Gtx_on = antenna_gain_from_pattern(tx_ant_A, 0.0, freq) if tx_ant_A else 0.0
        EIRP_A_dBW = Pt_dBW + Gtx_on - sat_main.get('tx_losses_dB', 0.0)

    if 'tx_eirp_dBW' in sat_interf:
        EIRP_B_dBW = sat_interf['tx_eirp_dBW'] - sat_interf.get('tx_losses_dB', 0.0)
    else:
        Pt_dBW = sat_interf.get('tx_power_dBW', 0.0)
        Gtx_on = antenna_gain_from_pattern(tx_ant_B, 0.0, freq) if tx_ant_B else 0.0
        EIRP_B_dBW = Pt_dBW + Gtx_on - sat_interf.get('tx_losses_dB', 0.0)

    # If satellite transmit pattern is not directed to ground (e.g., main lobe offset),
    # need to calculate transmit off-axis angle to target
    # Here simplified: assume tx satellite antenna points to respective service points (main satellite to ES is on-axis)
    # For more rigorous analysis, should calculate off-axis angle between satellite antenna pointing and earth station line and use pattern
    G_tx_A_dBi = 0.0  # already in EIRP
    G_tx_B_dBi = 0.0

    # Path losses
    FSL_A = free_space_loss_dB(dA, freq)
    FSL_B = free_space_loss_dB(dB, freq)

    # Receiver additional losses
    rx_losses = es['rx_system'].get('rx_losses_dB', 0.0)

    # Interference power I (dBW) from satellite B at earth station receive antenna
    # I = EIRP_B + G_rx(off-axis) - FSL_B - rx_losses
    I_dBW = EIRP_B_dBW + G_rx_off_interf - FSL_B - rx_losses

    # Carrier power C (dBW) from main satellite A
    # C = EIRP_A + G_rx(on-axis) - FSL_A - rx_losses
    C_dBW = EIRP_A_dBW + G_rx_on_main - FSL_A - rx_losses

    # C/I (dB)
    CI_dB = C_dBW - I_dBW

    # Calculate system noise N (dBW): N = k * T_sys * B
    T_sys = es['rx_system'].get('T_sys_K', 500.0)
    B = es['rx_system'].get('bandwidth_Hz', 36e6)
    N_W = k_B * T_sys * B
    N_dBW = 10.0 * math.log10(N_W) if N_W > 0 else -999.0

    # I/N
    IN_dB = I_dBW - N_dBW

    results = {
        'angle_deg': ang_deg,
        'distance_m_A': dA, 'distance_m_B': dB,
        'FSL_A_dB': FSL_A, 'FSL_B_dB': FSL_B,
        'EIRP_A_dBW': EIRP_A_dBW, 'EIRP_B_dBW': EIRP_B_dBW,
        'G_rx_on_main_dBi': G_rx_on_main, 'G_rx_off_interf_dBi': G_rx_off_interf,
        'C_dBW': C_dBW, 'I_dBW': I_dBW, 'C_over_I_dB': CI_dB,
        'N_dBW': N_dBW, 'I_over_N_dB': IN_dB
    }

    if verbose:
        for k,v in results.items():
            print(f"{k}: {v}")
    return results

def check_against_itu_thresholds(results, reuse=False):
    """
    Check interference against ITU S.1323 thresholds
    
    Args:
        results: interference calculation results
        reuse: whether frequency reuse is applied
    
    Returns:
        dict: threshold check results
    """
    # ITU S.1323: Maximum permissible interference = 25% of system noise (no reuse) or 20% with reuse
    # 25% -> 10*log10(0.25) = -6.0206 dB (I relative to N)
    thr_pct = 0.20 if reuse else 0.25
    thr_dB = 10.0 * math.log10(thr_pct)
    I_over_N_dB = results['I_over_N_dB']
    ok = I_over_N_dB <= thr_dB
    return {
        'threshold_pct': thr_pct,
        'threshold_dB': thr_dB,
        'I_over_N_dB': I_over_N_dB,
        'acceptable': ok
    }

#--- NGSO Interference ---
def kepler_to_eci(a, e, i, raan, argp, M0, epoch, time_utc=None):
    """
    Calculate satellite ECI coordinates at given time from Keplerian elements
    
    Args:
        a: semi-major axis (km)
        e: eccentricity
        i: inclination (degrees)
        raan: right ascension of ascending node (degrees)
        argp: argument of perigee (degrees)
        M0: mean anomaly at epoch (degrees)
        epoch: reference epoch
        time_utc: target time (default: current time)
    
    Returns:
        list: ECI position vector (km)
    """
    # Earth gravitational constant μ (km^3/s^2)
    MU_EARTH = 398600.4418
    
    i = np.radians(i)
    raan = np.radians(raan)
    argp = np.radians(argp)
    M0 = np.radians(M0)

    epoch = datetime.fromisoformat(epoch.replace("Z", "+00:00"))
    if time_utc is None:
        time_utc = datetime.now(timezone.utc)
    elif time_utc.tzinfo is None:
        time_utc = time_utc.replace(tzinfo=timezone.utc)
    dt = (time_utc - epoch).total_seconds()

    # Mean motion (rad/s)
    n = np.sqrt(MU_EARTH / a ** 3)

    # Current mean anomaly
    M = M0 + n * dt

    # Solve for eccentric anomaly E (Kepler's equation)
    E = M
    for _ in range(10):
        E = M + e * np.sin(E)

    # True anomaly
    nu = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2),
                        np.sqrt(1 - e) * np.cos(E / 2))

    # Position vector in orbital plane coordinates (km)
    r_orb = np.array([
        a * (np.cos(E) - e),
        a * np.sqrt(1 - e ** 2) * np.sin(E),
        0.0
    ])

    # Rotate coordinates to ECI
    R3_W = np.array([
        [ np.cos(raan), -np.sin(raan), 0],
        [ np.sin(raan),  np.cos(raan), 0],
        [ 0, 0, 1]
    ])
    R1_i = np.array([
        [1, 0, 0],
        [0, np.cos(i), -np.sin(i)],
        [0, np.sin(i),  np.cos(i)]
    ])
    R3_w = np.array([
        [ np.cos(argp), -np.sin(argp), 0],
        [ np.sin(argp),  np.cos(argp), 0],
        [ 0, 0, 1]
    ])

    R = R3_W @ R1_i @ R3_w
    r_eci = R @ r_orb

    return r_eci.tolist()

def free_space_path_loss_ngso(distance_km, frequency_Hz):
    """Calculate free space path loss for NGSO systems"""
    c = 3e8  # Speed of light (m/s)
    distance_m = distance_km * 1000  # Convert to meters
    frequency_Hz = float(frequency_Hz)
    fspl = 20 * np.log10(distance_m) + 20 * np.log10(frequency_Hz) - 147.55  # dB
    return fspl

def calculate_interference(satellite_pos, ground_station_pos, frequency_Hz, eirp_dBW, antenna_gain_dB):
    """Calculate interference between satellite and ground station"""
    # Calculate distance between satellite and ground station (km)
    satellite_position = np.array(satellite_pos)
    ground_station_position = np.array(ground_station_pos)
    distance_km = np.linalg.norm(satellite_position - ground_station_position)
    
    # Calculate free space path loss (dB)
    fspl = free_space_path_loss_ngso(distance_km, frequency_Hz)
    
    # Interference calculation, assuming EFPD is combination of FSPL, transmit power and antenna gain
    interference_dB = eirp_dBW + antenna_gain_dB - fspl
    
    return interference_dB

def update_ngso_interference(filename='satellites_ngso.json', ground_file='earth_stations.json', step=1, duration=86400):
    """
    Update NGSO to NGSO interference analysis, output EFPD vs time plot
    
    Args:
        filename: satellite data file
        ground_file: ground station data file
        step: time step in seconds
        duration: analysis duration in seconds
    
    Returns:
        list: interference over time
    """
    satellites = load_json(filename)
    ground_stations = load_json(ground_file)
    
    interference_over_time = []
    times = []

    # Iterate through each time step
    for t in range(0, duration, step):
        current_time = datetime.utcnow() + timedelta(seconds=t)
        total_interference = 0

        # Iterate through each satellite
        for sat_id, sat in satellites.items():
            if "keplerian" not in sat:
                continue

            kep = sat["keplerian"]
            try:
                # Calculate satellite position
                pos_eci = kepler_to_eci(
                    a=kep["a_km"],
                    e=kep["e"],
                    i=kep["i_deg"],
                    raan=kep["raan_deg"],
                    argp=kep["argp_deg"],
                    M0=kep["M0_deg"],
                    epoch=kep["epoch"],
                    time_utc=current_time
                )

                # Calculate interference with each ground station
                for gs_id, gs in ground_stations.items():
                    interference = calculate_interference(pos_eci, [gs["longitude_deg"], gs["latitude_deg"], 0],
                                                          sat["frequency_Hz"], sat["tx_eirp_dBW"], gs["antenna_gain_dB"])
                    total_interference += interference
            except Exception:
                pass

        # Record interference at current time
        interference_over_time.append(total_interference)
        times.append(current_time)

    # Plot interference over time
    plt.plot(times, interference_over_time)
    plt.xlabel('Time (UTC)')
    plt.ylabel('Total EFPD (dB)')
    plt.title('NGSO to NGSO Interference over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return interference_over_time


# Example main function (read JSON and calculate)
if __name__ == "__main__":
    gs = load_json('ground_stations.json')
    sats = load_json('satellites.json')
    ants = load_json('antennas.json')

    # Assume we want to evaluate ground station ES1, main satellite GSO_A, interfering satellite GSO_B
    es = gs['ES1']
    satA = sats['GSO_A']
    satB = sats['GSO_B']

    res = compute_ci_for_es(es, satA, satB, ants, verbose=True)
    check = check_against_itu_thresholds(res, reuse=False)
    print("\nITU S.1323 threshold check:", check)
