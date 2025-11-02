# Docs.ai
LegalDocQA - AI-Powered Legal Document Question Answering System
![](https://img.shields.io/badge/Python-3.8+-blue.svg)
![](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![](https://img.shields.io/badge/React-18+-blue.svg)
## Overview

LegalDocQA is an AI-powered legal assistant that enables users to upload legal documents and ask natural language questions about their content. The system uses Retrieval-Augmented Generation (RAG) to provide accurate, source-grounded answers from contracts, policies, laws, and other legal documents.

## Features

- **Document Upload**: Support for PDF, DOCX, and TXT files
- **Natural Language Q&A**: Ask questions like "What are the termination clauses?"
- **Source Citations**: View exact references to original document sections
- **Legal-Optimized Processing**: Specialized chunking for legal document structures
- **Open Source Models**: Built with freely available language models

## How It Works

LegalDocQA uses a RAG (Retrieval-Augmented Generation) pipeline:

1. **Document Processing**: Extract text from uploaded legal documents
2. **Smart Chunking**: Split documents into semantically meaningful sections
3. **Vector Embeddings**: Convert text to numerical representations using sentence transformers
4. **Similarity Search**: Find relevant document sections using FAISS vector database
5. **Answer Generation**: Generate contextual answers using open-source LLMs
6. **Source Attribution**: Provide citations to original document passages

## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **FastAPI** - Modern web framework for APIs
- **FAISS** - Vector similarity search
- **Hugging Face** - Open-source language models
- **PyMuPDF** - PDF document processing
- **python-docx** - Word document processing

### Frontend
- **React 18** - User interface library
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server

## Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- Git

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/DevTaneja/Docs.ai.git
cd Docsai/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
### Usage
 - Upload Documents: Use the web interface to upload legal documents
 - Ask Questions: Enter natural language questions about the document content
 - Review Answers: Get AI-generated answers with source citations
 - Verify Sources: Click on citations to view original document passages

API Endpoints
API Endpoints
Method	Endpoint	Description
- GET	/	Root endpoint - API information
- GET	/status	Get system status and statistics
- POST	/upload	Upload and process legal document
- POST	/ask	Ask question about uploaded documents
- GET	/documents	List all loaded documents
- DELETE	/documents	Clear all documents and reset system
- GET	/health	Health check endpoint
