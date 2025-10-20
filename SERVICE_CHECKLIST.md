# ✅ Service Startup Checklist

## Quick Check - What's Running?

Run these commands to check each service:

### ☑️ MongoDB (Required)
```bash
mongosh
```
- ✅ Connects → MongoDB is running
- ❌ Error → Start with: `mongod`

### ☑️ Roadmap API (Required for roadmap goals)
```bash
curl http://localhost:8001/health
```
- ✅ Returns JSON → API is running
- ❌ Cannot connect → Start with: `cd roadmap_api && python main.py`

### ☑️ Mentor Service (Required for scraping!) ← **THIS ONE IS MISSING**
```bash
curl http://localhost:8004/health
```
- ✅ Returns `{"status":"healthy"}` → Service is running
- ❌ Cannot connect → **START IT NOW!**

```bash
cd mentor_recommendation_service
python main.py
```

### ☑️ Frontend Dashboard
Open browser: http://localhost:5173
- ✅ Page loads → Frontend is running
- ❌ Cannot connect → Start with: `cd dashboard && npm run dev`

---

## Start Everything At Once

Instead of checking each one, just run:

```bash
start_complete_mentor_system.bat
```

This will:
1. Check MongoDB is running
2. Start Roadmap API (new terminal)
3. Start Mentor Service (new terminal) ← **Fixes your issue!**
4. Start Frontend (new terminal)
5. Open browser automatically

---

## Current Problem

Based on your browser console showing:
```
Failed to connect to http://localhost:8004/health
```

**The mentor service is NOT running!**

**Fix:**
1. Open a new terminal
2. Run:
   ```bash
   cd mentor_recommendation_service
   python main.py
   ```
3. Wait for: `Uvicorn running on http://0.0.0.0:8004`
4. Refresh your browser
5. Go to Mentors page
6. Should work now!

---

## Quick Start Command

Copy and paste this into a terminal:

```bash
cd mentor_recommendation_service && python main.py
```

Leave that terminal open and running!

---

## Verification

After starting mentor service, open browser console (F12) and go to Mentors page.

**You should see:**
```javascript
🔍 Loading mentors for: {userId: "...", goal: "...", domain: "..."}
✅ Received mentor response
📊 Found 10 mentors
🌟 Real LinkedIn profiles: X/10
```

**NOT:**
```javascript
❌ Error loading roadmap mentors
Failed to fetch
```

---

## Pro Tip

Keep all 4 terminals open side by side:

```
┌─────────────────┬─────────────────┐
│  Roadmap API    │  Mentor Service │ ← Watch this one for scraping logs!
│  Port 8001      │  Port 8004      │
├─────────────────┼─────────────────┤
│  Frontend       │  MongoDB        │
│  Port 5173      │  Port 27017     │
└─────────────────┴─────────────────┘
```

When you request mentors, you'll see real-time scraping logs in the **Mentor Service terminal**!

```
🚀 ADVANCED MENTOR SCRAPING INITIATED
🎯 Scraping mentors for: Become a React Developer
🔍 Searching for: React
⏳ Scraping profile 1: https://linkedin.com/in/...
   ✅ Sarah Chen - Senior React Engineer
```

---

**Start the mentor service now to fix the connection issue!** 🚀

