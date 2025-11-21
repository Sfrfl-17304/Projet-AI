"""
AI Configuration for SkillAtlas
Manages AI model settings, paths, and parameters
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class AISettings(BaseSettings):
    """AI/ML Configuration Settings"""
    
    # HuggingFace Settings
    huggingface_api_key: Optional[str] = None
    hf_model_cache_dir: str = "./models/cache"
    
    # Skill Extraction Models
    skill_extraction_model: str = "dslim/bert-base-NER"  # For general NER
    skill_bert_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # LLM Settings (Using HuggingFace)
    llm_model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024
    use_local_llm: bool = False  # Set True to use local models
    
    # Embeddings Settings
    embeddings_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embeddings_dimension: int = 384
    
    # RAG Settings
    chroma_persist_directory: str = "./data/chroma_db"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5
    
    # Vector Database
    vector_db_type: str = "chroma"  # Options: chroma, faiss
    
    # Device Configuration
    device: str = "cpu"  # Options: cpu, cuda, mps
    
    # Skills Database (predefined skills for matching)
    skills_taxonomy_path: str = "./data/skills_taxonomy.json"
    
    class Config:
        env_file = ".env"
        env_prefix = "AI_"
        case_sensitive = False


# Global AI settings instance
ai_settings = AISettings()


# Common skill categories for extraction
SKILL_CATEGORIES = {
    "programming_languages": [
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C#", "Go", 
        "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R", "SQL", "Scala"
    ],
    "frameworks": [
        "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI", 
        "Spring Boot", "Node.js", "Express", "Next.js", "TensorFlow",
        "PyTorch", "Scikit-learn", "Keras", "Pandas", "NumPy"
    ],
    "databases": [
        "MongoDB", "PostgreSQL", "MySQL", "Redis", "Cassandra", 
        "Neo4j", "Elasticsearch", "DynamoDB", "Oracle", "SQLite"
    ],
    "cloud_platforms": [
        "AWS", "Azure", "Google Cloud", "Heroku", "DigitalOcean",
        "Firebase", "Netlify", "Vercel"
    ],
    "tools": [
        "Git", "Docker", "Kubernetes", "Jenkins", "GitLab CI", 
        "GitHub Actions", "Terraform", "Ansible", "Jira", "Confluence"
    ],
    "soft_skills": [
        "Leadership", "Communication", "Problem Solving", "Teamwork",
        "Critical Thinking", "Project Management", "Agile", "Scrum"
    ],
    "data_science": [
        "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
        "Data Analysis", "Statistics", "Big Data", "Data Visualization"
    ]
}


# Prompt templates
CAREER_RECOMMENDATION_PROMPT = """
You are an expert career advisor. Based on the following user profile, suggest suitable career paths.

User Profile:
{user_profile}

Provide 3-5 career recommendations with:
1. Role name
2. Match score (0-100)
3. Brief explanation of why it's a good fit
4. Key skills to focus on

Be specific and practical in your recommendations.
"""


SKILL_GAP_ANALYSIS_PROMPT = """
Analyze the skill gap between the user's current skills and the target role requirements.

User's Current Skills:
{current_skills}

Target Role: {target_role}
Required Skills:
{required_skills}

Provide:
1. Missing skills (critical vs nice-to-have)
2. Skills user has but may need to improve
3. Priority order for learning
4. Estimated time to acquire each missing skill (be realistic)
"""


LEARNING_ROADMAP_PROMPT = """
Create a personalized learning roadmap for the user to transition into the target role.

Current Skills: {current_skills}
Target Role: {target_role}
Missing Skills: {missing_skills}
Timeline: {timeline}

Generate a structured roadmap with:
1. Phases (Foundation, Intermediate, Advanced)
2. Skills to learn in each phase
3. Time estimate for each phase
4. Recommended resources (courses, projects, books)
5. Milestones and projects to build

Make it practical and achievable.
"""


INTEREST_ANALYSIS_PROMPT = """
You are a career counselor helping a beginner explore career options.

User's Responses:
{user_responses}

Based on their interests, strengths, and preferences:
1. Identify 3-5 suitable career paths
2. Explain why each career matches their profile
3. Describe what each career involves
4. Suggest first steps to explore each career

Be encouraging and provide actionable guidance.
"""

