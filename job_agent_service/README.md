# PathWise Job Agent Service

Real-world job fetching service that aggregates jobs from **LinkedIn, Indeed, Glassdoor, ZipRecruiter** and uses **Groq AI** to match them to user's learning roadmap and career goals.

## 🚀 Features

- ✅ **Real Job Listings** from multiple sources
- ✅ **AI-Powered Matching** using Groq to score job relevance
- ✅ **Automatic User Profiling** from roadmap data
- ✅ **Smart Caching** to reduce API calls
- ✅ **Multiple API Sources** with automatic fallback
- ✅ **Salary Information** and remote job filtering

## 📊 Job Sources

### 1. **JSearch API (RapidAPI)** - Primary Source
- Aggregates from: LinkedIn, Indeed, Glassdoor, ZipRecruiter, etc.
- **Free Tier**: 250 requests/month
- **Signup**: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch

### 2. **Adzuna API** - Backup Source
- Real jobs from multiple countries
- **Free Tier**: 250 requests/month
- **Signup**: https://developer.adzuna.com/

### 3. **AI-Generated Jobs** - Fallback
- Uses Groq AI to generate realistic job listings
- Based on current market trends
- Activated when APIs are unavailable

## 🛠️ Setup

### 1. Install Dependencies
```bash
cd job_agent_service
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `job_agent_service/.env`:
```env
# Required: Copy from your existing chatbot_service/.env
GROQ_API_KEY=gsk_your_key_here

# Optional but Recommended: For real job listings
RAPIDAPI_KEY=your_rapidapi_key_here

# Optional: Backup job source
ADZUNA_APP_ID=your_app_id
ADZUNA_API_KEY=your_api_key

# MongoDB
MONGODB_URI=mongodb://localhost:27017/

# Port
PORT=5007
```

### 3. Get API Keys (Optional but Recommended)

#### RapidAPI (Recommended - Real Jobs from LinkedIn/Indeed)
1. Go to https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
2. Sign up (Free)
3. Subscribe to free tier (250 requests/month)
4. Copy your RapidAPI key
5. Add to `.env`: `RAPIDAPI_KEY=your_key`

#### Adzuna (Optional - Backup Source)
1. Go to https://developer.adzuna.com/
2. Sign up for free account
3. Get API credentials
4. Add to `.env`: `ADZUNA_APP_ID` and `ADZUNA_API_KEY`

**Note**: The service works without these APIs using Groq AI to generate realistic jobs, but real APIs provide actual live job listings.

### 4. Start the Service
```bash
# Windows
start_job_agent.bat

# Or directly
cd job_agent_service
python main.py
```

Service will be available at:
- API: http://localhost:5007
- Docs: http://localhost:5007/docs

## 📡 API Endpoints

### POST `/api/jobs/search`
Search for jobs with custom parameters.

**Request**:
```json
{
  "user_id": "user123",
  "query": "React Developer",
  "location": "United States",
  "remote": true,
  "limit": 10,
  "use_ai_matching": true
}
```

**Response**:
```json
{
  "success": true,
  "query": "React Developer",
  "jobs": [
    {
      "id": "job_123",
      "title": "Senior React Developer",
      "company": "Google",
      "location": "San Francisco, CA",
      "salary": "$150k-$200k/year",
      "description": "Build scalable web applications...",
      "requirements": ["React", "TypeScript", "Node.js"],
      "url": "https://linkedin.com/jobs/...",
      "posted_date": "2024-10-15T00:00:00Z",
      "remote": true,
      "match_score": 92,
      "match_reason": "Strong match with React and TypeScript skills",
      "source": "LinkedIn"
    }
  ],
  "total": 10,
  "ai_matched": true,
  "sources_used": ["JSearch (LinkedIn/Indeed/Glassdoor)"]
}
```

### GET `/api/jobs/user/{user_id}`
Get recommended jobs based on user's roadmap automatically.

**Response**: Same as above, but jobs are matched to user's learning path.

### GET `/health`
Check service status and configuration.

## 🤖 How AI Matching Works

1. **Profile Building**: Extracts user's skills, goals, and experience from their roadmap
2. **Job Fetching**: Retrieves real jobs from multiple APIs
3. **AI Scoring**: Groq AI analyzes each job and scores 0-100 based on:
   - Skill alignment with user's roadmap
   - Experience level fit
   - Career goal relevance
   - Learning path compatibility
4. **Ranking**: Jobs are sorted by match score
5. **Caching**: Results cached for 6 hours to reduce API calls

## 🧪 Testing

```bash
# Start the service first
start_job_agent.bat

# In another terminal, run tests
python test_job_agent.py
```

## 🔄 Integration with Frontend

The Jobs.jsx component automatically connects to this service. Users see:
- Real job listings from LinkedIn, Indeed, etc.
- Match scores showing relevance to their roadmap
- One-click "Get Jobs" based on their learning path
- Filtered results by location, remote, experience level

## 💡 Tips

1. **Free Tier Sufficient**: 250 requests/month from RapidAPI is usually enough
2. **Caching**: Jobs are cached for 6 hours to save API calls
3. **Fallback**: If APIs unavailable, AI generates realistic jobs
4. **Multiple Sources**: Service tries JSearch → Adzuna → AI (in that order)
5. **Roadmap Integration**: Works best when users have an active roadmap

## 🔧 Configuration Options

| Environment Variable | Required | Default | Description |
|---------------------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | For AI matching and fallback jobs |
| `RAPIDAPI_KEY` | ⚪ Recommended | - | Real jobs from LinkedIn/Indeed |
| `ADZUNA_APP_ID` | ⚪ Optional | - | Backup job source |
| `ADZUNA_API_KEY` | ⚪ Optional | - | Backup job source |
| `MONGODB_URI` | ⚪ Optional | `mongodb://localhost:27017/` | For caching |
| `PORT` | ⚪ Optional | `5007` | Service port |

## 📈 Performance

- **API Response Time**: 2-5 seconds
- **AI Matching**: +3-5 seconds
- **Cache Hit**: <1 second
- **Fallback Generation**: 5-10 seconds

## 🆘 Troubleshooting

### "No jobs found"
- Check API keys are configured correctly
- Verify you're not exceeding free tier limits
- Service will fallback to AI-generated jobs automatically

### "AI matching failed"
- Ensure GROQ_API_KEY is set
- Jobs will still be returned, just without match scores

### "MongoDB connection failed"
- Service works without MongoDB (no caching)
- Jobs will still be fetched normally

## 🚀 Next Steps

After starting the service:
1. The frontend Jobs page will automatically use this service
2. Users can click "Get AI Jobs" to fetch personalized listings
3. Jobs are matched to their roadmap skills
4. Match scores show relevance (higher = better fit)

Enjoy real-world job opportunities! 🎉

