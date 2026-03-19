"""
Chatbot Routes using Groq API
"""
from flask import Blueprint, request, jsonify
from app.config import Config
from app.utils.helpers import verify_token
from groq import Groq

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Initialize Groq client
groq_client = Groq(api_key=Config.GROQ_API_KEY)

def get_user_from_token():
    """Helper to get user_id from token"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return None
    return verify_token(token)


@chatbot_bp.route('/chat', methods=['POST'])
def chat():
    """Chat with the Groq-powered chatbot"""
    try:
        user_id = get_user_from_token()
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get conversation history if provided
        conversation_history = data.get('history', [])
        
        # Build messages for the API
        messages = []
        
        # Add system prompt for study buddy context
        system_prompt = {
            "role": "system",
            "content": "You are a helpful study buddy assistant. You help students with their studies by explaining concepts, answering questions, and providing study tips. Be friendly, encouraging, and provide clear explanations. If a student asks for help with homework, guide them to understand rather than just giving answers."
        }
        messages.append(system_prompt)
        
        # Add conversation history
        for msg in conversation_history:
            if 'role' in msg and 'content' in msg:
                messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Call Groq API
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Free model available on Groq
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        
        bot_response = response.choices[0].message.content
        
        return jsonify({
            'message': user_message,
            'response': bot_response,
            'timestamp': None  # Can be added if needed
        }), 200
        
    except Exception as e:
        print(f"Chatbot error: {str(e)}")
        return jsonify({'error': f'Chatbot error: {str(e)}'}), 500


@chatbot_bp.route('/health', methods=['GET'])
def chatbot_health():
    """Check if chatbot service is available"""
    try:
        if not Config.GROQ_API_KEY:
            return jsonify({
                'status': 'unavailable',
                'message': 'Groq API key not configured'
            }), 503
        
        return jsonify({
            'status': 'available',
            'message': 'Chatbot service is online'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
