"""
Subject Routes
"""
from flask import Blueprint, request, jsonify
from app.models.subject import Subject
from app.utils.helpers import verify_token, serialize_doc

subjects_bp = Blueprint('subjects', __name__, url_prefix='/api/subjects')

def get_user_from_token():
    """Helper to get user_id from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    return verify_token(token)


@subjects_bp.route('/', methods=['GET'])
def get_subjects():
    """Get all subjects for logged-in user"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        subjects = Subject.find_by_user(user_id)
        return jsonify({'subjects': serialize_doc(subjects)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subjects_bp.route('/', methods=['POST'])
def create_subject():
    """Create a new subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        if 'name' not in data:
            return jsonify({'error': 'Subject name required'}), 400
        
        subject_id = Subject.create(
            user_id=user_id,
            name=data['name'],
            color=data.get('color', '#3498db')
        )
        
        return jsonify({
            'message': 'Subject created successfully',
            'subject_id': subject_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subjects_bp.route('/<subject_id>', methods=['GET'])
def get_subject(subject_id):
    """Get a specific subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        subject = Subject.find_by_id(subject_id)
        
        if not subject:
            return jsonify({'error': 'Subject not found'}), 404
        
        return jsonify({'subject': serialize_doc(subject)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subjects_bp.route('/<subject_id>', methods=['PUT'])
def update_subject(subject_id):
    """Update a subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'color' in data:
            update_data['color'] = data['color']
        
        if not update_data:
            return jsonify({'error': 'No data to update'}), 400
        
        success = Subject.update(subject_id, update_data)
        
        if success:
            return jsonify({'message': 'Subject updated successfully'}), 200
        else:
            return jsonify({'error': 'Subject not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@subjects_bp.route('/<subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    """Delete a subject"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        success = Subject.delete(subject_id)
        
        if success:
            return jsonify({'message': 'Subject deleted successfully'}), 200
        else:
            return jsonify({'error': 'Subject not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
