# 📊 System Diagram - Project Recommendation Service

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                          USER INTERACTION                             │
│                                                                       │
│  User opens: http://localhost:5173/projects                          │
│  User types: "I want to become a full-stack developer"               │
│  User clicks: "Get Recommendations" button                           │
│                                                                       │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │
                                 │ (1) HTTP POST Request
                                 │ URL: http://localhost:5003/api/recommend
                                 │ Body: { aim: "...", limit: 5 }
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│               PROJECT RECOMMENDATION SERVICE                          │
│                    (Flask on Port 5003)                               │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                     ENDPOINT ROUTING                          │   │
│  │  POST /api/recommend      → recommend_projects()             │   │
│  │  GET  /api/projects       → get_all_projects()               │   │
│  │  GET  /api/projects/:id   → get_project(id)                  │   │
│  │  GET  /health             → health_check()                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                │                                      │
│                                ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              RECOMMENDATION ENGINE                            │   │
│  │                                                                │   │
│  │  ┌────────────────────┐         ┌─────────────────────┐     │   │
│  │  │   AI MODE          │         │  RULE-BASED MODE    │     │   │
│  │  │   (Primary)        │   OR    │  (Fallback)         │     │   │
│  │  ├────────────────────┤         ├─────────────────────┤     │   │
│  │  │ if GROQ_API_KEY:   │         │ if no API key:      │     │   │
│  │  │   ↓                │         │   ↓                 │     │   │
│  │  │ 1. Format prompt   │         │ 1. Tokenize aim     │     │   │
│  │  │ 2. Call Groq API   │         │ 2. Score projects:  │     │   │
│  │  │ 3. Get ranked IDs  │         │    - Skills: +5     │     │   │
│  │  │ 4. Map to projects │         │    - Topics: +4     │     │   │
│  │  │                    │         │    - Category: +3   │     │   │
│  │  │ Model:             │         │ 3. Sort by score    │     │   │
│  │  │ Mixtral-8x7b       │         │ 4. Return top N     │     │   │
│  │  │ Speed: ~500ms      │         │ Speed: ~10ms        │     │   │
│  │  └────────────────────┘         └─────────────────────┘     │   │
│  │                                                                │   │
│  └──────────────────────┬─────────────────────────────────────────┘
│                         │                                            │
│                         ▼                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                   PROJECTS DATABASE                          │   │
│  │                                                                │   │
│  │  Project 1: React E-commerce Platform                        │   │
│  │    - skills: [react, nodejs, mongodb]                        │   │
│  │    - difficulty: Intermediate                                │   │
│  │    - rating: 4.8                                             │   │
│  │                                                                │   │
│  │  Project 2: Machine Learning Model                           │   │
│  │    - skills: [python, ml, scikit-learn]                     │   │
│  │    - difficulty: Advanced                                    │   │
│  │    - rating: 4.9                                             │   │
│  │                                                                │   │
│  │  ... (10 total projects)                                     │   │
│  │                                                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │
                                 │ (2) HTTP Response
                                 │ Status: 200 OK
                                 │ Body: { success: true, 
                                 │        recommendations: [...] }
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                     FRONTEND PROCESSING                               │
│                    (React Component)                                  │
│                                                                       │
│  Projects.jsx receives response:                                     │
│  1. Updates state: setRecommendations(data.recommendations)          │
│  2. Shows method badge: "🤖 AI-Powered" or "🎯 Smart Match"         │
│  3. Renders project cards with animations                            │
│                                                                       │
└────────────────────────────────┬──────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                                                                       │
│                        DISPLAY RESULTS                                │
│                                                                       │
│  User sees:                                                           │
│  ✅ 5 personalized project recommendations                           │
│  ✅ Each with title, description, skills, rating                     │
│  ✅ Smooth animations and loading states                             │
│  ✅ Skill tags showing required technologies                         │
│  ✅ Duration and difficulty badges                                   │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Request/Response Example

### Request Flow
```javascript
// Frontend (Projects.jsx)
const response = await fetch('http://localhost:5003/api/recommend', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    aim: "I want to become a full-stack developer",
    limit: 5
  })
})
```

### Backend Processing
```python
# Backend (main.py)
@app.route('/api/recommend', methods=['POST'])
def recommend_projects():
    data = request.get_json()
    aim = data.get('aim')
    
    # Try AI first
    recommendations = recommend_with_groq(aim)
    
    # Fall back to rules if AI unavailable
    if recommendations is None:
        recommendations = recommend_with_rules(aim)
    
    return jsonify({
        "success": True,
        "recommendations": recommendations
    })
```

### Response Flow
```json
{
  "success": true,
  "aim": "I want to become a full-stack developer",
  "method": "ai-powered",
  "recommendations": [
    {
      "id": 1,
      "title": "React E-commerce Platform",
      "description": "Build a full-stack e-commerce application...",
      "skills": ["react", "nodejs", "mongodb"],
      "difficulty": "Intermediate",
      "rating": 4.8,
      "duration": "6 weeks"
    },
    // ... 4 more projects
  ],
  "total": 5
}
```

## Component Interaction

```
┌─────────────────┐
│   Projects.jsx  │
│   Component     │
└────────┬────────┘
         │
         ├─ useState hooks:
         │  - userAim
         │  - recommendations
         │  - loading
         │  - recommendationMethod
         │
         ├─ useEffect:
         │  └─ fetchAllProjects() on mount
         │
         ├─ Functions:
         │  ├─ getRecommendations()
         │  │  └─ POST to /api/recommend
         │  │
         │  ├─ filterProjects(category)
         │  │  └─ Filter by category/difficulty
         │  │
         │  └─ handleKeyPress(e)
         │     └─ Enter key triggers search
         │
         └─ Render:
            ├─ Header
            ├─ Aim Input Section
            │  ├─ Input field
            │  ├─ Get Recommendations button
            │  └─ Method badge
            ├─ Filter tabs
            └─ Project grid
               ├─ Top 3 projects
               └─ Remaining projects
```

## Data Flow Diagram

```
User Input
    ↓
[State: userAim]
    ↓
getRecommendations()
    ↓
[State: loading = true]
    ↓
HTTP POST → Microservice
    ↓
AI/Rule Engine
    ↓
Project Ranking
    ↓
HTTP Response ← Microservice
    ↓
[State: recommendations = data]
[State: loading = false]
[State: recommendationMethod = data.method]
    ↓
React Re-render
    ↓
Display Results
```

## Technology Stack Layers

```
┌─────────────────────────────────────────────┐
│           PRESENTATION LAYER                 │
│  - React Components (Projects.jsx)          │
│  - Framer Motion (Animations)               │
│  - CSS3 (Styling)                            │
│  - Lucide Icons                              │
└─────────────────┬───────────────────────────┘
                  │ HTTP/JSON
┌─────────────────▼───────────────────────────┐
│           APPLICATION LAYER                  │
│  - Flask REST API                            │
│  - Request/Response Handling                 │
│  - CORS Middleware                           │
│  - Error Handling                            │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           BUSINESS LOGIC LAYER               │
│  - Recommendation Engines:                   │
│    • AI Engine (Groq)                        │
│    • Rule-Based Engine                       │
│  - Scoring Algorithms                        │
│  - Data Processing                           │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           DATA LAYER                         │
│  - Projects Database (in-memory)            │
│  - Project Schema                            │
│  - Data Models                               │
└─────────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           EXTERNAL SERVICES                  │
│  - Groq API (Mixtral-8x7b)                  │
│  - Future: MongoDB, Redis, etc.             │
└─────────────────────────────────────────────┘
```

## Microservice Characteristics

```
┌────────────────────────────────────────────┐
│  MICROSERVICE ARCHITECTURE                  │
├────────────────────────────────────────────┤
│  ✅ Independent Deployment                 │
│     - Own process                          │
│     - Own port (5003)                      │
│     - Own start/stop                       │
│                                             │
│  ✅ Service Boundaries                     │
│     - Clear API contract                   │
│     - RESTful endpoints                    │
│     - JSON communication                   │
│                                             │
│  ✅ Technology Independence                │
│     - Python backend                       │
│     - React frontend                       │
│     - Any client can consume               │
│                                             │
│  ✅ Scalability                            │
│     - Stateless design                     │
│     - Horizontal scaling                   │
│     - Load balancing ready                 │
│                                             │
│  ✅ Fault Isolation                        │
│     - Service failure doesn't crash app    │
│     - Graceful error handling              │
│     - Fallback mechanisms                  │
│                                             │
│  ✅ Independent Evolution                  │
│     - Can update without frontend changes  │
│     - Versioned API                        │
│     - Backward compatibility               │
└────────────────────────────────────────────┘
```

## Deployment Architecture

```
Development:
┌────────────────────────┐     ┌────────────────────────┐
│  Frontend              │     │  Microservice          │
│  http://localhost:5173 │────▶│  http://localhost:5003 │
│  (Vite Dev Server)     │     │  (Flask Dev Server)    │
└────────────────────────┘     └────────────────────────┘

Production:
┌────────────────────────┐     ┌────────────────────────┐
│  Frontend              │     │  Microservice          │
│  (Nginx/Vercel)        │────▶│  (Gunicorn/Docker)     │
│  https://app.com       │     │  https://api.app.com   │
└────────────────────────┘     └────────────────────────┘
                                         │
                                         ▼
                                ┌────────────────────┐
                                │  External Services │
                                │  - Groq API        │
                                │  - MongoDB         │
                                │  - Redis Cache     │
                                └────────────────────┘
```

This diagram shows the complete system architecture and data flow!

