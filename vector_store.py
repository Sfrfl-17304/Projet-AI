"""
Vector Store Manager - Handle embeddings and similarity search
"""
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from mongodb_manager import mongo
import numpy as np

class VectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize with a sentence transformer model"""
        self.model = SentenceTransformer(model_name, device='cpu')
        self.collection = mongo.get_collection("documents")
        print(f"Loaded embedding model: {model_name}")
    
    def add_documents(self, documents: List[dict]):
        """Add documents with embeddings to MongoDB"""
        for doc in documents:
            # Generate embedding
            embedding = self.model.encode(doc["text"]).tolist()
            
            # Store in MongoDB
            doc_with_embedding = {
                "text": doc["text"],
                "metadata": doc.get("metadata", {}),
                "source": doc.get("source", ""),
                "embedding": embedding
            }
            
            self.collection.insert_one(doc_with_embedding)
        
        print(f"✓ Added {len(documents)} documents to vector store")
    
    def similarity_search(self, query: str, k: int = 4) -> List[dict]:
        """Find most similar documents to query"""
        # Generate query embedding
        query_embedding = self.model.encode(query)
        
        # Get all documents (for simple cosine similarity)
        # In production, use MongoDB Atlas Vector Search
        all_docs = list(self.collection.find())
        
        # Calculate cosine similarity
        similarities = []
        for doc in all_docs:
            doc_embedding = np.array(doc["embedding"])
            similarity = np.dot(query_embedding, doc_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
            )
            similarities.append((similarity, doc))
        
        # Sort by similarity and return top k
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        results = []
        for similarity, doc in similarities[:k]:
            results.append({
                "text": doc["text"],
                "metadata": doc.get("metadata", {}),
                "source": doc.get("source", ""),
                "similarity": float(similarity)
            })
        
        return results
    
    def clear(self):
        """Clear all documents from the collection"""
        self.collection.delete_many({})
        print("✓ Cleared vector store")
