# 🚀 Quick Start - LinkedIn Mentor Scraping

Get the LinkedIn mentor scraping system running in **5 minutes**!

## Prerequisites

✅ Python 3.8+ installed
✅ Chrome browser installed
✅ MongoDB running on localhost:27017
✅ Node.js for frontend

## Step 1: Start MongoDB (if not running)

```bash
# Check if MongoDB is running
mongod --version

# If not running, start it
# Windows:
mongod --dbpath C:\data\db

# Linux/Mac:
sudo systemctl start mongod
```

## Step 2: Start LinkedIn Scraping Service

```bash
# From project root
start_linkedin_mentor_service.bat

# Or manually:
cd linkedin_mentor_service
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8005
```

✅ Service should be running on **http://localhost:8005**

## Step 3: Start Frontend (if not running)

```bash
cd dashboard
npm install
npm run dev
```

✅ Frontend should be running on **http://localhost:5173**

## Step 4: Create a Roadmap

1. Login to the dashboard
2. Go to **Roadmap** page
3. Create a roadmap (e.g., "Become a React Developer")
4. This gets saved to MongoDB with your user ID

## Step 5: View Mentors

1. Go to **Mentors** page
2. The system will automatically:
   - Fetch your roadmap goal from MongoDB
   - Search LinkedIn for relevant mentors
   - Display real LinkedIn profiles

## Testing the Service

```bash
cd linkedin_mentor_service
python test_service.py
```

## Verify Everything is Working

### 1. Check Service Health

```bash
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

### 2. Check MongoDB Data

```bash
# Open MongoDB shell
mongo

# Switch to pathwise database
use pathwise

# Check roadmap collection
db.roadmap.find({user_id: "your_user_id"}).pretty()

# Check mentors collection
db.mentors.find({user_id: "your_user_id"}).pretty()
```

### 3. Test Scraping Manually

```bash
curl -X POST http://localhost:8005/api/mentors/scrape \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "limit": 5}'
```

## Troubleshooting

### "MongoDB not connected"

```bash
# Start MongoDB
mongod

# Or check if it's running on different port
netstat -ano | findstr :27017
```

### "Chrome driver error"

```bash
# Reinstall webdriver manager
pip install webdriver-manager --upgrade

# Or install Chrome if not present
# Download from: https://www.google.com/chrome/
```

### "No roadmap found"

1. Make sure you're logged in
2. Create a roadmap on the Roadmap page
3. Check MongoDB has the data:
   ```bash
   mongo
   use pathwise
   db.roadmap.find({source: "user_generated"})
   ```

### "Scraping takes too long"

- First run takes longer (30-60 seconds)
- Subsequent requests use cache (instant)
- Reduce limit: `{"limit": 5}` instead of 10

### "Port 8005 already in use"

```bash
# Find process using port 8005
netstat -ano | findstr :8005

# Kill the process
taskkill /PID <process_id> /F
```

## Architecture Overview

```
User → Frontend (5173) → LinkedIn Service (8005) → MongoDB (27017)
                              ↓
                         Google Search → LinkedIn
```

## What Gets Scraped

From each LinkedIn profile:
- ✅ Name, Title, Company
- ✅ Location, Connections
- ✅ Profile Picture
- ✅ About Section
- ✅ Skills (top 10)
- ✅ Experience Years
- ✅ Profile URL

## Default Behavior

- **Caching**: Results are cached in MongoDB
- **Refresh**: Use `refresh_cache: true` to force new scrape
- **Search**: Based on your roadmap goal + domain
- **Limit**: Default 10 mentors, max 20

## Production Checklist

- [ ] Set environment variables
- [ ] Use production MongoDB URI
- [ ] Enable HTTPS
- [ ] Add proxy rotation for large-scale scraping
- [ ] Implement rate limiting
- [ ] Add monitoring/logging
- [ ] Set up error alerts

## Next Actions

1. ✅ Create a roadmap
2. ✅ Visit Mentors page
3. ✅ View real LinkedIn profiles
4. ⏳ Implement contact/messaging
5. ⏳ Add mentor ratings
6. ⏳ Schedule calls with mentors

## Support

- 📖 Full docs: `LINKEDIN_MENTOR_SCRAPING_SETUP.md`
- 🔧 Service code: `linkedin_mentor_service/main.py`
- 🎨 Frontend: `dashboard/src/pages/Mentors.jsx`
- 💾 MongoDB: Collections `roadmap` and `mentors`

## FAQ

**Q: Does it scrape real LinkedIn profiles?**
A: Yes! It uses Selenium + Chrome to scrape actual LinkedIn profiles via Google search.

**Q: Is it legal?**
A: We're scraping publicly available information. Follow LinkedIn's ToS and use responsibly.

**Q: How fast is it?**
A: First scrape: 30-60 seconds. Cached results: Instant.

**Q: Can I customize the search?**
A: Yes! The search query is based on your roadmap goal + domain from MongoDB.

**Q: Does it require LinkedIn login?**
A: No! We use Google search to find profiles and scrape public profile pages.

**Q: What if I get rate limited?**
A: Use caching, increase delays, or add proxy rotation. Google intermediary helps avoid LinkedIn rate limits.

---

**Ready to start?** Run `start_linkedin_mentor_service.bat` and create your roadmap! 🚀


