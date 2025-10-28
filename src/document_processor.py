import os
import re
from typing import List, Dict, Any

# Professional PDF processing - preserves layout and tables
import pdfplumber

# Professional Word document processing  
from docx import Document

# Advanced text splitting - understands document structure
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Better sentence splitting - understands abbreviations, etc.
import nltk
from nltk.tokenize import sent_tokenize

# Download NLTK data for sentence splitting (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

class AdvancedDocumentProcessor:
    """
    🚀 UPGRADED DOCUMENT PROCESSOR
    Uses professional libraries but keeps code readable and understandable
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        WHAT EACH LIBRARY DOES:
        - pdfplumber: Reads PDFs with layout preservation (unlike pypdf which loses tables)
        - python-docx: Reads Word documents (same as before, but better than basic text)
        - langchain: Professional text splitting that understands document structure
        - nltk: Smart sentence splitting (knows "Dr." isn't end of sentence)
        """
        self.supported_formats = ['.pdf', '.docx', '.txt']
        
        # Initialize professional text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\nSECTION",    # Legal sections first (priority)
                "\nSECTION",      # Sections without double newline
                "\nArticle",      # Articles  
                "\nCLAUSE",       # Clauses
                "\n\n",           # Paragraph breaks
                "\n",             # Line breaks
                ". ",             # Sentences
                "! ", 
                "? ",
                " ",              # Words (last resort)
            ],
            length_function=len,
        )
        
        print("🚀 Advanced Document Processor Ready!")
        print("   - PDFs: pdfplumber (preserves tables & layout)")
        print("   - Splitting: langchain (understands document structure)")
        print("   - Sentences: nltk (knows abbreviations like 'Dr.')")
    
    def load_document(self, file_path: str) -> str:
        """
        Load document using improved libraries
        SIMPLE ALTERNATIVE: Use pypdf instead of pdfplumber (but lose tables)
        """
        print(f"🔍 Loading: {file_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ File not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in self.supported_formats:
            raise ValueError(f"❌ Unsupported format: {file_ext}")
        
        if file_ext == '.pdf':
            return self._read_pdf_advanced(file_path)
        elif file_ext == '.docx':
            return self._read_docx(file_path)
        elif file_ext == '.txt':
            return self._read_txt(file_path)
    
    def _read_pdf_advanced(self, file_path: str) -> str:
        """
        📄 PDF READING WITH pdfplumber
        WHAT IT DOES: Preserves layout, extracts tables, handles columns
        SIMPLE ALTERNATIVE: pypdf (basic text only, loses tables)
        """
        print("📖 Reading PDF with pdfplumber (preserves tables & layout)...")
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text with layout preservation
                    page_text = page.extract_text() or ""
                    
                    # EXCLUSIVE FEATURE: Extract tables (pypdf can't do this!)
                    tables = page.extract_tables()
                    if tables:
                        page_text += "\n\n--- EXTRACTED TABLES ---"
                        for table_num, table in enumerate(tables, 1):
                            page_text += f"\nTable {table_num}:"
                            for row in table:
                                # Clean and join table cells
                                clean_row = [str(cell).strip() if cell else "" for cell in row]
                                table_row = " | ".join(clean_row)
                                page_text += f"\n  {table_row}"
                    
                    text += f"\n\n--- Page {page_num} ---\n{page_text}"
            
            print(f"✅ PDF extracted with {len(pdf.pages)} pages (tables preserved)")
            return text
            
        except Exception as e:
            print(f"❌ PDF reading failed: {e}")
            # Fallback to simple text extraction
            return self._read_pdf_simple(file_path)
    
    def _read_pdf_simple(self, file_path: str) -> str:
        """
        🆘 FALLBACK PDF READER (if pdfplumber fails)
        Uses basic pypdf - loses tables but gets text
        """
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            text = ""
            for page_num, page in enumerate(reader.pages, 1):
                text += f"\n\n--- Page {page_num} ---\n{page.extract_text()}"
            print("📖 Used fallback PDF reader (no tables)")
            return text
        except Exception as e:
            raise Exception(f"PDF reading failed completely: {e}")
    
    def _read_docx(self, file_path: str) -> str:
        """
        📝 WORD DOCUMENT READING  
        WHAT IT DOES: Preserves paragraph structure
        SIMPLE ALTERNATIVE: Basic text reading (loses formatting)
        """
        print("📖 Reading Word document...")
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():  # Skip empty paragraphs
                    text += paragraph.text + "\n"
            print("✅ Word document extracted with paragraph structure")
            return text
        except Exception as e:
            print(f"❌ DOCX reading failed: {e}")
            raise
    
    def _read_txt(self, file_path: str) -> str:
        """Read plain text files"""
        print("📖 Reading text file...")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            print("✅ Text file loaded")
            return text
        except Exception as e:
            print(f"❌ Text reading failed: {e}")
            raise

class SmartLegalChunker:
    """
    ✂️ SMART CHUNKING WITH PROFESSIONAL LIBRARIES
    Uses langchain for structure-aware splitting + nltk for sentence detection
    """
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Professional text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\nSECTION", "\nSECTION", "\nArticle", "\nCLAUSE",  # Legal structure
                "\n\n", "\n",  # Paragraphs and lines  
                ". ", "! ", "? ",  # Sentences
                " ",  # Words
            ],
            length_function=len,
        )
        
        print("✂️ Smart Legal Chunker Ready!")
        print("   - Uses langchain for structure-aware splitting")
        print("   - Falls back to nltk for sentence detection")
    
    def smart_chunking(self, text: str) -> List[Dict[str, Any]]:
        """
        SMART CHUNKING STRATEGY:
        1. First try: Remove TOC and use langchain's professional splitting
        2. Fallback: Use nltk sentence tokenizer if langchain fails
        3. Last resort: Simple regex splitting
        """
        print("🔍 Analyzing document with professional chunking...")
        
        # Step 1: Clean the text
        cleaned_text = self._clean_document_text(text)
        
        # Step 2: Try professional splitting first
        try:
            chunks = self._split_with_langchain(cleaned_text)
            if len(chunks) > 1:
                print(f"✅ Langchain created {len(chunks)} structure-aware chunks")
                return chunks
        except Exception as e:
            print(f"⚠️ Langchain splitting failed, using fallback: {e}")
        
        # Step 3: Fallback to nltk sentence splitting
        chunks = self._split_with_nltk(cleaned_text)
        print(f"✅ NLTK created {len(chunks)} sentence-based chunks")
        
        return chunks
    
    def _clean_document_text(self, text: str) -> str:
        """Remove Table of Contents and other noisy elements"""
        cleaned_text = text
        
        # Remove Table of Contents
        toc_patterns = [
            r'TABLE OF CONTENTS[\s\S]{1,3000}?(?=\n\s*[A-Z0-9])',
            r'CONTENTS[\s\S]{1,3000}?(?=\n\s*[A-Z0-9])',
            r'INDEX[\s\S]{1,3000}?(?=\n\s*[A-Z0-9])',
        ]
        
        for pattern in toc_patterns:
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE)
        
        # Remove page numbers like "..........15" or "- 15 -"
        cleaned_text = re.sub(r'\.{4,}\d+', '', cleaned_text)
        cleaned_text = re.sub(r'\-\s*\d+\s*\-', '', cleaned_text)
        
        return cleaned_text
    
    def _split_with_langchain(self, text: str) -> List[Dict[str, Any]]:
        """Use langchain's professional text splitting"""
        chunk_texts = self.text_splitter.split_text(text)
        
        chunks = []
        for i, chunk_text in enumerate(chunk_texts):
            if self._is_meaningful_chunk(chunk_text):
                chunks.append({
                    'text': chunk_text.strip(),
                    'chunk_id': i,
                    'type': 'langchain_split',
                    'metadata': {
                        'word_count': len(chunk_text.split()),
                        'char_count': len(chunk_text),
                        'split_method': 'langchain'
                    }
                })
        
        return chunks
    
    def _split_with_nltk(self, text: str) -> List[Dict[str, Any]]:
        """Fallback: Use nltk for sentence-aware splitting"""
        try:
            # Use nltk for proper sentence splitting
            sentences = sent_tokenize(text)
        except:
            # Ultimate fallback: simple regex
            sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        chunk_id = 0
        
        for sentence in sentences:
            if len(current_chunk + sentence) > self.chunk_size and current_chunk:
                chunks.append({
                    'text': current_chunk.strip(),
                    'chunk_id': chunk_id,
                    'type': 'sentence_based',
                    'metadata': {
                        'word_count': len(current_chunk.split()),
                        'split_method': 'nltk_fallback'
                    }
                })
                chunk_id += 1
                # Keep overlap for context
                words = current_chunk.split()
                overlap_words = words[-self.chunk_overlap//4:] if len(words) > self.chunk_overlap//4 else words
                current_chunk = " ".join(overlap_words) + " " + sentence
            else:
                current_chunk += " " + sentence
        
        if current_chunk.strip():
            chunks.append({
                'text': current_chunk.strip(),
                'chunk_id': chunk_id,
                'type': 'sentence_based',
                'metadata': {
                    'word_count': len(current_chunk.split()),
                    'split_method': 'nltk_fallback'
                }
            })
        
        return chunks
    
    def _is_meaningful_chunk(self, text: str, min_words: int = 8) -> bool:
        """Check if chunk has actual content"""
        words = text.split()
        if len(words) < min_words:
            return False
        
        # Check if it's mostly special characters or numbers
        alpha_chars = sum(1 for char in text if char.isalpha())
        if alpha_chars < len(text) * 0.4:  # Less than 40% letters
            return False
        
        return True
    
    def print_chunk_analysis(self, chunks: List[Dict[str, Any]]):
        """Analyze and display chunking results"""
        print(f"\n📊 CHUNKING ANALYSIS:")
        print(f"Total chunks: {len(chunks)}")
        
        if not chunks:
            print("❌ No chunks created!")
            return
        
        # Calculate statistics
        total_words = sum(chunk['metadata']['word_count'] for chunk in chunks)
        avg_words = total_words / len(chunks)
        
        # Group by type
        chunk_types = {}
        split_methods = {}
        
        for chunk in chunks:
            chunk_type = chunk['type']
            split_method = chunk['metadata'].get('split_method', 'unknown')
            
            chunk_types[chunk_type] = chunk_types.get(chunk_type, 0) + 1
            split_methods[split_method] = split_methods.get(split_method, 0) + 1
        
        print(f"Average words per chunk: {avg_words:.1f}")
        print(f"Chunk types: {chunk_types}")
        print(f"Split methods: {split_methods}")
        
        # Show sample chunks
        print(f"\n📄 SAMPLE CHUNKS:")
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            preview = chunk['text'][:150] + "..." if len(chunk['text']) > 150 else chunk['text']
            print(f"  Chunk {i}: [{chunk['type']}] {preview}")

# Test the upgraded processor
if __name__ == "__main__":
    print("🧪 TESTING UPGRADED DOCUMENT PROCESSOR")
    print("=" * 50)
    
    # Create processors
    processor = AdvancedDocumentProcessor()
    chunker = SmartLegalChunker()
    
    # Test with sample legal text
    sample_text = """
    TABLE OF CONTENTS
    
    SECTION 1: Definitions..................1
    SECTION 2: Termination..................3  
    SECTION 3: Compensation.................5
    
    EMPLOYMENT AGREEMENT
    
    SECTION 1: DEFINITIONS
    
    1.1 "Employee" means John Doe, residing at 123 Main Street.
    1.2 "Company" means ABC Corporation, a Delaware entity.
    1.3 "Effective Date" means January 1, 2024.
    
    SECTION 2: TERMINATION
    
    2.1 Either party may terminate this Agreement by providing thirty (30) days written notice.
    2.2 The Company may terminate immediately for cause, including but not limited to: fraud, misconduct, or violation of company policies.
    2.3 Upon termination, the Employee shall return all company property.
    
    COMPENSATION SCHEDULE
    
    Position      Base Salary     Bonus Potential
    Developer     $100,000        Up to 15%
    Manager       $150,000        Up to 20%
    """
    
    print("📝 Processing sample legal document...")
    chunks = chunker.smart_chunking(sample_text)
    chunker.print_chunk_analysis(chunks)
    
    print("\n🎯 UPGRADE SUMMARY:")
    print("✅ pdfplumber: Will preserve tables in real PDFs")
    print("✅ langchain: Professional structure-aware splitting") 
    print("✅ nltk: Smart sentence detection (knows 'Dr.' etc.)")
    print("✅ TOC removal: Prevents useless chunks")
    print("✅ Fallback system: Always produces reasonable chunks")