"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.utils.helpers import verify_password, generate_token, serialize_doc

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create user
        user_id = User.create(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        if not user_id:
            return jsonify({'error': 'User already exists'}), 409
        
        # Generate token
        token = generate_token(user_id)
        
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user_id': user_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password required'}), 400
        
        # Find user
        user = User.find_by_email(data['email'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Verify password
        if not verify_password(data['password'], user['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token
        token = generate_token(str(user['_id']))
        
        # Return user data (without password)
        user_data = serialize_doc(user)
        del user_data['password']
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile (requires token)"""
    try:
        # Get token from header
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        from app.utils.helpers import verify_token
        user_id = verify_token(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid token'}), 401
        
        # Get user
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Return user data (without password)
        user_data = serialize_doc(user)
        del user_data['password']
        
        return jsonify({'user': user_data}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
