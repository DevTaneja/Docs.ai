from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import uuid
from typing import List, Optional
import json

# Import our system
from document_processor import AdvancedDocumentProcessor, SmartLegalChunker
from vector_store import VectorStore
from rag_pipeline import LegalAIPipeline

# Initialize FastAPI
app = FastAPI(
    title="Legal AI Assistant API",
    description="AI-powered Legal Document Q&A System",
    version="1.0.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global system instance
legal_ai_system = None
UPLOAD_DIR = "data/uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Pydantic models for request/response
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
    total_questions_answered: int = 0

# Initialize the system
def initialize_system():
    global legal_ai_system
    if legal_ai_system is None:
        legal_ai_system = {
            'document_processor': AdvancedDocumentProcessor(),
            'chunker': SmartLegalChunker(),
            'vector_store': VectorStore(),
            'rag_pipeline': None,
            'loaded_documents': [],
            'questions_answered': 0,
            'is_ready': False
        }
    return legal_ai_system

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
    """Get system status and statistics"""
    system = initialize_system()
    
    return SystemStatus(
        system_ready=system['is_ready'],
        loaded_documents=system['loaded_documents'],
        llm_available=system['rag_pipeline'].llm_available if system['rag_pipeline'] else False,
        vector_db_size=system['vector_store'].index.ntotal if hasattr(system['vector_store'], 'index') and system['vector_store'].index else 0,
        total_questions_answered=system['questions_answered']
    )

@app.post("/upload", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a legal document"""
    system = initialize_system()
    
    # Validate file type
    allowed_extensions = {'.pdf', '.docx', '.txt', '.doc'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not supported. Use: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")
        
        # Save uploaded file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
        
        print(f"📄 Processing: {file.filename}")
        
        # Process document
        text_content = system['document_processor'].load_document(file_path)
        chunks = system['chunker'].smart_chunking(text_content)
        system['vector_store'].create_embeddings(chunks)
        system['rag_pipeline'] = LegalAIPipeline(system['vector_store'])
        
        # Store document info
        doc_info = {
            'document_id': file_id,
            'filename': file.filename,
            'chunks_count': len(chunks),
            'file_size': len(contents),
            'file_path': file_path,
            'uploaded_at': json.dumps(os.path.getctime(file_path))
        }
        system['loaded_documents'].append(doc_info)
        system['is_ready'] = True
        
        return DocumentResponse(
            success=True,
            document_id=file_id,
            filename=file.filename,
            chunks_count=len(chunks),
            message=f"Document processed successfully. Created {len(chunks)} semantic chunks."
        )
        
    except Exception as e:
        # Clean up file if processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a legal question about the loaded documents"""
    system = initialize_system()
    
    if not system['is_ready']:
        return QuestionResponse(
            success=False,
            answer="No documents loaded. Please upload a legal document first.",
            confidence=0.0,
            sources=[],
            error="No documents available"
        )
    
    try:
        result = system['rag_pipeline'].answer_question(
            question=request.question,
            top_k=request.top_k
        )
        
        # Update statistics
        system['questions_answered'] += 1
        
        return QuestionResponse(
            success=True,
            answer=result['answer'],
            confidence=result['confidence'],
            sources=result['sources'],
            performance=result['performance']
        )
        
    except Exception as e:
        return QuestionResponse(
            success=False,
            answer="I encountered an error processing your question.",
            confidence=0.0,
            sources=[],
            error=str(e)
        )

@app.get("/documents")
async def list_documents():
    """List all loaded documents"""
    system = initialize_system()
    
    return {
        "success": True,
        "documents": system['loaded_documents'],
        "total_documents": len(system['loaded_documents'])
    }

@app.delete("/documents")
async def clear_documents():
    """Clear all loaded documents and reset the system"""
    system = initialize_system()
    
    # Clear all uploaded files
    for doc in system['loaded_documents']:
        if os.path.exists(doc['file_path']):
            os.remove(doc['file_path'])
    
    # Reset system
    system['loaded_documents'] = []
    system['is_ready'] = False
    system['vector_store'] = VectorStore()
    system['rag_pipeline'] = None
    system['questions_answered'] = 0
    
    return {
        "success": True,
        "message": "All documents cleared and system reset."
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    system = initialize_system()
    return {
        "status": "healthy",
        "llm_available": system['rag_pipeline'].llm_available if system['rag_pipeline'] else False,
        "documents_loaded": len(system['loaded_documents']),
        "system_ready": system['is_ready']
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Legal AI Assistant API Server...")
    print("📚 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)