from fastapi import APIRouter, HTTPException, Depends
from typing import List
from BD.services import MongoDBService, Neo4jService
from BD.models import Role, Skill, LearningResource

router = APIRouter(prefix="/api/bd", tags=["database"])

def get_mongo_service() -> MongoDBService:
    """Dependency: MongoDB service"""
    return MongoDBService()

def get_neo4j_service() -> Neo4jService:
    """Dependency: Neo4j service"""
    return Neo4jService()

# ===== ROLE ENDPOINTS =====
@router.get("/roles", response_model=List[Role])
async def get_all_roles(mongo: MongoDBService = Depends(get_mongo_service)):
    """Get all roles"""
    try:
        roles = mongo.get_all_roles()
        mongo.close()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/roles/{role_name}", response_model=Role)
async def get_role(role_name: str, mongo: MongoDBService = Depends(get_mongo_service)):
    """Get role by name"""
    try:
        role = mongo.get_role_by_name(role_name)
        mongo.close()
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== SKILL ENDPOINTS =====
@router.get("/skills", response_model=List[Skill])
async def get_all_skills(mongo: MongoDBService = Depends(get_mongo_service)):
    """Get all skills"""
    try:
        skills = mongo.get_all_skills()
        mongo.close()
        return skills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills/{skill_id}", response_model=Skill)
async def get_skill(skill_id: str, mongo: MongoDBService = Depends(get_mongo_service)):
    """Get skill by ID"""
    try:
        skill = mongo.get_skill_by_id(skill_id)
        mongo.close()
        if not skill:
            raise HTTPException(status_code=404, detail="Skill not found")
        return skill
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skills/category/{category}", response_model=List[Skill])
async def get_skills_by_category(category: str, mongo: MongoDBService = Depends(get_mongo_service)):
    """Get skills by category"""
    try:
        skills = mongo.get_skills_by_category(category)
        mongo.close()
        return skills
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== LEARNING RESOURCE ENDPOINTS =====
@router.get("/resources/{skill_id}", response_model=List[LearningResource])
async def get_resources(skill_id: str, mongo: MongoDBService = Depends(get_mongo_service)):
    """Get learning resources for a skill"""
    try:
        resources = mongo.get_resources_by_skill(skill_id)
        mongo.close()
        return resources
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== NEO4J GRAPH ENDPOINTS =====
@router.get("/learning-path/{start_skill}/{end_skill}")
async def get_learning_path(start_skill: str, end_skill: str, neo4j: Neo4jService = Depends(get_neo4j_service)):
    """Get learning path between two skills"""
    try:
        path = neo4j.get_learning_path(start_skill, end_skill)
        neo4j.close()
        return {"path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/role/{role_name}/skills")
async def get_role_skills(role_name: str, neo4j: Neo4jService = Depends(get_neo4j_service)):
    """Get all skills required for a role"""
    try:
        skills = neo4j.get_role_skills(role_name)
        neo4j.close()
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/career-path/{start_role}")
async def get_career_path(start_role: str, neo4j: Neo4jService = Depends(get_neo4j_service)):
    """Get career progression path"""
    try:
        path = neo4j.get_career_path(start_role)
        neo4j.close()
        return {"path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/prerequisites/{skill_id}")
async def get_prerequisites(skill_id: str, neo4j: Neo4jService = Depends(get_neo4j_service)):
    """Get prerequisite skills"""
    try:
        prereqs = neo4j.get_prerequisites(skill_id)
        neo4j.close()
        return {"prerequisites": prereqs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))