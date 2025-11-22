# BD/__init__.py
# Keep this minimal to avoid circular imports.
# If you want to re-export models you *can*, but do NOT import services here.

from BD.services import MongoDBService, Neo4jService
from BD.models import Role, Skill, LearningResource, UserProfile, Roadmap

__all__ = [
    "MongoDBService",
    "Neo4jService",
    "Role",
    "Skill",
    "LearningResource",
    "UserProfile",
    "Roadmap",
]
