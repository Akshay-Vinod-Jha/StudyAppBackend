"""
Notes Routes
"""
from flask import Blueprint, request, jsonify
from app.models.note import Note
from app.utils.helpers import verify_token, serialize_doc

notes_bp = Blueprint('notes', __name__, url_prefix='/api/notes')

def get_user_from_token():
    """Helper to get user_id from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    return verify_token(token)


@notes_bp.route('/', methods=['GET'])
def get_notes():
    """Get all notes for logged-in user"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        # Check if filtering by subject
        subject_id = request.args.get('subject_id')
        
        if subject_id:
            notes = Note.find_by_subject(subject_id)
        else:
            notes = Note.find_by_user(user_id)
        
        return jsonify({'notes': serialize_doc(notes)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notes_bp.route('/', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        required_fields = ['subject_id', 'title', 'content']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        note_id = Note.create(
            user_id=user_id,
            subject_id=data['subject_id'],
            title=data['title'],
            content=data['content']
        )
        
        return jsonify({
            'message': 'Note created successfully',
            'note_id': note_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notes_bp.route('/<note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        note = Note.find_by_id(note_id)
        
        if not note:
            return jsonify({'error': 'Note not found'}), 404
        
        return jsonify({'note': serialize_doc(note)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notes_bp.route('/<note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a note"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'content' in data:
            update_data['content'] = data['content']
        if 'subject_id' in data:
            update_data['subject_id'] = data['subject_id']
        
        if not update_data:
            return jsonify({'error': 'No data to update'}), 400
        
        success = Note.update(note_id, update_data)
        
        if success:
            return jsonify({'message': 'Note updated successfully'}), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@notes_bp.route('/<note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a note"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        success = Note.delete(note_id)
        
        if success:
            return jsonify({'message': 'Note deleted successfully'}), 200
        else:
            return jsonify({'error': 'Note not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
