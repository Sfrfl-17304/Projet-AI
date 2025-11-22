from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class RequiredSkill(BaseModel):
    skill_id: str
    skill_name: str
    proficiency_level: str
    priority: str

class Role(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    description: str
    category: str
    required_skills: List[RequiredSkill]
    average_salary: str
    growth_rate: str
    experience_level: str
    responsibilities: List[str]
    tools: List[str]
    industries: List[str]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }