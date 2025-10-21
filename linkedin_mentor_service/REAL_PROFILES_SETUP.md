# Real LinkedIn Profiles Setup Guide

## 🎯 Get REAL LinkedIn Profiles (Not Web Scraping!)

This guide shows you how to find **real, original LinkedIn profiles** matching your users' niche using **Serper API** (Google Search API) + **Groq AI**.

### ✅ What You'll Get:
- **Real LinkedIn profiles** from Google search
- **Mid-level professionals** (4-10 years exp, NOT CEOs/CTOs)
- **Same niche** as user's roadmap goal
- **Indian tech professionals** from top companies
- **No web scraping** - uses official APIs

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Serper API Key (FREE)

1. Go to **https://serper.dev/**
2. Click "Sign Up" (free tier: 2,500 searches/month)
3. Verify your email
4. Go to **Dashboard** → **API Key**
5. Copy your API key (starts with `xxx...`)

**Cost**: FREE for 2,500 searches/month ($50/month for 10,000 searches after)

### Step 2: Get Groq API Key (FREE)

1. Go to **https://console.groq.com/**
2. Sign up with Google/GitHub
3. Navigate to **API Keys**
4. Create new key
5. Copy the key (starts with `gsk_...`)

**Cost**: FREE (no credit card required)

### Step 3: Configure Environment

Create or update `linkedin_mentor_service/.env`:

```bash
# Real Profile Search Configuration
SERPER_API_KEY=your_serper_key_here
GROQ_API_KEY=your_groq_key_here

# MongoDB
MONGODB_URI=mongodb://localhost:27017/
```

**OR** if you already have Groq key in `chatbot_service/.env`, just add:

```bash
# In linkedin_mentor_service/.env
SERPER_API_KEY=your_serper_key_here
```

The service will automatically read Groq key from chatbot service!

### Step 4: Start the Service

```bash
cd linkedin_mentor_service
python main.py
```

### Step 5: Test It!

Open **http://localhost:5173/mentors** in your browser.

You should see:
- ✅ **"✓ Real Profile"** badges
- ✅ **"Real Profiles Active"** status
- ✅ **Actual LinkedIn URLs** that work when clicked

---

## 🔍 How It Works

### Without Serper API (Current Default):
```
User Goal → Groq AI generates realistic profiles → Static/AI-generated data
```

### With Serper API (REAL Profiles):
```
User Goal → Google Search (via Serper) → Real LinkedIn URLs → Groq extracts data → Real profiles!
```

**Key Difference**: 
- **Without Serper**: AI invents realistic-looking profiles
- **With Serper**: Finds actual people on LinkedIn and structures their data

---

## 📊 API Response Differences

### With Real Profiles (Serper + Groq):
```json
{
  "success": true,
  "mentors": [...],
  "search_source": "real",
  "is_real_profile": true,
  "profile_url": "https://www.linkedin.com/in/actual-person",
  "message": "Found 15 relevant mentors (Real profiles)"
}
```

### Without Serper (AI-Generated):
```json
{
  "success": true,
  "mentors": [...],
  "search_source": "ai",
  "is_ai_generated": true,
  "profile_url": "https://www.linkedin.com/in/generated-slug",
  "message": "Found 15 relevant mentors (AI-generated)"
}
```

---

## 🎨 Frontend Indicators

| Feature | Real Profiles | AI-Generated | Static |
|---------|---------------|--------------|--------|
| Badge | ✓ Real Profile | 🤖 AI-Generated | Recommended |
| Stats | X Real Profiles | X AI-Generated | X Curated |
| Status | ✓ Real Profiles Active | 🤖 AI Generation Active | Mentor Service Active |

---

## 🔧 Configuration Options

### Basic Setup (Recommended):
```bash
SERPER_API_KEY=xxx...          # For real profiles
GROQ_API_KEY=gsk_xxx...        # For data extraction
```

### Advanced Options:
```bash
SERPER_API_KEY=xxx...
GROQ_API_KEY=gsk_xxx...
MONGODB_URI=mongodb://localhost:27017/
ENABLE_WEB_SEARCH=true         # Enable AI features (default: auto)
```

---

## 💰 Cost Breakdown

### Free Tier (Perfect for MVP):
| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Serper API | 2,500 searches/month | $50/month for 10,000 |
| Groq API | Unlimited (rate limited) | FREE forever |
| MongoDB | Unlimited (local) | $0-$57/month (Atlas) |

**Total Cost for MVP**: $0/month (up to 2,500 mentor searches)

### Production (1000 users):
- Each user searches ~2x/month = 2,000 searches
- **Cost**: $0/month (still in free tier!)

### Scale (10,000 users):
- 20,000 searches/month
- **Cost**: $100/month (Serper API)

---

## 🐛 Troubleshooting

### Issue: Still showing "AI-Generated" profiles

**Check**:
```bash
# In terminal where service is running, look for:
[REAL SEARCH] Using Serper API + Groq AI for real profiles
[GOOGLE SEARCH] Found X LinkedIn profiles
[SUCCESS] Extracted X mentor profiles
```

**Fix**:
1. Verify Serper API key is correct in `.env`
2. Restart the service: `python main.py`
3. Clear browser cache
4. Click "Refresh Mentors" button

### Issue: "Serper API error: 401"

**Fix**: 
- Check API key is correct
- Ensure no extra spaces in `.env` file
- Format: `SERPER_API_KEY=xxx` (no quotes)

### Issue: "No profiles found"

**Fix**:
- User needs to create a roadmap first
- Check MongoDB is running
- Verify roadmap has clear domain/goal

### Issue: Profiles not matching user's niche

**Fix**: The search query is built from:
```python
search_query = f"{domain} engineer India site:linkedin.com/in -CEO -CTO"
```

It automatically:
- Filters by user's domain
- Only finds Indian profiles
- Excludes executives

---

## 🎯 Search Quality Examples

### Frontend Developer Roadmap:
**Search**: `frontend react javascript engineer India site:linkedin.com/in -CEO -CTO`

**Results**: Real profiles like:
- Senior React Developer at Razorpay
- Frontend Engineer at CRED
- UI Engineer at Flipkart

### Data Science Roadmap:
**Search**: `data science python machine learning engineer India site:linkedin.com/in -CEO -CTO`

**Results**: Real profiles like:
- Data Scientist at PhonePe
- ML Engineer at Swiggy
- Senior Data Analyst at Zomato

---

## 🔒 Privacy & Legal

### Is This Legal?
✅ **YES** - We're using:
1. **Serper API**: Official Google Search API (legal)
2. **Groq AI**: Just structures publicly available data
3. **No scraping**: We don't access LinkedIn directly

### What Data We Store:
- Name (public)
- Job title (public)
- Company (public)
- LinkedIn URL (public)
- Skills (inferred from public data)

**We DO NOT**:
- ❌ Scrape LinkedIn pages
- ❌ Access private profile data
- ❌ Violate LinkedIn TOS
- ❌ Store sensitive information

---

## 🚀 Production Checklist

- [ ] Get Serper API key
- [ ] Get Groq API key
- [ ] Add keys to `.env` file
- [ ] Test with `python main.py`
- [ ] Verify "Real Profile" badges show up
- [ ] Click profile links to confirm they're real
- [ ] Set up monitoring for API usage
- [ ] Configure rate limiting if needed

---

## 📈 Upgrade Path

### Current: Static/AI-Generated ($0/month)
→ Good for: Demo, testing

### Upgrade: Serper API ($0-50/month)
→ Good for: MVP, early users, getting real profiles

### Enterprise: Proxycurl API ($99-499/month)
→ Good for: Scale, more detailed profile data, LinkedIn verified

---

## 💡 Tips

1. **Cache Aggressively**: Real profile searches cost API credits
2. **Set Refresh=false**: Use cached data when possible
3. **Monitor Usage**: Check Serper dashboard regularly
4. **User Feedback**: Real profiles = better conversion

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Badges say "✓ Real Profile"
- ✅ Status shows "Real Profiles Active"
- ✅ LinkedIn URLs are actual people's profiles
- ✅ Names match real professionals
- ✅ Companies are real Indian tech companies
- ✅ Profiles match user's exact niche

---

## 📞 Support

**Issues?**
1. Check logs in terminal
2. Verify API keys are correct
3. Test API keys manually:
   - Serper: https://serper.dev/dashboard
   - Groq: https://console.groq.com/

**Need Help?**
- Service logs show detailed error messages
- Check `.env` file format
- Restart service after config changes

---

**Ready to get real profiles? Set up your API keys and start now! 🚀**

