import asyncio
import logging
from BD.services import MongoDBService, Neo4jService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_integration():
    """Test all services directly (without FastAPI)"""
    
    print("\n" + "="*60)
    print("TESTING BD ↔ BACKEND INTEGRATION")
    print("="*60)
    
    mongo = None
    neo4j = None
    
    try:
        # Initialize services
        mongo = MongoDBService()
        neo4j = Neo4jService()
        
        # Test 1: Get all roles
        print("\n[TEST 1] Get all roles...")
        roles = mongo.get_all_roles()
        print(f"✓ Retrieved {len(roles)} roles")
        for r in roles:
            print(f"  - {r.name} ({r.category})")
        
        # Test 2: Get all skills
        print("\n[TEST 2] Get all skills...")
        skills = mongo.get_all_skills()
        print(f"✓ Retrieved {len(skills)} skills")
        for s in skills:
            print(f"  - {s.name} [{s.difficulty}] (demand: {s.demand_level})")
        
        # Test 3: Get role skills (Neo4j)
        print("\n[TEST 3] Get skills for 'Python Developer'...")
        role_skills = neo4j.get_role_skills("Python Developer")
        print(f"✓ Retrieved {len(role_skills)} role skills")
        for skill in role_skills:
            print(f"  - {skill.get('name')} ({skill.get('difficulty')})")
        
        # Test 4: Get learning path (Neo4j)
        print("\n[TEST 4] Get learning path (python-101 → machine-learning)...")
        path = neo4j.get_learning_path("python-101", "machine-learning")
        print(f"✓ Learning path: {path}")
        
        # Test 5: Get career path (Neo4j)
        print("\n[TEST 5] Get career path from 'Python Developer'...")
        career = neo4j.get_career_path("Python Developer")
        print(f"✓ Career path: {' → '.join(career)}")
        
        # Test 6: Get prerequisites (Neo4j)
        print("\n[TEST 6] Get prerequisites for 'machine-learning'...")
        prereqs = neo4j.get_prerequisites("machine-learning")
        print(f"✓ Prerequisites: {prereqs}")
        
        # Test 7: Get resources
        print("\n[TEST 7] Get resources for 'python-101'...")
        resources = mongo.get_resources_by_skill("python-101")
        print(f"✓ Retrieved {len(resources)} resources")
        for r in resources:
            print(f"  - {r.title} ({r.provider})")
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nBD is ready to integrate with Backend!\n")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if mongo:
            mongo.close()
        if neo4j:
            neo4j.close()

if __name__ == "__main__":
    asyncio.run(test_integration())