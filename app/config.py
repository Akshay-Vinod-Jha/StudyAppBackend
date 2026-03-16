"""
Configuration file for Flask application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    MONGODB_URI = os.getenv('MONGODB_URI')
    DB_NAME = os.getenv('DB_NAME', 'study_buddy_db')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')
    
    # JWT Configuration
    JWT_EXPIRATION_HOURS = 24
    
    # CORS Configuration - includes local dev, Vercel frontend, and any custom domain
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://127.0.0.1:5500',
        'http://localhost:5500',
        'http://localhost:5173',
        'https://study-app-frontend-psi.vercel.app',  # Production Vercel frontend
    ]
    # Allow extra origins via ALLOWED_ORIGINS env var (comma-separated)
    if os.getenv('ALLOWED_ORIGINS'):
        CORS_ORIGINS.extend([o.strip() for o in os.getenv('ALLOWED_ORIGINS', '').split(',') if o.strip()])
