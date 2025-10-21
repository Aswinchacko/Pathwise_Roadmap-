# Quick Start - Real LinkedIn Profiles

## 🚀 5-Minute Setup for Real Profiles

### Step 1: Get API Keys (FREE)

**Serper API** (Google Search):
1. Visit: https://serper.dev/
2. Sign up (no credit card)
3. Copy your API key

**Groq API** (AI):
1. Visit: https://console.groq.com/
2. Sign up with Google/GitHub
3. Create and copy API key

### Step 2: Configure

```bash
cd linkedin_mentor_service
copy env.template .env
```

Edit `.env`:
```bash
SERPER_API_KEY=paste_your_serper_key
GROQ_API_KEY=paste_your_groq_key
```

### Step 3: Start

```bash
python main.py
```

### Step 4: Test

Open: http://localhost:5173/mentors

Look for: **"✓ Real Profile"** badges!

---

## 🎯 What You Get

### Real Profiles:
- ✅ Actual people on LinkedIn
- ✅ Same niche as user's roadmap
- ✅ Mid-level professionals (4-10 years)
- ✅ No CEOs, CTOs, founders
- ✅ India-based tech professionals
- ✅ Real companies (Razorpay, CRED, etc.)

### Visual Indicators:
- Badge: **"✓ Real Profile"**
- Stats: **"15 ✓ Real profiles"**
- Status: **"✓ Real Profiles Active"**

---

## 💰 Cost

- **Free tier**: 2,500 searches/month
- **Perfect for MVP**: $0/month
- **At scale**: $50/month for 10,000 searches

---

## 🐛 Troubleshooting

### Still seeing "AI-Generated"?
1. Check `.env` file has both keys
2. Restart service: `Ctrl+C`, then `python main.py`
3. Click "Refresh Mentors" in UI
4. Look in terminal for: `[REAL SEARCH] Using Serper API`

### Service won't start?
```bash
# Install dependencies
pip install -r requirements.txt

# Check MongoDB is running
mongod --version

# Try again
python main.py
```

---

## 📖 More Info

- **Full Guide**: [REAL_PROFILES_SETUP.md](./REAL_PROFILES_SETUP.md)
- **Solution Details**: [SOLUTION_SUMMARY.md](./SOLUTION_SUMMARY.md)
- **Test Script**: `python test_real_profiles.py`

---

## ✅ Success Checklist

- [ ] Got Serper API key
- [ ] Got Groq API key
- [ ] Added both to `.env` file
- [ ] Service started without errors
- [ ] Visited `/mentors` page
- [ ] See "✓ Real Profile" badges
- [ ] Clicked profile link → goes to real LinkedIn

**All checked? You're done! 🎉**

