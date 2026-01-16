# ProVerBs Legal AI Platform

An AI-powered legal assistance platform built with Gradio and deployed on Hugging Face Spaces.

## Overview

ProVerBs Legal AI combines advanced artificial intelligence with comprehensive legal knowledge to provide accessible, accurate legal information and tools. The platform features specialized AI chatbot modes, document processing, case management, and more.

## Features

- **7 Specialized AI Modes**:
  - Application Navigation Guide
  - General Legal Assistant
  - Document Validator
  - Legal Research Assistant
  - Legal Etymology Lookup
  - Case Management Helper
  - Regulatory Update Monitor

- **Document Processing**:
  - PDF extraction and analysis
  - OCR for handwritten documents
  - DOCX and text file processing
  - Image analysis

- **Advanced AI Capabilities**:
  - Multiple AI model support via Hugging Face
  - 100+ reasoning protocols (Chain-of-Thought, Tree-of-Thoughts, RAG, etc.)
  - Multi-agent orchestration

- **Professional Features**:
  - Case management with SQLite database
  - Legal document generation
  - Voice cloning and audio processing
  - Analytics and SEO optimization
  - Rotating professional logo display

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Solomon7890-jpeg/Proverbs_Law_MainPage_Official.git
cd Proverbs_Law_MainPage_Official/Proverbs_Law_MainPage_Official
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser to `http://localhost:7860`

### Deploy to Hugging Face Spaces

See the detailed deployment guides in the `Proverbs_Law_MainPage_Official/` directory:
- `START_HERE_DEPLOYMENT.md` - Quick start guide
- `DEPLOYMENT_GUIDE_WITH_LOGOS.md` - Comprehensive deployment instructions

## Requirements

- Python 3.9+
- See `requirements.txt` for full dependency list

## Project Structure

```
Proverbs_Law_MainPage_Official/
├── app.py                              # Main application entry point
├── integrated_chatbot_with_logos.py    # Enhanced chatbot with rotating logos
├── unified_brain.py                    # Core AI reasoning engine
├── agent_orchestrator.py               # Multi-agent orchestration
├── document_processor.py               # Document analysis
├── case_management_module.py           # Case management
├── database_manager.py                 # SQLite database management
├── assets/                             # Professional logos and images
├── utils/                              # Utility modules (OCR, PDF processing)
└── [multiple deployment scripts]       # Various deployment options
```

## Documentation

Comprehensive documentation is available in the `Proverbs_Law_MainPage_Official/` directory, including:
- Deployment guides
- Integration instructions
- Security audit reports
- Browser compatibility information
- Testing documentation

## Technology Stack

- **Framework**: Gradio 6.2.0
- **AI Models**: Hugging Face Transformers, Meta Llama 3.3
- **Document Processing**: PyPDF2, OpenCV, Pytesseract
- **Database**: SQLite
- **Deployment**: Hugging Face Spaces, Docker

## Legal Disclaimer

This platform provides general legal information only and does not constitute legal advice. Always consult with a licensed attorney for specific legal matters.

## License

MIT License - See LICENSE file for details

## Author

Solomon7890

## Links

- [Hugging Face Profile](https://huggingface.co/Solomon7890)
- [GitHub Profile](https://github.com/Solomon7890-jpeg)

---

**Pro'VerBs™** | Built with advanced AI for legal professionals worldwide
