# Quick Start: Payment Integration Testing

## Prerequisites
- MongoDB running on localhost:27017
- Python environment with dependencies installed
- Node.js and npm installed

## Step-by-Step Testing Guide

### 1. Start MongoDB
```bash
# Make sure MongoDB is running
mongod
```

### 2. Start Subscription Service
```bash
# Windows
start_subscription_service.bat

# Or manually
cd subscription_service
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8005
INFO:     Application startup complete.
```

### 3. Start Auth Backend
```bash
cd auth_back
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:5000
```

### 4. Start Frontend Dashboard
```bash
cd dashboard
npm run dev
```

Expected output:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

### 5. Test the Payment Flow

#### A. Login to Application
1. Open browser: http://localhost:5173/
2. Login with your credentials
3. You'll land on the Dashboard

#### B. Try Accessing Projects (Free User)
1. Click on "Projects" in the sidebar
2. Notice the **crown badge** 👑 next to Projects
3. You'll see the **Premium Gate** screen:
   - Lock icon with crown badge
   - "Premium Feature" heading
   - Your current plan status (Free)
   - List of premium features
   - "Upgrade to Premium" button

#### C. Upgrade with Dummy Payment (Recommended for Testing)
1. Click **"Upgrade to Premium"** button
2. Premium modal opens showing plans
3. Select "Pro Plan" (₹799/month) - should be pre-selected
4. Click **"Dummy Payment (Test)"** button
5. Wait 2 seconds for processing animation
6. Modal closes automatically
7. Projects page loads with full access! 🎉

#### D. Verify Premium Access
1. Notice the crown badge is now gone from sidebar
2. You can now access all projects
3. Try navigating away and back - access persists
4. Check MongoDB to see subscription record

### 6. Verify Database Update

Connect to MongoDB:
```bash
mongosh
use pathwise

# Check subscription
db.subscriptions.find({ user_id: "YOUR_USER_ID" }).pretty()

# Check user document
db.users.find({ _id: ObjectId("YOUR_USER_ID") }).pretty()
```

Expected subscription document:
```javascript
{
  user_id: "YOUR_USER_ID",
  plan: "pro",
  status: "active",
  start_date: ISODate("2024-..."),
  end_date: ISODate("2024-..."),
  razorpay_order_id: "order_dummy_...",
  razorpay_payment_id: "pay_dummy_...",
  is_test_payment: true
}
```

Expected user document additions:
```javascript
{
  ...existing fields...
  premium: true,
  subscription_plan: "pro"
}
```

## Testing Real Razorpay Payment

### Setup Razorpay Test Account

1. Go to https://razorpay.com/
2. Create test account
3. Get API keys from Dashboard
4. Add to `.env` file:
```env
RAZORPAY_KEY_ID=rzp_test_your_key_here
RAZORPAY_KEY_SECRET=your_secret_here
```

### Test Payment Flow

1. Follow steps 1-5B above
2. In premium modal, click **"Pay with Razorpay"** button
3. Razorpay checkout opens in new window
4. Use test card:
   - **Card Number**: 4111 1111 1111 1111
   - **CVV**: 123
   - **Expiry**: Any future date (e.g., 12/25)
   - **Name**: Your Name
5. Click "Pay Now"
6. Payment processes
7. Modal closes
8. Projects page loads with access

## Automated Testing

### Run Test Script
```bash
python test_payment_flow.py
```

This will:
1. Get subscription plans
2. Check user subscription
3. Test feature access
4. Simulate dummy payment
5. Verify subscription update
6. Display comprehensive results

### Expected Output
```
🚀 PATHWISE PAYMENT INTEGRATION TEST SUITE 🚀

==============================
TEST 1: Get Subscription Plans
==============================
✅ Successfully retrieved 2 plans

==============================
TEST 2: Get User Subscription
==============================
✅ Successfully retrieved subscription info

==============================
TEST 3: Check Feature Access
==============================
PROJECTS: ✅ ALLOWED

==============================
TEST 5: Dummy Payment Verification
==============================
✅ Payment verification successful!

==============================
TEST SUMMARY
==============================
Tests Passed: 4/4
Success Rate: 100.0%

🎉 ALL TESTS PASSED! 🎉
```

## Troubleshooting

### Issue: "Connection refused" on port 8005
**Solution**: 
```bash
# Check if service is running
netstat -an | findstr 8005

# Restart subscription service
start_subscription_service.bat
```

### Issue: "User not found" error
**Solution**:
```bash
# Update TEST_USER_ID in test_payment_flow.py
# Get your user ID from MongoDB:
mongosh
use pathwise
db.users.find({}, {_id: 1, email: 1})
```

### Issue: Premium gate still showing after payment
**Solution**:
```bash
# Hard refresh browser
Ctrl + Shift + R

# Or clear site data and reload
```

### Issue: Razorpay not opening
**Solution**:
1. Check browser console for errors
2. Disable ad-blocker temporarily
3. Verify Razorpay script loaded:
```javascript
console.log(typeof Razorpay) // Should be "function"
```

## Visual Indicators

### Sidebar
- **Free User**: Projects has pulsing gold crown badge 👑
- **Premium User**: No badge, normal access

### Premium Gate (Free Users)
- Lock icon with crown badge
- "Premium Feature" heading
- Current plan display
- Usage statistics
- List of premium features
- Upgrade button

### Payment Modal
- Plan cards with selection
- Most Popular badge on Pro plan
- Price in ₹ (Indian Rupees)
- Feature list with checkmarks
- Two payment options:
  - Dummy Payment (for testing)
  - Pay with Razorpay (real payment)

## What Happens on Payment Success

1. ✅ User subscription record created/updated in MongoDB
2. ✅ User document updated with `premium: true`
3. ✅ 30-day subscription validity set
4. ✅ Premium gate removes immediately
5. ✅ Projects page loads with full access
6. ✅ Crown badge removed from sidebar
7. ✅ Access persists across page refreshes

## Testing Checklist

Use this checklist to verify everything works:

- [ ] Subscription service starts without errors
- [ ] Auth backend connects to MongoDB
- [ ] Frontend loads at localhost:5173
- [ ] Can login successfully
- [ ] Dashboard displays correctly
- [ ] Projects link shows crown badge
- [ ] Clicking Projects shows premium gate
- [ ] Premium gate displays correctly
- [ ] Can click "Upgrade to Premium"
- [ ] Payment modal opens with plans
- [ ] Can select different plans
- [ ] Dummy payment button works
- [ ] Processing animation shows
- [ ] Modal closes after payment
- [ ] Projects page loads with access
- [ ] Crown badge disappears
- [ ] MongoDB subscription record exists
- [ ] User document has premium flag
- [ ] Access persists after refresh
- [ ] Can navigate to other pages and back
- [ ] Mobile responsive design works

## Next Steps

After successful testing:

1. **Production Setup**:
   - Replace Razorpay test keys with live keys
   - Update CORS origins for production domains
   - Set up SSL certificates
   - Configure production MongoDB

2. **Additional Features**:
   - Add payment history page
   - Implement automatic renewal
   - Add invoice generation
   - Create subscription management page
   - Add billing address collection
   - Implement refund system

3. **Monitoring**:
   - Set up payment success/failure tracking
   - Monitor subscription expiry dates
   - Track revenue metrics
   - Monitor API errors

## Support

If you encounter issues:
1. Check the comprehensive guide: `PAYMENT_INTEGRATION_COMPLETE.md`
2. Review error logs in terminal
3. Check browser console for frontend errors
4. Verify MongoDB is accessible
5. Ensure all services are running

---

**Happy Testing!** 🎉

The payment integration is complete and ready for testing.

