# 🚀 How to Start LinkedIn Mentor Scraping Service

## Quick Start

### Option 1: Using Batch File (Recommended)
```bash
# From project root
start_linkedin_mentor_service.bat
```

### Option 2: Manual Start
```bash
# Terminal 1: Navigate to service directory
cd linkedin_mentor_service

# Install dependencies (first time only)
pip install -r requirements.txt

# Start the service
python start_simple.py
```

### Option 3: Direct Uvicorn
```bash
cd linkedin_mentor_service
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8005
```

## Verify Service is Running

```bash
# Test from project root
python test_api_quick.py

# Or use curl
curl http://localhost:8005/api/mentors/health
```

Expected response:
```json
{
  "service": "LinkedIn Mentor Scraping Service",
  "status": "healthy",
  "mongodb": "connected",
  "browser": "chrome"
}
```

## Test the Scraping API

Once the service is running, you can test it:

### Using curl:
```bash
curl -X POST http://localhost:8005/api/mentors/scrape \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": \"test_user\", \"limit\": 5}"
```

### Using Python:
```python
import requests

response = requests.post(
    'http://localhost:8005/api/mentors/scrape',
    json={
        'user_id': 'test_user',
        'limit': 5,
        'refresh_cache': False
    }
)

print(response.json())
```

### Using the Frontend:
1. Start the dashboard: `cd dashboard && npm run dev`
2. Login to http://localhost:5173
3. Create a roadmap (e.g., "Become a React Developer")
4. Click "Mentors" page
5. The frontend will automatically call the API

## API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8005/docs
- **Alternative Docs**: http://localhost:8005/redoc

## Troubleshooting

### Service Won't Start

**Check Python version:**
```bash
python --version
# Should be Python 3.8 or higher
```

**Reinstall dependencies:**
```bash
cd linkedin_mentor_service
pip install -r requirements.txt --force-reinstall
```

**Check port availability:**
```bash
netstat -ano | findstr :8005
```

### MongoDB Not Connected

**Start MongoDB:**
```bash
mongod
```

**Verify MongoDB is running:**
```bash
mongo --eval "db.getMongo()"
```

**Check MongoDB connection in service:**
The service expects MongoDB at `mongodb://localhost:27017`

### Chrome Driver Issues

**Install/update webdriver-manager:**
```bash
pip install webdriver-manager --upgrade
```

**Install Chrome:**
Download from https://www.google.com/chrome/

### "No roadmap found" Error

1. Ensure you have a user roadmap in MongoDB:
```bash
mongo
use pathwise
db.roadmap.find({source: "user_generated"}).pretty()
```

2. Create a roadmap via the frontend:
   - Login → Roadmap page → Create roadmap

## Service Endpoints

### Health Check
```
GET http://localhost:8005/api/mentors/health
```

### Scrape Mentors
```
POST http://localhost:8005/api/mentors/scrape
Body: {
  "user_id": "user123",
  "limit": 10,
  "experience_level": "intermediate",
  "refresh_cache": false
}
```

### Clear Cache
```
DELETE http://localhost:8005/api/mentors/cache/{user_id}
```

### Root
```
GET http://localhost:8005/
```

## Environment Variables (Optional)

Create a `.env` file in `linkedin_mentor_service/`:

```env
MONGODB_URI=mongodb://localhost:27017
PORT=8005
CHROME_HEADLESS=true
```

## Logs

The service outputs logs to console:
- `✅` - Success messages
- `❌` - Error messages
- `🔍` - Scraping progress
- `📋` - Data extraction

## Performance Notes

- **First scrape**: 30-60 seconds (scraping LinkedIn)
- **Cached results**: < 1 second (from MongoDB)
- **Default limit**: 10 profiles
- **Maximum limit**: 20 profiles

## Next Steps

After starting the service:

1. ✅ Service running on http://localhost:8005
2. ✅ MongoDB connected
3. ✅ Chrome driver ready
4. 🔜 Start frontend: `cd dashboard && npm run dev`
5. 🔜 Create roadmap in app
6. 🔜 Visit Mentors page to see results!

## Support

- **Full docs**: `LINKEDIN_MENTOR_SCRAPING_SETUP.md`
- **Quick start**: `QUICK_START_LINKEDIN_MENTORS.md`
- **Complete guide**: `IMPLEMENTATION_COMPLETE.md`

## Common Commands

```bash
# Start service (background)
start_linkedin_mentor_service.bat

# Test service
python test_api_quick.py

# Check health
curl http://localhost:8005/api/mentors/health

# View logs (if running in background)
# Check the terminal where service is running

# Stop service
# Press Ctrl+C in the terminal running the service
```

---

**Service URL**: http://localhost:8005
**API Docs**: http://localhost:8005/docs
**Health Check**: http://localhost:8005/api/mentors/health


