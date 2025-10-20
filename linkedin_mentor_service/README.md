# LinkedIn Mentor Scraping Service

A dedicated microservice for scraping LinkedIn mentor profiles based on user roadmap goals stored in MongoDB.

## Features

- 🔍 **Smart Scraping**: Uses Selenium + Chrome to scrape LinkedIn profiles via Google search
- 🎯 **MongoDB Integration**: Fetches user roadmap goals directly from MongoDB
- 💾 **Intelligent Caching**: Caches scraped mentors in MongoDB to avoid repeated scraping
- 🤖 **Human-like Behavior**: Random delays and user-agent rotation to avoid detection
- ⚡ **Fast API**: Built with FastAPI for high performance

## Architecture

```
User creates roadmap → Saved to MongoDB
                             ↓
User visits Mentors page → Triggers scraping
                             ↓
Service fetches roadmap goal from MongoDB
                             ↓
Scrapes LinkedIn via Google search
                             ↓
Caches results in MongoDB → Returns to frontend
```

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser installed
- MongoDB running on localhost:27017

### Setup

1. **Install dependencies**:
```bash
cd linkedin_mentor_service
pip install -r requirements.txt
```

2. **Start the service**:
```bash
# Windows
start_server.bat

# Linux/Mac
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8005
```

## API Endpoints

### 1. Scrape Mentors
```http
POST http://localhost:8005/api/mentors/scrape
Content-Type: application/json

{
  "user_id": "user123",
  "limit": 10,
  "experience_level": "intermediate",
  "refresh_cache": false
}
```

**Response**:
```json
{
  "success": true,
  "mentors": [
    {
      "name": "John Doe",
      "title": "Senior React Developer",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "profile_url": "https://linkedin.com/in/johndoe",
      "headline": "Senior React Developer at Tech Corp",
      "about": "Passionate about frontend development...",
      "experience_years": 8,
      "connections": "500+",
      "avatar_url": "https://...",
      "skills": ["React", "JavaScript", "TypeScript"],
      "scraped_at": "2025-10-17T10:30:00"
    }
  ],
  "search_query": "React Developer Frontend Development",
  "total_found": 10,
  "cached": false,
  "message": "Successfully scraped 10 mentors"
}
```

### 2. Clear Cache
```http
DELETE http://localhost:8005/api/mentors/cache/{user_id}
```

### 3. Health Check
```http
GET http://localhost:8005/api/mentors/health
```

## MongoDB Collections

### Input: `pathwise.roadmap`
Reads user roadmap goals:
```json
{
  "user_id": "user123",
  "goal": "Become a React Developer",
  "domain": "Frontend Development",
  "source": "user_generated"
}
```

### Output: `pathwise.mentors`
Stores scraped mentors:
```json
{
  "user_id": "user123",
  "search_query": "React Developer Frontend Development",
  "roadmap_goal": "Become a React Developer",
  "domain": "Frontend Development",
  "name": "John Doe",
  "title": "Senior React Developer",
  "profile_url": "https://linkedin.com/in/johndoe",
  "scraped_at": "2025-10-17T10:30:00"
}
```

## How It Works

1. **Fetches Roadmap Goal**: Queries MongoDB for user's latest roadmap
2. **Creates Search Query**: Combines `goal` + `domain` for LinkedIn search
3. **Google Search**: Uses Google to find LinkedIn profiles (more accessible)
4. **Profile Scraping**: Selenium scrapes each profile page for:
   - Name, Title, Company
   - Location, Connections
   - About section
   - Skills
   - Experience years
5. **Caching**: Saves results to MongoDB for future requests
6. **Returns Data**: Sends formatted mentor profiles to frontend

## Anti-Detection Features

- ✅ Headless Chrome with stealth options
- ✅ Random delays between requests (2-5 seconds)
- ✅ Realistic user-agent strings
- ✅ Google search as intermediary (less LinkedIn rate limiting)
- ✅ Intelligent caching to minimize scraping

## Configuration

Edit `main.py` to customize:

```python
# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017')

# Chrome options
chrome_options.add_argument('--headless')  # Remove for visible browser
chrome_options.add_argument('user-agent=...')  # Change user agent

# Delays
time.sleep(random.uniform(2, 5))  # Adjust delay range
```

## Troubleshooting

### Chrome Driver Issues
```bash
# Manually install ChromeDriver
pip install webdriver-manager --upgrade
```

### MongoDB Connection Errors
```bash
# Ensure MongoDB is running
mongod --version
```

### Rate Limiting
- Increase delays between requests
- Enable caching to reduce scraping
- Use VPN if IP is blocked

## Development

### Run in development mode:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8005
```

### Test the API:
```bash
curl -X POST http://localhost:8005/api/mentors/scrape \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "limit": 5}'
```

## Production Deployment

1. Set environment variables:
```bash
export MONGODB_URI="mongodb://production-host:27017"
export PORT=8005
```

2. Use production ASGI server:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. Consider using proxy rotation for large-scale scraping

## License

MIT License


