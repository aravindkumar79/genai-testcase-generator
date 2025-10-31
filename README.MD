# 🤖 AI-Powered Test Case Generation POC

🚀 **An end-to-end Proof of Concept that automatically converts business requirements into executable Cucumber test scenarios using Generative AI**

---

## 📋 Overview

This POC demonstrates how AI can revolutionize software testing by automatically generating comprehensive test cases from business requirements documents.  
The system processes PDF requirements, understands domain context, and produces ready-to-execute Cucumber BDD scenarios.

---

## 🎯 Key Features

- **📄 PDF Processing** – Extracts requirements from PDF documents with OCR support for images and diagrams  
- **🤖 Multi-Model AI** – Supports local LLMs (Ollama)  
- **🔍 Semantic Search** – Uses ChromaDB vector database for context-aware test generation  
- **🔄 Domain Agnostic** – Works across financial, healthcare, and e-commerce domains without retraining  
- **✅ BDD Ready** – Generates executable Cucumber Gherkin syntax with proper Given/When/Then structure  
- **📊 Quality Scoring** – Automatically evaluates requirement testability and generates appropriate test coverage  

---

## 🏗️ Architecture

```
Business Requirements (PDF)
            ↓
PDF Processor (OCR + Text Extraction)
            ↓
Requirement Classification & Scoring
            ↓
Vector Store (ChromaDB) ← Semantic Search
            ↓
AI Test Generation (Ollama / Flan-T5)
            ↓
Cucumber Feature Files (.feature)
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) (for local LLM support)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

### Clone Repository
```bash
git clone https://github.com/yourusername/genai-testcase-generator.git
cd genai-testcase-generator
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral:7b
```

### Install Tesseract OCR
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract
```

---

## 📁 Project Structure

```
genai-testcase-generator/
├── pdf_processor.py          # PDF extraction & OCR
├── vector_store.py           # ChromaDB semantic search
├── cucumber_generator.py     # Ollama test generation
├── requirements.txt          # Python dependencies
├── extracted_requirements/   # Processed requirements
├── generated_features/       # Output Cucumber files
└── chroma_db/                # Vector database
```

---

## ⚡ Quick Start

### 1. Process Your Requirements PDF
```python
from pdf_processor import DomainAgnosticPDFProcessor

processor = DomainAgnosticPDFProcessor("your_requirements.pdf")
requirements = processor.process_pdf_with_workflows()
processor.save_requirements("extracted_requirements.json")
```

### 2. Generate Test Cases with Ollama
```python
from cucumber_generator import CucumberTestGenerator
from vector_store import RequirementVectorStore

vector_store = RequirementVectorStore()
vector_store.add_requirements(requirements)

generator = CucumberTestGenerator(vector_store)
results = generator.generate_all_tests(requirements)
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM support  
- [ChromaDB](https://www.trychroma.com) for vector database  
- [PyMuPDF](https://pymupdf.readthedocs.io/) for PDF processing  
