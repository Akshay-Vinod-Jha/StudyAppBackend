"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.utils.db import Database

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Disable strict slashes to prevent redirects
    app.url_map.strict_slashes = False
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": Config.CORS_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Initialize database
    Database.initialize()
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.subjects import subjects_bp
    from app.routes.notes import notes_bp
    from app.routes.study_logs import study_logs_bp
    from app.routes.analytics import analytics_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(study_logs_bp)
    app.register_blueprint(analytics_bp)
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'message': 'Study Buddy API is running'}, 200
    
    @app.route('/', methods=['GET'])
    def index():
        return {
            'name': 'Study Buddy API',
            'version': '1.0.0',
            'endpoints': [
                '/api/auth/signup',
                '/api/auth/login',
                '/api/subjects',
                '/api/notes',
                '/api/study-logs',
                '/api/analytics'
            ]
        }, 200
    
    return app
