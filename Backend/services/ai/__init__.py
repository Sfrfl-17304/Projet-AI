"""
AI Services Module for SkillAtlas

This module contains all AI/ML services including:
- Skill extraction from CVs
- RAG-based chat assistant
- Embeddings and semantic matching
- LLM-based career recommendations
"""

from .skill_extractor import SkillExtractor
# from .rag_service import RAGService  # Temporarily disabled - needs langchain.chains
from .embeddings_service import EmbeddingsService
# from .llm_service import LLMService  # Temporarily disabled - needs langchain.prompts

__all__ = [
    "SkillExtractor",
    # "RAGService",
    "EmbeddingsService",
    # "LLMService"
]

