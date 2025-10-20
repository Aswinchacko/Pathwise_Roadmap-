# PathWise Subscription Integration Guide

This guide shows how to integrate the subscription system with your existing PathWise features to unlock opportunities, projects, and premium content after payment.

## 🎯 Quick Integration Steps

### 1. Wrap Existing Components with FeatureGate

#### Projects Page
```jsx
// In dashboard/src/pages/Projects.jsx
import FeatureGate from '../components/FeatureGate'

// Wrap the project recommendations
<FeatureGate userId={user?.id} feature="projects">
  <ProjectRecommendationModal 
    isOpen={showProjectModal}
    onClose={() => setShowProjectModal(false)}
    // ... other props
  />
</FeatureGate>
```

#### Jobs/Opportunities Page  
```jsx
// In dashboard/src/pages/Jobs.jsx
import FeatureGate from '../components/FeatureGate'

// Wrap job opportunities
<FeatureGate userId={user?.id} feature="opportunities">
  <div className="job-listings">
    {jobs.map(job => (
      <JobCard key={job.id} job={job} />
    ))}
  </div>
</FeatureGate>
```

#### Resources Page
```jsx
// In dashboard/src/pages/Resources.jsx
import FeatureGate from '../components/FeatureGate'

// Wrap premium resources
<FeatureGate userId={user?.id} feature="resources">
  <ResourcesList resources={resources} />
</FeatureGate>
```

#### Roadmap Page
```jsx
// In dashboard/src/pages/Roadmap.jsx
import FeatureGate from '../components/FeatureGate'

// Wrap roadmap generation
<FeatureGate userId={user?.id} feature="roadmaps">
  <RoadmapGenerator />
</FeatureGate>
```

### 2. Add Subscription Check to Service Calls

#### Project Recommendation Service
```python
# In project_recommendation_service/main.py
from subscription_service.middleware import require_subscription

@app.post("/api/projects/recommend")
@require_subscription("projects")
async def recommend_projects(request: ProjectRecommendationRequest):
    # Existing code...
    return recommendations
```

#### Roadmap API
```python
# In roadmap_api/main.py
from subscription_service.middleware import require_subscription

@app.post("/api/roadmap/generate-roadmap")
@require_subscription("roadmaps") 
async def generate_roadmap(request: RoadmapRequest):
    # Existing code...
    return roadmap
```

### 3. Update Dashboard to Show Subscription Status

#### Dashboard.jsx
```jsx
// Add subscription info to dashboard
import { useState, useEffect } from 'react'
import subscriptionService from '../services/subscriptionService'

const Dashboard = () => {
  const [subscriptionInfo, setSubscriptionInfo] = useState(null)
  const user = authService.getCurrentUser()

  useEffect(() => {
    if (user?.id) {
      loadSubscriptionInfo()
    }
  }, [user])

  const loadSubscriptionInfo = async () => {
    const result = await subscriptionService.getUserSubscription(user.id)
    if (result.success) {
      setSubscriptionInfo(result.data)
    }
  }

  return (
    <div className="dashboard">
      {/* Add subscription status widget */}
      {subscriptionInfo && (
        <div className="subscription-status">
          <h3>Your Plan: {subscriptionInfo.plan_details.name}</h3>
          {subscriptionInfo.subscription.plan === 'free' && (
            <button onClick={() => setShowUpgradeModal(true)}>
              Upgrade to Pro
            </button>
          )}
        </div>
      )}
      
      {/* Wrap existing content with feature gates */}
      <FeatureGate userId={user?.id} feature="opportunities">
        <OpportunitiesWidget />
      </FeatureGate>
      
      {/* Rest of dashboard... */}
    </div>
  )
}
```

## 🔧 Advanced Integration Examples

### Conditional Rendering Based on Plan

```jsx
import { useState, useEffect } from 'react'
import subscriptionService from '../services/subscriptionService'

const AdvancedFeatures = ({ userId }) => {
  const [plan, setPlan] = useState('free')

  useEffect(() => {
    const checkPlan = async () => {
      const result = await subscriptionService.getUserSubscription(userId)
      if (result.success) {
        setPlan(result.data.subscription.plan)
      }
    }
    checkPlan()
  }, [userId])

  return (
    <div>
      {plan === 'pro' && <AdvancedAnalytics />}
      {plan === 'enterprise' && <TeamCollaboration />}
      
      {plan === 'free' && (
        <div className="upgrade-prompt">
          <h3>Unlock Advanced Features</h3>
          <p>Upgrade to Pro for advanced analytics and more!</p>
        </div>
      )}
    </div>
  )
}
```

### Usage-Based Limiting

```jsx
const ResourcesPage = ({ userId }) => {
  const [usage, setUsage] = useState(null)

  useEffect(() => {
    const checkUsage = async () => {
      const access = await subscriptionService.getFeatureUsage(userId, 'resources')
      setUsage(access)
    }
    checkUsage()
  }, [userId])

  return (
    <div>
      {usage && (
        <div className="usage-indicator">
          <p>Resources used: {usage.current} / {usage.limit === -1 ? '∞' : usage.limit}</p>
          <div className="progress-bar">
            <div 
              className="progress" 
              style={{ width: `${(usage.current / usage.limit) * 100}%` }}
            />
          </div>
        </div>
      )}
      
      <FeatureGate userId={userId} feature="resources">
        <ResourcesList />
      </FeatureGate>
    </div>
  )
}
```

## 🚀 Backend Service Integration

### Express.js Services (Node.js)

```javascript
// Add to auth_back/routes/auth.js or similar
const { checkSubscription } = require('../../subscription_service/middleware.js')

// Protect premium endpoints
router.get('/premium-data', 
  checkSubscription('advanced_analytics'),
  (req, res) => {
    // Return premium data
    res.json({ data: 'premium content' })
  }
)
```

### FastAPI Services (Python)

```python
# Add to any Python service
import sys
sys.path.append('../subscription_service')
from middleware import require_subscription

@app.get("/premium-endpoint")
@require_subscription("opportunities")
async def get_opportunities():
    # Return opportunities data
    return {"opportunities": [...]}
```

## 📊 Analytics & Tracking

### Track Feature Usage

```jsx
// Add usage tracking to components
const trackFeatureUsage = async (userId, feature) => {
  try {
    await fetch('/api/analytics/track-usage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ userId, feature, timestamp: Date.now() })
    })
  } catch (error) {
    console.error('Failed to track usage:', error)
  }
}

// Use in components
const handleFeatureUse = () => {
  trackFeatureUsage(user.id, 'projects')
  // ... rest of feature logic
}
```

## 🎨 UI/UX Enhancements

### Add Upgrade Prompts

```jsx
const UpgradePrompt = ({ feature, currentPlan }) => (
  <div className="upgrade-prompt">
    <div className="prompt-content">
      <Crown className="crown-icon" />
      <h3>Unlock {feature}</h3>
      <p>Upgrade to Pro to access this feature and more!</p>
      <div className="benefits">
        <div>✨ Unlimited access</div>
        <div>🚀 Priority support</div>
        <div>📊 Advanced analytics</div>
      </div>
      <button className="upgrade-btn">
        Upgrade Now - Only $9.99/month
      </button>
    </div>
  </div>
)
```

### Plan Comparison Widget

```jsx
const PlanComparison = () => (
  <div className="plan-comparison">
    <div className="plan free">
      <h3>Free</h3>
      <ul>
        <li>2 roadmaps/month</li>
        <li>3 projects/month</li>
        <li>10 resources/month</li>
      </ul>
    </div>
    <div className="plan pro popular">
      <h3>Pro - $9.99/month</h3>
      <ul>
        <li>Unlimited roadmaps</li>
        <li>Unlimited projects</li>
        <li>Unlimited resources</li>
        <li>Job opportunities</li>
        <li>Priority support</li>
      </ul>
    </div>
  </div>
)
```

## 🔒 Security Considerations

### Server-Side Validation

Always validate subscription status on the server:

```python
# Don't rely only on frontend checks
@app.post("/api/premium-action")
async def premium_action(user_id: str):
    # Always check subscription server-side
    access = await subscription_middleware.check_feature_access(user_id, "premium_feature")
    
    if not access["allowed"]:
        raise HTTPException(status_code=402, detail="Subscription required")
    
    # Proceed with premium action
    return {"result": "success"}
```

### Rate Limiting

```python
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

@app.post("/api/generate-roadmap")
@require_subscription("roadmaps")
async def generate_roadmap(
    request: RoadmapRequest,
    ratelimit: RateLimiter = Depends(RateLimiter(times=10, seconds=60))
):
    # Rate limited premium endpoint
    pass
```

## 📱 Mobile Responsiveness

Ensure subscription modals work on mobile:

```css
@media (max-width: 768px) {
  .subscription-modal {
    margin: 1rem;
    max-height: 90vh;
  }
  
  .plans-grid {
    grid-template-columns: 1fr;
  }
  
  .upgrade-prompt {
    padding: 1rem;
    text-align: center;
  }
}
```

## 🧪 Testing Your Integration

### Test Checklist

- [ ] Free users see upgrade prompts
- [ ] Pro users have unlimited access  
- [ ] Feature gates work correctly
- [ ] Payment flow completes successfully
- [ ] Webhooks update subscription status
- [ ] Cancelled subscriptions lose access
- [ ] UI shows correct plan status

### Test Commands

```bash
# Test subscription service
curl http://localhost:8004/api/subscription/plans

# Test feature access
curl http://localhost:8004/api/subscription/feature-access/user123/projects

# Test with different user IDs and features
curl http://localhost:8004/api/subscription/feature-access/user123/opportunities
```

## 🎉 Launch Checklist

Before going live:

- [ ] Test payment flow end-to-end
- [ ] Configure production Stripe keys
- [ ] Set up webhook endpoints
- [ ] Test feature gates on all pages
- [ ] Verify subscription status updates
- [ ] Test cancellation flow
- [ ] Add analytics tracking
- [ ] Update documentation
- [ ] Train support team

---

## 🚀 You're Ready!

With this integration, your PathWise platform now has:

✅ **Complete subscription management**
✅ **Feature-gated premium content** 
✅ **Seamless payment processing**
✅ **Automatic access control**
✅ **Beautiful upgrade prompts**
✅ **Real-time subscription updates**

Users will automatically unlock all opportunities, projects, and premium features when they complete payment! 🎯


