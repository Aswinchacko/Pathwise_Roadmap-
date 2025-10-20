# Project Recommendation Service 🎯

AI-powered microservice that recommends projects based on user's aims and goals.

## Features

- **AI-Powered** (optional): Uses Groq API for intelligent recommendations
- **Rule-Based Fallback**: Works without API keys using NLP matching
- **Real Microservice**: Independent Flask service with REST API
- **Fast & Free**: Groq API is free and blazing fast

## Quick Start

1. **Install dependencies**:
```bash
cd project_recommendation_service
pip install -r requirements.txt
```

2. **Run the service**:
```bash
# Option 1: Use batch file
start_project_recommendation_service.bat

# Option 2: Direct run
python main.py
```

3. **Service runs on**: `http://localhost:5003`

## API Endpoints

### 1. Get Recommendations
```bash
POST /api/recommend
Content-Type: application/json

{
  "aim": "I want to build web applications with React",
  "limit": 5
}
```

**Response**:
```json
{
  "success": true,
  "aim": "I want to build web applications with React",
  "method": "ai-powered",
  "recommendations": [
    {
      "id": 1,
      "title": "React E-commerce Platform",
      "description": "Build a full-stack e-commerce application...",
      "difficulty": "Intermediate",
      "category": "web-dev",
      "skills": ["react", "nodejs", "javascript"],
      "rating": 4.8,
      "students": 1247
    }
  ],
  "total": 5
}
```

### 2. Get All Projects
```bash
GET /api/projects
GET /api/projects?category=ai-ml
GET /api/projects?difficulty=beginner
```

### 3. Get Specific Project
```bash
GET /api/projects/1
```

### 4. Health Check
```bash
GET /health
```

## AI Setup (Optional)

For better recommendations:

1. Get free API key from [Groq Console](https://console.groq.com)
2. Add to `.env`:
```
GROQ_API_KEY=gsk_your_key_here
```

3. Restart service

**Without API key**: Uses rule-based matching (still works great!)
**With API key**: Uses Mixtral-8x7b for smarter recommendations

## Test It

```bash
# Test with curl
curl -X POST http://localhost:5003/api/recommend \
  -H "Content-Type: application/json" \
  -d "{\"aim\": \"learn machine learning and AI\"}"

# Test health
curl http://localhost:5003/health
```

## Integration with Frontend

The service is automatically called from `Projects.jsx` when user enters their aim.

## How It Works

1. **User enters aim**: "I want to become a full-stack developer"
2. **Service receives request**: POST to `/api/recommend`
3. **AI analyzes aim**: Matches against project database
4. **Returns ranked projects**: Based on relevance, skills, difficulty
5. **Frontend displays**: Personalized project cards

## Architecture

```
Frontend (React)
    ↓
[HTTP POST with aim]
    ↓
Project Recommendation Service (Flask:5003)
    ↓
[Groq AI or Rule-Based Engine]
    ↓
[Ranked Project List]
    ↓
Frontend displays recommendations
```

## Extending the Service

Add more projects in `PROJECTS_DB` in `main.py`:

```python
{
    "id": 11,
    "title": "Your New Project",
    "description": "Project description",
    "difficulty": "Intermediate",
    "category": "web-dev",
    "skills": ["skill1", "skill2"],
    "rating": 4.5,
    "students": 100,
    "duration": "4 weeks",
    "topics": ["topic1", "topic2"]
}
```

