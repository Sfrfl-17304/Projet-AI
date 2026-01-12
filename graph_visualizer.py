"""
Knowledge Graph Visualizer - Generate graph data for user skills
"""

class SkillsGraphVisualizer:
    def __init__(self, neo4j_manager):
        self.neo4j = neo4j_manager
    
    def get_person_graph_data(self, person_skills):
        """Get graph data for visualization of person's skills and field connections"""
        if not person_skills:
            return {"nodes": [], "edges": []}
        
        nodes = []
        edges = []
        node_ids = set()
        
        # Add center node for the person
        nodes.append({
            "id": "user",
            "label": "You",
            "type": "person",
            "size": 40,
            "color": "#06B6D4"  # Cyan
        })
        node_ids.add("user")
        
        # Query Neo4j for skill connections
        with self.neo4j.driver.session() as session:
            for skill in person_skills:
                skill_id = f"skill_{skill.replace(' ', '_')}"
                
                if skill_id not in node_ids:
                    # Add skill node
                    nodes.append({
                        "id": skill_id,
                        "label": skill,
                        "type": "skill",
                        "size": 25,
                        "color": "#8B5CF6"  # Purple
                    })
                    node_ids.add(skill_id)
                    
                    # Edge from user to skill
                    edges.append({
                        "from": "user",
                        "to": skill_id,
                        "label": "has",
                        "color": "#6B7A91"
                    })
                
                # Get fields this skill connects to
                result = session.run("""
                    MATCH (s:Skill {name: $skill_name})-[r:REQUIRED_FOR]->(f:Field)
                    RETURN f.name as field, r.level as level
                """, skill_name=skill)
                
                for record in result:
                    field = record["field"]
                    field_id = f"field_{field.replace(' ', '_')}"
                    
                    if field_id not in node_ids:
                        # Add field node
                        nodes.append({
                            "id": field_id,
                            "label": field,
                            "type": "field",
                            "size": 35,
                            "color": "#10B981"  # Emerald
                        })
                        node_ids.add(field_id)
                    
                    # Edge from skill to field
                    edges.append({
                        "from": skill_id,
                        "to": field_id,
                        "label": record["level"],
                        "color": "#9CA8B8",
                        "dashes": True
                    })
        
        return {"nodes": nodes, "edges": edges}
    
    def get_field_distribution(self, person_skills):
        """Get skill distribution across fields"""
        distribution = []
        
        with self.neo4j.driver.session() as session:
            # Get all fields
            fields_result = session.run("MATCH (f:Field) RETURN f.name as field")
            fields = [r["field"] for r in fields_result]
            
            for field in fields:
                # Count skills for this field
                result = session.run("""
                    MATCH (s:Skill)-[:REQUIRED_FOR]->(f:Field {name: $field_name})
                    WHERE s.name IN $person_skills
                    RETURN count(s) as count
                """, field_name=field, person_skills=person_skills)
                
                count = result.single()["count"]
                if count > 0:
                    distribution.append({
                        "field": field,
                        "skills_count": count
                    })
        
        distribution.sort(key=lambda x: x["skills_count"], reverse=True)
        return distribution
