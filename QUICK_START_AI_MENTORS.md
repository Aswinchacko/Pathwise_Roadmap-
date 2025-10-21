# 🤖 AI Mentor Search - QUICK START

## 🎯 What You Get

Real mentors from Indian tech companies found via AI based on your learning goals.

## ⚡ 3-Step Setup (2 minutes)

### Step 1: Get Groq API Key (FREE)
```
1. Visit: https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy key (starts with gsk_...)
```

### Step 2: Configure Key

**If you have chatbot running:** ✅ Already done!

**Otherwise:**
```bash
# Create/edit: linkedin_mentor_service/.env
GROQ_API_KEY=gsk_your_key_here
```

### Step 3: Start Service
```bash
start_ai_mentor_service.bat
```

## ✅ Test It

```bash
# Run test
python test_ai_mentor_service.py

# Or check manually
curl http://localhost:8001/api/mentors/health
```

Expected output:
```json
{
  "ai_search": "enabled",
  "search_mode": "ai"
}
```

## 🎨 Use It

1. Open: http://localhost:5173/mentors
2. Create a roadmap (if needed)
3. See **🤖 AI-Found** mentors!

## 📊 How to Know It's Working

✅ Service logs: `[AI] Attempting Groq-powered web search...`
✅ Frontend: "🤖 AI-Found" badges
✅ Status: "AI Web Search Active"
✅ Real companies: Razorpay, CRED, Flipkart, etc.

## 🐛 Troubleshooting

**"ai_enabled": false?**
→ Check Groq API key in .env file

**Still seeing static data?**
→ Click "Refresh Mentors" button

**Service won't start?**
→ Check MongoDB is running

## 📚 More Info

- Full guide: `AI_MENTOR_SEARCH_COMPLETE.md`
- Setup details: `linkedin_mentor_service/AI_SETUP.md`
- API docs: http://localhost:8001/docs

---

**That's it! Enjoy AI-powered mentor search! 🚀**

