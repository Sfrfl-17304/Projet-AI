from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from bson import ObjectId

class UserProfile(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str
    extracted_skills: List[str] = Field(default_factory=list)
    target_roles: List[str] = Field(default_factory=list)
    completed_skills: List[str] = Field(default_factory=list)
    learning_roadmap: Optional[str] = None
    preferences: Dict = Field(default_factory=dict)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }