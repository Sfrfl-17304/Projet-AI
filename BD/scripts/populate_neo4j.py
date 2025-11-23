from BD.services import Neo4jService
from BD.services import MongoDBService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_neo4j(neo4j_service: Neo4jService):
    """Clear existing data from Neo4j"""
    try:
        with neo4j_service.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("✓ Neo4j cleared")
    except Exception as e:
        logger.warning(f"Could not clear Neo4j (may be empty): {e}")

def populate_neo4j():
    """Populate Neo4j with nodes and relationships"""
    neo4j_service = Neo4jService()
    mongo_service = MongoDBService()

    try:
        # Clear existing data
        clear_neo4j(neo4j_service)
        
        # Fetch all skills and roles from MongoDB
        skills = mongo_service.get_all_skills()
        roles = mongo_service.get_all_roles()

        logger.info("Creating Skill nodes...")
        for skill in skills:
            neo4j_service.create_skill_node({
                "id": skill.id,
                "name": skill.name,
                "category": skill.category,
                "difficulty": skill.difficulty,
                "demand_level": skill.demand_level
            })

        logger.info("Creating Role nodes...")
        for role in roles:
            neo4j_service.create_role_node({
                "name": role.name,
                "category": role.category,
                "experience_level": role.experience_level
            })

        logger.info("Creating REQUIRES relationships...")
        for role in roles:
            for req_skill in role.required_skills:
                try:
                    neo4j_service.create_requires_relationship(role.name, req_skill.skill_id)
                except Exception as e:
                    logger.warning(f"Could not create REQUIRES: {e}")

        logger.info("Creating PREREQUISITE_OF relationships...")
        for skill in skills:
            for prereq_id in skill.prerequisites:
                try:
                    neo4j_service.create_prerequisite_relationship(prereq_id, skill.id)
                except Exception as e:
                    logger.warning(f"Could not create PREREQUISITE_OF: {e}")

        logger.info("Creating USES relationships...")
        for role in roles:
            for tool in role.tools:
                try:
                    neo4j_service.create_tool_relationship(role.name, tool)
                except Exception as e:
                    logger.warning(f"Could not create USES: {e}")

        logger.info("Creating LEADS_TO relationships...")
        career_paths = [
            ("Python Developer", "Data Engineer"),
            ("Data Engineer", "ML Engineer"),
            ("Python Developer", "ML Engineer"),
        ]
        for source, target in career_paths:
            try:
                neo4j_service.create_leads_to_relationship(source, target)
            except Exception as e:
                logger.warning(f"Could not create LEADS_TO: {e}")

        logger.info("✓ Neo4j population complete!")
    except Exception as e:
        logger.error(f"Error during Neo4j population: {e}")
    finally:
        neo4j_service.close()
        mongo_service.close()

if __name__ == "__main__":
    populate_neo4j()