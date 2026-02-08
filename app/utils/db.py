"""
Database connection and utilities
"""
from pymongo import MongoClient
from app.config import Config

class Database:
    """MongoDB Database connection handler"""
    client = None
    db = None
    
    @staticmethod
    def initialize():
        """Initialize MongoDB connection"""
        try:
            Database.client = MongoClient(Config.MONGODB_URI)
            Database.db = Database.client[Config.DB_NAME]
            
            # Test connection
            Database.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {Config.DB_NAME}")
            return True
        except Exception as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            return False
    
    @staticmethod
    def get_db():
        """Get database instance"""
        if Database.db is None:
            Database.initialize()
        return Database.db
    
    @staticmethod
    def close():
        """Close database connection"""
        if Database.client:
            Database.client.close()
            print("🔒 MongoDB connection closed")
