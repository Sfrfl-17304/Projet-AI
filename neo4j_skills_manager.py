"""
Neo4j Skills Knowledge Graph Manager
"""
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
import json

load_dotenv()

class Neo4jSkillsManager:
    def __init__(self):
        """Initialize Neo4j connection"""
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        username = os.getenv("NEO4J_USERNAME", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        
        try:
            self.driver = GraphDatabase.driver(uri, auth=(username, password))
            self.driver.verify_connectivity()
            print("✓ Connected to Neo4j")
            self._create_constraints()
        except Exception as e:
            print(f"⚠ Neo4j connection failed: {e}")
            self.driver = None
    
    def _create_constraints(self):
        """Create constraints and indexes"""
        with self.driver.session() as session:
            # Create constraints
            queries = [
                "CREATE CONSTRAINT skill_name IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
                "CREATE CONSTRAINT field_name IF NOT EXISTS FOR (f:Field) REQUIRE f.name IS UNIQUE",
                "CREATE CONSTRAINT person_name IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE"
            ]
            for query in queries:
                try:
                    session.run(query)
                except:
                    pass
    
    def load_skills_dataset(self, dataset):
        """Load skills dataset into Neo4j
        Expected format: [
            {
                "field": "Software Development",
                "skills": ["Python", "JavaScript", "React"],
                "level": "Intermediate"
            }
        ]
        """
        print(f"📊 Loading {len(dataset)} fields into Neo4j...")
        
        with self.driver.session() as session:
            for item in dataset:
                field_name = item.get("field", "Unknown")
                skills = item.get("skills", [])
                level = item.get("level", "Entry")
                
                print(f"  ↳ Creating Field: {field_name} with {len(skills)} skills")
                
                # Create Field node
                session.run("""
                    MERGE (f:Field {name: $field_name})
                    SET f.description = $description
                """, field_name=field_name, description=item.get("description", ""))
                
                # Create Skill nodes and relationships
                for skill in skills:
                    session.run("""
                        MERGE (s:Skill {name: $skill_name})
                        MERGE (f:Field {name: $field_name})
                        MERGE (s)-[r:REQUIRED_FOR]->(f)
                        SET r.level = $level
                    """, skill_name=skill, field_name=field_name, level=level)
            
            print(f"✓ Neo4j: Loaded {len(dataset)} field-skill mappings with relationships")
            
            # Verify what was created
            result = session.run("MATCH (s:Skill)-[r:REQUIRED_FOR]->(f:Field) RETURN count(r) as total")
            total_rels = result.single()["total"]
            print(f"✓ Neo4j: Created {total_rels} REQUIRED_FOR relationships in graph")
    
    def extract_cv_skills(self, cv_text):
        """Extract skills from CV by matching against known skills in graph"""
        with self.driver.session() as session:
            # Get all skills from graph
            result = session.run("MATCH (s:Skill) RETURN s.name as skill")
            known_skills = [record["skill"].lower() for record in result]
            
            # Simple matching - check if skill appears in CV
            cv_lower = cv_text.lower()
            found_skills = []
            
            for skill in known_skills:
                if skill in cv_lower:
                    found_skills.append(skill.title())
            
            return found_skills
    
    def create_person_profile(self, person_id, name, skills):
        """Create a person node with their skills"""
        with self.driver.session() as session:
            # Create Person node
            session.run("""
                MERGE (p:Person {id: $person_id})
                SET p.name = $name
            """, person_id=person_id, name=name)
            
            # Link to skills
            for skill in skills:
                session.run("""
                    MATCH (p:Person {id: $person_id})
                    MERGE (s:Skill {name: $skill_name})
                    MERGE (p)-[:HAS_SKILL]->(s)
                """, person_id=person_id, skill_name=skill)
            
            print(f"✓ Created profile for {name} with {len(skills)} skills")
    
    def evaluate_skills(self, person_skills):
        """Evaluate skills against fields in the graph"""
        with self.driver.session() as session:
            evaluation = []
            
            # Get all fields
            result = session.run("MATCH (f:Field) RETURN DISTINCT f.name as field")
            fields = [record["field"] for record in result]
            
            print(f"🔍 Neo4j Query: Evaluating {len(person_skills)} skills against {len(fields)} fields in graph")
            
            for field in fields:
                # Count matching skills for this field
                match_query = """
                    MATCH (s:Skill)-[:REQUIRED_FOR]->(f:Field {name: $field_name})
                    WHERE s.name IN $person_skills
                    RETURN count(s) as matched,
                           collect(s.name) as matched_skills
                """
                print(f"  ↳ Neo4j: Checking field '{field}'")
                
                match_result = session.run(match_query, field_name=field, person_skills=person_skills)
                match_data = match_result.single()
                
                # Get total required skills for field
                total_query = """
                    MATCH (s:Skill)-[:REQUIRED_FOR]->(f:Field {name: $field_name})
                    RETURN count(s) as total,
                           collect(s.name) as all_skills
                """
                total_result = session.run(total_query, field_name=field)
                total_data = total_result.single()
                
                matched = match_data["matched"]
                total = total_data["total"]
                
                if total > 0:
                    score = (matched / total) * 100
                    print(f"    ✓ {matched}/{total} skills matched ({score:.1f}%)")
                    
                    evaluation.append({
                        "field": field,
                        "matched_skills": match_data["matched_skills"],
                        "total_required": total,
                        "score": round(score, 1),
                        "missing_skills": [s for s in total_data["all_skills"] 
                                         if s not in person_skills]
                    })
            
            # Sort by score
            evaluation.sort(key=lambda x: x["score"], reverse=True)
            print(f"✓ Neo4j: Best match is '{evaluation[0]['field']}' with {evaluation[0]['score']:.1f}%")
            return evaluation
    
    def get_field_recommendations(self, person_skills):
        """Get field recommendations based on skills"""
        evaluation = self.evaluate_skills(person_skills)
        
        # Get top 3 matches
        top_matches = evaluation[:3]
        
        recommendations = []
        for match in top_matches:
            if match["score"] > 30:  # At least 30% match
                recommendations.append({
                    "field": match["field"],
                    "match_percentage": match["score"],
                    "your_skills": match["matched_skills"],
                    "skills_to_learn": match["missing_skills"][:5]  # Top 5 missing
                })
        
        return recommendations
    
    def find_similar_profiles(self, person_skills, limit=5):
        """Find people with similar skill sets"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
                WHERE s.name IN $skills
                WITH p, count(s) as common_skills
                WHERE common_skills > 0
                RETURN p.name as name, 
                       p.id as id,
                       common_skills
                ORDER BY common_skills DESC
                LIMIT $limit
            """, skills=person_skills, limit=limit)
            
            return [{"name": r["name"], "id": r["id"], "common_skills": r["common_skills"]} 
                    for r in result]
    
    def get_graph_stats(self):
        """Get graph statistics"""
        with self.driver.session() as session:
            stats = {}
            
            # Count nodes
            result = session.run("MATCH (s:Skill) RETURN count(s) as count")
            stats["skills"] = result.single()["count"]
            
            result = session.run("MATCH (f:Field) RETURN count(f) as count")
            stats["fields"] = result.single()["count"]
            
            result = session.run("MATCH (p:Person) RETURN count(p) as count")
            stats["people"] = result.single()["count"]
            
            # Count relationships
            result = session.run("MATCH ()-[r:REQUIRED_FOR]->() RETURN count(r) as count")
            stats["skill_field_links"] = result.single()["count"]
            
            result = session.run("MATCH ()-[r:HAS_SKILL]->() RETURN count(r) as count")
            stats["person_skill_links"] = result.single()["count"]
            
            return stats
    
    def clear_all_data(self):
        """Clear all data from Neo4j"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("✓ Cleared all Neo4j data")
    
    def close(self):
        """Close Neo4j connection"""
        if self.driver:
            self.driver.close()
            print("✓ Neo4j connection closed")

# Global instance
neo4j_skills = Neo4jSkillsManager()
