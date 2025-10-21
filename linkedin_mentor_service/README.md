# LinkedIn Mentor Service

A dedicated microservice for finding mentor profiles based on user roadmap goals.

## 🚀 Quick Start

Want **REAL LinkedIn profiles** matching your users' niche?

👉 **[Read REAL_PROFILES_SETUP.md](./REAL_PROFILES_SETUP.md)** (5 minutes setup)

## Features

- ✅ **Real Profiles**: Uses Serper API + Groq AI to find actual LinkedIn profiles
- 🎯 **Niche Matching**: Finds mentors in the exact same field as user's goal
- 👥 **Mid-Level Focus**: Filters out CEOs/CTOs, focuses on accessible mentors (4-10 years exp)
- 🇮🇳 **India-Focused**: Prioritizes Indian tech professionals from top companies
- 💾 **Smart Caching**: Caches results in MongoDB to save API calls
- 🔄 **Multi-Tier Fallback**: Real profiles → AI-generated → Static curated data

## Architecture

### With Serper API (Real Profiles - Recommended):
```
User creates roadmap → MongoDB
         ↓
User visits Mentors page
         ↓
Service reads roadmap goal → Searches Google (Serper API)
         ↓
Finds real LinkedIn URLs → Groq AI extracts data
         ↓
Filters mid-level profiles → Caches in MongoDB → Returns real profiles
```

### Without Serper API (AI-Generated Fallback):
```
User creates roadmap → MongoDB
         ↓
User visits Mentors page
         ↓
Service reads goal → Groq AI generates realistic profiles
         ↓
Caches in MongoDB → Returns AI profiles
```

## Installation

### Prerequisites
- Python 3.8+
- MongoDB running on localhost:27017
- (Optional) Serper API key for real profiles
- (Optional) Groq API key for AI features

### Quick Setup

**Option 1: With Real Profiles (Recommended)**

```bash
cd linkedin_mentor_service

# 1. Copy environment template
copy env.template .env

# 2. Edit .env and add your API keys:
#    SERPER_API_KEY=your_key_here
#    GROQ_API_KEY=your_key_here

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start service
python main.py
```

**Option 2: Without API Keys (Static Data)**

```bash
cd linkedin_mentor_service
pip install -r requirements.txt
python main.py
```

See **[REAL_PROFILES_SETUP.md](./REAL_PROFILES_SETUP.md)** for detailed setup instructions.

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

## Comparison: Real vs AI-Generated vs Static

| Feature | Real Profiles (Serper) | AI-Generated (Groq) | Static Curated |
|---------|------------------------|---------------------|----------------|
| **Profiles** | ✓ Real people on LinkedIn | AI-generated realistic profiles | Consistent curated data |
| **URLs** | ✓ Actual LinkedIn profiles | Generated profile slugs | Generated profile slugs |
| **Niche Match** | ✓ Exact match to user goal | ✓ Good match | Basic domain match |
| **Experience Level** | ✓ Mid-level (4-10 yrs) | ✓ Mid-level (4-10 yrs) | Mixed levels |
| **Companies** | ✓ Real Indian tech companies | ✓ Real company names | Real company names |
| **Setup Required** | Serper + Groq API keys | Groq API key only | None |
| **Cost** | $0-50/month | FREE | FREE |
| **Best For** | Production, real connections | MVP, testing | Demo, fallback |

## Which Mode Should I Use?

### Use Real Profiles (Serper API) if:
- ✓ You want users to find and connect with actual people
- ✓ You have a budget ($0-50/month for MVP)
- ✓ User trust and authenticity matter
- ✓ You're building for production

### Use AI-Generated (Groq only) if:
- ✓ You're in early development/testing
- ✓ You want realistic-looking data without cost
- ✓ You need placeholder mentors for UI testing
- ✓ Users won't actually contact mentors yet

### Use Static Curated if:
- ✓ You're just trying out the platform
- ✓ No API keys configured yet
- ✓ Need a quick demo

## Getting Started

1. **For Real Profiles**: Read [REAL_PROFILES_SETUP.md](./REAL_PROFILES_SETUP.md)
2. **For AI Mode**: Read [AI_SETUP.md](./AI_SETUP.md)
3. **For Static Mode**: Just run `python main.py`

## License

MIT License


