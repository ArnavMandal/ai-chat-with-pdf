from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline import rag_pipeline
from vector_store import vector_store
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chat with PDF API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    answer: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF file"""
    try:
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Read file content
        content = await file.read()
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Process PDF
        chunk_count = rag_pipeline.process_pdf(content)
        
        logger.info(f"Successfully processed PDF: {file.filename}, {chunk_count} chunks")
        
        return {
            "message": f"PDF processed successfully. Created {chunk_count} chunks.",
            "filename": file.filename,
            "chunks": chunk_count
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded PDF"""
    try:
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        answer = rag_pipeline.query_pdf(request.question)
        
        logger.info(f"Question: {request.question[:50]}...")
        
        return QuestionResponse(answer=answer)
    
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.delete("/clear")
async def clear_database():
    """Clear the vector database"""
    vector_store.clear()
    return {"message": "Database cleared successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)