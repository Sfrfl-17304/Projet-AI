"""
LLM Service
Handles Large Language Model interactions for career recommendations,
skill gap analysis, and roadmap generation
"""

from langchain_huggingface import HuggingFaceEndpoint, HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Dict, List, Optional
from config.ai_config import (
    ai_settings,
    CAREER_RECOMMENDATION_PROMPT,
    SKILL_GAP_ANALYSIS_PROMPT,
    LEARNING_ROADMAP_PROMPT,
    INTEREST_ANALYSIS_PROMPT
)
import logging
import json

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM-based career guidance and recommendations"""
    
    def __init__(self):
        """Initialize the LLM service"""
        self._initialize_llm()
    
    def _initialize_llm(self):
        """Initialize LLM model"""
        try:
            if ai_settings.use_local_llm:
                # Use local HuggingFace model
                from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
                
                tokenizer = AutoTokenizer.from_pretrained(
                    ai_settings.llm_model_name,
                    cache_dir=ai_settings.hf_model_cache_dir
                )
                model = AutoModelForCausalLM.from_pretrained(
                    ai_settings.llm_model_name,
                    cache_dir=ai_settings.hf_model_cache_dir,
                    device_map="auto"
                )
                
                pipe = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_new_tokens=ai_settings.llm_max_tokens,
                    temperature=ai_settings.llm_temperature,
                )
                
                self.llm = HuggingFacePipeline(pipeline=pipe)
                logger.info(f"Local LLM loaded: {ai_settings.llm_model_name}")
            
            else:
                # Use HuggingFace API
                if not ai_settings.huggingface_api_key:
                    logger.warning("No HuggingFace API key set, using demo mode")
                
                self.llm = HuggingFaceEndpoint(
                    repo_id=ai_settings.llm_model_name,
                    huggingfacehub_api_token=ai_settings.huggingface_api_key,
                    temperature=ai_settings.llm_temperature,
                    max_new_tokens=ai_settings.llm_max_tokens,
                )
                logger.info(f"HuggingFace API LLM initialized: {ai_settings.llm_model_name}")
        
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            # Fallback to mock LLM for testing
            self.llm = None
            logger.warning("LLM not available, using fallback mode")
    
    def recommend_careers(
        self,
        user_profile: Dict[str, any],
        num_recommendations: int = 5
    ) -> List[Dict[str, any]]:
        """
        Recommend career paths based on user profile
        
        Args:
            user_profile: Dictionary with user's skills, interests, background
            num_recommendations: Number of careers to recommend
            
        Returns:
            List of career recommendations with match scores and explanations
        """
        if not self.llm:
            return self._fallback_career_recommendations(user_profile)
        
        try:
            # Format user profile
            profile_text = self._format_user_profile(user_profile)
            
            # Create prompt
            prompt = PromptTemplate(
                input_variables=["user_profile"],
                template=CAREER_RECOMMENDATION_PROMPT
            )
            
            # Generate recommendations
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(user_profile=profile_text)
            
            # Parse response
            recommendations = self._parse_career_recommendations(response)
            
            return recommendations[:num_recommendations]
        
        except Exception as e:
            logger.error(f"Error generating career recommendations: {e}")
            return self._fallback_career_recommendations(user_profile)
    
    def analyze_skill_gap(
        self,
        current_skills: List[str],
        target_role: str,
        required_skills: List[str]
    ) -> Dict[str, any]:
        """
        Analyze skill gap between current and required skills
        
        Args:
            current_skills: User's current skills
            target_role: Target career role
            required_skills: Skills required for target role
            
        Returns:
            Skill gap analysis with priorities and time estimates
        """
        if not self.llm:
            return self._fallback_skill_gap_analysis(
                current_skills, target_role, required_skills
            )
        
        try:
            # Create prompt
            prompt = PromptTemplate(
                input_variables=["current_skills", "target_role", "required_skills"],
                template=SKILL_GAP_ANALYSIS_PROMPT
            )
            
            # Generate analysis
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(
                current_skills=", ".join(current_skills),
                target_role=target_role,
                required_skills=", ".join(required_skills)
            )
            
            # Parse response
            analysis = self._parse_skill_gap_analysis(
                response, current_skills, required_skills
            )
            
            return analysis
        
        except Exception as e:
            logger.error(f"Error analyzing skill gap: {e}")
            return self._fallback_skill_gap_analysis(
                current_skills, target_role, required_skills
            )
    
    def generate_learning_roadmap(
        self,
        current_skills: List[str],
        target_role: str,
        missing_skills: List[str],
        timeline: str = "6 months"
    ) -> Dict[str, any]:
        """
        Generate personalized learning roadmap
        
        Args:
            current_skills: User's current skills
            target_role: Target career role
            missing_skills: Skills to acquire
            timeline: Desired timeline (e.g., "6 months", "1 year")
            
        Returns:
            Structured learning roadmap with phases and milestones
        """
        if not self.llm:
            return self._fallback_learning_roadmap(
                current_skills, target_role, missing_skills, timeline
            )
        
        try:
            # Create prompt
            prompt = PromptTemplate(
                input_variables=[
                    "current_skills", "target_role", "missing_skills", "timeline"
                ],
                template=LEARNING_ROADMAP_PROMPT
            )
            
            # Generate roadmap
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(
                current_skills=", ".join(current_skills),
                target_role=target_role,
                missing_skills=", ".join(missing_skills),
                timeline=timeline
            )
            
            # Parse response
            roadmap = self._parse_learning_roadmap(response, timeline)
            
            return roadmap
        
        except Exception as e:
            logger.error(f"Error generating roadmap: {e}")
            return self._fallback_learning_roadmap(
                current_skills, target_role, missing_skills, timeline
            )
    
    def analyze_interests(
        self,
        user_responses: Dict[str, str]
    ) -> List[Dict[str, any]]:
        """
        Analyze user interests and suggest career paths for beginners
        
        Args:
            user_responses: Dictionary of question-answer pairs
            
        Returns:
            List of suggested career paths with explanations
        """
        if not self.llm:
            return self._fallback_interest_analysis(user_responses)
        
        try:
            # Format responses
            responses_text = "\n".join([
                f"{q}: {a}" for q, a in user_responses.items()
            ])
            
            # Create prompt
            prompt = PromptTemplate(
                input_variables=["user_responses"],
                template=INTEREST_ANALYSIS_PROMPT
            )
            
            # Generate analysis
            chain = LLMChain(llm=self.llm, prompt=prompt)
            response = chain.run(user_responses=responses_text)
            
            # Parse response
            suggestions = self._parse_interest_analysis(response)
            
            return suggestions
        
        except Exception as e:
            logger.error(f"Error analyzing interests: {e}")
            return self._fallback_interest_analysis(user_responses)
    
    # Helper methods for formatting
    
    def _format_user_profile(self, profile: Dict[str, any]) -> str:
        """Format user profile for LLM prompt"""
        formatted = []
        
        if 'skills' in profile:
            formatted.append(f"Skills: {', '.join(profile['skills'])}")
        if 'interests' in profile:
            formatted.append(f"Interests: {', '.join(profile['interests'])}")
        if 'education' in profile:
            formatted.append(f"Education: {profile['education']}")
        if 'experience' in profile:
            formatted.append(f"Experience: {profile['experience']}")
        if 'goals' in profile:
            formatted.append(f"Goals: {profile['goals']}")
        
        return "\n".join(formatted)
    
    # Parsing methods
    
    def _parse_career_recommendations(self, response: str) -> List[Dict[str, any]]:
        """Parse LLM response into structured career recommendations"""
        # Simple parsing - in production, use more robust parsing
        recommendations = []
        
        # Extract recommendations (basic implementation)
        lines = response.strip().split('\n')
        current_rec = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                if current_rec:
                    recommendations.append(current_rec)
                    current_rec = {}
            elif line.startswith(('1.', '2.', '3.', '4.', '5.')):
                if current_rec:
                    recommendations.append(current_rec)
                current_rec = {'role': line[2:].strip()}
            elif 'score' in line.lower():
                # Extract score
                import re
                score_match = re.search(r'(\d+)', line)
                if score_match:
                    current_rec['match_score'] = int(score_match.group(1))
            elif current_rec:
                # Add to explanation
                current_rec.setdefault('explanation', []).append(line)
        
        if current_rec:
            recommendations.append(current_rec)
        
        # Clean up explanations
        for rec in recommendations:
            if 'explanation' in rec:
                rec['explanation'] = ' '.join(rec['explanation'])
        
        return recommendations
    
    def _parse_skill_gap_analysis(
        self, 
        response: str,
        current_skills: List[str],
        required_skills: List[str]
    ) -> Dict[str, any]:
        """Parse skill gap analysis response"""
        # Calculate basic gap
        current_set = set(skill.lower() for skill in current_skills)
        required_set = set(skill.lower() for skill in required_skills)
        
        missing = [s for s in required_skills if s.lower() not in current_set]
        matched = [s for s in required_skills if s.lower() in current_set]
        
        return {
            "current_skills": current_skills,
            "required_skills": required_skills,
            "matched_skills": matched,
            "missing_skills": missing,
            "gap_percentage": len(missing) / len(required_skills) * 100 if required_skills else 0,
            "analysis": response,
            "priority_skills": missing[:5] if len(missing) > 5 else missing
        }
    
    def _parse_learning_roadmap(self, response: str, timeline: str) -> Dict[str, any]:
        """Parse learning roadmap response"""
        return {
            "timeline": timeline,
            "roadmap": response,
            "phases": self._extract_phases(response)
        }
    
    def _extract_phases(self, roadmap_text: str) -> List[Dict[str, any]]:
        """Extract learning phases from roadmap text"""
        # Simple phase extraction
        phases = []
        phase_keywords = ["foundation", "intermediate", "advanced", "phase"]
        
        lines = roadmap_text.lower().split('\n')
        current_phase = None
        
        for line in lines:
            if any(keyword in line for keyword in phase_keywords):
                if current_phase:
                    phases.append(current_phase)
                current_phase = {"name": line.strip(), "content": []}
            elif current_phase:
                current_phase["content"].append(line.strip())
        
        if current_phase:
            phases.append(current_phase)
        
        return phases
    
    def _parse_interest_analysis(self, response: str) -> List[Dict[str, any]]:
        """Parse interest analysis response"""
        # Similar to career recommendations parsing
        return self._parse_career_recommendations(response)
    
    # Fallback methods (when LLM is not available)
    
    def _fallback_career_recommendations(
        self, 
        user_profile: Dict[str, any]
    ) -> List[Dict[str, any]]:
        """Fallback career recommendations using rule-based approach"""
        skills = user_profile.get('skills', [])
        
        # Simple rule-based recommendations
        recommendations = []
        
        if any(s.lower() in ['python', 'machine learning', 'tensorflow', 'pytorch'] 
               for s in skills):
            recommendations.append({
                "role": "Machine Learning Engineer",
                "match_score": 85,
                "explanation": "Your ML and Python skills align well with this role"
            })
        
        if any(s.lower() in ['react', 'javascript', 'vue', 'angular'] 
               for s in skills):
            recommendations.append({
                "role": "Frontend Developer",
                "match_score": 80,
                "explanation": "Your frontend framework skills are a great match"
            })
        
        if any(s.lower() in ['python', 'django', 'fastapi', 'flask'] 
               for s in skills):
            recommendations.append({
                "role": "Backend Developer",
                "match_score": 82,
                "explanation": "Your backend development skills fit this role well"
            })
        
        return recommendations if recommendations else [{
            "role": "Software Developer",
            "match_score": 70,
            "explanation": "A versatile role that matches your skill set"
        }]
    
    def _fallback_skill_gap_analysis(
        self,
        current_skills: List[str],
        target_role: str,
        required_skills: List[str]
    ) -> Dict[str, any]:
        """Fallback skill gap analysis"""
        current_set = set(s.lower() for s in current_skills)
        required_set = set(s.lower() for s in required_skills)
        
        missing = [s for s in required_skills if s.lower() not in current_set]
        matched = [s for s in required_skills if s.lower() in current_set]
        
        return {
            "current_skills": current_skills,
            "required_skills": required_skills,
            "matched_skills": matched,
            "missing_skills": missing,
            "gap_percentage": len(missing) / len(required_skills) * 100 if required_skills else 0,
            "analysis": f"You have {len(matched)} out of {len(required_skills)} required skills.",
            "priority_skills": missing[:5]
        }
    
    def _fallback_learning_roadmap(
        self,
        current_skills: List[str],
        target_role: str,
        missing_skills: List[str],
        timeline: str
    ) -> Dict[str, any]:
        """Fallback learning roadmap"""
        return {
            "timeline": timeline,
            "roadmap": f"Focus on learning: {', '.join(missing_skills[:5])}",
            "phases": [
                {
                    "name": "Foundation",
                    "skills": missing_skills[:len(missing_skills)//2],
                    "duration": "2-3 months"
                },
                {
                    "name": "Advanced",
                    "skills": missing_skills[len(missing_skills)//2:],
                    "duration": "2-3 months"
                }
            ]
        }
    
    def _fallback_interest_analysis(
        self,
        user_responses: Dict[str, str]
    ) -> List[Dict[str, any]]:
        """Fallback interest analysis"""
        return [
            {
                "role": "Software Developer",
                "match_score": 75,
                "explanation": "A versatile career path suitable for various interests"
            },
            {
                "role": "Data Analyst",
                "match_score": 70,
                "explanation": "Good for analytical thinkers"
            }
        ]


# Global instance
_llm_service_instance = None


def get_llm_service() -> LLMService:
    """Get singleton instance of LLMService"""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance

