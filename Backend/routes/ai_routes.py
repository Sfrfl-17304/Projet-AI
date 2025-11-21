"""
AI Routes - Comprehensive AI endpoints for SkillAtlas
Integrates skill extraction, career recommendations, skill gap analysis, 
roadmap generation, and chat assistant
"""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status, Body
from routes.auth import get_current_user
from models.user import User
from models.ai_models import (
    SkillExtractionRequest, SkillExtractionResponse,
    InterestQuestionnaire, CareerRecommendationResponse,
    SkillGapRequest, SkillGapResponse,
    RoadmapRequest, RoadmapResponse,
    ChatRequest, ChatResponse,
    SemanticMatchRequest, SemanticMatchResponse,
    RoleMatchRequest, RoleMatchResponse,
    AddKnowledgeRequest, AddKnowledgeResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse
)
from services.ai.skill_extractor import get_skill_extractor
from services.ai.embeddings_service import get_embeddings_service
from services.ai.llm_service import get_llm_service
from services.ai.rag_service import get_rag_service
import PyPDF2
import io
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["AI Services"])


# --- Skill Extraction Endpoints ---

@router.post("/extract-skills", response_model=SkillExtractionResponse)
async def extract_skills_from_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Extract skills from uploaded CV using NLP/NER models
    
    Supports:
    - PDF files (.pdf)
    - Text files (.txt)
    
    Returns categorized skills with proficiency levels
    """
    try:
        # Validate file type
        if file.content_type not in ["application/pdf", "text/plain"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF and TXT files are supported"
            )
        
        # Read file content
        content = await file.read()
        
        # Extract text based on file type
        if file.content_type == "application/pdf":
            try:
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                cv_text = ""
                for page in pdf_reader.pages:
                    cv_text += page.extract_text() + "\n"
            except Exception as e:
                logger.error(f"PDF extraction error: {e}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to extract text from PDF. Please ensure it's not password protected or corrupted."
                )
        else:
            cv_text = content.decode('utf-8')
        
        if not cv_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text content found in the file"
            )
        
        # Extract skills using AI service
        skill_extractor = get_skill_extractor()
        result = skill_extractor.extract_from_text(cv_text)
        
        logger.info(f"Extracted {result['total_count']} skills for user {current_user.email}")
        
        return SkillExtractionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Skill extraction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting skills: {str(e)}"
        )


@router.post("/extract-skills-text", response_model=SkillExtractionResponse)
async def extract_skills_from_text(
    request: SkillExtractionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Extract skills from CV text (alternative to file upload)
    
    Provide either:
    - cv_text: Full CV as text
    - cv_sections: Dictionary with section names and text
    """
    try:
        skill_extractor = get_skill_extractor()
        
        if request.cv_sections:
            result = skill_extractor.extract_from_sections(request.cv_sections)
        elif request.cv_text:
            result = skill_extractor.extract_from_text(request.cv_text)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either cv_text or cv_sections must be provided"
            )
        
        return SkillExtractionResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Skill extraction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error extracting skills: {str(e)}"
        )


# --- Career Recommendation Endpoints ---

@router.post("/recommend-careers", response_model=CareerRecommendationResponse)
async def recommend_careers(
    questionnaire: InterestQuestionnaire,
    current_user: User = Depends(get_current_user)
):
    """
    Get personalized career recommendations based on interests and background
    
    For beginners without a CV - analyzes interests, strengths, and goals
    to suggest suitable career paths
    """
    try:
        llm_service = get_llm_service()
        
        # Prepare user profile
        user_profile = {
            "interests": questionnaire.interests,
            "strengths": questionnaire.strengths,
            "education": questionnaire.education,
            "experience_level": questionnaire.experience_level,
            "goals": questionnaire.goals
        }
        
        # Get recommendations from LLM
        recommendations = llm_service.recommend_careers(user_profile, num_recommendations=5)
        
        logger.info(f"Generated {len(recommendations)} career recommendations for {current_user.email}")
        
        return CareerRecommendationResponse(recommendations=recommendations)
    
    except Exception as e:
        logger.error(f"Career recommendation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating recommendations: {str(e)}"
        )


# --- Skill Gap Analysis Endpoints ---

@router.post("/skill-gap-analysis", response_model=SkillGapResponse)
async def analyze_skill_gap(
    request: SkillGapRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Analyze skill gap between current skills and target role requirements
    
    Identifies:
    - Skills you already have
    - Skills you're missing
    - Priority order for learning
    - Estimated time to acquire missing skills
    """
    try:
        llm_service = get_llm_service()
        
        # Mock required skills for target role (in production, fetch from Neo4j)
        required_skills_db = {
            "Data Engineer": ["Python", "SQL", "Apache Spark", "Airflow", "Docker", 
                            "AWS", "ETL", "Data Modeling", "Kafka"],
            "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning",
                           "Docker", "MLOps", "AWS", "Git", "SQL"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python",
                                    "SQL", "MongoDB", "Docker", "Git", "REST APIs"],
            "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript",
                                  "Vue.js", "Git", "Responsive Design"],
            "Backend Developer": ["Python", "Node.js", "SQL", "MongoDB", "REST APIs",
                                 "Docker", "Git", "Microservices"]
        }
        
        required_skills = required_skills_db.get(
            request.target_role,
            ["Python", "SQL", "Git", "Docker"]  # default
        )
        
        # Analyze gap
        analysis = llm_service.analyze_skill_gap(
            request.current_skills,
            request.target_role,
            required_skills
        )
        
        logger.info(f"Skill gap analysis for {current_user.email}: {analysis['gap_percentage']:.1f}% gap")
        
        return SkillGapResponse(**analysis)
    
    except Exception as e:
        logger.error(f"Skill gap analysis error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing skill gap: {str(e)}"
        )


# --- Learning Roadmap Endpoints ---

@router.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_learning_roadmap(
    request: RoadmapRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Generate personalized learning roadmap
    
    Creates a structured, time-aware learning plan with:
    - Learning phases (Foundation, Intermediate, Advanced)
    - Skills to learn in each phase
    - Time estimates
    - Recommended resources and projects
    """
    try:
        llm_service = get_llm_service()
        
        # First, analyze skill gap to get missing skills
        required_skills_db = {
            "Data Engineer": ["Python", "SQL", "Apache Spark", "Airflow", "Docker", 
                            "AWS", "ETL", "Data Modeling", "Kafka"],
            "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Machine Learning",
                           "Docker", "MLOps", "AWS", "Git", "SQL"],
            "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python",
                                    "SQL", "MongoDB", "Docker", "Git", "REST APIs"],
            "Frontend Developer": ["JavaScript", "React", "HTML", "CSS", "TypeScript",
                                  "Vue.js", "Git", "Responsive Design"],
            "Backend Developer": ["Python", "Node.js", "SQL", "MongoDB", "REST APIs",
                                 "Docker", "Git", "Microservices"]
        }
        
        required_skills = required_skills_db.get(request.target_role, [])
        current_skills_lower = [s.lower() for s in request.current_skills]
        missing_skills = [s for s in required_skills if s.lower() not in current_skills_lower]
        
        # Generate roadmap
        roadmap = llm_service.generate_learning_roadmap(
            request.current_skills,
            request.target_role,
            missing_skills,
            request.timeline
        )
        
        # Calculate estimated hours
        estimated_hours = request.hours_per_week * 26  # Rough estimate for 6 months
        
        response = RoadmapResponse(
            timeline=roadmap["timeline"],
            phases=roadmap.get("phases", []),
            total_skills=len(missing_skills),
            estimated_hours=estimated_hours,
            roadmap_text=roadmap["roadmap"]
        )
        
        logger.info(f"Generated roadmap for {current_user.email} - {request.target_role}")
        
        return response
    
    except Exception as e:
        logger.error(f"Roadmap generation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating roadmap: {str(e)}"
        )


# --- Chat Assistant Endpoints ---

@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Chat with AI career advisor assistant
    
    RAG-based chat that provides grounded, reliable answers about:
    - Career paths and roles
    - Skill requirements
    - Learning paths
    - Career transitions
    - Industry insights
    """
    try:
        rag_service = get_rag_service()
        
        # Get answer from RAG
        result = rag_service.ask_question(
            request.question,
            request.conversation_history
        )
        
        logger.info(f"Chat query from {current_user.email}: {request.question[:50]}...")
        
        return ChatResponse(**result)
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )


# --- Semantic Matching Endpoints ---

@router.post("/semantic-match", response_model=SemanticMatchResponse)
async def semantic_match(
    request: SemanticMatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Find semantically similar texts using embeddings
    
    Useful for:
    - Finding similar skills
    - Matching job descriptions
    - Comparing career paths
    """
    try:
        embeddings_service = get_embeddings_service()
        
        similar = embeddings_service.find_most_similar(
            request.query,
            request.candidates,
            request.top_k
        )
        
        results = [
            {"text": text, "similarity_score": float(score), "rank": idx + 1}
            for idx, (_, text, score) in enumerate(similar)
        ]
        
        return SemanticMatchResponse(query=request.query, results=results)
    
    except Exception as e:
        logger.error(f"Semantic matching error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in semantic matching: {str(e)}"
        )


@router.post("/match-roles", response_model=RoleMatchResponse)
async def match_user_to_roles(
    request: RoleMatchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Match user skills to suitable career roles using semantic similarity
    
    Returns ranked list of roles with match scores and skill coverage
    """
    try:
        embeddings_service = get_embeddings_service()
        
        # Mock role database (in production, fetch from Neo4j)
        roles = [
            {
                "role": "Data Engineer",
                "required_skills": ["Python", "SQL", "Apache Spark", "Airflow", "Docker", "AWS"],
                "description": "Build and maintain data pipelines"
            },
            {
                "role": "ML Engineer",
                "required_skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Docker"],
                "description": "Develop and deploy ML models"
            },
            {
                "role": "Full Stack Developer",
                "required_skills": ["JavaScript", "React", "Node.js", "Python", "SQL", "MongoDB"],
                "description": "Build full-stack web applications"
            },
            {
                "role": "Frontend Developer",
                "required_skills": ["JavaScript", "React", "HTML", "CSS", "TypeScript"],
                "description": "Create user interfaces"
            },
            {
                "role": "Backend Developer",
                "required_skills": ["Python", "Node.js", "SQL", "MongoDB", "REST APIs"],
                "description": "Build server-side logic"
            }
        ]
        
        # Match skills to roles
        matches = embeddings_service.match_skills_to_roles(
            request.user_skills,
            roles,
            role_skills_field="required_skills"
        )
        
        logger.info(f"Matched {len(matches)} roles for {current_user.email}")
        
        return RoleMatchResponse(matches=matches, user_skills=request.user_skills)
    
    except Exception as e:
        logger.error(f"Role matching error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error matching roles: {str(e)}"
        )


# --- Knowledge Base Management Endpoints ---

@router.post("/knowledge/add", response_model=AddKnowledgeResponse)
async def add_to_knowledge_base(
    request: AddKnowledgeRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Add documents to the knowledge base
    
    Requires admin privileges (to be implemented)
    """
    try:
        rag_service = get_rag_service()
        
        documents = [
            {
                "content": doc.content,
                "metadata": doc.metadata or {}
            }
            for doc in request.documents
        ]
        
        count = rag_service.add_documents(documents, chunk=request.chunk)
        
        logger.info(f"Added {count} documents to knowledge base by {current_user.email}")
        
        return AddKnowledgeResponse(
            documents_added=count,
            status="success" if count > 0 else "failed"
        )
    
    except Exception as e:
        logger.error(f"Knowledge base add error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding to knowledge base: {str(e)}"
        )


@router.post("/knowledge/search", response_model=KnowledgeSearchResponse)
async def search_knowledge_base(
    request: KnowledgeSearchRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Search the knowledge base for relevant information
    """
    try:
        rag_service = get_rag_service()
        
        results = rag_service.search_knowledge_base(
            request.query,
            request.top_k,
            request.filter_metadata
        )
        
        return KnowledgeSearchResponse(results=results, query=request.query)
    
    except Exception as e:
        logger.error(f"Knowledge search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching knowledge base: {str(e)}"
        )


@router.get("/knowledge/stats")
async def get_knowledge_base_stats(
    current_user: User = Depends(get_current_user)
):
    """Get statistics about the knowledge base"""
    try:
        rag_service = get_rag_service()
        stats = rag_service.get_knowledge_base_stats()
        return stats
    except Exception as e:
        logger.error(f"Knowledge stats error: {e}")
        return {"status": "error", "message": str(e)}

