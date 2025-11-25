# Calference Project

Calference is a satellite interference simulation and analysis platform that combines a core computation engine with an automated report generation tool.

## Project Structure

The repository follows a **partially open-source** strategy:

- **`itu_report_generator/`** – ITU interference report generator (**open source, GPL-3.0**)
- **`Calself/`** – Core simulation system (**proprietary, not included in the public repo**)

## Open-Source Component

### ITU Report Generator

An LLM-powered automation pipeline that analyzes satellite-interference plots and produces ITU-compliant Word reports.

**Key capabilities**
- Intelligent analysis for single or multiple plots
- Structured Word report generation
- Bilingual support (Chinese & English)
- ITU terminology alignment

**Read more:** [itu_report_generator/README.md](itu_report_generator/README.md)

## Getting Started

### Open component (ITU Report Generator)

```bash
cd itu_report_generator
pip install -r requirements.txt
cp config.py.example config.py
# Update config.py with your settings
python main.py --single your_image.png
```

See the detailed guide in [itu_report_generator/README.md](itu_report_generator/README.md).

### Proprietary component (Calself)

The `Calself/` directory references the closed-source computation engine, which is not distributed in this repository.

## License

This project uses a **mixed licensing** model:

- **`itu_report_generator/`** – [GNU General Public License v3.0 (GPL-3.0)](itu_report_generator/LICENSE)
- **`Calself/`** – Proprietary license (closed source)

## Project Status

- ✅ `itu_report_generator` – open and maintained
- 🔒 `Calself` – proprietary module

## Contributing

We only accept contributions to the open component `itu_report_generator/`. Please:

1. Fork the repository
2. Create a feature branch
3. Submit changes (restricted to `itu_report_generator/`)
4. Open a pull request

## Contact

For questions or suggestions, please open an issue.

---

**Note:** This repository only contains the open-source component. The proprietary `Calself/` module is excluded from the public history.

