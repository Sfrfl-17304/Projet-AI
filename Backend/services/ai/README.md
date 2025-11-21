# SkillAtlas AI Module

Comprehensive AI/ML services using LangChain and HuggingFace for career guidance and skill analysis.

## 📋 Table of Contents

- [Overview](#overview)
- [Services](#services)
- [Setup](#setup)
- [Usage Examples](#usage-examples)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The AI module provides four core services:

1. **Skill Extraction** - Extract skills from CVs using NER and pattern matching
2. **Embeddings Service** - Semantic similarity matching for skills and roles
3. **LLM Service** - Career recommendations and roadmap generation
4. **RAG Service** - Chat assistant with grounded knowledge base

## 🛠️ Services

### 1. Skill Extractor (`skill_extractor.py`)

Extracts skills from CV text using:
- HuggingFace NER models (BERT-based)
- Regex pattern matching for known skills
- Context-based extraction
- Proficiency estimation

**Key Features:**
- Multi-method extraction (NER + patterns + context)
- Skill categorization (programming languages, frameworks, tools, etc.)
- Proficiency level estimation (beginner, intermediate, expert)
- Support for structured CV sections

**Models Used:**
- `dslim/bert-base-NER` - Named Entity Recognition
- Custom skill taxonomy with 100+ tech skills

### 2. Embeddings Service (`embeddings_service.py`)

Semantic similarity using sentence transformers:
- Generate embeddings for text
- Find similar skills/roles
- Match user skills to career paths
- Cluster related skills

**Key Features:**
- Fast semantic search
- Batch embedding generation
- Cosine similarity calculations
- Role-skill matching with coverage percentage

**Models Used:**
- `sentence-transformers/all-MiniLM-L6-v2` - 384-dimensional embeddings
- Optimized for semantic similarity

### 3. LLM Service (`llm_service.py`)

Language model integration for intelligent recommendations:
- Career path recommendations
- Skill gap analysis
- Learning roadmap generation
- Interest-based career matching

**Key Features:**
- Support for local and API-based LLMs
- Fallback to rule-based recommendations
- Structured prompt templates
- Context-aware responses

**Models Used:**
- `mistralai/Mistral-7B-Instruct-v0.2` (default)
- Configurable to use GPT, Claude, or other HuggingFace models

### 4. RAG Service (`rag_service.py`)

Retrieval-Augmented Generation for chat assistant:
- Knowledge base with career information
- Vector database (ChromaDB)
- Context-aware question answering
- Source citation

**Key Features:**
- Persistent vector database
- Semantic document retrieval
- Grounded, cited responses
- Dynamic knowledge base updates

**Components:**
- ChromaDB for vector storage
- HuggingFace embeddings
- LangChain retrieval chains
- Initial knowledge base with 12+ career documents

## 🚀 Setup

### 1. Install Dependencies

```bash
cd Backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file (or use `.env.example`):

```env
# AI Configuration
AI_HUGGINGFACE_API_KEY=your_hf_api_key_here  # Optional, for API-based models
AI_HF_MODEL_CACHE_DIR=./models/cache
AI_CHROMA_PERSIST_DIRECTORY=./data/chroma_db

# LLM Settings
AI_LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
AI_USE_LOCAL_LLM=False  # Set True to use local models
AI_LLM_TEMPERATURE=0.7
AI_LLM_MAX_TOKENS=1024

# Device (cpu, cuda, mps)
AI_DEVICE=cpu
```

### 3. Download Models (First Run)

Models will be downloaded automatically on first use. This may take a few minutes.

```bash
# Optional: Pre-download models
python -c "from services.ai import get_skill_extractor; get_skill_extractor()"
```

### 4. Initialize Knowledge Base

The RAG service creates an initial knowledge base on first run. You can add more documents via API.

## 💡 Usage Examples

### Skill Extraction

```python
from services.ai.skill_extractor import get_skill_extractor

extractor = get_skill_extractor()
result = extractor.extract_from_text(cv_text)

print(f"Found {result['total_count']} skills")
print(f"Categories: {result['categories']}")
print(f"Skills by category: {result['skills']}")
```

### Semantic Matching

```python
from services.ai.embeddings_service import get_embeddings_service

embeddings = get_embeddings_service()

# Find similar skills
similar = embeddings.find_most_similar(
    "Python programming",
    ["JavaScript", "Java", "Ruby", "Python development"],
    top_k=3
)

# Match skills to roles
user_skills = ["Python", "TensorFlow", "Docker"]
roles = [...]  # List of role dicts with required_skills
matches = embeddings.match_skills_to_roles(user_skills, roles)
```

### Career Recommendations

```python
from services.ai.llm_service import get_llm_service

llm = get_llm_service()

user_profile = {
    "skills": ["Python", "SQL"],
    "interests": ["Data Analysis", "Machine Learning"],
    "experience_level": "intermediate"
}

recommendations = llm.recommend_careers(user_profile, num_recommendations=5)
```

### Chat Assistant

```python
from services.ai.rag_service import get_rag_service

rag = get_rag_service()

response = rag.ask_question(
    "What skills do I need for a Data Engineer role?",
    conversation_history=[]
)

print(f"Answer: {response['answer']}")
print(f"Sources: {len(response['sources'])}")
```

## 🌐 API Endpoints

All endpoints require authentication (Bearer token).

### Skill Extraction

**POST** `/ai/extract-skills`
- Upload CV file (PDF or TXT)
- Returns categorized skills with proficiency

**POST** `/ai/extract-skills-text`
- Submit CV as text
- Returns categorized skills

### Career Recommendations

**POST** `/ai/recommend-careers`
- Submit interest questionnaire
- Returns 3-5 career recommendations

### Skill Gap Analysis

**POST** `/ai/skill-gap-analysis`
- Provide current skills and target role
- Returns gap analysis with priorities

### Learning Roadmap

**POST** `/ai/generate-roadmap`
- Provide skills, target role, timeline
- Returns structured learning roadmap

### Chat Assistant

**POST** `/ai/chat`
- Ask career-related questions
- Returns grounded answers with sources

### Semantic Matching

**POST** `/ai/semantic-match`
- Find similar texts using embeddings

**POST** `/ai/match-roles`
- Match user skills to suitable roles

### Knowledge Base

**POST** `/ai/knowledge/add`
- Add documents to knowledge base

**POST** `/ai/knowledge/search`
- Search knowledge base

**GET** `/ai/knowledge/stats`
- Get knowledge base statistics

## ⚙️ Configuration

### Model Selection

Edit `config/ai_config.py`:

```python
class AISettings(BaseSettings):
    # Change models here
    skill_extraction_model: str = "dslim/bert-base-NER"
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    llm_model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"
```

### Using Local LLMs

For better privacy and no API costs:

```env
AI_USE_LOCAL_LLM=True
AI_LLM_MODEL_NAME=mistralai/Mistral-7B-Instruct-v0.2
AI_DEVICE=cuda  # Use GPU if available
```

Note: Local models require significant RAM/VRAM (8GB+ recommended).

### Using HuggingFace API

For lower resource usage:

```env
AI_USE_LOCAL_LLM=False
AI_HUGGINGFACE_API_KEY=your_api_key
```

Get API key from: https://huggingface.co/settings/tokens

### GPU Acceleration

If you have NVIDIA GPU with CUDA:

```env
AI_DEVICE=cuda
```

For Apple Silicon:

```env
AI_DEVICE=mps
```

## 🐛 Troubleshooting

### Issue: Models not downloading

**Solution:**
```bash
# Set HuggingFace cache directory
export TRANSFORMERS_CACHE=./models/cache
# Try downloading manually
huggingface-cli download sentence-transformers/all-MiniLM-L6-v2
```

### Issue: Out of memory errors

**Solution:**
- Use smaller models
- Set `AI_USE_LOCAL_LLM=False` to use API
- Reduce batch sizes
- Use CPU instead of GPU if VRAM is limited

### Issue: LLM responses are slow

**Solution:**
- Use API-based models instead of local
- Reduce `AI_LLM_MAX_TOKENS`
- Use smaller, faster models like `facebook/opt-1.3b`

### Issue: Skill extraction not accurate

**Solution:**
- Update skill taxonomy in `config/ai_config.py`
- Add more skills to `SKILL_CATEGORIES`
- Fine-tune NER model on your domain (advanced)

### Issue: RAG returns irrelevant answers

**Solution:**
- Add more documents to knowledge base
- Adjust `retrieval_top_k` in config
- Improve document chunking parameters

## 📊 Performance Tips

1. **First Run**: Model downloads take time, be patient
2. **Caching**: Models are cached, subsequent runs are faster
3. **Batch Processing**: Use batch endpoints for multiple CVs
4. **GPU**: Use CUDA/MPS for 3-5x speedup
5. **API vs Local**: API is slower but uses less resources

## 🔗 Related Documentation

- [Backend README](../../README.md) - Main backend documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [LangChain Docs](https://python.langchain.com/)
- [HuggingFace Docs](https://huggingface.co/docs)

## 📝 License

UIR - 4th Year AI Course Project

## 👥 Contributors

- Oubahmane Mohamed Omar (120119) - AI/NLP and RAG Implementation

