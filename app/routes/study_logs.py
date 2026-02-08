"""
Study Logs Routes
"""
from flask import Blueprint, request, jsonify
from app.models.study_log import StudyLog
from app.utils.helpers import verify_token, serialize_doc
from datetime import datetime

study_logs_bp = Blueprint('study_logs', __name__, url_prefix='/api/study-logs')

def get_user_from_token():
    """Helper to get user_id from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    return verify_token(token)


@study_logs_bp.route('/', methods=['GET'])
def get_study_logs():
    """Get study logs for logged-in user"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        days = int(request.args.get('days', 30))
        logs = StudyLog.find_by_user(user_id, days=days)
        
        return jsonify({'logs': serialize_doc(logs)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@study_logs_bp.route('/', methods=['POST'])
def create_study_log():
    """Create a new study log"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        required_fields = ['subject_id', 'hours_studied']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Parse date if provided
        date = None
        if 'date' in data:
            date = datetime.fromisoformat(data['date'])
        
        log_id = StudyLog.create(
            user_id=user_id,
            subject_id=data['subject_id'],
            hours_studied=data['hours_studied'],
            date=date,
            notes=data.get('notes', '')
        )
        
        return jsonify({
            'message': 'Study log created successfully',
            'log_id': log_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@study_logs_bp.route('/subject/<subject_id>', methods=['GET'])
def get_logs_by_subject(subject_id):
    """Get study logs for a specific subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        logs = StudyLog.find_by_subject(subject_id)
        return jsonify({'logs': serialize_doc(logs)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@study_logs_bp.route('/total', methods=['GET'])
def get_total_hours():
    """Get total hours studied"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        subject_id = request.args.get('subject_id')
        total = StudyLog.get_total_hours(user_id, subject_id)
        
        return jsonify({'total_hours': total}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@study_logs_bp.route('/<log_id>', methods=['DELETE'])
def delete_study_log(log_id):
    """Delete a study log"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        success = StudyLog.delete(log_id)
        
        if success:
            return jsonify({'message': 'Study log deleted successfully'}), 200
        else:
            return jsonify({'error': 'Study log not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
