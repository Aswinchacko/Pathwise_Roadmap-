# 🚀 Quick Start - Project Recommendation Service

## 1. Install Dependencies (One-time)

```bash
cd project_recommendation_service
pip install -r requirements.txt
```

## 2. Start the Service

### Option A: Use Batch File
```bash
start_project_recommendation_service.bat
```

### Option B: Manual Start
```bash
cd project_recommendation_service
python main.py
```

Service runs on: **http://localhost:5003**

## 3. Test the Service

```bash
# Run comprehensive tests
python test_project_recommendation.py

# Or use batch file
test_project_recommendation.bat
```

## 4. Start Frontend

```bash
# In a new terminal
start_frontend.bat
```

Then navigate to the **Projects** page and try entering your goal!

## API Examples

### Get Recommendations
```bash
curl -X POST http://localhost:5003/api/recommend \
  -H "Content-Type: application/json" \
  -d "{\"aim\": \"I want to become a full-stack developer\"}"
```

### Get All Projects
```bash
curl http://localhost:5003/api/projects
```

### Get Specific Project
```bash
curl http://localhost:5003/api/projects/1
```

## Optional: Enable AI Mode

For smarter recommendations:

1. Get free API key from [Groq Console](https://console.groq.com)
2. Add to `.env`:
   ```
   GROQ_API_KEY=gsk_your_key_here
   ```
3. Restart service

**Note**: Works great without API key using rule-based matching!

## Test Examples

Try these aims in the frontend:
- "I want to become a full-stack web developer"
- "I'm interested in machine learning and AI"
- "I want to learn data visualization"
- "I'm a beginner looking to start with Python"
- "I want to build mobile applications"

## Troubleshooting

**Port already in use?**
Change in `.env`:
```
PORT=5004
```

**Frontend can't connect?**
Make sure service is running and check browser console for CORS errors.

**Want to add more projects?**
Edit `PROJECTS_DB` in `main.py` and add your project objects.

