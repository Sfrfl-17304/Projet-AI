"""
Document Loader - Load and process documents
"""
import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader

class DocumentLoader:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
    
    def load_pdf(self, file_path: str) -> List[dict]:
        """Load and split PDF document"""
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        return [
            {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
                "source": file_path
            }
            for chunk in chunks
        ]
    
    def load_text(self, file_path: str) -> List[dict]:
        """Load and split text document"""
        loader = TextLoader(file_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        
        return [
            {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
                "source": file_path
            }
            for chunk in chunks
        ]
    
    def load_directory(self, directory_path: str) -> List[dict]:
        """Load all supported documents from a directory"""
        all_chunks = []
        
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            if filename.endswith('.pdf'):
                chunks = self.load_pdf(file_path)
                all_chunks.extend(chunks)
                print(f"✓ Loaded {len(chunks)} chunks from {filename}")
            elif filename.endswith('.txt'):
                chunks = self.load_text(file_path)
                all_chunks.extend(chunks)
                print(f"✓ Loaded {len(chunks)} chunks from {filename}")
        
        return all_chunks
