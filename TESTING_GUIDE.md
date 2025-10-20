# 🧪 Testing Guide - Updated Roadmap System

## 🚀 Quick Test Steps

### Option 1: Use Test Page (Easiest)

I've opened **`test_roadmap_browser.html`** in your browser. This page:

✅ **Tests the API** automatically  
✅ **Tests the Database** automatically  
✅ **Shows status** of both services  
✅ **Lets you test roadmap generation** with a simple form  

**Try these goals:**
- "Full Stack Developer"
- "AI Engineer"  
- "React Native Developer"
- "DevOps Engineer"
- "Cybersecurity Specialist"

Click "Generate Roadmap" and see:
- ✅ Difficulty badge
- ⏱️ Estimated hours
- 📚 Domain
- ✨ Match score
- 📋 Prerequisites
- 🎯 Learning outcomes

---

### Option 2: Test in Main Dashboard

1. **Open Dashboard**: Click "Open Dashboard" link or go to:
   ```
   http://localhost:5173
   ```

2. **Navigate to Roadmap Page**

3. **Click "Generate Roadmap"**

4. **Enter a Goal**:
   - "Full Stack Web Developer"
   - "Mobile App Developer"
   - "Data Scientist"
   - etc.

5. **Check the Display**:
   
   ✅ **Metadata Badges** (should appear at top):
   - Difficulty badge (color-coded)
   - Hours badge (blue)
   - Domain badge (purple)
   - Match badge (pink)
   
   ✅ **Expandable Sections**:
   - Click "📋 Prerequisites" - should expand
   - Click "🎯 Learning Outcomes" - should expand
   
   ✅ **Progress Bar**:
   - Shows skills completed
   - Updates as you check items
   
   ✅ **Goal Saved**:
   - Open DevTools (F12)
   - Go to "Application" → "Local Storage"
   - Find `current_goal` - should have your goal saved

---

## 🎯 What to Test

### 1. **Metadata Display** ✨

Generate a roadmap and verify you see:

```
┌────────────────────────────────────────────────────┐
│           Full Stack Web Developer                  │
│                                                     │
│  [Advanced] [⏱️ 520 hrs] [📚 Full Stack] [✨ 95%] │
│                                                     │
│  📋 Prerequisites ▼                                 │
│     (Click to expand)                               │
│                                                     │
│  🎯 Learning Outcomes ▼                             │
│     (Click to expand)                               │
└────────────────────────────────────────────────────┘
```

### 2. **Color-Coded Badges** 🎨

Check difficulty colors:
- 🟢 **Beginner** = Green
- 🟠 **Intermediate** = Orange
- 🔴 **Advanced** = Red

### 3. **Expandable Sections** 📋

- Click "Prerequisites" → Should expand smoothly
- Click again → Should collapse
- Click "Learning Outcomes" → Should expand
- Click again → Should collapse

### 4. **Goal Saving** 💾

After generating:
- Open browser DevTools (F12)
- Application → Local Storage → `http://localhost:5173`
- Look for `current_goal`
- Should contain:
  ```json
  {
    "goal": "Full Stack Web Developer",
    "domain": "Full Stack Development",
    "createdAt": "2025-10-16T...",
    "roadmapId": "roadmap_..."
  }
  ```

### 5. **Different Queries** 🔍

Test various goals to see matching:

| Goal | Expected Domain | Expected Difficulty |
|------|----------------|-------------------|
| "Full Stack Developer" | Full Stack Development | Advanced |
| "AI Engineer" | Machine Learning | Advanced |
| "React Native App" | Mobile Development | Intermediate |
| "UI UX Designer" | Design | Intermediate |
| "DevOps Engineer" | DevOps | Advanced |
| "Data Analyst" | Data Analytics | Intermediate |

---

## 📊 Expected Results

### Example: Full Stack Developer

**Metadata Displayed:**
```
Difficulty: Advanced (Red badge)
Hours: 520 hours (Blue badge)
Domain: Full Stack Development (Purple badge)
Match: 95% (Pink badge)

Prerequisites: ▼
  Basic programming knowledge; Computer fundamentals;
  Problem-solving skills

Learning Outcomes: ▼
  Build production-ready full-stack applications;
  Implement secure authentication systems;
  Design and deploy scalable APIs;
  Optimize application performance;
  Work with modern development workflows
```

**Roadmap Structure:**
- 13 Categories (Foundations → Deployment)
- 80+ Skills
- Progress tracking
- Collapsible steps

---

## 🔍 Troubleshooting

### API Not Running?
```bash
cd roadmap_api
python main.py
```
Should see: `Uvicorn running on http://0.0.0.0:8003`

### Frontend Not Running?
```bash
cd dashboard
npm run dev
```
Should see: `Local: http://localhost:5173`

### Database Empty?
```bash
python reload_roadmap_data_auto.py
```
Should load 810 roadmaps

### No Metadata Showing?
- Check browser console (F12)
- Look for any errors
- Verify API response includes metadata

---

## ✅ Success Checklist

Test complete when you see:

- [ ] Test page shows "✅ API Running"
- [ ] Test page shows "✅ Database (24+ domains)"
- [ ] Can generate roadmap in test page
- [ ] Metadata badges display in dashboard
- [ ] Difficulty badge is color-coded
- [ ] Prerequisites section expands/collapses
- [ ] Learning outcomes section expands/collapses
- [ ] Goal saved in localStorage
- [ ] Progress bar works
- [ ] Skills can be marked complete

---

## 🎉 Quick Links

- **Test Page**: `test_roadmap_browser.html` (already open)
- **Dashboard**: http://localhost:5173
- **API Docs**: http://localhost:8003/docs
- **Health Check**: http://localhost:8003/health

---

## 📸 Screenshots to Verify

Take screenshots or verify you see:

1. **Metadata badges** at the top of roadmap
2. **Color-coded difficulty** (green/orange/red)
3. **Expandable details** for prerequisites
4. **Expandable details** for learning outcomes
5. **Progress bar** with percentage
6. **Goal in localStorage** (DevTools)

---

## 🎊 You're Testing!

The test page should be open in your browser now. Try:

1. ✨ **Generate a roadmap** in the test page
2. 🎨 **Open the dashboard** and generate there
3. 📋 **Click to expand** prerequisites and outcomes
4. ✅ **Mark some skills** as complete
5. 💾 **Check localStorage** for saved goal

**Everything should work perfectly!** 🚀

---

**Happy Testing!** 🧪

