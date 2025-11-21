# SkillAtlas Backend API

AI-Driven Career Guidance and Learning Roadmap Platform - Backend Service

## Features

- ✅ **FastAPI Framework** - Modern, fast, async Python web framework
- ✅ **User Authentication** - JWT-based signup/login with secure password hashing
- ✅ **MongoDB Integration** - Async database operations with Motor
- ✅ **Health Check** - API and database connectivity monitoring
- ✅ **Modular Architecture** - Organized routes, services, models, and config
- ✅ **Placeholder Endpoints** - Ready for AI/NLP and Neo4j integration
- ✅ **Testing Suite** - Pytest-based tests for auth and health endpoints
- ✅ **CORS Support** - Configured for frontend integration
- ✅ **Environment Config** - `.env` based configuration management

## Project Structure

```
Backend/
├── config/              # Configuration and database setup
│   ├── __init__.py
│   ├── settings.py      # Environment settings
│   └── database.py      # MongoDB connection
├── models/              # Pydantic data models
│   ├── __init__.py
│   └── user.py          # User and auth models
├── routes/              # API endpoints
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── health.py        # Health check endpoint
│   ├── skills.py        # Skill extraction (placeholder)
│   └── profile.py       # User profile management (placeholder)
├── services/            # Business logic
│   ├── __init__.py
│   ├── auth_service.py  # JWT and password handling
│   └── user_service.py  # User operations
├── tests/               # Unit tests
│   ├── __init__.py
│   ├── test_auth.py     # Auth endpoint tests
│   └── test_health.py   # Health check tests
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── pytest.ini           # Pytest configuration
└── README.md            # This file
```

## Prerequisites

- Python 3.9+
- MongoDB (local or cloud instance)
- Virtual environment tool (venv, conda, etc.)

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd Backend
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# venv\Scripts\activate   # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

**Important**: Update the following in `.env`:
- `SECRET_KEY` - Generate a secure key: `openssl rand -hex 32`
- `MONGODB_URL` - Your MongoDB connection string
- `ALLOWED_ORIGINS` - Your frontend URL(s)

### 4. Start MongoDB

Make sure MongoDB is running locally or you have a cloud connection.

**Local MongoDB:**
```bash
# Linux/Mac
sudo systemctl start mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 5. Run the Application

```bash
python main.py
# Or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Access Documentation

- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

- `GET /` - Root endpoint with API info
- `GET /health` - Health check (API + DB status)

### Authentication (`/auth`)

- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (requires auth)

### Skills (`/skills`) - **Placeholder**

- `POST /skills/extract` - Extract skills from CV (requires auth)
- `GET /skills/analyze` - Analyze skill gap for target role (requires auth)

### Profile (`/profile`) - **Placeholder**

- `GET /profile/me` - Get user profile (requires auth)
- `POST /profile/interests` - Submit interests for career matching (requires auth)
- `GET /profile/roadmap` - Get learning roadmap (requires auth)

## Testing

Run the test suite:

```bash
pytest
# With coverage
pytest --cov=. --cov-report=html
# Verbose output
pytest -v
```

## Usage Examples

### 1. Signup

```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "full_name": "John Doe",
    "password": "securepass123"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepass123"
```

### 3. Get Current User (with token)

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

## Next Steps for Integration

### AI/NLP Integration (Track 2)

The following endpoints are placeholders ready for integration:

1. **Skill Extraction** (`POST /skills/extract`)
   - Integrate NLP model to parse CV
   - Extract and normalize skills
   - Store in user profile

2. **Career Matching** (`POST /profile/interests`)
   - Integrate LLM for interest analysis
   - Generate career recommendations
   - Use embeddings for semantic matching

### Neo4j Integration (Track 1)

1. **Knowledge Graph Queries**
   - Add Neo4j driver to `config/database.py`
   - Implement skill gap analysis using graph queries
   - Generate learning roadmaps from graph data

2. **Endpoints to enhance:**
   - `GET /skills/analyze` - Query Neo4j for role requirements
   - `GET /profile/roadmap` - Generate roadmap from graph

### Frontend Integration (Track 4)

- Base URL: `http://localhost:8000`
- All endpoints return JSON
- Authentication uses Bearer token in `Authorization` header
- CORS configured for `localhost:3000` and `localhost:5173`

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name | SkillAtlas API |
| `APP_VERSION` | API version | 1.0.0 |
| `DEBUG` | Debug mode | True |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `SECRET_KEY` | JWT secret key | (change in production) |
| `ALGORITHM` | JWT algorithm | HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | 30 |
| `MONGODB_URL` | MongoDB connection | mongodb://localhost:27017 |
| `MONGODB_DB_NAME` | Database name | skillatlas |
| `ALLOWED_ORIGINS` | CORS origins | localhost:3000,localhost:5173 |

## Security Notes

- ⚠️ Change `SECRET_KEY` in production
- ⚠️ Use HTTPS in production
- ⚠️ Implement rate limiting for production
- ⚠️ Add input validation and sanitization
- ⚠️ Use environment-specific `.env` files

## Team Responsibilities

- **Track 1 (Data/Neo4j)**: Implement knowledge graph queries in `routes/skills.py`
- **Track 2 (AI/NLP)**: Integrate models in `services/` and update skill endpoints
- **Track 3 (Backend)**: Enhance existing endpoints, add error handling, optimize performance
- **Track 4 (Frontend)**: Consume these APIs in the UI

## Troubleshooting

**MongoDB connection fails:**
- Check if MongoDB is running: `systemctl status mongod`
- Verify `MONGODB_URL` in `.env`
- Check firewall/network settings

**Import errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Port already in use:**
- Change `PORT` in `.env`
- Kill process using port: `lsof -ti:8000 | xargs kill -9`

## License

UIR - 4th Year AI Course Project

## Contributors

- Hanae OUAZZANI-AMRI (119276) - Data & Knowledge Graph
- Oubahmane Mohamed Omar (120119) - AI/NLP and RAG
- Akoujan Ali (118588) - Backend APIs Integration
- Ramou Nassim (120068) - Frontend
