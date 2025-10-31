# AI-Powered Test Case Generation POC

🚀 **An end-to-end Proof of Concept that automatically converts business requirements into executable Cucumber test scenarios using Generative AI**

## 📋 Overview

This POC demonstrates how AI can revolutionize software testing by automatically generating comprehensive test cases from business requirements documents. The system processes PDF requirements, understands domain context, and produces ready-to-execute Cucumber BDD scenarios.

## 🎯 Key Features

- **📄 PDF Processing**: Extracts requirements from PDF documents with OCR support for images and diagrams
- **🤖 Multi-Model AI**: Supports local LLMs (Ollama)
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

## Clone Repository
git clone https://github.com/yourusername/genai-testcase-generator.git
cd genai-testcase-generator

## Install Dependencies
pip install -r requirements.txt
