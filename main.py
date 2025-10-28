#!/usr/bin/env python3
"""
🏛️ LEGAL AI ASSISTANT - API SERVER ONLY
Pure API server without CLI
"""

import os
import sys
import uvicorn
from typing import List, Dict, Any, Optional
import time
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from document_processor import AdvancedDocumentProcessor, SmartLegalChunker
    from vector_store import VectorStore
    from rag_pipeline import LegalAIPipeline
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure all modules are in the src/ directory")
    sys.exit(1)

class LegalAIAssistant:
    """
    🏛️ LEGAL AI ASSISTANT - Core System
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.upload_dir = os.path.join(data_dir, "uploaded_docs")
        self.vector_db_dir = os.path.join(data_dir, "vector_db")
        
        # Create directories
        os.makedirs(self.upload_dir, exist_ok=True)
        os.makedirs(self.vector_db_dir, exist_ok=True)
        
        # Initialize components
        self.document_processor = AdvancedDocumentProcessor()
        self.chunker = SmartLegalChunker()
        self.vector_store = VectorStore()
        self.rag_pipeline = None
        
        self.loaded_documents = []
        self.questions_answered = 0
        self.is_ready = False
        
        print("🏛️" + "="*60)
        print("           LEGAL AI ASSISTANT - API Server")
        print("="*60)
        print("✅ System Initialized!")
        print("💡 Ready to accept API requests")
        print("📁 Data Directory:", self.data_dir)
    
    def load_document(self, file_path: str) -> Dict[str, Any]:
        """Load and process a legal document"""
        print(f"📄 Processing: {os.path.basename(file_path)}")
        
        try:
            # Step 1: Read document
            text_content = self.document_processor.load_document(file_path)
            
            # Step 2: Chunk document
            chunks = self.chunker.smart_chunking(text_content)
            
            # Step 3: Create embeddings
            self.vector_store.create_embeddings(chunks)
            
            # Step 4: Initialize RAG pipeline
            self.rag_pipeline = LegalAIPipeline(self.vector_store)
            
            # Store document info
            doc_info = {
                'document_id': str(uuid.uuid4()),
                'filename': os.path.basename(file_path),
                'chunks_count': len(chunks),
                'file_size': os.path.getsize(file_path),
                'file_path': file_path,
                'loaded_at': time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.loaded_documents.append(doc_info)
            self.is_ready = True
            
            print(f"✅ Document loaded: {len(chunks)} chunks")
            
            return {
                'success': True,
                'document': doc_info,
                'chunks_count': len(chunks)
            }
            
        except Exception as e:
            print(f"❌ Error loading document: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def ask_question(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        """Ask a legal question about the loaded documents"""
        if not self.is_ready:
            return {
                'success': False,
                'error': "No documents loaded. Please load a legal document first.",
                'answer': "Please load a legal document before asking questions."
            }
        
        print(f"\n🎯 LEGAL QUESTION: {question}")
        
        try:
            result = self.rag_pipeline.answer_question(question, top_k=top_k)
            self.questions_answered += 1
            
            # Ensure all values are JSON serializable
            response = {
                'success': True,
                'question': question,
                'answer': result['answer'],
                'sources': result['sources'],
                'confidence': float(result['confidence']),  # Convert numpy to Python float
                'performance': result['performance']
            }
            
            # Convert all numpy types in performance metrics
            for key in response['performance']:
                if isinstance(response['performance'][key], (np.float32, np.float64)):
                    response['performance'][key] = float(response['performance'][key])
            
            # Convert all numpy types in sources
            for source in response['sources']:
                if 'relevance_score' in source:
                    source['relevance_score'] = float(source['relevance_score'])
            
            return response
            
        except Exception as e:
            print(f"❌ Error processing question: {e}")
            return {
                'success': False,
                'error': str(e),
                'answer': "I encountered an error processing your question. Please try again."
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and statistics"""
        return {
            'system_ready': self.is_ready,
            'loaded_documents': self.loaded_documents,
            'llm_available': self.rag_pipeline.llm_available if self.rag_pipeline else False,
            'vector_db_size': self.vector_store.index.ntotal if hasattr(self.vector_store, 'index') and self.vector_store.index else 0,
            'total_questions_answered': self.questions_answered,
        }
    
    def clear_documents(self):
        """Clear all loaded documents and reset the system"""
        print("🗑️ Clearing all documents...")
        
        for doc in self.loaded_documents:
            if os.path.exists(doc['file_path']):
                os.remove(doc['file_path'])
        
        self.loaded_documents = []
        self.is_ready = False
        self.questions_answered = 0
        self.vector_store = VectorStore()
        self.rag_pipeline = None
        
        print("✅ All documents cleared")

# Initialize the assistant
assistant = LegalAIAssistant()

# FastAPI Models
class QuestionRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class QuestionResponse(BaseModel):
    success: bool
    answer: str
    confidence: float
    sources: List[dict]
    performance: dict
    error: Optional[str] = None

class DocumentResponse(BaseModel):
    success: bool
    document_id: str
    filename: str
    chunks_count: int
    message: str
    error: Optional[str] = None

class SystemStatus(BaseModel):
    system_ready: bool
    loaded_documents: List[dict]
    llm_available: bool
    vector_db_size: int
    total_questions_answered: int

# Create FastAPI app
app = FastAPI(
    title="Legal AI Assistant API",
    description="AI-powered Legal Document Q&A System",
    version="1.0.0"
)

# CORS middleware - FIXED
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173", 
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
@app.get("/")
async def root():
    return {
        "message": "🏛️ Legal AI Assistant API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /status": "System status",
            "POST /upload": "Upload legal document",
            "POST /ask": "Ask legal question",
            "GET /documents": "List loaded documents",
            "DELETE /documents": "Clear all documents"
        }
    }

@app.get("/status", response_model=SystemStatus)
async def get_status():
    status = assistant.get_system_status()
    return SystemStatus(**status)

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.txt', '.doc'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not supported. Use: {', '.join(allowed_extensions)}"
        )
    
    file_path = None
    try:
        # Save uploaded file
        file_id = str(uuid.uuid4())
        file_path = os.path.join(assistant.upload_dir, f"{file_id}{file_ext}")
        
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Process document
        result = assistant.load_document(file_path)
        
        if result['success']:
            return DocumentResponse(
                success=True,
                document_id=result['document']['document_id'],
                filename=result['document']['filename'],
                chunks_count=result['chunks_count'],
                message=f"Document processed successfully. Created {result['chunks_count']} semantic chunks."
            )
        else:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=500, detail=result.get('error', 'Processing failed'))
            
    except Exception as e:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    result = assistant.ask_question(request.question, request.top_k)
    
    # Convert NumPy types to Python native types for serialization
    if result['success']:
        # Convert confidence (numpy.float32) to Python float
        result['confidence'] = float(result['confidence'])
        
        # Convert all numpy types in sources
        for source in result['sources']:
            if 'relevance_score' in source:
                source['relevance_score'] = float(source['relevance_score'])
        
        # Convert all numpy types in performance
        for key in result['performance']:
            if isinstance(result['performance'][key], (np.float32, np.float64)):
                result['performance'][key] = float(result['performance'][key])
    
    return QuestionResponse(**result)

@app.get("/documents")
async def list_documents():
    return {
        "success": True,
        "documents": assistant.loaded_documents,
        "total_documents": len(assistant.loaded_documents)
    }

@app.delete("/documents")
async def clear_documents():
    assistant.clear_documents()
    return {
        "success": True,
        "message": "All documents cleared and system reset."
    }

@app.get("/health")
async def health_check():
    status = assistant.get_system_status()
    return {
        "status": "healthy",
        "llm_available": status['llm_available'],
        "documents_loaded": len(status['loaded_documents']),
        "system_ready": status['system_ready']
    }

if __name__ == "__main__":
    print("🚀 Starting Legal AI Assistant API Server...")
    print("🌐 Server: http://127.0.0.1:8000")
    print("📚 Docs: http://127.0.0.1:8000/docs")
    print("🔧 CORS enabled for frontend development")
    print("=" * 50)
    
    # Start the server directly
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")