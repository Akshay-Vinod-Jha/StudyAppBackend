"""
Subject Model
"""
from app.utils.db import Database
from app.utils.helpers import get_current_datetime
from bson import ObjectId

class Subject:
    """Subject model for managing study subjects"""
    
    collection_name = 'subjects'
    
    @staticmethod
    def create(user_id, name, color='#3498db'):
        """Create a new subject"""
        db = Database.get_db()
        
        subject_data = {
            'user_id': ObjectId(user_id),
            'name': name,
            'color': color,
            'created_at': get_current_datetime(),
            'updated_at': get_current_datetime()
        }
        
        result = db[Subject.collection_name].insert_one(subject_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id):
        """Get all subjects for a user"""
        db = Database.get_db()
        subjects = db[Subject.collection_name].find({'user_id': ObjectId(user_id)})
        return list(subjects)
    
    @staticmethod
    def find_by_id(subject_id):
        """Find subject by ID"""
        db = Database.get_db()
        return db[Subject.collection_name].find_one({'_id': ObjectId(subject_id)})
    
    @staticmethod
    def update(subject_id, update_data):
        """Update subject"""
        db = Database.get_db()
        update_data['updated_at'] = get_current_datetime()
        
        result = db[Subject.collection_name].update_one(
            {'_id': ObjectId(subject_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(subject_id):
        """Delete subject"""
        db = Database.get_db()
        result = db[Subject.collection_name].delete_one({'_id': ObjectId(subject_id)})
        return result.deleted_count > 0
