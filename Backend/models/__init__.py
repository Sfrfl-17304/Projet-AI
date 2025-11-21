from .user import User, UserInDB, UserCreate, UserLogin, Token, TokenData
from .ai_models import (
    SkillExtractionRequest, SkillExtractionResponse, SkillInfo,
    InterestQuestionnaire, CareerRecommendation, CareerRecommendationResponse,
    SkillGapRequest, SkillGapResponse,
    RoadmapRequest, RoadmapResponse, LearningPhase,
    ChatRequest, ChatResponse, ChatMessage, ChatSource,
    SemanticMatchRequest, SemanticMatchResponse, SemanticMatchResult,
    RoleMatchRequest, RoleMatchResponse, RoleMatch,
    KnowledgeDocument, AddKnowledgeRequest, AddKnowledgeResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse, KnowledgeSearchResult
)

__all__ = [
    # User models
    "User", "UserInDB", "UserCreate", "UserLogin", "Token", "TokenData",
    # AI models
    "SkillExtractionRequest", "SkillExtractionResponse", "SkillInfo",
    "InterestQuestionnaire", "CareerRecommendation", "CareerRecommendationResponse",
    "SkillGapRequest", "SkillGapResponse",
    "RoadmapRequest", "RoadmapResponse", "LearningPhase",
    "ChatRequest", "ChatResponse", "ChatMessage", "ChatSource",
    "SemanticMatchRequest", "SemanticMatchResponse", "SemanticMatchResult",
    "RoleMatchRequest", "RoleMatchResponse", "RoleMatch",
    "KnowledgeDocument", "AddKnowledgeRequest", "AddKnowledgeResponse",
    "KnowledgeSearchRequest", "KnowledgeSearchResponse", "KnowledgeSearchResult"
]
