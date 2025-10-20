# PathWise Subscription Service

A comprehensive subscription management system for PathWise that handles payment processing, feature access control, and subscription lifecycle management.

## 🚀 Features

- **Multiple Subscription Plans**: Free, Pro, and Enterprise tiers
- **Stripe Integration**: Secure payment processing with Stripe Checkout
- **Feature Access Control**: Granular control over feature availability
- **Usage Tracking**: Monitor user feature consumption
- **Subscription Lifecycle**: Handle upgrades, cancellations, and renewals
- **Webhook Support**: Real-time subscription status updates
- **MongoDB Integration**: Persistent subscription data storage

## 📋 Subscription Plans

### Free Plan
- 2 custom roadmaps per month
- 3 project recommendations per month  
- 10 learning resources per month
- No job opportunities access
- Basic support

### Pro Plan - $9.99/month
- ✅ **Unlimited** custom roadmaps
- ✅ **Unlimited** project recommendations
- ✅ **Unlimited** learning resources
- ✅ **Unlimited** job opportunities
- ✅ Mentorship access
- ✅ Advanced analytics
- ✅ Priority support
- ✅ AI-powered roadmaps

### Enterprise Plan - $29.99/month
- ✅ **All Pro features**
- ✅ Team collaboration tools
- ✅ API access
- ✅ White-label solution
- ✅ Dedicated support

## 🛠 Installation & Setup

### 1. Install Dependencies

```bash
cd subscription_service
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_PRO_PRICE_ID=price_your_pro_plan_price_id
STRIPE_ENTERPRISE_PRICE_ID=price_your_enterprise_plan_price_id

# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017

# Service URLs
FRONTEND_URL=http://localhost:5173
```

### 3. Stripe Setup

1. Create a [Stripe account](https://stripe.com)
2. Get your API keys from the Stripe Dashboard
3. Create products and prices in Stripe:
   - Pro Plan: $9.99/month recurring
   - Enterprise Plan: $29.99/month recurring
4. Copy the price IDs to your `.env` file
5. Set up webhooks (see Webhooks section below)

### 4. Start the Service

```bash
# Using the batch file (Windows)
start_server.bat

# Or manually
python main.py
```

The service will start on `http://localhost:8004`

## 🔗 API Endpoints

### Subscription Plans
- `GET /api/subscription/plans` - Get all available plans
- `GET /api/subscription/user/{user_id}` - Get user subscription info
- `GET /api/subscription/feature-access/{user_id}/{feature}` - Check feature access

### Payment & Checkout
- `POST /api/subscription/create-checkout` - Create Stripe checkout session
- `POST /api/subscription/webhook` - Handle Stripe webhooks
- `POST /api/subscription/cancel/{user_id}` - Cancel subscription

### Configuration
- `GET /api/subscription/config` - Get Stripe publishable key

## 🎯 Frontend Integration

### 1. Install Dependencies

The subscription components are already included in the dashboard. Make sure you have:

```bash
npm install framer-motion lucide-react
```

### 2. Import Components

```jsx
import SubscriptionModal from '../components/SubscriptionModal'
import FeatureGate from '../components/FeatureGate'
```

### 3. Usage Examples

#### Subscription Modal
```jsx
<SubscriptionModal
  isOpen={showModal}
  onClose={() => setShowModal(false)}
  userId={user.id}
  currentPlan="free"
/>
```

#### Feature Gate
```jsx
<FeatureGate 
  userId={user.id} 
  feature="projects"
  showUpgradePrompt={true}
>
  <ProjectRecommendations />
</FeatureGate>
```

## 🔒 Feature Access Control

### Available Features
- `roadmaps` - Custom roadmap generation
- `projects` - Project recommendations  
- `resources` - Learning resources
- `opportunities` - Job opportunities
- `mentorship` - Mentor access
- `advanced_analytics` - Analytics dashboard

### Usage in Services

#### Python (FastAPI)
```python
from middleware import require_subscription

@app.post("/api/roadmap/generate")
@require_subscription("roadmaps")
async def generate_roadmap(request: RoadmapRequest):
    # Your existing code
    pass
```

#### Node.js (Express)
```javascript
const { checkSubscription } = require('./middleware');

app.post('/api/projects/recommend', 
  checkSubscription('projects'),
  (req, res) => {
    // Your existing code
  }
);
```

## 🔔 Webhooks Setup

### 1. Create Webhook Endpoint in Stripe

1. Go to Stripe Dashboard → Webhooks
2. Add endpoint: `https://yourdomain.com/api/subscription/webhook`
3. Select events:
   - `checkout.session.completed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`

### 2. Configure Webhook Secret

Add the webhook signing secret to your `.env`:

```env
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## 🗄 Database Schema

### Subscriptions Collection

```javascript
{
  "_id": ObjectId,
  "user_id": "user123",
  "plan": "pro", // free, pro, enterprise
  "status": "active", // active, canceled, expired, trial
  "start_date": ISODate,
  "end_date": ISODate,
  "stripe_subscription_id": "sub_stripe123",
  "stripe_customer_id": "cus_stripe123",
  "trial_end": ISODate,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

## 🧪 Testing

### Test Payment Flow

1. Use Stripe test cards:
   - Success: `4242424242424242`
   - Declined: `4000000000000002`

2. Test webhook events using Stripe CLI:
```bash
stripe listen --forward-to localhost:8004/api/subscription/webhook
```

### Test Feature Access

```python
# Test script
import requests

# Check feature access
response = requests.get(
    "http://localhost:8004/api/subscription/feature-access/user123/projects"
)
print(response.json())
```

## 🚀 Deployment

### Production Checklist

1. ✅ Update Stripe keys to live mode
2. ✅ Configure production MongoDB
3. ✅ Set up webhook endpoints
4. ✅ Enable HTTPS
5. ✅ Configure CORS for production domains
6. ✅ Set up monitoring and logging

### Environment Variables

```env
# Production Stripe keys
STRIPE_SECRET_KEY=sk_live_your_live_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_live_key

# Production MongoDB
MONGODB_URL=mongodb://your-production-db

# Production URLs
FRONTEND_URL=https://your-domain.com
```

## 🔧 Customization

### Adding New Plans

1. Update `SUBSCRIPTION_PLANS` in `main.py`:

```python
SUBSCRIPTION_PLANS["custom"] = {
    "name": "Custom Plan",
    "price": 19.99,
    "price_id": "price_custom_id",
    "features": {
        "roadmaps": -1,
        "custom_feature": True
    }
}
```

2. Create corresponding Stripe product and price
3. Update frontend components if needed

### Adding New Features

1. Add feature to plan definitions
2. Update feature checking logic
3. Add feature gates to relevant components

## 🐛 Troubleshooting

### Common Issues

1. **Stripe webhook not working**
   - Check webhook URL is accessible
   - Verify webhook secret is correct
   - Check Stripe webhook logs

2. **Feature access always denied**
   - Check user_id is being passed correctly
   - Verify subscription service is running
   - Check MongoDB connection

3. **Payment not updating subscription**
   - Check webhook events are being received
   - Verify webhook handler is processing correctly
   - Check MongoDB updates

### Debug Mode

Enable debug logging by setting:
```env
DEBUG=true
```

## 📞 Support

For issues or questions:
1. Check the logs in the subscription service
2. Verify Stripe webhook delivery
3. Test API endpoints manually
4. Check MongoDB subscription data

## 🔄 Updates & Migration

When updating subscription plans or features:
1. Update the backend service first
2. Deploy frontend changes
3. Communicate changes to existing subscribers
4. Handle grandfathering of existing plans if needed

---

## 🎉 Success!

Your PathWise subscription system is now ready! Users can:

- ✅ View subscription plans
- ✅ Upgrade/downgrade plans
- ✅ Access premium features
- ✅ Manage subscriptions
- ✅ Receive feature-gated content

The system automatically unlocks all opportunities, projects, and premium features when users complete payment through the Stripe checkout flow.


