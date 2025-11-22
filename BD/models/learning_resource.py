from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class LearningResource(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    url: str
    type: str
    provider: str
    price: str
    duration_hours: int
    skill: str
    difficulty: str
    rating: float
    description: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }