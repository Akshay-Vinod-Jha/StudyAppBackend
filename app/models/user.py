"""
User Model
"""
from app.utils.db import Database
from app.utils.helpers import hash_password, get_current_datetime
from bson import ObjectId

class User:
    """User model for authentication and profile management"""
    
    collection_name = 'users'
    
    @staticmethod
    def create(name, email, password):
        """Create a new user"""
        db = Database.get_db()
        
        # Check if user already exists
        existing_user = db[User.collection_name].find_one({'email': email})
        if existing_user:
            return None
        
        user_data = {
            'name': name,
            'email': email,
            'password': hash_password(password),
            'created_at': get_current_datetime(),
            'updated_at': get_current_datetime()
        }
        
        result = db[User.collection_name].insert_one(user_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = Database.get_db()
        return db[User.collection_name].find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        db = Database.get_db()
        return db[User.collection_name].find_one({'_id': ObjectId(user_id)})
    
    @staticmethod
    def update(user_id, update_data):
        """Update user information"""
        db = Database.get_db()
        update_data['updated_at'] = get_current_datetime()
        
        result = db[User.collection_name].update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
