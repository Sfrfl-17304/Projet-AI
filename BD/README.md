# BD - Database & Knowledge Graph Layer

Track 1 implementation for SkillAtlas AI project.

## Overview

- **MongoDB**: Stores roles, skills, learning resources, user profiles, roadmaps
- **Neo4j**: Graph database for skill relationships and career paths

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Edit `.env`:
```
MONGO_URL=mongodb://localhost:27017
MONGO_DB_NAME=skillatlas
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=skillatlas123
```

### 3. Initialize Databases
```bash
python -m BD.scripts.init_databases
```

## Usage

### Verify MongoDB
```bash
python -m BD.scripts.check-mongo
```

### Verify Neo4j
```bash
python -m BD.scripts.check-neo4j
```

## API Routes

When integrated with Backend:

### Roles
- `GET /api/bd/roles` - Get all roles
- `GET /api/bd/roles/{role_name}` - Get role by name

### Skills
- `GET /api/bd/skills` - Get all skills
- `GET /api/bd/skills/{skill_id}` - Get skill by ID
- `GET /api/bd/skills/category/{category}` - Get skills by category

### Resources
- `GET /api/bd/resources/{skill_id}` - Get learning resources for skill

### Graph Queries
- `GET /api/bd/learning-path/{start_skill}/{end_skill}` - Get learning path
- `GET /api/bd/role/{role_name}/skills` - Get required skills for role
- `GET /api/bd/career-path/{start_role}` - Get career progression
- `GET /api/bd/prerequisites/{skill_id}` - Get prerequisite skills

## Models

### Role
```json
{
  "name": "string",
  "description": "string",
  "category": "string",
  "required_skills": [...],
  "average_salary": "string",
  "growth_rate": "string",
  "experience_level": "string",
  "responsibilities": [...],
  "tools": [...],
  "industries": [...]
}
```

### Skill
```json
{
  "id": "string",
  "name": "string",
  "category": "string",
  "description": "string",
  "difficulty": "string",
  "learning_time_hours": "int",
  "prerequisites": [...],
  "related_skills": [...],
  "resources": [...],
  "popularity_score": "int",
  "demand_level": "string"
}
```

## Services

### MongoDBService
- `get_all_roles()` - Fetch all roles
- `get_role_by_name(name)` - Fetch role by name
- `get_all_skills()` - Fetch all skills
- `get_skill_by_id(skill_id)` - Fetch skill by ID
- `get_resources_by_skill(skill_id)` - Fetch learning resources
- `get_user_profile(user_id)` - Fetch user profile
- `save_roadmap(roadmap)` - Save learning roadmap

### Neo4jService
- `get_learning_path(start, end)` - Get skill learning path
- `get_role_skills(role_name)` - Get skills for role
- `get_career_path(start_role)` - Get career progression
- `get_prerequisites(skill_id)` - Get prerequisite skills

## Project Structure

```
BD/
├── models/          # Pydantic models
├── services/        # MongoDB & Neo4j services
├── scripts/         # Data population & verification
├── api/             # FastAPI routes
└── config.py        # Configuration
```