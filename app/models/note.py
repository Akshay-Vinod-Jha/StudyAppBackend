"""
Note Model
"""
from app.utils.db import Database
from app.utils.helpers import get_current_datetime
from bson import ObjectId

class Note:
    """Note model for managing study notes"""
    
    collection_name = 'notes'
    
    @staticmethod
    def create(user_id, subject_id, title, content):
        """Create a new note"""
        db = Database.get_db()
        
        note_data = {
            'user_id': ObjectId(user_id),
            'subject_id': ObjectId(subject_id),
            'title': title,
            'content': content,
            'created_at': get_current_datetime(),
            'updated_at': get_current_datetime()
        }
        
        result = db[Note.collection_name].insert_one(note_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id):
        """Get all notes for a user"""
        db = Database.get_db()
        notes = db[Note.collection_name].find({'user_id': ObjectId(user_id)}).sort('created_at', -1)
        return list(notes)
    
    @staticmethod
    def find_by_subject(subject_id):
        """Get all notes for a subject"""
        db = Database.get_db()
        notes = db[Note.collection_name].find({'subject_id': ObjectId(subject_id)}).sort('created_at', -1)
        return list(notes)
    
    @staticmethod
    def find_by_id(note_id):
        """Find note by ID"""
        db = Database.get_db()
        return db[Note.collection_name].find_one({'_id': ObjectId(note_id)})
    
    @staticmethod
    def update(note_id, update_data):
        """Update note"""
        db = Database.get_db()
        update_data['updated_at'] = get_current_datetime()
        
        result = db[Note.collection_name].update_one(
            {'_id': ObjectId(note_id)},
            {'$set': update_data}
        )
        return result.modified_count > 0
    
    @staticmethod
    def delete(note_id):
        """Delete note"""
        db = Database.get_db()
        result = db[Note.collection_name].delete_one({'_id': ObjectId(note_id)})
        return result.deleted_count > 0
