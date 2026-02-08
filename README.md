# Study Buddy App - Backend

Flask-based RESTful API backend for the Study Buddy App, providing authentication, data management, and analytics services.

## 📋 Overview

The backend is a Python Flask application that provides a complete REST API for managing users, subjects, notes, study logs, and analytics. It uses MongoDB for data persistence and JWT for secure authentication.

## 🛠️ Technology Stack

- **Flask 3.0.0** - Web framework
- **MongoDB** - NoSQL database (via PyMongo 4.6.1)
- **JWT** - Authentication (PyJWT 2.8.0)
- **BCrypt 4.1.2** - Password hashing
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Python-dotenv 1.0.0** - Environment variable management

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **MongoDB** - Either:
  - Local MongoDB installation, OR
  - MongoDB Atlas account (free tier available)
- **pip** - Python package manager

### Installation

1. **Navigate to the backend directory**

   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended)

   On Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Create a `.env` file** in the backend directory:

   ```env
   # MongoDB Configuration
   MONGODB_URI=mongodb://localhost:27017/
   # OR use MongoDB Atlas:
   # MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/

   DB_NAME=study_buddy_db

   # Flask Configuration
   SECRET_KEY=your-secret-key-here-change-in-production
   FLASK_ENV=development
   FLASK_DEBUG=True

   # Server Configuration
   HOST=0.0.0.0
   PORT=5000
   ```

2. **Update environment variables**
   - Replace `your-secret-key-here-change-in-production` with a strong secret key
   - Update `MONGODB_URI` with your MongoDB connection string
   - For production, set `FLASK_ENV=production` and `FLASK_DEBUG=False`

### MongoDB Setup

#### Option 1: Local MongoDB

1. **Install MongoDB** from https://www.mongodb.com/try/download/community
2. **Start MongoDB service**

   On Windows:

   ```bash
   net start MongoDB
   ```

   On macOS:

   ```bash
   brew services start mongodb-community
   ```

   On Linux:

   ```bash
   sudo systemctl start mongod
   ```

3. **Verify connection**
   ```bash
   mongosh
   ```

#### Option 2: MongoDB Atlas (Cloud)

1. Create a free account at https://www.mongodb.com/cloud/atlas
2. Create a new cluster (free tier M0)
3. Create a database user
4. Whitelist your IP address (or use 0.0.0.0/0 for development)
5. Get your connection string and update `MONGODB_URI` in `.env`

### Running the Server

Start the Flask development server:

```bash
python run.py
```

Or using Flask's CLI:

```bash
flask run
```

The API will be available at:

- **Local**: http://localhost:5000
- **Network**: http://[your-ip]:5000

You should see output like:

```
🚀 Starting Study Buddy API on http://0.0.0.0:5000
📚 Database: study_buddy_db
🔧 Environment: development
```

### Verify Installation

Test the health check endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "healthy",
  "message": "Study Buddy API is running"
}
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config.py             # Configuration settings
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── subject.py        # Subject model
│   │   ├── note.py           # Note model
│   │   └── study_log.py      # Study log model
│   ├── routes/               # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication routes
│   │   ├── subjects.py       # Subject routes
│   │   ├── notes.py          # Note routes
│   │   ├── study_logs.py     # Study log routes
│   │   └── analytics.py      # Analytics routes
│   └── utils/                # Utility modules
│       ├── __init__.py
│       ├── db.py             # Database connection
│       └── helpers.py        # Helper functions
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔌 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user (requires auth)

### Subjects

- `GET /api/subjects` - Get all subjects for user
- `POST /api/subjects` - Create new subject
- `GET /api/subjects/<id>` - Get subject by ID
- `PUT /api/subjects/<id>` - Update subject
- `DELETE /api/subjects/<id>` - Delete subject

### Notes

- `GET /api/notes` - Get all notes for user
- `POST /api/notes` - Create new note
- `GET /api/notes/<id>` - Get note by ID
- `PUT /api/notes/<id>` - Update note
- `DELETE /api/notes/<id>` - Delete note

### Study Logs

- `GET /api/study-logs` - Get all study logs for user
- `POST /api/study-logs` - Create new study log
- `GET /api/study-logs/<id>` - Get study log by ID
- `PUT /api/study-logs/<id>` - Update study log
- `DELETE /api/study-logs/<id>` - Delete study log

### Analytics

- `GET /api/analytics/overview` - Get study overview statistics
- `GET /api/analytics/subject-distribution` - Get study time by subject
- `GET /api/analytics/weekly-trends` - Get weekly study trends
- `GET /api/analytics/study-streak` - Get current study streak

### Health Check

- `GET /health` - API health status
- `GET /` - API information

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### How to authenticate:

1. **Register or login** to receive a JWT token
2. **Include the token** in the Authorization header for protected routes:
   ```
   Authorization: Bearer <your-jwt-token>
   ```

### Example using curl:

```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Use token
curl -X GET http://localhost:5000/api/subjects \
  -H "Authorization: Bearer <your-jwt-token>"
```

## 📊 Database Models

### User

- `_id` (ObjectId) - Unique identifier
- `username` (str) - Username
- `email` (str) - Email address (unique)
- `password_hash` (str) - Hashed password
- `created_at` (datetime) - Account creation date

### Subject

- `_id` (ObjectId) - Unique identifier
- `user_id` (ObjectId) - Reference to user
- `name` (str) - Subject name
- `color` (str) - Display color
- `created_at` (datetime) - Creation date

### Note

- `_id` (ObjectId) - Unique identifier
- `user_id` (ObjectId) - Reference to user
- `subject_id` (ObjectId) - Reference to subject
- `title` (str) - Note title
- `content` (str) - Note content
- `created_at` (datetime) - Creation date
- `updated_at` (datetime) - Last update date

### Study Log

- `_id` (ObjectId) - Unique identifier
- `user_id` (ObjectId) - Reference to user
- `subject_id` (ObjectId) - Reference to subject
- `duration` (int) - Duration in minutes
- `date` (datetime) - Study session date
- `notes` (str) - Optional session notes

## 🔧 Configuration Options

Edit `app/config.py` to customize:

- `SECRET_KEY` - JWT encryption key
- `MONGODB_URI` - Database connection string
- `DB_NAME` - Database name
- `FLASK_ENV` - Environment (development/production)
- `DEBUG` - Debug mode
- `HOST` - Server host
- `PORT` - Server port
- `JWT_EXPIRATION_HOURS` - Token expiration time
- `CORS_ORIGINS` - Allowed frontend origins

## 🐛 Troubleshooting

### MongoDB Connection Error

```
pymongo.errors.ServerSelectionTimeoutError
```

**Solutions:**

- Verify MongoDB is running: `mongosh` or check MongoDB Atlas dashboard
- Check `MONGODB_URI` in `.env` file
- Ensure firewall allows MongoDB connection (port 27017)
- For Atlas: verify IP whitelist and credentials

### Port Already in Use

```
OSError: [Errno 48] Address already in use
```

**Solutions:**

- Change `PORT` in `.env` file
- Kill process using port 5000:

  ```bash
  # On Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F

  # On macOS/Linux
  lsof -ti:5000 | xargs kill -9
  ```

### Import Errors

```
ModuleNotFoundError: No module named 'flask'
```

**Solutions:**

- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### JWT Token Issues

- Ensure `SECRET_KEY` is set in `.env`
- Check token is included in Authorization header
- Verify token hasn't expired (default: 24 hours)

## 🧪 Testing

Test API endpoints using:

- **curl** - Command line tool
- **Postman** - API testing platform
- **Thunder Client** - VS Code extension
- **Python requests** - For automated testing

Example test script:

```python
import requests

BASE_URL = "http://localhost:5000"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
})
print(response.json())
```

## 📦 Dependencies

```
Flask==3.0.0              # Web framework
flask-cors==4.0.0         # CORS support
pymongo==4.6.1            # MongoDB driver
dnspython==2.4.2          # DNS toolkit (for MongoDB)
python-dotenv==1.0.0      # Environment variables
bcrypt==4.1.2             # Password hashing
pyjwt==2.8.0              # JWT authentication
python-dateutil==2.8.2    # Date utilities
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Use strong `SECRET_KEY`
- [ ] Use production-grade WSGI server (Gunicorn, uWSGI)
- [ ] Configure proper CORS origins
- [ ] Set up environment variables securely
- [ ] Use MongoDB Atlas or managed MongoDB
- [ ] Enable HTTPS
- [ ] Set up logging and monitoring

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 🔗 Related Documentation

- [Main Project README](../README.md)
- [Frontend README](../frontend/README.md)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)

---

For questions or issues, please refer to the main project documentation or create an issue in the repository.
