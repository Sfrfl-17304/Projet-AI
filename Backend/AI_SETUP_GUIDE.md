# SkillAtlas AI Module - Quick Setup Guide

Complete guide to setting up and running the AI services for SkillAtlas.

## 📦 Prerequisites

- Python 3.9+
- 8GB RAM minimum (16GB recommended for local LLMs)
- Optional: NVIDIA GPU with CUDA for faster processing
- MongoDB running (for user data)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

This will install:
- LangChain & LangChain Community
- HuggingFace Transformers
- Sentence Transformers
- PyTorch
- ChromaDB (vector database)
- PDF processing libraries

**Note**: First installation may take 5-10 minutes due to large packages.

### Step 2: Configure Environment

Create a `.env` file in the `Backend` directory:

```env
# Database
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=skillatlas

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
AI_HUGGINGFACE_API_KEY=  # Optional, leave empty for local models
AI_HF_MODEL_CACHE_DIR=./models/cache
AI_CHROMA_PERSIST_DIRECTORY=./data/chroma_db
AI_SKILLS_TAXONOMY_PATH=./data/skills_taxonomy.json

# LLM Settings
AI_LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
AI_USE_LOCAL_LLM=False  # Set to True if you have 16GB+ RAM and want local models
AI_LLM_TEMPERATURE=0.7
AI_LLM_MAX_TOKENS=1024

# Embeddings
AI_EMBEDDINGS_MODEL=sentence-transformers/all-MiniLM-L6-v2
AI_EMBEDDINGS_DIMENSION=384

# Skill Extraction
AI_SKILL_EXTRACTION_MODEL=dslim/bert-base-NER

# RAG Settings
AI_RETRIEVAL_TOP_K=5
AI_CHUNK_SIZE=1000
AI_CHUNK_OVERLAP=200

# Device Configuration
AI_DEVICE=cpu  # Options: cpu, cuda (NVIDIA GPU), mps (Apple Silicon)

# Server
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

### Step 3: Create Required Directories

```bash
cd Backend
mkdir -p models/cache
mkdir -p data/chroma_db
```

### Step 4: Start the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Verify AI Services

Visit the interactive API docs: **http://localhost:8000/docs**

Test the AI endpoints:
1. Sign up and login to get an auth token
2. Try `/ai/knowledge/stats` to verify RAG service is initialized
3. Try `/ai/chat` with a simple question

## 🧪 Testing AI Endpoints

### 1. Test Skill Extraction

```bash
# Create a test CV file
echo "I am a Python developer with experience in FastAPI, React, MongoDB, and Docker. 
I have worked with machine learning using TensorFlow and scikit-learn." > test_cv.txt

# Upload and extract skills
curl -X POST "http://localhost:8000/ai/extract-skills" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@test_cv.txt"
```

**Expected Response:**
```json
{
  "skills": {
    "programming_languages": [
      {"name": "Python", "proficiency": "intermediate", "mentions": 1}
    ],
    "frameworks": [
      {"name": "FastAPI", "proficiency": "beginner", "mentions": 1},
      {"name": "React", "proficiency": "beginner", "mentions": 1},
      {"name": "TensorFlow", "proficiency": "beginner", "mentions": 1}
    ],
    ...
  },
  "total_count": 7,
  "categories": ["programming_languages", "frameworks", "databases", "tools"]
}
```

### 2. Test Career Recommendations

```bash
curl -X POST "http://localhost:8000/ai/recommend-careers" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "interests": ["Data Analysis", "Programming", "Problem Solving"],
    "strengths": ["Analytical Thinking", "Mathematics"],
    "education": "Computer Science Bachelor",
    "experience_level": "beginner",
    "goals": "Work with data and machine learning"
  }'
```

### 3. Test Skill Gap Analysis

```bash
curl -X POST "http://localhost:8000/ai/skill-gap-analysis" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "SQL", "Git"],
    "target_role": "Data Engineer"
  }'
```

### 4. Test Chat Assistant

```bash
curl -X POST "http://localhost:8000/ai/chat" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What skills do I need to become a Machine Learning Engineer?",
    "conversation_history": []
  }'
```

### 5. Test Learning Roadmap

```bash
curl -X POST "http://localhost:8000/ai/generate-roadmap" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_skills": ["Python", "SQL"],
    "target_role": "Data Engineer",
    "timeline": "6 months",
    "hours_per_week": 15
  }'
```

## 🔧 Configuration Options

### Option 1: Use HuggingFace API (Recommended for Development)

**Pros:**
- Lower resource usage
- No need for powerful hardware
- Faster startup

**Cons:**
- Requires internet connection
- API rate limits
- Small cost per request

**Setup:**
1. Get API key from https://huggingface.co/settings/tokens
2. Set in `.env`:
```env
AI_USE_LOCAL_LLM=False
AI_HUGGINGFACE_API_KEY=hf_your_api_key_here
```

### Option 2: Use Local Models (Recommended for Production)

**Pros:**
- No API costs
- Better privacy
- No rate limits

**Cons:**
- Requires 16GB+ RAM
- Slower first run (model downloads)
- Takes disk space (5-10GB)

**Setup:**
```env
AI_USE_LOCAL_LLM=True
AI_DEVICE=cpu  # or cuda if you have GPU
```

### Option 3: Hybrid Approach

Use local embeddings but API for LLM:
```env
AI_USE_LOCAL_LLM=False  # Use API for LLM
# Embeddings are always local (lightweight)
```

## 📊 Performance Benchmarks

### Model Download Times (First Run)
- Skill Extraction Model: ~500MB, 2-3 minutes
- Embeddings Model: ~80MB, 30-60 seconds
- LLM (if local): ~5GB, 10-15 minutes

### API Response Times
- Skill Extraction: 1-3 seconds
- Chat Assistant: 2-5 seconds
- Career Recommendations: 3-7 seconds
- Semantic Matching: 0.5-1 second

### Resource Usage
- CPU Mode: 2-4GB RAM
- With Local LLM: 8-16GB RAM
- GPU Mode: 4-8GB VRAM

## 🐛 Common Issues & Solutions

### Issue 1: "Module not found" errors

**Solution:**
```bash
pip install --upgrade -r requirements.txt
```

### Issue 2: Models downloading slowly

**Solution:**
```bash
# Use mirror (if in China or slow regions)
export HF_ENDPOINT=https://hf-mirror.com
```

### Issue 3: Out of memory with local LLM

**Solution:**
Switch to API mode:
```env
AI_USE_LOCAL_LLM=False
```

Or use a smaller model:
```env
AI_LLM_MODEL_NAME=facebook/opt-1.3b
```

### Issue 4: ChromaDB persistence errors

**Solution:**
```bash
# Clear and reinitialize
rm -rf data/chroma_db
# Restart server - will recreate knowledge base
```

### Issue 5: Skill extraction not finding skills

**Solution:**
The skill taxonomy is in `config/ai_config.py`. Add your specific skills:

```python
SKILL_CATEGORIES = {
    "programming_languages": [
        # Add more languages
        "Python", "JavaScript", "TypeScript", "Go", "Rust"
    ],
    # ... add more categories
}
```

## 📝 Development Tips

### 1. Testing AI Services Locally

Create a test script `test_ai.py`:

```python
from services.ai import get_skill_extractor, get_rag_service

# Test skill extraction
extractor = get_skill_extractor()
result = extractor.extract_from_text("I know Python and React")
print(f"Extracted: {result['raw_skills']}")

# Test chat
rag = get_rag_service()
response = rag.ask_question("What is a Data Engineer?")
print(f"Answer: {response['answer']}")
```

Run:
```bash
python test_ai.py
```

### 2. Monitoring AI Performance

Enable logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### 3. Updating the Knowledge Base

Add new career information via API:

```python
import requests

documents = [
    {
        "content": "DevOps Engineer: Focuses on automation, CI/CD, and infrastructure...",
        "metadata": {"category": "role_description", "role": "DevOps Engineer"}
    }
]

response = requests.post(
    "http://localhost:8000/ai/knowledge/add",
    headers={"Authorization": f"Bearer {token}"},
    json={"documents": documents, "chunk": True}
)
```

## 🎓 Next Steps

1. ✅ Verify all AI services are working
2. ✅ Test each endpoint with real data
3. ⬜ Integrate with Neo4j for knowledge graph
4. ⬜ Add more career documents to knowledge base
5. ⬜ Fine-tune models on your specific domain
6. ⬜ Set up monitoring and logging
7. ⬜ Deploy to production

## 📚 Additional Resources

- **LangChain**: https://python.langchain.com/docs/get_started
- **HuggingFace**: https://huggingface.co/docs
- **Sentence Transformers**: https://www.sbert.net/
- **ChromaDB**: https://docs.trychroma.com/

## 🆘 Getting Help

1. Check logs: `tail -f logs/app.log`
2. Review API docs: http://localhost:8000/docs
3. Check AI service README: `services/ai/README.md`
4. GitHub Issues: [Create issue if public repo]

## ✅ Verification Checklist

- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] MongoDB running and accessible
- [ ] Server starts without errors
- [ ] Can access API docs at /docs
- [ ] Can login and get auth token
- [ ] Skill extraction endpoint works
- [ ] Chat assistant responds
- [ ] Career recommendations work
- [ ] Knowledge base initialized

If all checked, you're ready to go! 🚀

