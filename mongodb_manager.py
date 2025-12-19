"""
MongoDB Connection Manager
"""
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Connect to MongoDB"""
        mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        mongodb_db = os.getenv("MONGODB_DB", "rag_db")
        
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[mongodb_db]
        print(f"✓ Connected to MongoDB: {mongodb_db}")
        return self.db
    
    def get_collection(self, collection_name):
        """Get a specific collection"""
        if self.db is None:
            self.connect()
        return self.db[collection_name]
    
    def close(self):
        """Close connection"""
        if self.client:
            self.client.close()
            print("✓ MongoDB connection closed")

# Global instance
mongo = MongoDB()
