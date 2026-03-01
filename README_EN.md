# Calference - Satellite Interference Analysis and Report Generation System

> **SPACENET** - Fudan University Space Internet Research Institute  
> Intelligent Satellite Interference Analysis and Compliance Assessment Platform

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## 📖 Project Overview

Calference is a professional satellite interference analysis and report generation system designed to help researchers and engineers:
- 🛰️ Analyze interference patterns in satellite communication systems
- 📊 Automatically generate professional analysis reports compliant with ITU standards
- 🔍 Provide intelligent compliance assessment based on RAG (Retrieval-Augmented Generation) technology
- 🤖 Generate high-quality technical documents using multi-agent collaboration

### Key Features

- ✅ **Intelligent Report Generation**: Automatically analyze interference charts and generate detailed reports based on multi-agent architecture
- ✅ **ITU Standard Compliance**: Integrated ITU standard documents for compliance assessment and recommendations
- ✅ **Multiple Output Formats**: Support both Markdown and Word format outputs
- ✅ **RAG Enhancement**: Use retrieval-augmented generation technology to cite relevant standard documents
- ✅ **Flexible Architecture**: Support multiple LLM backends (GLM, Claude, etc.)
- ✅ **REST API**: Provide standardized HTTP API interfaces

## 🏗️ System Architecture

![Calference System Architecture](image/README_EN/system_architecture.png)

### Open Source Notice

**This project is partially open source:**

- ✅ **Open Source Components**:
  - ITU Interference Report Generator (`itu_report_generator/`)
  - API Client Wrapper (`calself_client/`)
  - Usage Examples and Documentation (`examples/`, `docs/`)
  - Frontend Interface (`frontend/`)

- 🔒 **Closed Source Components**:
  - Calself Core Simulation Engine (satellite interference calculation algorithms)
  - Simulation Server Implementation
  
**Note**: The Calself simulation service is provided via REST API. Users can call it through the client without accessing the underlying implementation.

## 📁 Project Structure

```
Calference v1.0/
├── examples/                          # 📚 Usage Examples
│   ├── example_calself_usage.py       # Calself Service Usage Example
│   ├── example_itu_report.py          # ITU Report Generation Example
│   └── README.md                      # Example Documentation
│
├── calself_client/                    # 🔌 API Client (Open Source)
│   ├── client.py                      # REST API Client Implementation
│   └── __init__.py
│
├── calself_service/                   # 🎯 Service Middleware (Open Source)
│   └── service.py                     # Service Interface Wrapper
│
├── itu_report_generator/              # 📊 Report Generator (Open Source)
│   ├── itu_interference_analyzer.py   # Main Program (4-Agent Dialogue)
│   ├── report_service.py              # Service Interface
│   ├── config.py                      # Configuration File
│   ├── src/                           # Source Code
│   │   ├── itu_file_rag.py            # RAG Retrieval Module (File System)
│   │   ├── prepare_data.py            # Data Preparation Script
│   │   └── download_embedding_model.py # Model Download Script
│   ├── frontend/                      # Web Frontend
│   │   ├── api.py                     # FastAPI Service
│   │   └── static/                    # Static Files
│   └── data/                          # Data Directory (Module Level, Optional)
│
├── docs/                              # 📖 Documentation
│   └── USER_MANUAL.md                 # Detailed User Manual
│
├── requirements.txt                   # Python Dependencies
├── LICENSE                            # GPL-3.0 License
└── README.md                          # This File
```

## 🚀 Quick Start

### System Requirements

- Python 3.10 or higher
- 4GB+ RAM
- (Optional) pandoc (for Word document generation)
- (Optional) CUDA (for GPU acceleration)

### One-Click Initialization (Recommended)

```bash
# 1. Clone the repository
git clone <repository_url>
cd Calference11.3

# 2. Create virtual environment (recommended)
conda create -n itu python=3.10
conda activate itu

# 3. One-click initialization (auto-install dependencies, download models, prepare data)
python init.py --auto

# 4. Configure LLM API Key
export LLM_API_KEY="your_api_key_here"

# 5. Run example
python run.py itu-report
```

### Manual Installation

```bash
# 1. Clone the repository
git clone <repository_url>
cd Calference11.3

# 2. Create virtual environment (recommended)
conda create -n itu python=3.10
conda activate itu

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Install pandoc for Word document generation
# Ubuntu/Debian:
sudo apt install pandoc

# macOS:
brew install pandoc

# Windows:
# Download installer: https://pandoc.org/installing.html

# 5. Prepare data
python run.py download-model
python run.py prepare-rag
```

### Configure LLM API

Edit `itu_report_generator/config.py` or set environment variables:

```bash
# GLM Configuration (Recommended)
export LLM_MODEL_NAME="glm-4v-flash"
export LLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export LLM_API_KEY="your_api_key_here"

# Or Claude Configuration
export LLM_MODEL_NAME="claude-3-7-sonnet-20250219"
export LLM_BASE_URL="http://your-proxy:8000"
export LLM_API_KEY="your_api_key_here"
```

### Running Examples

#### Method 1: Using Unified Run Script (Recommended)

The project provides a unified `run.py` script for quick access to all features:

```bash
# View all available commands
python run.py --help

# Generate ITU interference report
python run.py itu-report

# Specify custom image
python run.py itu-report --image path/to/your/image.png

# Run Calself satellite simulation (0.1 hours)
python run.py calself-sim --duration 0.1

# Prepare RAG data
python run.py prepare-rag

# Download embedding model
python run.py download-model

# Start Web API service (default port 8001)
python run.py web-api

# Start Calself simulation service (default port 8000, developers only)
python run.py calself-service

# Show project status
python run.py status

# Run examples
python run.py example itu_report
python run.py example calself_usage
```

#### Method 2: Using Makefile (Quick Commands)

The project provides a Makefile for concise commands:

```bash
# View all available commands
make help

# Complete project setup (install dependencies + prepare data)
make setup

# Generate ITU interference report
make itu-report

# Run Calself satellite simulation
make calself-sim

# Prepare RAG data
make prepare-rag

# Download embedding model
make download-model

# Start Web API service
make web-api

# Start Calself simulation service
make calself-service

# Run examples
make example-itu
make example-calself

# Show project status
make status

# Clean temporary files
make clean
```

#### Method 3: Using Quick Start Script

The project provides `quickstart.sh` script for Linux/macOS:

```bash
# Add execute permission
chmod +x quickstart.sh

# View help
./quickstart.sh help

# Generate ITU interference report
./quickstart.sh itu-report

# Run Calself simulation
./quickstart.sh calself-sim --duration 0.5

# Start Web service (default port 8001)
./quickstart.sh web-api

# Show project status
./quickstart.sh status
```

#### Method 4: Directly Run Example Scripts

```bash
# Use default example image
python examples/example_itu_report.py

# Or specify custom image
python examples/example_itu_report.py path/to/your/image.png

# Calself simulation service (requires server to be started first)
export CALSELF_BASE_URL="http://localhost:8000"
python examples/example_calself_usage.py
```

## 🛠️ Project Tools

The project provides various convenient tools for different use cases:

### 1. Unified Run Script (`run.py`)

Full-featured Python script supporting all project features:

```bash
python run.py --help                    # View all commands
python run.py itu-report                # Generate report
python run.py calself-sim               # Run simulation
python run.py web-api                   # Start Web service
python run.py status                    # Show project status
```

### 2. Makefile Quick Commands

Concise Makefile commands for frequent use:

```bash
make help                               # View all commands
make setup                              # Complete project setup
make itu-report                         # Generate report
make web-api                            # Start Web service
make clean                              # Clean temporary files
```

### 3. Quick Start Script (`quickstart.sh`)

Shell script for Linux/macOS:

```bash
chmod +x quickstart.sh
./quickstart.sh help                    # View help
./quickstart.sh itu-report              # Generate report
./quickstart.sh web-api --port 8000     # Start service
```

### 4. Project Initialization Script (`init.py`)

One-click project initialization, automatically installs dependencies and prepares data:

```bash
python init.py                          # Interactive initialization
python init.py --auto                   # Automatic initialization
python init.py --check                  # Environment check only
```

### 5. Comprehensive Usage Example (`examples_comprehensive.py`)

Interactive example script demonstrating all main features:

```bash
python examples_comprehensive.py        # Launch interactive menu
```

## 📖 Documentation

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- **Command Reference**: [COMMANDS.md](COMMANDS.md) - Complete command reference card
- **User Manual**: [docs/USER_MANUAL.md](docs/USER_MANUAL.md) - Detailed user manual

## 📊 Main Features

### 1. Automatic ITU Interference Report Generation

Generate professional interference analysis reports using multi-agent collaboration:

```python
from pathlib import Path
from itu_report_generator.report_service import generate_report

# Generate report
result = await generate_report(
    image_path=Path("data/input/oneweb_total_earth_cinr.png"),
    use_rag=True  # Enable RAG retrieval
)

print(f"Report generated: {result['markdown_path']}")
```

**Report Generation Process:**
1. Parser Agent - Parse image information
2. Analysis Agent - Analyze interference data
3. Review Agent - Review analysis results
4. Report Agent - Generate final report (Markdown + Word)

### 2. Calself Simulation Service Call

Call satellite interference simulation service via REST API:

```python
from datetime import datetime
from calself_service import get_service

# Initialize service
service = get_service("http://localhost:8000")

# Run simulation
result = service.run_simulation(
    start_time=datetime(2024, 12, 16, 0, 0, 0),
    duration_hours=0.1,
    step=2
)

# Get results
files = service.get_inference_files(company_id=1)
data = service.load_inference_file(1, files["1"][0])
```

#### ⚠️ About TLE Error Messages

When running simulations, you may see many TLE (Two-Line Element) error messages, for example:

```
Error 6 for tle 1 at time 2026-02-10 15:57:00.360973
Error 1 for tle 20 at time 2026-02-10 15:57:00.360973
...
```

**This is normal and not a concern.** These errors come from the SGP4 orbital prediction library and indicate:

- **Error 1**: Decayed satellite - The satellite orbit has decayed or the satellite has re-entered
- **Error 6**: Satellite decay or orbital calculation exception - Satellite orbital parameters exceed valid range

**Reasons:**
1. TLE data may not be up-to-date
2. Some satellites' orbits have decayed and are no longer valid
3. Orbital parameters exceed the valid range of the SGP4 model

**This does not affect the simulation** - The program will continue running and the simulation will complete normally. To reduce these messages, update TLE data to the latest version.

### 3. RAG Retrieval Enhancement

Integrated ITU standard documents for automatic retrieval of relevant standards:

```python
from itu_report_generator.src.itu_file_rag import get_itu_file_rag_instance

rag = get_itu_file_rag_instance()
results = rag.search("CINR threshold limit", top_k=3)

for result in results:
    print(f"Source: {result['source']}")
    print(f"Relevance: {result['score']:.3f}")
    print(f"Content: {result['text'][:200]}...")
```

## 🛠️ Development Guide

### Multi-Agent Architecture

The report generator uses a 4-agent dialogue architecture:

```python
Parser Agent (parser_agent)
    ↓ Parse image information, extract structured data
    
Analysis Agent (analysis_agent)
    ↓ Analyze interference data, generate analysis results
    
Review Agent (review_agent)
    ↓ Review analysis results, ensure accuracy
    
Report Agent (report_agent)
    ↓ Generate final report (Markdown + Word)
```

**Advantages:**
- ✅ Each agent focuses on specific tasks
- ✅ Improve quality through dialogue collaboration
- ✅ Automatically track data flow and audit logs
- ✅ Output high-quality professional reports

### Custom LLM Backend

Modify `itu_report_generator/config.py`:

```python
# LLM Configuration
LLM_MODEL_NAME = "your-model-name"
LLM_BASE_URL = "https://your-api-endpoint"
LLM_API_KEY = "your-api-key"

# RAG Configuration
USE_RAG = True
RAG_TOP_K = 3

# Output Configuration
OUTPUT_REPORT_DIR = "data/output_reports"
```

## 📖 Documentation

### Quick Reference

- **Quick Reference Card**: [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Most commonly used commands quick reference
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - 5-minute quick start guide
- **Command Reference**: [COMMANDS.md](COMMANDS.md) - Complete command reference card
- **Script Summary**: [SCRIPTS_SUMMARY.md](SCRIPTS_SUMMARY.md) - Detailed description of all run scripts
- **Setup Checklist**: [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Project setup verification checklist

### Detailed Documentation

- **Usage Examples**: [examples/README.md](examples/README.md)
- **Detailed User Manual**: [docs/USER_MANUAL.md](docs/USER_MANUAL.md)
- **API Documentation**: [docs/api.md](docs/api.md) (Coming soon)

### Environment Configuration

- **Environment Variable Example**: [.env.example](.env.example) - Copy and edit this file to configure environment variables

## 🤝 Contributing

We welcome contributions to the open source components!

### What You Can Contribute:
- ✅ ITU Report Generator improvements
- ✅ Documentation improvements
- ✅ Bug fixes
- ✅ New feature suggestions
- ✅ Example code

### Contribution Process:
1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Note**: Please do not attempt to modify or reverse engineer the closed-source Calself components.

## 📄 License

The open source components of this project are licensed under **GNU General Public License v3.0**.

- **Open Source Components** (GPL-3.0):
  - ITU Report Generator
  - API Client
  - Documentation and Examples

- **Closed Source Components** (Proprietary License):
  - Calself Simulation Engine
  
See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- SPACENET - Fudan University Space Internet Research Institute
- AutoGen Team (Multi-Agent Framework)
- ITU (International Telecommunication Union, Standard Documents)
- Zhipu AI / Anthropic (LLM Support)

## 📞 Contact

- **Research Institution**: SPACENET - Fudan University Space Internet Research Institute
- **Issue Reporting**: [GitHub Issues](https://github.com/your-org/Calference/issues)
- **Email**: support@example.com

---

## 🔖 Version History

### v1.1.0 (2026-02-06)
- ✨ Added 4-agent dialogue-based report generation
- 🚀 Optimized project structure, separated open source and closed source components
- 📚 Improved documentation and usage examples
- 🐛 Fixed token limit issues
- 🎨 Improved report format and quality

### v1.0.0 (2025-11-03)
- 🎉 Initial release
- ✨ ITU Report Generator
- ✨ Calself API Client
- ✨ RAG Retrieval Feature

---

**Made with ❤️ by SPACENET**

