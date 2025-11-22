from BD.services import MongoDBService, Neo4jService

def get_mongo_service() -> MongoDBService:
    """Dependency for MongoDB service"""
    return MongoDBService()

def get_neo4j_service() -> Neo4jService:
    """Dependency for Neo4j service"""
    return Neo4jService()