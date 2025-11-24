#!/usr/bin/env python3
"""Test database connections"""

import sys
from pymongo import MongoClient
from neo4j import GraphDatabase

# Test MongoDB
try:
    print("Testing MongoDB connection...")
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    client.server_info()  # Force connection
    db = client["skillatlas"]
    print(f"✅ MongoDB connected successfully")
    print(f"   Database: skillatlas")
    print(f"   Collections: {db.list_collection_names()}")
    client.close()
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    sys.exit(1)

# Test Neo4j
try:
    print("\nTesting Neo4j connection...")
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "skillatlas123"))
    with driver.session() as session:
        result = session.run("RETURN 1 AS test")
        record = result.single()
        print(f"✅ Neo4j connected successfully")
        print(f"   Test query result: {record['test']}")
    driver.close()
except Exception as e:
    print(f"❌ Neo4j connection failed: {e}")
    sys.exit(1)

print("\n🎉 All database connections successful!")
