# Interference Analysis Report

## 1. Basic Information

| **Field** | **Value** |
| --- | --- |
| **Report date** | 2025-10-14 |
| **Time range** | 00:00–24:00 |
| **Research institution** | **Institute of Space Internet, Fudan University** |
| **Chart title** | Oneweb constellation Ground Terminal System interference analysis |
| **File name** | oneweb_total_earth_cinr.png |
| **System type** | Ground Terminal System |
| **Monitoring metric** | CINR |
| **Image path** | D:\系统\Calference\itu_report_generator\data\total\oneweb_total_earth_cinr.png |
| **Image description** | Oneweb constellation – Ground Terminal System |



## Figure

![Interference figure](D:/系统/Calference/itu_report_generator/data/total/oneweb_total_earth_cinr.png)

## 2. Data Analysis

**Interference presence**: Yes

### 2.1 Numerical Analysis

| **Metric** | **Typical range** | **Minimum** | **Maximum** | **Average** |
| --- | --- | --- | --- | --- |
| **CINR** | **[58, 62] dB** | **57.8 dB** | **62.8 dB** | **60.0 dB** |

### 2.2 Temporal Characteristics

- Abnormal time periods: N/A
- Interference duration: short-lived
- Interference magnitude: Moderate, based on occasional dips and spikes in CINR values.

### 2.3 Variability Description

The CINR fluctuates consistently throughout the **24-hour** period, characterized by frequent, short-duration spikes and dips. The signal generally remains within a **4 dB** range, but instances of significant drops and increases are observed.

The variability appears stochastic, with no clear periodic patterns or trends identifiable. The CINR values tend to oscillate around the **60 dB** mark.

### 2.4 Potential Interference Sources

- **Terrestrial microwave links**: Potential for sporadic interference due to shared frequency bands and line-of-sight propagation.
- **Adjacent satellite systems**: Overlapping coverage areas could result in interference.
- **Atmospheric effects**: Scintillation or other atmospheric phenomena can cause rapid signal fluctuations, mimicking interference.
- **Ground-based radar systems**: Intermittent radar transmissions could lead to pulsed interference.
- **Other ground terminals**: Erroneous signals from nearby ground terminals could lead to interference.

## 3. Evidence Summary

- The CINR plot shows many short-lived spikes and dips, indicating potential interference events.
- The signal consistently varies, with the value fluctuating between **57.8 dB** and **62.8 dB**.
- There is a wide range of CINR values, which may be due to external interference.
- A few significant dips below the typical range suggest temporary disruptions.
- No periodic pattern is observed in the variations.

## 4. Conclusions and Recommendations

### 4.1 Overall Conclusion

The analysis reveals the presence of interference affecting the Oneweb Ground Terminal System. While the CINR values generally remain within an acceptable range, the observed fluctuations and occasional dips suggest that the system is susceptible to external interference. These disturbances could potentially impact the system's performance and reliability.

### 4.2 Actionable Recommendations

1. Implement interference monitoring techniques to track and identify the sources of interference: This will improve the understanding of interference sources and their impact.
2. Employ interference mitigation techniques like frequency hopping or adaptive coding: This could enhance the system's resilience to interference and maintain acceptable performance levels.
3. Conduct further investigations to pinpoint the specific sources of interference, including spectrum analysis and geolocation techniques: This will enable targeted mitigation strategies and coordination with relevant stakeholders.

## 5. Compliance Considerations

The CINR fluctuations may result in periods where the signal falls below established performance thresholds. Follow-up measurements are recommended to quantify the duration and frequency of threshold exceedances. Further analysis should be performed to determine if PFD or EPFD limits are being exceeded.

## 6. Appendix: Metadata

- Constellation: Oneweb
- Terminal type: Ground Terminal System
- Monitoring metric: CINR
- Source file: oneweb_total_earth_cinr.png
- Path: D:\系统\Calference\itu_report_generator\data\total\oneweb_total_earth_cinr.png