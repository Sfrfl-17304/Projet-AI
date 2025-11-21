"""
Skill Extraction Service
Extracts skills from CVs using HuggingFace NER models and pattern matching
"""

from transformers import (
    AutoTokenizer, 
    AutoModelForTokenClassification, 
    pipeline
)
from typing import List, Dict, Set, Optional
import re
from config.ai_config import ai_settings, SKILL_CATEGORIES
import logging

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract skills from CV text using NLP and pattern matching"""
    
    def __init__(self):
        """Initialize the skill extractor with models"""
        self.device = ai_settings.device
        self.skill_categories = SKILL_CATEGORIES
        
        # Initialize NER pipeline for general entity extraction
        try:
            self.ner_pipeline = pipeline(
                "ner",
                model=ai_settings.skill_extraction_model,
                tokenizer=ai_settings.skill_extraction_model,
                aggregation_strategy="simple",
                device=self.device
            )
            logger.info(f"NER model loaded: {ai_settings.skill_extraction_model}")
        except Exception as e:
            logger.warning(f"Could not load NER model: {e}. Using pattern matching only.")
            self.ner_pipeline = None
        
        # Build skill patterns for regex matching
        self._build_skill_patterns()
    
    def _build_skill_patterns(self):
        """Build regex patterns for all known skills"""
        all_skills = []
        for category, skills in self.skill_categories.items():
            all_skills.extend(skills)
        
        # Create case-insensitive patterns
        self.skill_patterns = [
            (skill, re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE))
            for skill in all_skills
        ]
    
    def extract_from_text(self, cv_text: str) -> Dict[str, any]:
        """
        Extract skills from CV text
        
        Args:
            cv_text: The text content of the CV
            
        Returns:
            Dictionary containing extracted skills by category
        """
        # Clean text
        cv_text = self._clean_text(cv_text)
        
        # Extract using multiple methods
        pattern_skills = self._extract_by_patterns(cv_text)
        ner_skills = self._extract_by_ner(cv_text) if self.ner_pipeline else set()
        context_skills = self._extract_by_context(cv_text)
        
        # Combine all extracted skills
        all_skills = pattern_skills | ner_skills | context_skills
        
        # Categorize skills
        categorized_skills = self._categorize_skills(all_skills)
        
        # Calculate proficiency indicators (based on context)
        skills_with_proficiency = self._estimate_proficiency(cv_text, categorized_skills)
        
        return {
            "skills": skills_with_proficiency,
            "total_count": sum(len(skills) for skills in categorized_skills.values()),
            "categories": list(categorized_skills.keys()),
            "raw_skills": list(all_skills)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize CV text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.,;:()\-/+#]', '', text)
        return text.strip()
    
    def _extract_by_patterns(self, text: str) -> Set[str]:
        """Extract skills using regex patterns"""
        found_skills = set()
        
        for skill_name, pattern in self.skill_patterns:
            if pattern.search(text):
                found_skills.add(skill_name)
        
        return found_skills
    
    def _extract_by_ner(self, text: str) -> Set[str]:
        """Extract skills using NER model"""
        if not self.ner_pipeline:
            return set()
        
        found_skills = set()
        
        try:
            # Run NER on text
            entities = self.ner_pipeline(text)
            
            # Extract relevant entities (MISC, ORG might contain tech terms)
            for entity in entities:
                entity_text = entity['word'].strip()
                entity_type = entity['entity_group']
                
                # Check if entity matches known skills
                entity_lower = entity_text.lower()
                for category, skills in self.skill_categories.items():
                    for skill in skills:
                        if skill.lower() == entity_lower:
                            found_skills.add(skill)
                            break
        
        except Exception as e:
            logger.error(f"NER extraction error: {e}")
        
        return found_skills
    
    def _extract_by_context(self, text: str) -> Set[str]:
        """Extract skills by looking at context patterns"""
        found_skills = set()
        
        # Common skill-indicating phrases
        skill_contexts = [
            r'skills?[:\s]+([^\.]+)',
            r'technologies?[:\s]+([^\.]+)',
            r'experienced? (?:in|with)[:\s]+([^\.]+)',
            r'proficient (?:in|with)[:\s]+([^\.]+)',
            r'knowledge of[:\s]+([^\.]+)',
            r'expertise in[:\s]+([^\.]+)',
            r'worked with[:\s]+([^\.]+)',
            r'used[:\s]+([^\.]+)',
            r'familiar with[:\s]+([^\.]+)',
        ]
        
        for pattern in skill_contexts:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                context_text = match.group(1)
                # Extract skills from this context
                context_skills = self._extract_skills_from_snippet(context_text)
                found_skills.update(context_skills)
        
        return found_skills
    
    def _extract_skills_from_snippet(self, snippet: str) -> Set[str]:
        """Extract known skills from a text snippet"""
        found_skills = set()
        snippet_lower = snippet.lower()
        
        for category, skills in self.skill_categories.items():
            for skill in skills:
                if skill.lower() in snippet_lower:
                    found_skills.add(skill)
        
        return found_skills
    
    def _categorize_skills(self, skills: Set[str]) -> Dict[str, List[str]]:
        """Categorize extracted skills"""
        categorized = {category: [] for category in self.skill_categories.keys()}
        
        for skill in skills:
            for category, category_skills in self.skill_categories.items():
                if skill in category_skills:
                    categorized[category].append(skill)
                    break
        
        # Remove empty categories
        categorized = {k: v for k, v in categorized.items() if v}
        
        return categorized
    
    def _estimate_proficiency(
        self, 
        text: str, 
        categorized_skills: Dict[str, List[str]]
    ) -> Dict[str, List[Dict[str, any]]]:
        """
        Estimate proficiency level for each skill based on context
        Returns skills with proficiency indicators
        """
        result = {}
        
        # Proficiency indicators
        expert_patterns = [
            r'expert', r'advanced', r'mastery', r'lead', r'architect',
            r'senior', r'\d+ years?'
        ]
        intermediate_patterns = [
            r'intermediate', r'proficient', r'experienced', r'solid',
            r'good knowledge', r'working knowledge'
        ]
        
        for category, skills in categorized_skills.items():
            skills_with_prof = []
            
            for skill in skills:
                # Find skill mentions in text
                skill_pattern = re.compile(
                    r'(.{0,50}' + re.escape(skill) + r'.{0,50})',
                    re.IGNORECASE
                )
                matches = skill_pattern.findall(text)
                
                # Determine proficiency
                proficiency = "beginner"  # default
                
                for match in matches:
                    match_lower = match.lower()
                    if any(re.search(p, match_lower) for p in expert_patterns):
                        proficiency = "expert"
                        break
                    elif any(re.search(p, match_lower) for p in intermediate_patterns):
                        proficiency = "intermediate"
                
                skills_with_prof.append({
                    "name": skill,
                    "proficiency": proficiency,
                    "mentions": len(matches)
                })
            
            result[category] = skills_with_prof
        
        return result
    
    def normalize_skill(self, skill: str) -> str:
        """Normalize skill name to canonical form"""
        # Mapping of variations to canonical names
        normalizations = {
            "react.js": "React",
            "reactjs": "React",
            "vue": "Vue.js",
            "vuejs": "Vue.js",
            "node": "Node.js",
            "nodejs": "Node.js",
            "js": "JavaScript",
            "ts": "TypeScript",
            "py": "Python",
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence",
            "postgresql": "PostgreSQL",
            "postgres": "PostgreSQL",
            "mongo": "MongoDB",
            "k8s": "Kubernetes",
        }
        
        skill_lower = skill.lower().strip()
        return normalizations.get(skill_lower, skill)
    
    def extract_from_sections(self, cv_sections: Dict[str, str]) -> Dict[str, any]:
        """
        Extract skills from structured CV sections
        
        Args:
            cv_sections: Dictionary with section names as keys and text as values
                        e.g., {"skills": "...", "experience": "...", "education": "..."}
        """
        all_skills = set()
        section_skills = {}
        
        for section_name, section_text in cv_sections.items():
            result = self.extract_from_text(section_text)
            section_skills[section_name] = result
            all_skills.update(result['raw_skills'])
        
        # Combine and deduplicate
        combined_categorized = self._categorize_skills(all_skills)
        
        return {
            "skills": self._estimate_proficiency(
                ' '.join(cv_sections.values()), 
                combined_categorized
            ),
            "by_section": section_skills,
            "total_count": len(all_skills),
            "categories": list(combined_categorized.keys())
        }


# Global instance
_skill_extractor_instance = None


def get_skill_extractor() -> SkillExtractor:
    """Get singleton instance of SkillExtractor"""
    global _skill_extractor_instance
    if _skill_extractor_instance is None:
        _skill_extractor_instance = SkillExtractor()
    return _skill_extractor_instance

