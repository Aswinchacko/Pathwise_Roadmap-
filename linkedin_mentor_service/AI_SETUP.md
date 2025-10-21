# AI-Powered Mentor Search Setup Guide

## 🎯 Overview

The mentor service now supports **TWO modes**:

1. **Real Profiles Mode** (Recommended): Uses **Serper API** + **Groq AI** to find actual LinkedIn profiles
2. **AI-Generated Mode** (Fallback): Uses **Groq API** alone to generate realistic profiles

**For real, original profiles → See [REAL_PROFILES_SETUP.md](./REAL_PROFILES_SETUP.md)**

## 🔧 Setup Steps

### 1. Get Groq API Key

1. Go to https://console.groq.com
2. Sign up (it's FREE)
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### 2. Configure Environment Variable

You can configure the Groq API key in TWO ways:

#### Option A: Copy from Existing Service (Recommended)

If you already have chatbot service running:

```bash
# The mentor service will automatically read from chatbot_service/.env
# No additional setup needed!
```

#### Option B: Create New .env File

Create `linkedin_mentor_service/.env`:

```bash
# AI-Powered Mentor Search Configuration
GROQ_API_KEY=gsk_your_actual_key_here
MONGODB_URI=mongodb://localhost:27017/
```

### 3. Install Dependencies

```bash
cd linkedin_mentor_service
pip install -r requirements.txt
```

### 4. Start the Service

```bash
# Option 1: Using Python directly
python main.py

# Option 2: Using the batch file
start_server.bat

# Option 3: Using uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 🚀 How It Works

### With Groq API (Recommended)

When `GROQ_API_KEY` is configured:
- 🤖 Uses AI to search for REAL mentors
- 🌐 Searches based on user's goal and domain
- 📊 Returns verified professionals from Indian tech companies
- ✅ LinkedIn profiles included
- 🎯 Highly relevant to user's learning path

### Without Groq API (Fallback)

When `GROQ_API_KEY` is NOT configured:
- 📝 Uses static curated data
- 🔄 Generates consistent recommendations
- ✅ Still functional but less personalized

## 📊 Testing the Setup

### 1. Check Service Health

```bash
curl http://localhost:8001/
```

Expected response with AI enabled:
```json
{
  "service": "AI-Powered Mentor Search Service",
  "status": "running",
  "mongodb": "connected",
  "ai_enabled": true,
  "groq_api_key_configured": true,
  "search_capabilities": {
    "web_search": true,
    "ai_powered": true,
    "static_fallback": true
  }
}
```

### 2. Test Mentor Search

Open frontend and navigate to `/mentors` page:
- Should see "🤖 AI Web Search" indicator
- Badges should show "🤖 AI-Found"
- Results should be highly relevant to your roadmap goal

### 3. Check Logs

Look for these log messages:
```
[AI] Attempting Groq-powered web search for mentors...
[AI SEARCH] Using Groq to find mentors for: [query]
[AI RESPONSE] Received X characters
[SUCCESS] Groq found X mentors
```

## 🎨 Frontend Indicators

The frontend will show different indicators based on search mode:

| Feature | AI Mode | Static Mode |
|---------|---------|-------------|
| Badge | 🤖 AI-Found | Recommended |
| Stats | X AI-Powered Recommendations | X Curated Recommendations |
| Status | 🤖 AI Web Search | Freshly Generated |
| Service Status | AI Web Search Active | Mentor Service Active |

## 🐛 Troubleshooting

### Issue: "ai_enabled": false

**Solution:**
1. Check if `GROQ_API_KEY` is set in `.env` file
2. Ensure `.env` file is in `linkedin_mentor_service/` directory
3. Restart the service after adding the key

### Issue: Still showing static data

**Solution:**
1. Clear browser cache
2. Click "Refresh Mentors" button
3. Check service logs for errors
4. Verify API key starts with `gsk_`

### Issue: Groq API errors

**Solution:**
1. Verify API key is valid at https://console.groq.com
2. Check if you've exceeded rate limits (unlikely on free tier)
3. Check internet connection
4. Service will automatically fallback to static data

## 📁 File Structure

```
linkedin_mentor_service/
├── main.py                 # Main service with AI integration
├── requirements.txt        # Dependencies (includes requests)
├── .env                    # Configuration (create this)
├── AI_SETUP.md            # This file
└── README.md              # General documentation
```

## 🎯 API Response Format

### With AI Search

```json
{
  "success": true,
  "mentors": [...],
  "search_query": "frontend development react",
  "total_found": 15,
  "cached": false,
  "search_source": "ai",
  "message": "Found 15 relevant mentors in frontend (AI-powered web search)"
}
```

### With Static Fallback

```json
{
  "success": true,
  "mentors": [...],
  "search_query": "frontend development react",
  "total_found": 10,
  "cached": false,
  "search_source": "static",
  "message": "Found 10 relevant mentors in frontend (curated recommendations)"
}
```

## 🚀 Next Steps

1. ✅ Set up Groq API key
2. ✅ Start the mentor service
3. ✅ Open frontend at http://localhost:5173/mentors
4. ✅ Create a roadmap if you haven't already
5. ✅ See AI-powered mentor recommendations!

## 💡 Tips

- **API Key Security**: Never commit `.env` files to git
- **Performance**: First search takes 3-5 seconds, then cached
- **Quality**: AI finds real professionals from top Indian companies
- **Relevance**: Results match your specific roadmap goal
- **Fallback**: Always works even without API key

## 📞 Support

If you encounter issues:
1. Check the logs in terminal
2. Verify MongoDB is running
3. Ensure port 8001 is available
4. Check Groq API key is valid

---

**Enjoy AI-powered mentor recommendations! 🚀**

