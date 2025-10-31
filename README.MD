# AI-Powered Test Case Generation POC

🚀 **An end-to-end Proof of Concept that automatically converts business requirements into executable Cucumber test scenarios using Generative AI**

## 📋 Overview

This POC demonstrates how AI can revolutionize software testing by automatically generating comprehensive test cases from business requirements documents. The system processes PDF requirements, understands domain context, and produces ready-to-execute Cucumber BDD scenarios.

## 🎯 Key Features

- **📄 PDF Processing**: Extracts requirements from PDF documents with OCR support for images and diagrams
- **🤖 Multi-Model AI**: Supports both local LLMs (Ollama) and transformer models (Flan-T5)
- **🔍 Semantic Search**: Uses ChromaDB vector database for context-aware test generation
- **🔄 Domain Agnostic**: Works across financial, healthcare, e-commerce domains without retraining
- **✅ BDD Ready**: Generates executable Cucumber Gherkin syntax with proper Given/When/Then structure
- **📊 Quality Scoring**: Automatically evaluates requirement testability and generates appropriate test coverage

## 🏗️ Architecture
Business Requirements (PDF)
↓
PDF Processor (OCR + Text Extraction)
↓
Requirement Classification & Scoring
↓
Vector Store (ChromaDB) ← Semantic Search
↓
AI Test Generation (Ollama/Flan-T5)
↓
Cucumber Feature Files (.feature)

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Ollama (for local LLM support)
- Tesseract OCR

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/ai-test-generation-poc.git
cd ai-test-generation-poc

2. Install Dependencies
pip install -r requirements.txt


3. Setup Ollama (Optional - for local LLM)
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Mistral model
ollama pull mistral:7b

4. Install Tesseract OCR

Mac: brew install tesseract
Ubuntu: sudo apt-get install tesseract-ocr
Windows: Download from UB-Mannheim/tesseract

5.Project Structure
genai-testcase-generator/
├── pdf_processor.py          # PDF extraction & OCR
├── vector_store.py           # ChromaDB semantic search
├── cucumber_generator.py     # Ollama test generation
├── requirements.txt          # Python dependencies
├── extracted_requirements/   # Processed requirements
├── generated_features/       # Output Cucumber files
└── chroma_db/               # Vector database
