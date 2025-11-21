"""
Pydantic models for AI-related requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


# Skill Extraction Models

class SkillExtractionRequest(BaseModel):
    """Request for skill extraction from CV"""
    cv_text: Optional[str] = None
    cv_sections: Optional[Dict[str, str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "cv_text": "Experienced Python developer with React and MongoDB skills..."
            }
        }


class SkillInfo(BaseModel):
    """Information about an extracted skill"""
    name: str
    proficiency: str = Field(default="beginner", description="beginner, intermediate, or expert")
    mentions: int = Field(default=1, description="Number of times mentioned")


class SkillExtractionResponse(BaseModel):
    """Response from skill extraction"""
    skills: Dict[str, List[SkillInfo]]
    total_count: int
    categories: List[str]
    raw_skills: List[str]


# Career Recommendation Models

class InterestQuestionnaire(BaseModel):
    """User responses to interest questions"""
    interests: List[str] = Field(description="Areas of interest")
    strengths: List[str] = Field(description="Personal strengths")
    education: Optional[str] = None
    experience_level: str = Field(default="beginner", description="beginner, intermediate, advanced")
    preferred_work_style: Optional[str] = Field(default=None, description="remote, office, hybrid")
    goals: Optional[str] = None


class CareerRecommendation(BaseModel):
    """A career recommendation"""
    role: str
    match_score: float = Field(ge=0, le=100)
    explanation: str
    key_skills: Optional[List[str]] = None
    average_salary: Optional[str] = None
    growth_potential: Optional[str] = None


class CareerRecommendationResponse(BaseModel):
    """Response with career recommendations"""
    recommendations: List[CareerRecommendation]
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# Skill Gap Analysis Models

class SkillGapRequest(BaseModel):
    """Request for skill gap analysis"""
    current_skills: List[str]
    target_role: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_skills": ["Python", "SQL", "Git"],
                "target_role": "Data Engineer"
            }
        }


class SkillGapResponse(BaseModel):
    """Response from skill gap analysis"""
    current_skills: List[str]
    required_skills: List[str]
    matched_skills: List[str]
    missing_skills: List[str]
    gap_percentage: float
    analysis: str
    priority_skills: List[str]


# Learning Roadmap Models

class RoadmapRequest(BaseModel):
    """Request for learning roadmap generation"""
    current_skills: List[str]
    target_role: str
    timeline: str = Field(default="6 months", description="e.g., 6 months, 1 year")
    hours_per_week: Optional[int] = Field(default=10, ge=1, le=40)
    
    class Config:
        json_schema_extra = {
            "example": {
                "current_skills": ["Python", "SQL"],
                "target_role": "Data Engineer",
                "timeline": "6 months",
                "hours_per_week": 15
            }
        }


class LearningPhase(BaseModel):
    """A phase in the learning roadmap"""
    name: str
    skills: List[str]
    duration: str
    resources: Optional[List[str]] = []
    milestones: Optional[List[str]] = []


class RoadmapResponse(BaseModel):
    """Response with learning roadmap"""
    timeline: str
    phases: List[LearningPhase]
    total_skills: int
    estimated_hours: Optional[int] = None
    roadmap_text: str


# Chat Assistant Models

class ChatMessage(BaseModel):
    """A chat message"""
    role: str = Field(description="user or assistant")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request for chat assistant"""
    question: str
    conversation_history: Optional[List[Dict[str, str]]] = None
    context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional context like user profile, current skills, etc."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What skills do I need to become a Machine Learning Engineer?",
                "conversation_history": []
            }
        }


class ChatSource(BaseModel):
    """Source document for chat response"""
    content: str
    metadata: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Response from chat assistant"""
    answer: str
    sources: List[ChatSource]
    confidence: str = Field(description="high, medium, or low")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Semantic Matching Models

class SemanticMatchRequest(BaseModel):
    """Request for semantic matching"""
    query: str
    candidates: List[str]
    top_k: int = Field(default=5, ge=1, le=20)


class SemanticMatchResult(BaseModel):
    """A semantic match result"""
    text: str
    similarity_score: float
    rank: int


class SemanticMatchResponse(BaseModel):
    """Response from semantic matching"""
    query: str
    results: List[SemanticMatchResult]


# Role Matching Models

class RoleMatchRequest(BaseModel):
    """Request for matching user skills to roles"""
    user_skills: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_skills": ["Python", "TensorFlow", "Machine Learning", "Docker"]
            }
        }


class RoleMatch(BaseModel):
    """A role match result"""
    role: str
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    coverage_percentage: float
    description: Optional[str] = None


class RoleMatchResponse(BaseModel):
    """Response with role matches"""
    matches: List[RoleMatch]
    user_skills: List[str]


# Knowledge Base Models

class KnowledgeDocument(BaseModel):
    """A document for the knowledge base"""
    content: str
    metadata: Optional[Dict[str, str]] = Field(
        default=None,
        description="Metadata like category, role, skill, etc."
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "Python is a versatile programming language...",
                "metadata": {
                    "category": "learning_path",
                    "skill": "Python"
                }
            }
        }


class AddKnowledgeRequest(BaseModel):
    """Request to add documents to knowledge base"""
    documents: List[KnowledgeDocument]
    chunk: bool = Field(default=True, description="Whether to chunk large documents")


class AddKnowledgeResponse(BaseModel):
    """Response from adding knowledge"""
    documents_added: int
    status: str


class KnowledgeSearchRequest(BaseModel):
    """Request to search knowledge base"""
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    filter_metadata: Optional[Dict[str, str]] = None


class KnowledgeSearchResult(BaseModel):
    """A knowledge search result"""
    content: str
    metadata: Optional[Dict[str, Any]] = None
    similarity_score: float


class KnowledgeSearchResponse(BaseModel):
    """Response from knowledge search"""
    results: List[KnowledgeSearchResult]
    query: str

