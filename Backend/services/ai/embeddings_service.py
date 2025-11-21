"""
Embeddings Service
Handles text embeddings for semantic similarity matching
"""

from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Dict
import numpy as np
from config.ai_config import ai_settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingsService:
    """Service for generating and comparing text embeddings"""
    
    def __init__(self):
        """Initialize the embeddings model"""
        try:
            self.model = SentenceTransformer(
                ai_settings.embeddings_model,
                cache_folder=ai_settings.hf_model_cache_dir
            )
            self.model.to(ai_settings.device)
            logger.info(f"Embeddings model loaded: {ai_settings.embeddings_model}")
        except Exception as e:
            logger.error(f"Failed to load embeddings model: {e}")
            raise
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text string
            
        Returns:
            numpy array of embeddings
        """
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            raise
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of text strings
            
        Returns:
            numpy array of embeddings (shape: [num_texts, embedding_dim])
        """
        try:
            embeddings = self.model.encode(
                texts, 
                convert_to_numpy=True,
                show_progress_bar=len(texts) > 10
            )
            return embeddings
        except Exception as e:
            logger.error(f"Error encoding batch: {e}")
            raise
    
    def cosine_similarity(
        self, 
        embedding1: np.ndarray, 
        embedding2: np.ndarray
    ) -> float:
        """
        Calculate cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Similarity score between 0 and 1
        """
        # Normalize vectors
        embedding1 = embedding1 / np.linalg.norm(embedding1)
        embedding2 = embedding2 / np.linalg.norm(embedding2)
        
        # Calculate cosine similarity
        similarity = np.dot(embedding1, embedding2)
        return float(similarity)
    
    def find_most_similar(
        self,
        query_text: str,
        candidate_texts: List[str],
        top_k: int = 5
    ) -> List[Tuple[int, str, float]]:
        """
        Find most similar texts to query
        
        Args:
            query_text: Query text
            candidate_texts: List of candidate texts to compare
            top_k: Number of top results to return
            
        Returns:
            List of tuples (index, text, similarity_score)
        """
        # Generate embeddings
        query_embedding = self.encode_text(query_text)
        candidate_embeddings = self.encode_batch(candidate_texts)
        
        # Calculate similarities
        similarities = []
        for idx, candidate_emb in enumerate(candidate_embeddings):
            similarity = self.cosine_similarity(query_embedding, candidate_emb)
            similarities.append((idx, candidate_texts[idx], similarity))
        
        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[2], reverse=True)
        
        return similarities[:top_k]
    
    def semantic_search(
        self,
        query: str,
        documents: List[Dict[str, any]],
        document_field: str = "text",
        top_k: int = 5
    ) -> List[Dict[str, any]]:
        """
        Perform semantic search on documents
        
        Args:
            query: Search query
            documents: List of document dictionaries
            document_field: Field name containing text to search
            top_k: Number of results to return
            
        Returns:
            List of documents with similarity scores
        """
        # Extract texts from documents
        texts = [doc.get(document_field, "") for doc in documents]
        
        # Find similar texts
        similar = self.find_most_similar(query, texts, top_k)
        
        # Return documents with scores
        results = []
        for idx, text, score in similar:
            doc_with_score = documents[idx].copy()
            doc_with_score['similarity_score'] = score
            doc_with_score['rank'] = len(results) + 1
            results.append(doc_with_score)
        
        return results
    
    def match_skills_to_roles(
        self,
        user_skills: List[str],
        roles: List[Dict[str, any]],
        role_skills_field: str = "required_skills"
    ) -> List[Dict[str, any]]:
        """
        Match user skills to suitable roles using semantic similarity
        
        Args:
            user_skills: List of user's skills
            roles: List of role dictionaries with required skills
            role_skills_field: Field containing list of required skills
            
        Returns:
            List of roles with match scores
        """
        # Create skill profile text
        user_profile = " ".join(user_skills)
        user_embedding = self.encode_text(user_profile)
        
        # Calculate match for each role
        role_matches = []
        for role in roles:
            required_skills = role.get(role_skills_field, [])
            role_profile = " ".join(required_skills)
            role_embedding = self.encode_text(role_profile)
            
            # Calculate similarity
            match_score = self.cosine_similarity(user_embedding, role_embedding)
            
            # Calculate skill overlap
            matched_skills = set(user_skills) & set(required_skills)
            missing_skills = set(required_skills) - set(user_skills)
            
            role_with_match = role.copy()
            role_with_match['match_score'] = float(match_score)
            role_with_match['matched_skills'] = list(matched_skills)
            role_with_match['missing_skills'] = list(missing_skills)
            role_with_match['coverage_percentage'] = (
                len(matched_skills) / len(required_skills) * 100 
                if required_skills else 0
            )
            
            role_matches.append(role_with_match)
        
        # Sort by match score
        role_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return role_matches
    
    def cluster_similar_skills(
        self,
        skills: List[str],
        similarity_threshold: float = 0.8
    ) -> List[List[str]]:
        """
        Cluster similar skills together
        
        Args:
            skills: List of skill names
            similarity_threshold: Threshold for considering skills similar
            
        Returns:
            List of skill clusters
        """
        if not skills:
            return []
        
        # Generate embeddings
        embeddings = self.encode_batch(skills)
        
        # Simple clustering by similarity threshold
        clusters = []
        used = set()
        
        for i, skill_i in enumerate(skills):
            if i in used:
                continue
            
            cluster = [skill_i]
            used.add(i)
            
            for j, skill_j in enumerate(skills):
                if j <= i or j in used:
                    continue
                
                similarity = self.cosine_similarity(embeddings[i], embeddings[j])
                if similarity >= similarity_threshold:
                    cluster.append(skill_j)
                    used.add(j)
            
            clusters.append(cluster)
        
        return clusters
    
    def expand_skill_query(
        self,
        skill: str,
        skill_database: List[str],
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Find related skills to expand a skill query
        
        Args:
            skill: Skill to expand
            skill_database: Database of all skills
            top_k: Number of related skills to return
            
        Returns:
            List of (skill, similarity) tuples
        """
        similar = self.find_most_similar(skill, skill_database, top_k + 1)
        
        # Remove the skill itself if it's in the results
        related_skills = [
            (text, score) for idx, text, score in similar 
            if text.lower() != skill.lower()
        ][:top_k]
        
        return related_skills


# Global instance
_embeddings_service_instance = None


def get_embeddings_service() -> EmbeddingsService:
    """Get singleton instance of EmbeddingsService"""
    global _embeddings_service_instance
    if _embeddings_service_instance is None:
        _embeddings_service_instance = EmbeddingsService()
    return _embeddings_service_instance

