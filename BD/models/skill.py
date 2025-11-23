from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

class Skill(BaseModel):
    id: Optional[str] = Field(None, alias="_id")  # ← FIXED: Accept both id and _id
    name: str
    category: str
    description: str
    difficulty: str
    learning_time_hours: int
    prerequisites: List[str] = Field(default_factory=list)
    related_skills: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    popularity_score: int
    demand_level: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True  # ← Allow both id and _id
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }