from neo4j import GraphDatabase, Session
from typing import List, Dict, Any, Optional
from BD.config import NEO4J_URL, NEO4J_USER, NEO4J_PASSWORD
import logging

logger = logging.getLogger(__name__)

class Neo4jService:
    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URL,
                auth=(NEO4J_USER, NEO4J_PASSWORD),
                encrypted=False
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
            logger.info("✓ Neo4j connected")
        except Exception as e:
            logger.error(f"✗ Neo4j connection failed: {e}")
            raise

    def close(self):
        if self.driver:
            self.driver.close()

    # ===== ROLE OPERATIONS =====
    def create_role_node(self, role_data: Dict[str, Any]) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MERGE (r:Role {name: $name})
                    SET r.category = $category,
                        r.experience_level = $experience_level
                    """,
                    name=role_data.get("name"),
                    category=role_data.get("category"),
                    experience_level=role_data.get("experience_level")
                )
            logger.info(f"Role node created: {role_data.get('name')}")
            return True
        except Exception as e:
            logger.error(f"Error creating role node: {e}")
            raise

    # ===== SKILL OPERATIONS =====
    def create_skill_node(self, skill_data: Dict[str, Any]) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MERGE (s:Skill {id: $id})
                    SET s.name = $name,
                        s.category = $category,
                        s.difficulty = $difficulty,
                        s.demand_level = $demand_level
                    """,
                    id=skill_data.get("id"),
                    name=skill_data.get("name"),
                    category=skill_data.get("category"),
                    difficulty=skill_data.get("difficulty"),
                    demand_level=skill_data.get("demand_level")
                )
            logger.info(f"Skill node created: {skill_data.get('name')}")
            return True
        except Exception as e:
            logger.error(f"Error creating skill node: {e}")
            raise

    # ===== RELATIONSHIP OPERATIONS =====
    def create_requires_relationship(self, role_name: str, skill_id: str) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (r:Role {name: $role_name})
                    MATCH (s:Skill {id: $skill_id})
                    MERGE (r)-[:REQUIRES]->(s)
                    """,
                    role_name=role_name,
                    skill_id=skill_id
                )
            logger.info(f"REQUIRES relationship: {role_name} -> {skill_id}")
            return True
        except Exception as e:
            logger.warning(f"Could not create REQUIRES relationship: {e}")
            return False

    def create_prerequisite_relationship(self, skill_id_1: str, skill_id_2: str) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (s1:Skill {id: $skill_id_1})
                    MATCH (s2:Skill {id: $skill_id_2})
                    MERGE (s1)-[:PREREQUISITE_OF]->(s2)
                    """,
                    skill_id_1=skill_id_1,
                    skill_id_2=skill_id_2
                )
            logger.info(f"PREREQUISITE_OF: {skill_id_1} -> {skill_id_2}")
            return True
        except Exception as e:
            logger.warning(f"Could not create PREREQUISITE_OF: {e}")
            return False

    def create_tool_relationship(self, role_name: str, tool_name: str) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (r:Role {name: $role_name})
                    MERGE (t:Tool {name: $tool_name})
                    MERGE (r)-[:USES]->(t)
                    """,
                    role_name=role_name,
                    tool_name=tool_name
                )
            logger.info(f"USES: {role_name} -> {tool_name}")
            return True
        except Exception as e:
            logger.warning(f"Could not create USES: {e}")
            return False

    def create_leads_to_relationship(self, role_name_1: str, role_name_2: str) -> bool:
        try:
            with self.driver.session() as session:
                session.run(
                    """
                    MATCH (r1:Role {name: $role_name_1})
                    MATCH (r2:Role {name: $role_name_2})
                    MERGE (r1)-[:LEADS_TO]->(r2)
                    """,
                    role_name_1=role_name_1,
                    role_name_2=role_name_2
                )
            logger.info(f"LEADS_TO: {role_name_1} -> {role_name_2}")
            return True
        except Exception as e:
            logger.warning(f"Could not create LEADS_TO: {e}")
            return False

    # ===== LEARNING PATH OPERATIONS =====
    def get_learning_path(self, start_skill_id: str, end_skill_id: str) -> List[Dict]:
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH path = shortestPath(
                        (s1:Skill {id: $start})-[:PREREQUISITE_OF*]->(s2:Skill {id: $end})
                    )
                    RETURN [node IN nodes(path) | {id: node.id, name: node.name}] as path
                    """,
                    start=start_skill_id,
                    end=end_skill_id
                )
                records = result.data()
                return records[0]["path"] if records else []
        except Exception as e:
            logger.warning(f"Error retrieving learning path: {e}")
            return []

    def get_role_skills(self, role_name: str) -> List[Dict]:
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (r:Role {name: $role_name})-[:REQUIRES]->(s:Skill)
                    RETURN DISTINCT s.id as id, s.name as name, s.difficulty as difficulty
                    """,
                    role_name=role_name
                )
                return [dict(record) for record in result]
        except Exception as e:
            logger.warning(f"Error retrieving role skills: {e}")
            return []

    def get_career_path(self, start_role: str) -> List[str]:
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH path = (r:Role {name: $start})-[:LEADS_TO*]->(r2:Role)
                    RETURN [node IN nodes(path) | node.name] as path
                    """,
                    start=start_role
                )
                records = result.data()
                return records[0]["path"] if records else [start_role]
        except Exception as e:
            logger.warning(f"Error retrieving career path: {e}")
            return [start_role]

    def get_prerequisites(self, skill_id: str) -> List[Dict]:
        try:
            with self.driver.session() as session:
                result = session.run(
                    """
                    MATCH (s1:Skill)-[:PREREQUISITE_OF]->(s:Skill {id: $skill_id})
                    RETURN DISTINCT s1.id as id, s1.name as name, s1.difficulty as difficulty
                    """,
                    skill_id=skill_id
                )
                return [dict(record) for record in result]
        except Exception as e:
            logger.warning(f"Error retrieving prerequisites: {e}")
            return []