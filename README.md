# Simple RAG System with MongoDB

A minimalist Retrieval-Augmented Generation (RAG) system using MongoDB for document storage and vector similarity search.

## 🚀 Features

- **Document Loading**: Upload PDF and TXT files
- **Vector Embeddings**: Uses Sentence Transformers for efficient embeddings
- **MongoDB Storage**: Stores documents and embeddings in MongoDB
- **RAG Pipeline**: Retrieves relevant context and generates answers
- **Two Interfaces**: 
  - Streamlit web interface
  - Terminal interface

## 📋 Prerequisites

- Python 3.8+
- Docker (for MongoDB)

## 🛠️ Setup

### 1. Start MongoDB

```bash
docker-compose up -d
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Edit `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=rag_db
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for better responses
```

## 🎯 Usage

### Option 1: Streamlit Interface (Recommended)

```bash
streamlit run app.py
```

Then:
1. Upload documents using the sidebar
2. Click "Process Documents"
3. Ask questions in the chat interface

### Option 2: Terminal Interface

```bash
python terminal_app.py
```

Follow the menu:
1. Load documents from a directory
2. Ask questions
3. View database stats
4. Clear database

## 📁 Project Structure

```
.
├── app.py                  # Streamlit interface
├── terminal_app.py         # Terminal interface
├── rag_pipeline.py         # Main RAG logic
├── vector_store.py         # Vector embeddings & search
├── document_loader.py      # Document processing
├── mongodb_manager.py      # MongoDB connection
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # MongoDB setup
└── .env                    # Configuration
```

## 🔧 How It Works

1. **Document Loading**: PDFs and text files are loaded and split into chunks
2. **Embeddings**: Each chunk is converted to a vector embedding using Sentence Transformers
3. **Storage**: Chunks and embeddings are stored in MongoDB
4. **Query**: User questions are embedded and matched against stored documents using cosine similarity
5. **Response**: Retrieved context is used to generate an answer (with or without LLM)

## 💡 Tips

- **Without OpenAI**: The system works without an API key but will return raw context instead of generated answers
- **With OpenAI**: Set `OPENAI_API_KEY` in `.env` for better, more natural responses
- **Performance**: For large datasets, consider MongoDB Atlas Vector Search for faster queries

## 🐛 Troubleshooting

### MongoDB connection failed
```bash
# Check if MongoDB is running
docker ps

# Restart MongoDB
docker-compose restart
```

### Port already in use
```bash
# Stop existing MongoDB
docker-compose down

# Or change port in docker-compose.yml
```

## 🎓 Example Usage

```python
# Quick start example
from rag_pipeline import RAGPipeline
from document_loader import DocumentLoader

# Initialize
loader = DocumentLoader()
rag = RAGPipeline()

# Load documents
chunks = loader.load_pdf("my_document.pdf")
rag.vector_store.add_documents(chunks)

# Query
response = rag.query("What is this document about?")
print(response["answer"])
```

## 📝 License

MIT License - feel free to use and modify as needed!
