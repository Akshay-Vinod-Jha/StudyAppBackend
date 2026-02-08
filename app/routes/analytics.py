"""
Analytics Routes
"""
from flask import Blueprint, request, jsonify
from app.models.study_log import StudyLog
from app.models.subject import Subject
from app.utils.helpers import verify_token, serialize_doc
from collections import defaultdict

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

def get_user_from_token():
    """Helper to get user_id from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    return verify_token(token)


@analytics_bp.route('/overview', methods=['GET'])
def get_overview():
    """Get study overview for user"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        days = int(request.args.get('days', 30))
        
        # Get all logs
        logs = StudyLog.find_by_user(user_id, days=days)
        
        # Get all subjects
        subjects = Subject.find_by_user(user_id)
        subject_map = {str(s['_id']): s['name'] for s in subjects}
        
        # Calculate hours and sessions per subject
        subject_stats = defaultdict(lambda: {'hours': 0, 'sessions': 0})
        daily_stats = defaultdict(float)
        
        for log in logs:
            subject_id = str(log['subject_id'])
            subject_stats[subject_id]['hours'] += log['hours_studied']
            subject_stats[subject_id]['sessions'] += 1
            
            # Group by date for daily hours
            log_date = log['date'].strftime('%Y-%m-%d')
            daily_stats[log_date] += log['hours_studied']
        
        # Format by_subject data
        by_subject = [
            {
                'subject_name': subject_map.get(sid, 'Unknown'),
                'total_hours': round(stats['hours'], 2),
                'sessions_count': stats['sessions']
            }
            for sid, stats in subject_stats.items()
        ]
        
        # Format daily_hours data
        daily_hours = [
            {
                'date': date,
                'total_hours': round(hours, 2)
            }
            for date, hours in sorted(daily_stats.items())
        ]
        
        # Calculate total hours
        total_hours = sum(stats['hours'] for stats in subject_stats.values())
        
        # Calculate average hours per day
        avg_hours = total_hours / days if days > 0 else 0
        
        return jsonify({
            'total_hours': round(total_hours, 2),
            'average_per_day': round(avg_hours, 2),
            'subjects_count': len(subjects),
            'logs_count': len(logs),
            'by_subject': by_subject,
            'daily_hours': daily_hours
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@analytics_bp.route('/subject/<subject_id>', methods=['GET'])
def get_subject_analytics(subject_id):
    """Get analytics for a specific subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Get subject
        subject = Subject.find_by_id(subject_id)
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        # Get logs for this subject
        logs = StudyLog.find_by_subject(subject_id)
        
        # Calculate total hours
        total_hours = sum(log['hours_studied'] for log in logs)
        
        # Get study sessions count
        sessions_count = len(logs)
        
        return jsonify({
            'subject': serialize_doc(subject),
            'total_hours': total_hours,
            'sessions_count': sessions_count,
            'logs': serialize_doc(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
