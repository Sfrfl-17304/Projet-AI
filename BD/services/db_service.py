from __future__ import annotations

from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import List, Optional, Dict, Any
from BD.config import MONGO_URL, MONGO_DB_NAME
from BD.models import Role, Skill, LearningResource, UserProfile, Roadmap
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


def convert_objectid_to_str(doc: Dict) -> Dict:
    """Convert ObjectId to string in document"""
    if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


class MongoDBService:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')  # Test connection
            self.db = self.client[MONGO_DB_NAME]
            self.roles_collection = self.db["roles"]
            self.skills_collection = self.db["skills"]
            self.resources_collection = self.db["learning_resources"]
            self.users_collection = self.db["user_profiles"]
            self.roadmaps_collection = self.db["roadmaps"]
            logger.info("✓ MongoDB connected")
        except Exception as e:
            logger.error(f"✗ MongoDB connection failed: {e}")
            raise

    def close(self):
        self.client.close()

    # ===== ROLE OPERATIONS =====
    def insert_role(self, role: Role) -> str:
        try:
            result = self.roles_collection.insert_one(
                role.model_dump(exclude={"id"}, by_alias=True)
            )
            logger.info(f"Role inserted: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting role: {e}")
            raise

    def get_all_roles(self) -> List[Role]:
        try:
            roles_data = list(self.roles_collection.find())
            return [Role(**convert_objectid_to_str(role)) for role in roles_data]
        except PyMongoError as e:
            logger.error(f"Error fetching roles: {e}")
            raise

    def get_role_by_name(self, name: str) -> Optional[Role]:
        try:
            role_data = self.roles_collection.find_one({"name": name})
            return Role(**convert_objectid_to_str(role_data)) if role_data else None
        except PyMongoError as e:
            logger.error(f"Error fetching role: {e}")
            raise

    def get_role_by_id(self, role_id: str) -> Optional[Role]:
        try:
            role_data = self.roles_collection.find_one({"_id": ObjectId(role_id)})
            return Role(**convert_objectid_to_str(role_data)) if role_data else None
        except (PyMongoError, Exception) as e:
            logger.error(f"Error fetching role: {e}")
            raise

    # ===== SKILL OPERATIONS =====
    def insert_skill(self, skill: Skill) -> str:
        try:
            # Don't convert to _id, keep as "id"
            data = skill.model_dump(exclude_none=True)
            result = self.skills_collection.insert_one(data)
            logger.info(f"Skill inserted: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting skill: {e}")
            raise

    def get_all_skills(self) -> List[Skill]:
        try:
            skills_data = list(self.skills_collection.find())
            # Handle both _id and id fields
            return [Skill(**convert_objectid_to_str(skill)) for skill in skills_data]
        except PyMongoError as e:
            logger.error(f"Error fetching skills: {e}")
            raise

    def get_skill_by_id(self, skill_id: str) -> Optional[Skill]:
        try:
            # Try finding by both _id and id field
            skill_data = self.skills_collection.find_one({"$or": [{"_id": skill_id}, {"id": skill_id}]})
            if skill_data:
                return Skill(**convert_objectid_to_str(skill_data))
            return None
        except (PyMongoError, ValueError) as e:
            logger.error(f"Error fetching skill: {e}")
            return None

    def get_skills_by_category(self, category: str) -> List[Skill]:
        try:
            skills_data = list(self.skills_collection.find({"category": category}))
            return [Skill(**convert_objectid_to_str(skill)) for skill in skills_data]
        except PyMongoError as e:
            logger.error(f"Error fetching skills by category: {e}")
            raise

    # ===== LEARNING RESOURCE OPERATIONS =====
    def insert_resource(self, resource: LearningResource) -> str:
        try:
            result = self.resources_collection.insert_one(
                resource.model_dump(exclude={"id"}, by_alias=True)
            )
            logger.info(f"Resource inserted: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error inserting resource: {e}")
            raise

    def get_resources_by_skill(self, skill_id: str) -> List[LearningResource]:
        try:
            resources_data = list(self.resources_collection.find({"skill": skill_id}))
            return [LearningResource(**convert_objectid_to_str(resource)) for resource in resources_data]
        except PyMongoError as e:
            logger.error(f"Error fetching resources: {e}")
            raise

    # ===== USER PROFILE OPERATIONS =====
    def create_user_profile(self, user_profile: UserProfile) -> str:
        try:
            result = self.users_collection.insert_one(
                user_profile.model_dump(exclude={"id"}, by_alias=True)
            )
            logger.info(f"User profile created: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error creating user profile: {e}")
            raise

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        try:
            profile_data = self.users_collection.find_one({"user_id": user_id})
            return UserProfile(**convert_objectid_to_str(profile_data)) if profile_data else None
        except PyMongoError as e:
            logger.error(f"Error fetching user profile: {e}")
            raise

    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        try:
            result = self.users_collection.update_one(
                {"user_id": user_id}, {"$set": updates}
            )
            return result.modified_count > 0
        except PyMongoError as e:
            logger.error(f"Error updating user profile: {e}")
            raise

    # ===== ROADMAP OPERATIONS =====
    def save_roadmap(self, roadmap: Roadmap) -> str:
        try:
            result = self.roadmaps_collection.insert_one(
                roadmap.model_dump(exclude={"id"}, by_alias=True)
            )
            logger.info(f"Roadmap saved: {result.inserted_id}")
            return str(result.inserted_id)
        except PyMongoError as e:
            logger.error(f"Error saving roadmap: {e}")
            raise

    def get_roadmap(self, user_id: str) -> Optional[Roadmap]:
        try:
            roadmap_data = self.roadmaps_collection.find_one({"user_id": user_id})
            return Roadmap(**convert_objectid_to_str(roadmap_data)) if roadmap_data else None
        except PyMongoError as e:
            logger.error(f"Error fetching roadmap: {e}")
            raise

    def create_indexes(self):
        try:
            self.roles_collection.create_index("name", unique=True)
            self.skills_collection.create_index("id", unique=True)
            self.users_collection.create_index("user_id", unique=True)
            self.roadmaps_collection.create_index("user_id", unique=True)
            logger.info("Indexes created successfully")
        except PyMongoError as e:
            logger.error(f"Error creating indexes: {e}")
            raise
