"""
Main entry point for Flask application
"""
from app import create_app
from app.config import Config

app = create_app()

if __name__ == '__main__':
    print(f"🚀 Starting Study Buddy API on http://{Config.HOST}:{Config.PORT}")
    print(f"📚 Database: {Config.DB_NAME}")
    print(f"🔧 Environment: {Config.FLASK_ENV}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
