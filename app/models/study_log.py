"""
Study Log Model
"""
from app.utils.db import Database
from app.utils.helpers import get_current_datetime
from bson import ObjectId
from datetime import datetime, timedelta

class StudyLog:
    """Study log model for tracking study sessions"""
    
    collection_name = 'study_logs'
    
    @staticmethod
    def create(user_id, subject_id, hours_studied, date=None, notes=''):
        """Create a new study log"""
        db = Database.get_db()
        
        if date is None:
            date = get_current_datetime()
        
        log_data = {
            'user_id': ObjectId(user_id),
            'subject_id': ObjectId(subject_id),
            'hours_studied': float(hours_studied),
            'date': date,
            'notes': notes,
            'created_at': get_current_datetime()
        }
        
        result = db[StudyLog.collection_name].insert_one(log_data)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_user(user_id, days=30):
        """Get study logs for a user (default last 30 days)"""
        db = Database.get_db()
        start_date = datetime.utcnow() - timedelta(days=days)
        
        logs = db[StudyLog.collection_name].find({
            'user_id': ObjectId(user_id),
            'date': {'$gte': start_date}
        }).sort('date', -1)
        
        return list(logs)
    
    @staticmethod
    def find_by_subject(subject_id):
        """Get all study logs for a subject"""
        db = Database.get_db()
        logs = db[StudyLog.collection_name].find({'subject_id': ObjectId(subject_id)}).sort('date', -1)
        return list(logs)
    
    @staticmethod
    def get_total_hours(user_id, subject_id=None):
        """Get total hours studied"""
        db = Database.get_db()
        
        query = {'user_id': ObjectId(user_id)}
        if subject_id:
            query['subject_id'] = ObjectId(subject_id)
        
        pipeline = [
            {'$match': query},
            {'$group': {
                '_id': None,
                'total_hours': {'$sum': '$hours_studied'}
            }}
        ]
        
        result = list(db[StudyLog.collection_name].aggregate(pipeline))
        return result[0]['total_hours'] if result else 0
    
    @staticmethod
    def delete(log_id):
        """Delete study log"""
        db = Database.get_db()
        result = db[StudyLog.collection_name].delete_one({'_id': ObjectId(log_id)})
        return result.deleted_count > 0
