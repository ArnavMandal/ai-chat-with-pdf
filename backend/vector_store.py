import faiss
import numpy as np
import pickle
import os
from typing import List, Optional

class VectorStore:
    def __init__(self):
        self.index: Optional[faiss.Index] = None
        self.chunks: List[str] = []
        self.dimension = 1536  # OpenAI embedding dimension
        
    def store_embeddings(self, chunks: List[str], embeddings: List[List[float]]):
        """Store chunks and their embeddings in FAISS index"""
        self.chunks = chunks
        
        # Convert to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Create FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings_array)
        
        print(f"Stored {len(chunks)} chunks in vector database")
    
    def search(self, query_embedding: List[float], k: int = 5) -> List[str]:
        """Search for most similar chunks"""
        if self.index is None:
            return []
        
        query_array = np.array([query_embedding]).astype('float32')
        distances, indices = self.index.search(query_array, k)
        
        # Return the corresponding chunks
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]
    
    def clear(self):
        """Clear the vector store"""
        self.index = None
        self.chunks = []

# Global vector store instance
vector_store = VectorStore()