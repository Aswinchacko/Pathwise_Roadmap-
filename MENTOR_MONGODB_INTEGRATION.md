# 🔄 Mentor Service - MongoDB Integration Complete

## What Changed

The mentor recommendation system now fetches roadmap data **directly from MongoDB** instead of relying on localStorage.

## The Complete Flow

```
User Creates Roadmap
    ↓
Saved to MongoDB (via Roadmap API)
    ↓
User Visits Mentors Page
    ↓
Frontend Fetches User's Roadmap from MongoDB
    ↓
Calls Mentor API with Roadmap Goal
    ↓
Mentor Service Scrapes LinkedIn
    ↓
Displays Mentors
```

## Technical Details

### 1. Data Storage (MongoDB)

**Collection:** `pathwise.roadmap`

**Document Structure:**
```json
{
  "roadmap_id": "roadmap_20251016_123456_7890",
  "title": "Become a React Developer",
  "goal": "Become a React Developer",
  "domain": "Frontend Development",
  "user_id": "user123",
  "steps": [...],
  "created_at": "2025-10-16T...",
  "updated_at": "2025-10-16T...",
  "source": "user_generated"
}
```

### 2. API Endpoints

#### Roadmap API (Port 8000)

**Get User Roadmaps:**
```
GET http://localhost:8000/api/roadmap/roadmaps/user/{user_id}
```

**Response:**
```json
{
  "roadmaps": [
    {
      "id": "roadmap_20251016_123456_7890",
      "goal": "Become a React Developer",
      "domain": "Frontend Development",
      "created_at": "2025-10-16T...",
      "updated_at": "2025-10-16T...",
      "steps": [...]
    }
  ]
}
```

**Create Roadmap:**
```
POST http://localhost:8000/api/roadmap/generate-roadmap
{
  "goal": "Become a React Developer",
  "domain": "Frontend Development",
  "user_id": "user123"
}
```

#### Mentor API (Port 8004)

**Get Mentors for Roadmap:**
```
POST http://localhost:8004/api/mentors/roadmap-based
{
  "user_id": "user123",
  "roadmap_goal": "Become a React Developer",
  "domain": "Frontend Development",
  "experience_level": "intermediate",
  "preferred_platforms": ["linkedin"],
  "limit": 10
}
```

**Response:**
```json
{
  "mentors": [
    {
      "mentor_id": "...",
      "name": "John Doe",
      "title": "Senior React Developer",
      "company": "Google",
      "rating": 4.8,
      "is_real_profile": true,
      "profile_url": "https://linkedin.com/in/..."
    }
  ],
  "total_found": 10,
  "message": "Found 10 mentors (5 real LinkedIn profiles)"
}
```

### 3. Frontend Integration

**File:** `dashboard/src/services/mentorService.js`

**Key Method:** `getCurrentRoadmapGoal(userId)`

**Fetch Priority:**
1. ✅ **MongoDB (via Roadmap API)** - Primary source
2. 📦 **localStorage** - Fallback only if MongoDB fails

**Code:**
```javascript
async getCurrentRoadmapGoal(userId = null) {
  // 1. Try MongoDB first (if userId provided)
  if (userId) {
    const response = await axios.get(
      `${ROADMAP_API_URL}/api/roadmap/roadmaps/user/${userId}`
    );
    if (response.data.roadmaps.length > 0) {
      const latest = response.data.roadmaps[0];
      return {
        goal: latest.goal,
        domain: latest.domain,
        roadmapId: latest.id
      };
    }
  }
  
  // 2. Fallback to localStorage
  const savedRoadmap = localStorage.getItem('current_roadmap');
  if (savedRoadmap) {
    return JSON.parse(savedRoadmap);
  }
  
  return null;
}
```

## Why `/health` is Called

The `/health` endpoint is called **before** the actual mentor API to verify the service is running:

```javascript
// Step 1: Check if mentor service is online
const available = await mentorService.checkMentorServiceHealth();
// Calls: GET http://localhost:8004/health

if (!available) {
  setError('Mentor service is offline');
  return; // STOPS HERE
}

// Step 2: Get roadmap from MongoDB
const roadmap = await mentorService.getCurrentRoadmapGoal(userId);
// Calls: GET http://localhost:8001/api/roadmap/roadmaps/user/{userId}

if (!roadmap) {
  setError('Create a roadmap first');
  return; // STOPS HERE
}

// Step 3: Get mentors based on roadmap
await fetchMentorsForRoadmap(userId, roadmap.goal, roadmap.domain);
// Calls: POST http://localhost:8004/api/mentors/roadmap-based
```

**So if you only see `/health` calls:**
- ✅ Service health check passed
- ❌ Either no roadmap in MongoDB OR service check failed
- ❌ Never reaches the actual mentor API call

## Testing

### Test File: `test_mentor_api_directly.html`

Open in browser to test each step:

**Button 1:** Test Roadmap API (MongoDB)
- Fetches user's roadmaps from MongoDB
- Shows what roadmaps exist

**Button 2:** Test Mentor Service Health
- Calls `/health` endpoint
- Verifies service is running

**Button 3:** Test Mentor API (Scraping)
- Calls `/api/mentors/roadmap-based`
- Tests actual mentor scraping

**Button 4:** Save Test Roadmap to MongoDB
- Creates a test roadmap in MongoDB
- Then you can test the full flow

### Manual Testing Steps

**1. Start All Services:**
```bash
# Terminal 1 - MongoDB
mongod

# Terminal 2 - Roadmap API
cd roadmap_api
python main.py

# Terminal 3 - Mentor Service
cd mentor_recommendation_service
python main.py

# Terminal 4 - Frontend
cd dashboard
npm run dev
```

**2. Create a Roadmap:**
- Go to http://localhost:5173/roadmap
- Click "Generate Roadmap"
- Enter: "Become a React Developer"
- Click Generate
- **This saves to MongoDB**

**3. View Mentors:**
- Go to http://localhost:5173/mentors
- Should automatically:
  1. Check mentor service health (`/health`)
  2. Fetch roadmap from MongoDB
  3. Call mentor API (`/api/mentors/roadmap-based`)
  4. Display mentors with green badges for real profiles

**4. Verify in MongoDB:**
```bash
mongosh
use pathwise
db.roadmap.find({"source": "user_generated"}).pretty()
```

## Troubleshooting

### Issue: Only see `/health` calls, no mentors

**Cause:** No roadmap in MongoDB for this user

**Solution:**
1. Check browser console for logs:
   ```
   🔍 Fetching roadmap from MongoDB for user: ...
   ⚠️ No roadmaps found in MongoDB for this user
   ```

2. Create a roadmap first in the Roadmap page

3. Or use test file to save one:
   ```
   Open: test_mentor_api_directly.html
   Click: "4️⃣ Save Test Roadmap to MongoDB"
   ```

### Issue: "Cannot connect to roadmap API"

**Cause:** Roadmap API not running on port 8001

**Solution:**
```bash
cd roadmap_api
python main.py
```

Verify:
```bash
curl http://localhost:8001/health
```

### Issue: "Mentor service is offline"

**Cause:** Mentor service not running on port 8004

**Solution:**
```bash
cd mentor_recommendation_service
python main.py
```

Verify:
```bash
curl http://localhost:8004/health
```

### Issue: "Create a roadmap first"

**Cause:** User has no roadmaps in MongoDB

**Solution:**
- Go to `/roadmap` page and generate one
- Or the user is not logged in properly

## Benefits of MongoDB Integration

✅ **Persistent Storage** - Roadmaps saved permanently, not lost on browser clear

✅ **Multi-Device** - Access roadmaps from any device

✅ **User-Specific** - Each user sees only their roadmaps

✅ **Timestamp Tracking** - Know when roadmaps were created/updated

✅ **Scalable** - Can store unlimited roadmaps per user

✅ **Reliable** - Single source of truth (not localStorage)

## Architecture Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ├──────────────────────────────────┐
       │                                  │
       ▼                                  ▼
┌──────────────┐                  ┌──────────────┐
│  Roadmap API │                  │ Mentor API   │
│  Port 8001   │                  │  Port 8004   │
└──────┬───────┘                  └──────────────┘
       │                                  │
       ▼                                  │
┌──────────────┐                         │
│   MongoDB    │                         │
│  Port 27017  │                         │
│              │                         │
│ Collection:  │                         │
│  roadmap     │                         │
└──────────────┘                         │
                                         │
                                         ▼
                                  ┌──────────────┐
                                  │   LinkedIn   │
                                  │  (Scraping)  │
                                  └──────────────┘
```

## Next Steps

1. ✅ Roadmaps now fetched from MongoDB
2. ✅ localStorage used only as fallback
3. ✅ Mentor API receives roadmap data from MongoDB
4. ✅ Full integration tested

The system now properly uses MongoDB as the primary data source! 🎉

