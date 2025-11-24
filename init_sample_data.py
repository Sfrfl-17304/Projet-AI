#!/usr/bin/env python3
"""Initialize databases with sample data"""

from pymongo import MongoClient
from neo4j import GraphDatabase
from datetime import datetime

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["skillatlas"]

# Neo4j connection
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "skillatlas123"))

print("🗄️  Initializing databases with sample data...\n")

# Sample Skills
skills_data = [
    {"skill_id": "python", "name": "Python", "category": "Programming Languages", "difficulty": "intermediate", "demand": "very_high", "popularity": 95},
    {"skill_id": "javascript", "name": "JavaScript", "category": "Programming Languages", "difficulty": "intermediate", "demand": "very_high", "popularity": 98},
    {"skill_id": "react", "name": "React", "category": "Frontend Frameworks", "difficulty": "intermediate", "demand": "very_high", "popularity": 90},
    {"skill_id": "nodejs", "name": "Node.js", "category": "Backend Frameworks", "difficulty": "intermediate", "demand": "high", "popularity": 85},
    {"skill_id": "sql", "name": "SQL", "category": "Databases", "difficulty": "intermediate", "demand": "very_high", "popularity": 92},
    {"skill_id": "mongodb", "name": "MongoDB", "category": "Databases", "difficulty": "intermediate", "demand": "high", "popularity": 80},
    {"skill_id": "git", "name": "Git", "category": "Tools", "difficulty": "beginner", "demand": "very_high", "popularity": 97},
    {"skill_id": "docker", "name": "Docker", "category": "DevOps", "difficulty": "advanced", "demand": "high", "popularity": 85},
    {"skill_id": "aws", "name": "AWS", "category": "Cloud Platforms", "difficulty": "advanced", "demand": "very_high", "popularity": 88},
    {"skill_id": "machine_learning", "name": "Machine Learning", "category": "Data Science", "difficulty": "expert", "demand": "very_high", "popularity": 82},
    {"skill_id": "data_analysis", "name": "Data Analysis", "category": "Data Science", "difficulty": "intermediate", "demand": "high", "popularity": 87},
    {"skill_id": "communication", "name": "Communication", "category": "Soft Skills", "difficulty": "intermediate", "demand": "very_high", "popularity": 99},
    {"skill_id": "problem_solving", "name": "Problem Solving", "category": "Soft Skills", "difficulty": "intermediate", "demand": "very_high", "popularity": 98},
    {"skill_id": "teamwork", "name": "Teamwork", "category": "Soft Skills", "difficulty": "intermediate", "demand": "very_high", "popularity": 97},
]

# Sample Roles
roles_data = [
    {
        "role_id": "software_engineer",
        "title": "Software Engineer",
        "category": "Engineering",
        "description": "Design, develop, and maintain software applications",
        "avg_salary": 95000,
        "growth_rate": 22,
        "required_skills": [
            {"skill_id": "python", "priority": "critical"},
            {"skill_id": "javascript", "priority": "high"},
            {"skill_id": "git", "priority": "critical"},
            {"skill_id": "sql", "priority": "high"},
            {"skill_id": "problem_solving", "priority": "critical"},
            {"skill_id": "communication", "priority": "high"},
        ]
    },
    {
        "role_id": "frontend_developer",
        "title": "Frontend Developer",
        "category": "Engineering",
        "description": "Build user-facing web applications and interfaces",
        "avg_salary": 85000,
        "growth_rate": 18,
        "required_skills": [
            {"skill_id": "javascript", "priority": "critical"},
            {"skill_id": "react", "priority": "critical"},
            {"skill_id": "git", "priority": "high"},
            {"skill_id": "problem_solving", "priority": "high"},
            {"skill_id": "communication", "priority": "high"},
        ]
    },
    {
        "role_id": "backend_developer",
        "title": "Backend Developer",
        "category": "Engineering",
        "description": "Build server-side logic and database systems",
        "avg_salary": 92000,
        "growth_rate": 20,
        "required_skills": [
            {"skill_id": "python", "priority": "critical"},
            {"skill_id": "nodejs", "priority": "high"},
            {"skill_id": "sql", "priority": "critical"},
            {"skill_id": "mongodb", "priority": "high"},
            {"skill_id": "git", "priority": "critical"},
            {"skill_id": "problem_solving", "priority": "critical"},
        ]
    },
    {
        "role_id": "data_scientist",
        "title": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Analyze complex data and build predictive models",
        "avg_salary": 120000,
        "growth_rate": 31,
        "required_skills": [
            {"skill_id": "python", "priority": "critical"},
            {"skill_id": "machine_learning", "priority": "critical"},
            {"skill_id": "data_analysis", "priority": "critical"},
            {"skill_id": "sql", "priority": "high"},
            {"skill_id": "communication", "priority": "high"},
        ]
    },
    {
        "role_id": "devops_engineer",
        "title": "DevOps Engineer",
        "category": "Engineering",
        "description": "Manage infrastructure and deployment pipelines",
        "avg_salary": 105000,
        "growth_rate": 25,
        "required_skills": [
            {"skill_id": "docker", "priority": "critical"},
            {"skill_id": "aws", "priority": "critical"},
            {"skill_id": "git", "priority": "high"},
            {"skill_id": "python", "priority": "high"},
            {"skill_id": "problem_solving", "priority": "critical"},
        ]
    },
]

# Sample Learning Resources
resources_data = [
    {"resource_id": "python_course", "skill_id": "python", "title": "Python for Beginners", "type": "course", "url": "https://www.python.org/about/gettingstarted/", "duration_hours": 40},
    {"resource_id": "js_course", "skill_id": "javascript", "title": "JavaScript Fundamentals", "type": "course", "url": "https://developer.mozilla.org/en-US/docs/Learn/JavaScript", "duration_hours": 35},
    {"resource_id": "react_docs", "skill_id": "react", "title": "React Official Documentation", "type": "documentation", "url": "https://react.dev/", "duration_hours": 30},
    {"resource_id": "sql_tutorial", "skill_id": "sql", "title": "SQL Tutorial", "type": "tutorial", "url": "https://www.w3schools.com/sql/", "duration_hours": 25},
    {"resource_id": "docker_docs", "skill_id": "docker", "title": "Docker Documentation", "type": "documentation", "url": "https://docs.docker.com/", "duration_hours": 20},
]

# Clear existing data
print("Clearing existing collections...")
db["skills"].delete_many({})
db["roles"].delete_many({})
db["learning_resources"].delete_many({})

# Insert Skills into MongoDB
print(f"\nInserting {len(skills_data)} skills into MongoDB...")
db["skills"].insert_many(skills_data)
print(f"✅ {len(skills_data)} skills inserted")

# Insert Roles into MongoDB
print(f"\nInserting {len(roles_data)} roles into MongoDB...")
db["roles"].insert_many(roles_data)
print(f"✅ {len(roles_data)} roles inserted")

# Insert Learning Resources into MongoDB
print(f"\nInserting {len(resources_data)} learning resources into MongoDB...")
db["learning_resources"].insert_many(resources_data)
print(f"✅ {len(resources_data)} resources inserted")

# Populate Neo4j Graph
print("\n🕸️  Populating Neo4j knowledge graph...")

with neo4j_driver.session() as session:
    # Clear existing data
    print("Clearing existing Neo4j data...")
    session.run("MATCH (n) DETACH DELETE n")
    
    # Create Skills nodes
    print(f"\nCreating {len(skills_data)} skill nodes...")
    for skill in skills_data:
        session.run("""
            CREATE (s:Skill {
                id: $id,
                name: $name,
                category: $category,
                difficulty: $difficulty,
                demand: $demand,
                popularity: $popularity
            })
        """, 
        id=skill["skill_id"],
        name=skill["name"],
        category=skill["category"],
        difficulty=skill["difficulty"],
        demand=skill["demand"],
        popularity=skill["popularity"])
    print(f"✅ {len(skills_data)} skill nodes created")
    
    # Create Role nodes and relationships
    print(f"\nCreating {len(roles_data)} role nodes with relationships...")
    for role in roles_data:
        # Create role node
        session.run("""
            CREATE (r:Role {
                id: $id,
                title: $title,
                category: $category,
                description: $description,
                avg_salary: $avg_salary,
                growth_rate: $growth_rate
            })
        """,
        id=role["role_id"],
        title=role["title"],
        category=role["category"],
        description=role["description"],
        avg_salary=role["avg_salary"],
        growth_rate=role["growth_rate"])
        
        # Create REQUIRES relationships to skills
        for req_skill in role["required_skills"]:
            session.run("""
                MATCH (r:Role {id: $role_id})
                MATCH (s:Skill {id: $skill_id})
                CREATE (r)-[:REQUIRES {priority: $priority}]->(s)
            """,
            role_id=role["role_id"],
            skill_id=req_skill["skill_id"],
            priority=req_skill["priority"])
    print(f"✅ {len(roles_data)} role nodes and relationships created")
    
    # Create skill prerequisites (example relationships)
    print("\nCreating skill prerequisite relationships...")
    prerequisites = [
        ("react", "javascript"),
        ("nodejs", "javascript"),
        ("mongodb", "sql"),
        ("docker", "git"),
        ("aws", "docker"),
        ("machine_learning", "python"),
        ("machine_learning", "data_analysis"),
    ]
    
    for skill_id, prereq_id in prerequisites:
        session.run("""
            MATCH (s:Skill {id: $skill_id})
            MATCH (p:Skill {id: $prereq_id})
            CREATE (s)-[:PREREQUISITE]->(p)
        """, skill_id=skill_id, prereq_id=prereq_id)
    print(f"✅ {len(prerequisites)} prerequisite relationships created")

# Verify data
print("\n" + "="*50)
print("📊 Database Summary:")
print("="*50)

print(f"\nMongoDB (skillatlas):")
print(f"  - Skills: {db['skills'].count_documents({})}")
print(f"  - Roles: {db['roles'].count_documents({})}")
print(f"  - Resources: {db['learning_resources'].count_documents({})}")

with neo4j_driver.session() as session:
    result = session.run("MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
    print(f"\nNeo4j Graph:")
    for record in result:
        print(f"  - {record['label']}: {record['count']} nodes")
    
    result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
    for record in result:
        print(f"  - {record['type']}: {record['count']} relationships")

print("\n🎉 Database initialization complete!")
print("\nYou can now:")
print("  - View Neo4j Browser at: http://localhost:7474")
print("  - Set MOCK_DB=false in .env to use real databases")
print("  - Restart the frontend server")

# Close connections
mongo_client.close()
neo4j_driver.close()
