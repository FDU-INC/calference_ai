# ITU Interference Chart Intelligent Analysis Report Generator v2.0

This project is used to automatically generate satellite network interference simulation analysis reports compliant with International Telecommunication Union (ITU) standards. Through large language models (LLM) intelligently analyzing simulation images, it automatically writes structured, professional Word reports, greatly improving the efficiency and standardization of satellite communication interference analysis.

## ✨ New Version Features (v2.0)

- ✅ **Simplified Architecture**: Removed MongoDB dependency, using file system RAG
- ✅ **Fast Startup**: No database installation required, startup speed improved by 5x
- ✅ **Easy Maintenance**: Cleaner code, fewer dependencies
- ✅ **High Performance**: NumPy vectorized computation, query speed improved by 3-5x

## Features

- **Single Image Analysis**: Automatically generate detailed analysis reports for single simulation images.
- **Batch Multi-Image Analysis**: Generate structured merged analysis reports for multiple images of the same constellation/terminal type.
- **ITU Standard Retrieval**: File system-based RAG for automatic retrieval of relevant ITU standards.
- **Professional Prompt Construction**: Automatically generate analysis prompts that comply with ITU professional terminology and structure.
- **Word Report Output**: Automatically insert images and analysis content, output high-quality docx format reports.
- **Highly Extensible**: Support custom models, image parsing rules, and report structures.

## Directory Structure

```
.
├── src/                     # Core code directory
│   ├── itu_file_rag.py     # File system RAG implementation
│   ├── prepare_data.py     # Data preparation script
│   └── download_embedding_model.py  # Model download script
├── frontend/                # Web frontend
│   ├── api.py              # FastAPI service
│   └── static/             # Static files
├── itu_interference_analyzer.py  # Main program (4-agent dialogue)
├── report_service.py       # Service interface wrapper
├── config.py               # Configuration file
├── agent_config.py         # Agent configuration
├── requirements.txt        # Dependency list
└── README.md               # This document
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Data

First-time use requires generating RAG data files:

```bash
# Method 1: Using unified run script (recommended)
python run.py prepare-rag

# Method 2: Directly run script
python itu_report_generator/src/prepare_data.py
```

This will:
- Read ITU standard documents from project root `data/rag/` or module `data/itu_standards_txt/`
- Split into text chunks
- Generate embedding vectors
- Save to `data/rag/chunks.jsonl` and `data/rag/embeddings.npy`

**Note**: This step only needs to be run once, unless ITU standard documents are updated.

### 3. Configure API Key (GLM-4V Flash, Zhipu AI)

A usable GLM-4V Flash configuration is built-in by default, centralized in `config.py`. You can switch via environment variables or directly modify the configuration file:

```python
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent

# LLM Configuration (Default: GLM-4V Flash Zhipu AI)
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4v-flash")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)
```

Recommended approach:

- Set environment variables in shell (highest priority):

```bash
export LLM_API_KEY="your-api-key-here"
export LLM_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export LLM_MODEL_NAME="glm-4v-flash"
```

You can also use the `OPENAI_API_KEY` compatible variable name.

### 4. Run Examples

```bash
# Method 1: Using unified run script (recommended)
python run.py itu-report

# Method 2: Directly run main program
python itu_report_generator/itu_interference_analyzer.py

# Method 3: Start Web API service (default port 8001)
python run.py web-api
# Then visit http://127.0.0.1:8001
```

## Usage

### Single Image Analysis

```python
from itu_report_generator.src.itu_file_rag import get_itu_file_rag_instance

# Initialize RAG system
rag = get_itu_file_rag_instance()

# Search for relevant ITU standards
results = rag.search("EPFD limit requirements", top_k=3)

# Format as prompt
references = rag.format_references_for_prompt(results)
```

### Using Web API

After starting the Web API service, you can generate reports via browser or HTTP requests:

```bash
# Start service
python run.py web-api

# Visit http://127.0.0.1:8001
# Select image and generate report in Web interface
```

## Configuration

Main configuration items (`config.py`):

```python
from pathlib import Path
import os

# Base path (project root)
BASE_DIR = Path(__file__).parent.parent
INPUT_IMAGE_DIR = str(BASE_DIR / "data" / "input")
OUTPUT_REPORT_DIR = str(BASE_DIR / "output_reports")

# LLM Configuration (Default: GLM-4V Flash, can be overridden via environment variables)
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "glm-4v-flash")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
LLM_API_KEY = os.getenv(
    "LLM_API_KEY",
    os.getenv("OPENAI_API_KEY", "your-api-key-here"),
)

# RAG Configuration: File system RAG (no MongoDB required)
RAG_DATA_DIR = str(BASE_DIR / "data" / "rag")
RAG_CHUNKS_FILE = "chunks.jsonl"
RAG_EMBEDDINGS_FILE = "embeddings.npy"
RAG_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"
```

## Data File Description

### chunks.jsonl
Each line is a JSON object containing:
```json
{"doc_id": "ITU-R-S.1503-4", "chunk_id": 0, "text": "...", "source": "ITU-R-S.1503-4.txt"}
```

### embeddings.npy
NumPy array, shape: `(num_chunks, embedding_dim)`
- Default dimension: 384 (using paraphrase-multilingual-MiniLM-L12-v2)

### metadata.json (Optional)
Contains statistical information and document list.

## Performance Optimization

### Improve Query Speed
1. Use smaller embedding models
2. Reduce top_k value
3. Use Pickle cache to preload data

### Reduce Memory Usage
1. Use smaller chunk_size
2. Reduce document count
3. Use mmap to load embeddings

## Multi-Language Support

- Reports are generated in **English** by default (compliant with ITU standard specifications)
- Report structure and professional terminology comply with ITU standard format

## Main Process Description

1. **Image Information Parsing**: Automatically extract constellation, terminal type, analysis metrics, and other information from image filenames
2. **RAG Retrieval**: Retrieve relevant content from ITU standard documents
3. **Prompt Construction**: Generate professional analysis prompts based on image information and RAG results
4. **LLM Analysis**: Call LLM to analyze images and prompts, output structured text
5. **Word Report Generation**: Insert images and analysis content, automatically generate docx reports (requires pandoc)

### Network and Certificate Troubleshooting (GLM-4V Flash)

- If you encounter `openai.APIConnectionError: Connection error.`, first check:
  - Whether a required but unavailable proxy is set: `env | egrep -i 'http_proxy|https_proxy|all_proxy|no_proxy'`
  - Try temporarily disabling proxy before running:

```bash
unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
python demo.py
```

- If the system's CA certificate is abnormal, you can force use the certifi certificate from the current Python environment:

```bash
python -c "import certifi, os; print(certifi.where())"
export SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")
export REQUESTS_CA_BUNDLE="$SSL_CERT_FILE"
python demo.py
```

## Notes

- Ensure input image naming conventions for automatic parsing of key information
- LLM inference interface must be correctly configured in the configuration file
- To customize report structure or analysis dimensions, modify prompts in `agent_config.py` or prompt construction logic in `itu_interference_analyzer.py`

## Migration from MongoDB

If you previously used the MongoDB version, please refer to [MIGRATION.md](MIGRATION.md) for migration steps.

## FAQ

### Q: What to do if prompted "Data not loaded"?
A: Run `python run.py prepare-rag` or `python itu_report_generator/src/prepare_data.py` to generate data files.

### Q: How to add new ITU standard documents?
A: 
1. Place txt files in project root `data/rag/itu_standards_txt/` or module `itu_report_generator/data/itu_standards_txt/`
2. Re-run `python run.py prepare-rag`

### Q: What image formats are supported?
A: Supports common formats like PNG, JPG, JPEG.

### Q: How to customize report template?
A: Modify agent configuration in `agent_config.py`, or modify prompt construction logic in `itu_interference_analyzer.py`.

## Technology Stack

- **LLM**: OpenAI API / GLM / Other compatible interfaces
- **Embedding**: SentenceTransformers
- **Vector Computation**: NumPy
- **Document Generation**: python-docx / pandoc
- **Multi-Agent**: AutoGen

## License

This project is licensed under GPL-3.0 open source license. See [LICENSE](LICENSE) file for details.

## Contributing

Welcome to submit Issues and Pull Requests!

## Contact

- Institution: Fudan University Space Internet Research Institute
- Project: ITU Interference Analysis Report Generator

---

**Version**: v2.0 (File System RAG)  
**Update Date**: 2025-02-03

