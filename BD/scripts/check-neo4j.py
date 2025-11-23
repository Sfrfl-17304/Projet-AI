from BD.services import Neo4jService

def main():
    neo4j = Neo4jService()
    
    print("------ LEARNING PATHS ------")
    path = neo4j.get_learning_path("python-101", "machine-learning")
    print(f"Path: {path}")
    
    print("\n------ ROLE SKILLS ------")
    skills = neo4j.get_role_skills("Python Developer")
    for s in skills:
        print(f"- {s['name']} ({s['difficulty']})")
    
    print("\n------ CAREER PATH ------")
    career = neo4j.get_career_path("Python Developer")
    print(f"Path: {' -> '.join(career)}")
    
    neo4j.close()

if __name__ == "__main__":
    main()