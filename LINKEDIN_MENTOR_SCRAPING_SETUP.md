# 🎯 LinkedIn Mentor Scraping System - Complete Setup

## Overview

A dedicated microservice that scrapes **real LinkedIn profiles** based on user roadmap goals stored in MongoDB. The system uses browser automation (Selenium + Chrome) to find and extract mentor profiles dynamically.

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Frontend  │────▶│  LinkedIn    │────▶│    MongoDB      │
│  (Mentors   │     │  Scraping    │     │   (pathwise)    │
│   Page)     │     │  Service     │     │                 │
└─────────────┘     │  Port: 8005  │     │  - roadmap      │
                    └──────────────┘     │  - mentors      │
                           │              └─────────────────┘
                           ▼
                    ┌──────────────┐
                    │   LinkedIn   │
                    │  (via Google)│
                    └──────────────┘
```

## Features

✅ **Real LinkedIn Scraping**: Uses Selenium to scrape actual LinkedIn profiles
✅ **MongoDB Integration**: Fetches user roadmap goals automatically
✅ **Smart Caching**: Stores scraped mentors to avoid repeated scraping
✅ **Google Search**: Uses Google as intermediary to avoid LinkedIn rate limits
✅ **Anti-Detection**: Headless Chrome with realistic delays and user agents
✅ **Clean Modern UI**: Redesigned Mentors page with professional look

## Setup Instructions

### 1. Install Chrome Browser

Make sure Chrome is installed on your system.

### 2. Setup LinkedIn Scraping Service

```bash
cd linkedin_mentor_service

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Ensure MongoDB is Running

```bash
# Check MongoDB status
mongod --version

# Start MongoDB (if not running)
# Windows: mongod --dbpath C:\data\db
# Linux: sudo systemctl start mongod
```

### 4. Start the Service

```bash
# Windows
start_server.bat

# Linux/Mac
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8005
```

The service will start on **http://localhost:8005**

### 5. Test the Service

```bash
python test_service.py
```

## API Documentation

### 1. Scrape Mentors

**Endpoint**: `POST /api/mentors/scrape`

**Request**:
```json
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
      "about": "Passionate frontend developer...",
      "experience_years": 8,
      "connections": "500+",
      "avatar_url": "https://...",
      "skills": ["React", "JavaScript", "TypeScript"],
      "scraped_at": "2025-10-17T10:30:00",
      "user_id": "user123",
      "roadmap_goal": "Become a React Developer",
      "domain": "Frontend Development"
    }
  ],
  "search_query": "React Developer Frontend Development",
  "total_found": 10,
  "cached": false,
  "message": "Successfully scraped 10 mentors"
}
```

### 2. Clear Cache

**Endpoint**: `DELETE /api/mentors/cache/{user_id}`

**Response**:
```json
{
  "success": true,
  "deleted_count": 10,
  "message": "Cleared 10 cached mentors"
}
```

### 3. Health Check

**Endpoint**: `GET /api/mentors/health`

**Response**:
```json
{
  "service": "LinkedIn Mentor Scraping Service",
  "status": "healthy",
  "mongodb": "connected",
  "browser": "chrome"
}
```

## How It Works

### 1. User Creates Roadmap

User creates a roadmap on the Roadmap page:
- Goal: "Become a React Developer"
- Domain: "Frontend Development"
- Stored in MongoDB: `pathwise.roadmap` collection

### 2. User Visits Mentors Page

Frontend component (`Mentors.jsx`) loads and calls the scraping service:

```javascript
const response = await fetch('http://localhost:8005/api/mentors/scrape', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user123',
    limit: 10
  })
})
```

### 3. Service Fetches Roadmap Goal

```python
# Query MongoDB for user's latest roadmap
user_roadmap = roadmap_collection.find_one(
    {"user_id": request.user_id, "source": "user_generated"},
    sort=[("created_at", -1)]
)

roadmap_goal = user_roadmap.get('goal')  # "Become a React Developer"
domain = user_roadmap.get('domain')       # "Frontend Development"
```

### 4. Creates Search Query

```python
search_query = f"{roadmap_goal} {domain}"
# Result: "Become a React Developer Frontend Development"
```

### 5. Scrapes LinkedIn Profiles

```python
# Use Google to find LinkedIn profiles
google_query = f'site:linkedin.com/in/ {search_query} mentor OR expert'
driver.get(f'https://www.google.com/search?q={google_query}')

# Extract LinkedIn URLs
profile_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="linkedin.com/in/"]')

# Scrape each profile
for profile_url in profile_links:
    driver.get(profile_url)
    
    # Extract data
    name = driver.find_element(By.CSS_SELECTOR, 'h1').text
    headline = driver.find_element(By.CSS_SELECTOR, '.headline').text
    # ... etc
```

### 6. Caches Results in MongoDB

```python
mentors_collection.update_one(
    {"profile_url": mentor['profile_url'], "user_id": user_id},
    {"$set": mentor},
    upsert=True
)
```

### 7. Returns to Frontend

Frontend displays mentors in a clean, modern grid layout.

## MongoDB Collections

### Input: `pathwise.roadmap`

```json
{
  "_id": ObjectId("..."),
  "user_id": "user123",
  "goal": "Become a React Developer",
  "domain": "Frontend Development",
  "source": "user_generated",
  "created_at": ISODate("2025-10-17T10:00:00Z")
}
```

### Output: `pathwise.mentors`

```json
{
  "_id": ObjectId("..."),
  "user_id": "user123",
  "search_query": "Become a React Developer Frontend Development",
  "roadmap_goal": "Become a React Developer",
  "domain": "Frontend Development",
  "name": "John Doe",
  "title": "Senior React Developer",
  "company": "Tech Corp",
  "location": "San Francisco, CA",
  "profile_url": "https://linkedin.com/in/johndoe",
  "headline": "Senior React Developer at Tech Corp",
  "about": "Passionate about...",
  "experience_years": 8,
  "connections": "500+",
  "avatar_url": "https://...",
  "skills": ["React", "JavaScript", "TypeScript"],
  "scraped_at": "2025-10-17T10:30:00"
}
```

## Frontend Integration

The Mentors page (`dashboard/src/pages/Mentors.jsx`) has been completely redesigned with:

✅ **Clean Modern UI**: White cards, subtle shadows, professional design
✅ **Real Profile Badges**: Shows "Real Profile" badge on each card
✅ **LinkedIn Integration**: Displays LinkedIn verification
✅ **Roadmap Context**: Shows the roadmap goal being used for search
✅ **Smart Filtering**: Search and experience level filters
✅ **Scraping Stats**: Shows real profiles count and cache status
✅ **Refresh Button**: Allows users to refresh mentors manually

## Scraping Details

### Profile Data Extracted

- ✅ Name
- ✅ Title/Headline
- ✅ Company (from headline)
- ✅ Location
- ✅ Number of Connections
- ✅ Profile Picture
- ✅ About Section
- ✅ Skills (up to 10)
- ✅ Estimated Experience Years
- ✅ Profile URL

### Anti-Detection Features

```python
# Headless Chrome
chrome_options.add_argument('--headless')

# Realistic User Agent
chrome_options.add_argument('user-agent=Mozilla/5.0 ...')

# Disable automation flags
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Random delays
time.sleep(random.uniform(2, 5))

# Google as intermediary (less rate limiting)
google_query = f'site:linkedin.com/in/ {search_query}'
```

## Troubleshooting

### Service Won't Start

```bash
# Check if port 8005 is already in use
netstat -ano | findstr :8005

# Install Chrome driver manually
pip install webdriver-manager --upgrade
```

### MongoDB Connection Error

```bash
# Ensure MongoDB is running
mongod --version

# Check connection string in main.py
mongo_client = MongoClient('mongodb://localhost:27017')
```

### Scraping Takes Too Long

```python
# Reduce limit in request
{"user_id": "user123", "limit": 5}  # Instead of 10

# Or use cached results
{"user_id": "user123", "refresh_cache": false}
```

### Rate Limiting from LinkedIn

- The service uses Google search as intermediary to reduce rate limiting
- Increase delays between requests in `main.py`
- Enable caching to minimize scraping
- Consider using a VPN if your IP is blocked

## Production Deployment

### 1. Environment Variables

```bash
export MONGODB_URI="mongodb://production-host:27017"
export PORT=8005
export CHROME_HEADLESS=true
```

### 2. Use Production Server

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8005
```

### 3. Add Proxy Rotation (Optional)

For large-scale scraping, consider adding proxy rotation:

```python
chrome_options.add_argument(f'--proxy-server={proxy_url}')
```

## Complete System Flow

```
1. User logs in → Dashboard
2. User creates roadmap → Stored in MongoDB (roadmap collection)
   - Goal: "Become a React Developer"
   - Domain: "Frontend Development"
3. User clicks "Mentors" page
4. Frontend calls LinkedIn Scraping Service (port 8005)
5. Service reads roadmap goal from MongoDB
6. Service scrapes LinkedIn via Google search
   - Searches: "Become a React Developer Frontend Development site:linkedin.com/in/"
   - Extracts profile URLs from Google results
   - Visits each LinkedIn profile and scrapes data
7. Service caches results in MongoDB (mentors collection)
8. Service returns mentors to frontend
9. Frontend displays mentors in clean grid layout
10. User can:
    - View LinkedIn profile (opens in new tab)
    - Contact mentor (future feature)
    - Search/filter mentors
    - Refresh to get new mentors
```

## Next Steps

- [ ] Add messaging/contact feature
- [ ] Implement mentor availability calendar
- [ ] Add mentor ratings and reviews
- [ ] Create mentor onboarding flow
- [ ] Add video call scheduling integration
- [ ] Implement mentor recommendation algorithm
- [ ] Add payment integration for mentorship sessions

## Support

For issues or questions:
1. Check service logs: `tail -f logs/scraping.log`
2. Test API: `python test_service.py`
3. Verify MongoDB: `mongo --eval "db.getMongo()"`
4. Check Chrome: `google-chrome --version`

## License

MIT License


