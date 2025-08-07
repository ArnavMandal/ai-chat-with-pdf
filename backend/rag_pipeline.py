import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai  # Using older openai library (0.28.1)
import os
from dotenv import load_dotenv
from typing import List
from vector_store import vector_store

load_dotenv()

class RAGPipeline:
    def __init__(self):
        # Set the API key directly for older openai versions
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY in your .env file.")
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            full_text = ""
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                full_text += page.get_text()
                full_text += "\n"
            
            doc.close()
            return full_text.strip()
        
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks"""
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for text chunks"""
        try:
            response = openai.Embedding.create(
                input=texts,
                model="text-embedding-ada-002"
            )
            return [item['embedding'] for item in response['data']]
        
        except Exception as e:
            raise Exception(f"Error getting embeddings: {str(e)}")
    
    def process_pdf(self, file_bytes: bytes):
        """Complete PDF processing pipeline"""
        # Extract text
        text = self.extract_text_from_pdf(file_bytes)
        
        if not text.strip():
            raise Exception("No text found in PDF")
        
        # Chunk text
        chunks = self.chunk_text(text)
        
        if not chunks:
            raise Exception("No chunks created from PDF text")
        
        # Get embeddings
        embeddings = self.get_embeddings(chunks)
        
        # Store in vector database
        vector_store.store_embeddings(chunks, embeddings)
        
        return len(chunks)
    
    def query_pdf(self, question: str) -> str:
        """Query the processed PDF"""
        try:
            # Get question embedding
            question_embedding = self.get_embeddings([question])[0]
            
            # Search for relevant chunks
            relevant_chunks = vector_store.search(question_embedding, k=5)
            
            if not relevant_chunks:
                return "I don't have any information to answer this question. Please upload a PDF first."
            
            # Create context from relevant chunks
            context = "\n\n".join(relevant_chunks)
            
            # Create prompt
            prompt = f"""Answer the question based on the following context. If the answer is not in the context, say so.

Context:
{context}

Question: {question}

Answer:"""
            
            # Get response from OpenAI using the older API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            return f"Error processing question: {str(e)}"

# Global RAG pipeline instance  
rag_pipeline = RAGPipeline()