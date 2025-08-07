# 📚 Chat with PDF Notes

A personal RAG (Retrieval-Augmented Generation) application that lets you upload PDF documents and have intelligent conversations with your notes. Built with FastAPI, React, and OpenAI.

## 🎯 Project Background / Motivation

I wanted a way to "talk" to my study notes and documents instead of manually searching through them. This tool uses RAG to intelligently retrieve relevant sections from uploaded PDFs and provides contextual answers to questions about the content.
This allows the LLM to utilize its own information alongside the notes itself.

## ✨ Features

- 📄 **PDF Upload & Processing** - Extract text from any PDF document
- 🔍 **Intelligent Search** - Vector similarity search using FAISS
- 💬 **Natural Conversations** - Chat interface powered by OpenAI GPT-4
- 🧠 **Context-Aware Responses** - Answers are grounded in your document content
- 🎨 **Modern UI** - Clean, responsive interface built with React
- ⚡ **Fast Processing** - Efficient text chunking and embedding storage

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  React Frontend │────│   FastAPI Backend │────│   OpenAI API   │
│                 │    │                  │    │                 │
│ • File Upload   │    │ • PDF Processing │    │ • Embeddings    │
│ • Chat Interface│    │ • Text Chunking  │    │ • Chat Response │
│ • Message History│   │ • Vector Search  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                       ┌────────┴────────┐
                       │ FAISS Vector DB │
                       │                 │
                       │ • Embeddings    │
                       │ • Similarity    │
                       │   Search        │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### Installation

1. **Clone the repository**
   

2. **Backend Setup**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   # Create .env file in backend/
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

4. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

5. **Run the Application**
   
   **Backend** (Terminal 1):
   ```bash
   cd backend
   source venv/bin/activate
   python3 main.py
   ```
   
   **Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```

6. **Access the App**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📖 Usage

1. **Upload a PDF**: Click "Upload PDF" and select your document
2. **Wait for Processing**: The app will extract text, create chunks, and generate embeddings
3. **Start Chatting**: Ask questions about your document content
4. **Get Contextual Answers**: Responses are based on relevant sections from your PDF

### Example Questions
- "What are the main points discussed in this document?"
- "Can you summarize the conclusion?"
- "What does the author say about [specific topic]?"

## 💡 How RAG Works

1. **Document Processing**: PDF text is extracted and split into manageable chunks
2. **Embedding Generation**: Each chunk is converted to a vector representation using OpenAI's embeddings
3. **Vector Storage**: Embeddings are stored in FAISS for fast similarity search
4. **Question Processing**: User questions are embedded using the same model
5. **Relevant Retrieval**: Most similar document chunks are found using vector search
6. **Response Generation**: Retrieved chunks provide context for GPT-4 to generate accurate answers

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyMuPDF** - PDF text extraction
- **LangChain** - Text processing and chunking
- **FAISS** - Vector similarity search
- **OpenAI API** - Embeddings and chat completion

### Frontend
- **React w/ TypeScript** - User interface
- **CSS** - Styling and responsive design
- **Axios** - API communication
- **Lucide React** - Icons

## 📁 Project Structure

```
chat-with-pdf/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── rag_pipeline.py      # RAG processing logic
│   ├── vector_store.py      # FAISS vector database
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main React component
│   │   ├── App.css          # Custom styles
│   │   ├── api.ts           # API client
│   │   └── index.css        # Global styles
│   ├── public/
│   └── package.json         # Node.js dependencies
├── .gitignore
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Customization Options

**Text Chunking** (in `rag_pipeline.py`):
```python
RecursiveCharacterTextSplitter(
    chunk_size=500,        # Adjust chunk size
    chunk_overlap=100,     # Overlap between chunks
    length_function=len,
)
```

**Search Results** (in `rag_pipeline.py`):
```python
relevant_chunks = vector_store.search(question_embedding, k=5)  # Number of chunks to retrieve
```

**OpenAI Model** (in `rag_pipeline.py`):
```python
model="gpt-4",           # Change to gpt-3.5-turbo for lower cost
temperature=0.7,         # Adjust creativity (0.0-2.0)
max_tokens=500          # Maximum response length
```

## 💰 Cost Estimation

OpenAI API usage costs:
- **Text Embeddings**: ~$0.0001 per 1K tokens
- **GPT-4 Responses**: ~$0.03 per 1K tokens
- **Typical Session**: $0.05 - $0.20 per document

## 🔧 Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

**OpenAI API errors**:
- Check your API key in `.env`
- Ensure you have credits in your OpenAI account
- Verify your API key has the required permissions

**CORS errors**:
- Make sure backend is running on port 8000
- Check CORS settings in `main.py`

**PDF processing errors**:
- Ensure PDF contains extractable text (not scanned images)
- Try with a different PDF file

### Performance Tips

- **Large PDFs**: Consider splitting very large documents
- **Memory Usage**: FAISS keeps vectors in memory
- **Response Time**: Fewer retrieved chunks = faster responses

## 🚀 Deployment

### Local Production Build

**Frontend**:
```bash
cd frontend
npm run build
```

**Backend**:
```bash
cd backend
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000
```

### Docker Deployment

Create `Dockerfile` for containerized deployment:

```dockerfile
# Backend
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔮 Future Enhancements

- [ ] **Multiple File Support** - Handle multiple PDFs simultaneously
- [ ] **User Authentication** - Personal document libraries


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


**Happy note-chatting! 📚💬**