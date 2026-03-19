"""
Chatbot Routes using Groq API
"""
from flask import Blueprint, request, jsonify
from app.config import Config
from app.utils.helpers import verify_token

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Lazy-initialize Groq client to avoid compatibility issues
_groq_client = None

def get_groq_client():
    """Lazy-initialize and return Groq client"""
    global _groq_client
    if _groq_client is None:
        if not Config.GROQ_API_KEY:
            print("ERROR: GROQ_API_KEY not configured")
            return None
        
        try:
            from groq import Groq
            _groq_client = Groq(api_key=Config.GROQ_API_KEY)
            print("DEBUG: Groq client initialized successfully")
        except Exception as e:
            print(f"ERROR initializing Groq client: {str(e)}")
            return None
    
    return _groq_client

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
        
        # Check API key
        groq_client = get_groq_client()
        if not groq_client:
            print("ERROR: Groq API key not configured")
            return jsonify({'error': 'Groq API not configured'}), 503
        
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
        
        print(f"DEBUG: Sending {len(messages)} messages to Groq")
        print(f"DEBUG: Using model: mixtral-8x7b-32768")
        
        # Call Groq API with error handling
        try:
            response = groq_client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=messages,
                max_tokens=1024,
                temperature=0.7,
            )
            
            bot_response = response.choices[0].message.content
            
            print(f"DEBUG: Chatbot response generated successfully")
            
            return jsonify({
                'message': user_message,
                'response': bot_response,
                'timestamp': None
            }), 200
        
        except Exception as groq_err:
            groq_error_msg = str(groq_err)
            print(f"ERROR calling Groq API: {groq_error_msg}")
            import traceback
            print(traceback.format_exc())
            return jsonify({
                'error': f'Groq API error: {groq_error_msg}'
            }), 503
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        traceback_str = traceback.format_exc()
        print(f"ERROR in chatbot: {error_msg}")
        print(f"TRACEBACK: {traceback_str}")
        
        # Return user-friendly error
        return jsonify({
            'error': 'An unexpected error occurred. The chatbot service may be temporarily unavailable.',
            'details': error_msg
        }), 500


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
