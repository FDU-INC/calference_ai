# Satellite Communication Interference Analysis System

A comprehensive microservices-based system for analyzing satellite communication interference, supporting both GSO (Geostationary) and NGSO (Non-Geostationary) satellite systems with ITU S.1323 standard compliance and AI-powered report generation.

## 🚀 Features

- **Microservices Architecture**: Scalable and maintainable service-oriented design
- **GSO Interference Analysis**: Carrier-to-Interference (C/I) ratio calculations for geostationary satellites
- **NGSO Time-Series Analysis**: Dynamic interference analysis for non-geostationary satellite constellations
- **ITU S.1323 Compliance**: International standard threshold checking
- **RESTful APIs**: Clean and intuitive API design with JSON data exchange
- **Real-time Calculations**: Efficient orbital mechanics and antenna gain computations
- **AI-Powered Reports**: Multi-agent system for generating comprehensive interference analysis reports
- **Process Management**: Unified service startup and management with graceful shutdown

## 🏗️ Architecture

The system consists of five independent microservices:

| Service | Port | Description |
|---------|------|-------------|
| **Earth Station Service** | 5001 | Manages ground station data and configurations |
| **Satellites Service** | 5002 | Handles satellite orbital parameters and metadata |
| **Antennas Service** | 5003 | Manages antenna configurations and gain patterns |
| **Interference Service** | 5004 | Performs core interference calculations and analysis |
| **Multi-Agent Report Service** | 5005 | AI-powered interference analysis report generation |

## 📋 Prerequisites

- Python 3.7+
- Flask
- NumPy
- Matplotlib
- Requests
- AutoGen (for AI report generation)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calference
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare data files**
   - `earth_stations_ngso.json`: NGSO ground station configurations
   - `satellites_ngso.json`: NGSO satellite orbital data
   - `antennas.json`: Antenna gain patterns and specifications

## 🚀 Quick Start

### Automated Startup (Recommended)
```bash
# Start all microservices automatically
python start_services.py

# In another terminal, run the analysis
python main_client.py
```

### Manual Startup
```bash
# Start each service individually
python earth_station_service.py &
python satellites_service.py &
python antennas_service.py &
python interference_service.py &
python itu_report_generator/demo_ms.py &
```

### Stop All Services
```bash
# Press Ctrl+C in the start_services.py terminal
# Or force stop all Python processes:
taskkill /F /IM python.exe  # Windows
```

## 📡 API Documentation

### Earth Station Service (Port 5001)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/stations` | Get all earth stations |
| GET | `/stations/<id>` | Get specific earth station |
| POST | `/stations` | Create new earth station |
| PUT | `/stations/<id>` | Update earth station |
| DELETE | `/stations/<id>` | Delete earth station |
| GET | `/health` | Health check |

### Satellites Service (Port 5002)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/satellites` | Get all satellites |
| GET | `/satellites/<id>` | Get specific satellite |
| POST | `/satellites` | Create new satellite |
| PUT | `/satellites/<id>` | Update satellite |
| DELETE | `/satellites/<id>` | Delete satellite |
| GET | `/health` | Health check |

### Antennas Service (Port 5003)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/antennas` | Get all antennas |
| GET | `/antennas/<id>` | Get specific antenna |
| POST | `/antennas` | Create new antenna |
| PUT | `/antennas/<id>` | Update antenna |
| DELETE | `/antennas/<id>` | Delete antenna |
| GET | `/health` | Health check |

### Interference Service (Port 5004)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/compute_ci` | Calculate C/I ratio |
| POST | `/check_itu_thresholds` | Check ITU S.1323 compliance |
| POST | `/update_ngso_interference` | Run NGSO interference analysis |
| GET | `/health` | Health check |
| GET | `/services/health` | Check dependency services |

### Multi-Agent Report Service (Port 5005)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/analyze` | Generate AI-powered interference analysis report |
| GET | `/health` | Health check |

## 💡 Usage Examples

### Create a Satellite
```bash
curl -X POST http://localhost:5002/satellites \
  -H "Content-Type: application/json" \
  -d '{
    "satellite_id": "GSO_A",
    "name": "Geostationary Satellite A",
    "lon_deg": 123.0,
    "tx_eirp_dBW": 45.0,
    "frequency_Hz": 12000000000
  }'
```

### Calculate Interference
```bash
curl -X POST http://localhost:5004/compute_ci \
  -H "Content-Type: application/json" \
  -d '{
    "station_id": "BEIJING_GS",
    "main_satellite_id": "GSO_A",
    "interf_satellite_id": "GSO_B"
  }'
```

### Run NGSO Analysis
```bash
curl -X POST http://localhost:5004/update_ngso_interference \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "satellites_ngso.json",
    "ground_file": "earth_stations_ngso.json",
    "step": 1,
    "duration": 3600
  }'
```

### Generate AI Report
```bash
# Analyze by image name
curl -X POST http://localhost:5005/analyze \
  -F "image_name=oneweb_total_earth_cinr.png" \
  -F "download=false"

# Analyze by file upload
curl -X POST http://localhost:5005/analyze \
  -F "file=@interference_plot.png" \
  -F "download=false"
```

## 📊 Data Models

### Earth Station
```json
{
  "station_id": "BEIJING_GS",
  "name": "Beijing Ground Station",
  "lat_deg": 39.9042,
  "lon_deg": 116.4074,
  "altitude_m": 50.0,
  "antenna_id": "ANT_001"
}
```

### Satellite
```json
{
  "satellite_id": "GSO_A",
  "name": "Geostationary Satellite A",
  "lon_deg": 123.0,
  "tx_eirp_dBW": 45.0,
  "frequency_Hz": 12000000000,
  "orbit_type": "GSO"
}
```

### Antenna
```json
{
  "antenna_id": "ANT_001",
  "name": "Parabolic Antenna",
  "diameter_m": 3.0,
  "efficiency": 0.65,
  "gain_pattern": "parabolic"
}
```

## 🔬 Technical Details

### Interference Calculation
- **Free Space Path Loss**: Calculated using standard FSPL formula
- **Antenna Gain**: Directional gain based on antenna patterns
- **C/I Ratio**: Carrier-to-Interference ratio computation
- **I/N Ratio**: Interference-to-Noise ratio analysis
- **ITU Thresholds**: S.1323 standard compliance checking

### NGSO Analysis
- **Orbital Mechanics**: Keplerian element propagation
- **Time-Series**: Dynamic interference over time
- **Coordinate Systems**: ECI (Earth-Centered Inertial) transformations
- **Visualization**: Matplotlib-based plotting (optional)

### AI Report Generation
- **Multi-Agent System**: Collaborative AI agents for analysis
- **Image Processing**: Automatic interference plot analysis
- **Report Formats**: Markdown and Word document generation
- **LLM Integration**: Advanced language model for report writing

## 🧪 Testing

```bash
# Test all microservices
python test_services.py

# Test individual service health
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health
curl http://localhost:5005/health
```

## 📁 Project Structure

```
satellite-interference-analysis/
├── earth_station_service.py      # Earth station microservice
├── satellites_service.py         # Satellite microservice
├── antennas_service.py           # Antenna microservice
├── interference_service.py       # Interference calculation service
├── main_client.py               # Main analysis client
├── start_services.py            # Service startup script
├── test_services.py             # Service testing script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── README_微服务版.md           # Chinese documentation
├── itu_report_generator/        # AI report generation
│   ├── demo_ms.py              # AI report microservice
│   ├── demo.py                 # Core AI logic
│   ├── report_service.py       # Report generation service
│   └── data/                   # Report data directory
├── earth_stations_ngso.json     # NGSO ground station data
├── satellites_ngso.json         # NGSO satellite data
└── antennas.json                # Antenna configurations
```

## 🚀 Process Management

### Service Startup
The `start_services.py` script provides:
- **Automated startup**: Launches all 5 microservices
- **Process tracking**: Monitors all running processes
- **Graceful shutdown**: Clean termination with Ctrl+C
- **Error handling**: Reports startup failures

### Service Monitoring
- **Health checks**: All services provide `/health` endpoints
- **Process status**: Automatic detection of crashed services
- **Unified control**: Single script manages all services

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ITU (International Telecommunication Union) for S.1323 standards
- Satellite communication research community
- AutoGen framework for AI agent capabilities
- Open source contributors

## 📞 Support

For questions, issues, or contributions, please:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 🔧 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 5001-5005 are available
2. **Service startup failures**: Check dependencies and file paths
3. **AI service timeout**: Allow extra time for AI model initialization
4. **Process management**: Use Ctrl+C for graceful shutdown

### Performance Tips

1. **Resource allocation**: AI service requires significant memory
2. **Network optimization**: Local services minimize latency
3. **Concurrent processing**: Services can handle multiple requests
4. **Caching**: Consider implementing result caching for repeated calculations

---

**Note**: This system is designed for research and educational purposes. For production use, additional security, monitoring, and scalability considerations should be implemented.