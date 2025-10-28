import os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import json

class VectorStore:
    """
    🧠 BRAIN OF OUR AI SYSTEM
    Turns text into numbers and enables lightning-fast semantic search
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        WHAT EACH COMPONENT DOES:
        - SentenceTransformer: Turns text into number vectors (embeddings)
        - FAISS: Vector database for ultra-fast similarity search
        - Metadata: Remembers which chunk came from which document
        """
        print("🚀 Initializing Vector Store...")
        
        # Load embedding model - converts text → numbers
        self.embedding_model = SentenceTransformer(model_name)
        print(f"✅ Loaded embedding model: {model_name}")
        
        # Initialize FAISS index (our vector database)
        self.index = None
        self.chunks_data = []  # Store original text + metadata
        self.is_trained = False
        
    def create_embeddings(self, chunks: List[Dict[str, Any]]) -> None:
        """
        Convert text chunks into number vectors
        SIMPLE ANALOGY: Like creating a "numerical fingerprint" for each chunk
        """
        print("🔢 Creating embeddings from text chunks...")
        
        if not chunks:
            raise ValueError("❌ No chunks provided for embedding")
        
        # Extract text from chunks
        texts = [chunk['text'] for chunk in chunks]
        
        # MAGIC HAPPENS HERE: Convert text → numbers
        embeddings = self.embedding_model.encode(texts)
        
        print(f"✅ Created {len(embeddings)} embeddings")
        print(f"📊 Each embedding has {embeddings.shape[1]} dimensions")
        
        # Store chunks metadata
        self.chunks_data = chunks
        
        # Create FAISS index for fast searching
        self._create_faiss_index(embeddings)
        
    def _create_faiss_index(self, embeddings: np.ndarray) -> None:
        """
        Create FAISS vector database for lightning-fast similarity search
        SIMPLE ANALOGY: Like creating a super-fast library catalog system
        """
        print("🗄️ Creating FAISS vector database...")
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Create FAISS index - L2 distance for similarity search
        dimension = embeddings_array.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        
        # Add embeddings to index
        self.index.add(embeddings_array)
        
        self.is_trained = True
        print(f"✅ FAISS index created with {self.index.ntotal} vectors")
        
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Find most similar chunks to user's question
        SIMPLE ANALOGY: Like finding books with similar topics in a library
        """
        if not self.is_trained:
            raise ValueError("❌ Vector store not initialized. Call create_embeddings first.")
        
        print(f"🔍 Searching for: '{query}'")
        
        # Convert query to embedding (same process as chunks)
        query_embedding = self.embedding_model.encode([query])
        query_vector = np.array(query_embedding).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_vector, top_k)
        
        # Get matching chunks
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.chunks_data):  # Safety check
                chunk = self.chunks_data[idx]
                results.append({
                    'chunk': chunk,
                    'similarity_score': 1 / (1 + distance),  # Convert distance to similarity
                    'rank': i + 1
                })
        
        print(f"✅ Found {len(results)} relevant chunks")
        return results
    
    def save_index(self, save_path: str) -> None:
        """Save vector database to disk"""
        if not self.is_trained:
            raise ValueError("❌ No index to save")
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f"{save_path}.faiss")
        
        # Save chunks metadata
        with open(f"{save_path}_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(self.chunks_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved vector database to: {save_path}")
    
    def load_index(self, load_path: str) -> None:
        """Load vector database from disk"""
        # Load FAISS index
        self.index = faiss.read_index(f"{load_path}.faiss")
        
        # Load chunks metadata
        with open(f"{load_path}_metadata.json", 'r', encoding='utf-8') as f:
            self.chunks_data = json.load(f)
        
        self.is_trained = True
        print(f"📂 Loaded vector database from: {load_path}")
        print(f"📊 Index contains {self.index.ntotal} vectors")

# Test our vector store
if __name__ == "__main__":
    print("🧪 TESTING VECTOR STORE SYSTEM")
    print("=" * 50)
    
    # Sample chunks (from our document processor)
    sample_chunks = [
        {
            'text': 'SECTION 1: DEFINITIONS 1.1 Employee means John Smith. 1.2 Company means TechCorp Inc.',
            'chunk_id': 0,
            'type': 'legal_section',
            'metadata': {'word_count': 15}
        },
        {
            'text': 'SECTION 2: COMPENSATION 2.1 Salary: $120,000 annually. 2.2 Bonus: Up to 15% based on performance.',
            'chunk_id': 1, 
            'type': 'legal_section',
            'metadata': {'word_count': 18}
        },
        {
            'text': 'SECTION 3: TERMINATION 3.1 Either party may terminate with 30 days written notice. 3.2 Immediate termination for cause.',
            'chunk_id': 2,
            'type': 'legal_section', 
            'metadata': {'word_count': 20}
        }
    ]
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Create embeddings
    vector_store.create_embeddings(sample_chunks)
    
    # Test searches
    test_queries = [
        "What are the termination conditions?",
        "How much is the salary?",
        "Who is the employee?"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        results = vector_store.search(query, top_k=2)
        
        for result in results:
            chunk = result['chunk']
            print(f"   📄 Rank {result['rank']} (Score: {result['similarity_score']:.3f}): {chunk['text'][:80]}...")