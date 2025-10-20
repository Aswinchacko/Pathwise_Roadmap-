# 🚀 Quick Start & Test Guide

## ✅ Step-by-Step Instructions

### Step 1: Start the Backend API

**Option A - Using Batch File (Easiest):**
```
Double-click: start_api.bat
```

**Option B - Manual:**
1. Open a command prompt or PowerShell
2. Navigate to the project folder
3. Run:
```bash
cd roadmap_api
python main.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

---

### Step 2: Start the Frontend

**Option A - Using Batch File (Easiest):**
```
Double-click: start_frontend.bat
```

**Option B - Manual:**
1. Open another command prompt or PowerShell
2. Navigate to the project folder
3. Run:
```bash
cd dashboard
npm run dev
```

**Wait for:**
```
  VITE v... ready in ...ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

### Step 3: Open the Dashboard

**In your browser, go to:**
```
http://localhost:5173
```

---

### Step 4: Navigate to Roadmap Page

Click on "**Roadmap**" in the navigation menu.

---

### Step 5: Generate a Roadmap

1. Click "**Generate Roadmap**" button
2. Enter a goal, for example:
   - "Full Stack Developer"
   - "AI Engineer"
   - "React Native Developer"
3. (Optional) Select a domain
4. Click "**Generate**"

---

### Step 6: Verify Enhanced Display

✅ **You should see:**

```
┌──────────────────────────────────────────────────┐
│          Full Stack Web Developer                │
│                                                  │
│  [Advanced] [⏱️ 520 hours] [📚 Full Stack] [✨ 95%] │
│                                                  │
│  📋 Prerequisites ▼                              │
│     Basic programming knowledge...               │
│                                                  │
│  🎯 Learning Outcomes ▼                          │
│     Build production-ready applications...       │
│                                                  │
│  Progress: ▓▓▓░░░░░░░ 0 / 80 (0%)              │
└──────────────────────────────────────────────────┘
```

**Color-coded badges:**
- 🔴 Advanced (Red)
- 🟠 Intermediate (Orange)  
- 🟢 Beginner (Green)
- 🔵 Hours (Blue)
- 🟣 Domain (Purple)
- 🩷 Match % (Pink)

**Expandable sections:**
- Click "📋 Prerequisites" - expands/collapses
- Click "🎯 Learning Outcomes" - expands/collapses

---

## 🧪 Test Checklist

### ✅ Visual Tests:

- [ ] Metadata badges appear at top
- [ ] Difficulty badge is color-coded
- [ ] Hours badge shows correct time
- [ ] Domain badge shows category
- [ ] Match score badge shows percentage
- [ ] Prerequisites section expands when clicked
- [ ] Learning outcomes section expands when clicked
- [ ] Prerequisites section collapses when clicked again
- [ ] Learning outcomes section collapses when clicked again

### ✅ Functional Tests:

- [ ] Progress bar displays correctly
- [ ] Can check/uncheck skills
- [ ] Progress updates when marking skills
- [ ] Percentage updates correctly
- [ ] All skills are organized in categories
- [ ] Categories can be collapsed/expanded

### ✅ Goal Saving Test:

1. Press F12 (open DevTools)
2. Go to "Application" tab
3. Click "Local Storage" → `http://localhost:5173`
4. Look for key: `current_goal`
5. Should contain:
```json
{
  "goal": "Full Stack Web Developer",
  "domain": "Full Stack Development",
  "createdAt": "2025-10-16T...",
  "roadmapId": "roadmap_..."
}
```

---

## 🎯 Test Different Goals

Try generating roadmaps for:

| Goal | Expected Difficulty | Expected Hours |
|------|-------------------|----------------|
| "Full Stack Web Developer" | 🔴 Advanced | 520 |
| "AI/ML Engineer" | 🔴 Advanced | 650 |
| "Mobile App Developer React Native" | 🟠 Intermediate | 480 |
| "UI/UX Designer" | 🟠 Intermediate | 420 |
| "DevOps Engineer" | 🔴 Advanced | 550 |
| "Cybersecurity Specialist" | 🔴 Advanced | 600 |
| "Data Analyst" | 🟠 Intermediate | 400 |
| "Blockchain Developer" | 🔴 Advanced | 580 |

---

## ❌ Troubleshooting

### Problem: "Failed to fetch" error

**Solution:**
1. Make sure the API is running (check the command window)
2. Look for: `Uvicorn running on http://0.0.0.0:8000`
3. If not running, double-click `start_api.bat` again

### Problem: Dashboard not loading

**Solution:**
1. Make sure frontend is running (check the command window)
2. Look for: `Local: http://localhost:5173/`
3. If not running, double-click `start_frontend.bat` again

### Problem: No metadata badges showing

**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Hard refresh (Ctrl+F5)
3. Check browser console for errors (F12)

### Problem: Database empty

**Solution:**
```bash
python reload_roadmap_data_auto.py
```

---

## 📍 Quick Reference

### URLs:
- **Dashboard**: http://localhost:5173
- **API Health**: http://localhost:8000/health
- **API Docs**: http://localhost:8000/docs
- **Roadmap API**: http://localhost:8000/api/roadmap/generate-roadmap

### Files to Run:
- `start_api.bat` - Start backend
- `start_frontend.bat` - Start frontend
- `test_roadmap_browser.html` - Quick test page

### Check if Running:
```powershell
Get-NetTCPConnection -LocalPort 8000,5173 | Select-Object LocalPort, State
```

Should show:
- Port 8000: Listen (API)
- Port 5173: Listen (Frontend)

---

## 🎉 Success!

When you see:
- ✅ Color-coded difficulty badges
- ✅ Expandable prerequisites section
- ✅ Expandable learning outcomes section  
- ✅ Progress tracking works
- ✅ Goal saved in localStorage

**Your roadmap system is working perfectly!** 🚀

---

## 💡 Tips

1. **Keep command windows open** - Don't close them while testing
2. **Use browser DevTools** - F12 to inspect localStorage and console
3. **Try different goals** - See how the matching algorithm works
4. **Check the badges** - Colors indicate difficulty level
5. **Expand the details** - Click to see prerequisites and outcomes

---

**Ready to test!** Open your browser and follow the steps above! 🎊

