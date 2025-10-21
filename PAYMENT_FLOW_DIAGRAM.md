# Payment Flow Diagram

## Complete User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER JOURNEY                            │
└─────────────────────────────────────────────────────────────────┘

1. USER LOGIN
   └─→ Auth Service (Port 5000)
       └─→ Returns JWT Token + User Info
           └─→ Store in localStorage


2. NAVIGATE TO PROJECTS TAB
   └─→ Sidebar Component
       ├─→ Shows Crown Badge 👑 (if free user)
       └─→ Route: /projects


3. PROTECTED FEATURE CHECK
   └─→ ProtectedFeature Component
       └─→ Call: GET /api/subscription/feature-access/{user_id}/projects
           ├─→ Subscription Service (Port 8005)
           │   └─→ Check MongoDB subscriptions collection
           │       ├─→ FREE USER → allowed: false
           │       └─→ PREMIUM USER → allowed: true
           │
           ├─→ IF PREMIUM: Show Projects Page
           └─→ IF FREE: Show Premium Gate ⬇️


4. PREMIUM GATE (FREE USERS ONLY)
   ┌──────────────────────────────────────┐
   │  🔒 Premium Feature                 │
   │                                      │
   │  Current Plan: Free                  │
   │  Projects Used: 3/3                  │
   │                                      │
   │  Premium Features:                   │
   │  ✓ Unlimited Projects                │
   │  ✓ Unlimited Roadmaps                │
   │  ✓ Advanced Analytics                │
   │  ✓ Mentorship Access                 │
   │                                      │
   │  [Upgrade to Premium]                │
   └──────────────────────────────────────┘
           │
           └─→ CLICK UPGRADE


5. PAYMENT MODAL OPENS
   ┌──────────────────────────────────────┐
   │  👑 Upgrade to Premium               │
   │                                      │
   │  ┌────────┐  ┌────────┐             │
   │  │  PRO   │  │ ENTER  │             │
   │  │ ₹799/mo│  │₹2999/mo│             │
   │  └────────┘  └────────┘             │
   │                                      │
   │  [Dummy Payment (Test)]              │
   │  [Pay with Razorpay]                 │
   └──────────────────────────────────────┘
           │
           ├─→ OPTION A: DUMMY PAYMENT (Testing)
           └─→ OPTION B: RAZORPAY PAYMENT


┌─────────────────────────────────────────────────────────────────┐
│                    OPTION A: DUMMY PAYMENT                      │
└─────────────────────────────────────────────────────────────────┘

6A. DUMMY PAYMENT FLOW
    └─→ Frontend simulates payment
        ├─→ Show loading animation (2 seconds)
        └─→ Generate dummy IDs:
            ├─→ order_dummy_1234567890
            ├─→ pay_dummy_1234567890
            └─→ dummy_signature_1234567890
                │
                └─→ Call: POST /api/subscription/verify-payment
                    {
                      razorpay_order_id: "order_dummy_...",
                      razorpay_payment_id: "pay_dummy_...",
                      razorpay_signature: "dummy_signature_...",
                      user_id: "USER_ID",
                      plan: "pro"
                    }


┌─────────────────────────────────────────────────────────────────┐
│                   OPTION B: RAZORPAY PAYMENT                    │
└─────────────────────────────────────────────────────────────────┘

6B. RAZORPAY PAYMENT FLOW
    └─→ Call: POST /api/subscription/create-order
        {
          user_id: "USER_ID",
          plan: "pro"
        }
        │
        └─→ Subscription Service
            └─→ Call Razorpay API: order.create()
                └─→ Returns Order ID
                    │
                    └─→ Frontend opens Razorpay Checkout
                        ┌──────────────────────────────┐
                        │   Razorpay Secure Checkout   │
                        │                              │
                        │   Card: 4111 1111 1111 1111  │
                        │   CVV: 123                   │
                        │   Expiry: 12/25              │
                        │                              │
                        │   [Pay ₹799]                 │
                        └──────────────────────────────┘
                        │
                        └─→ User enters card details
                            └─→ Razorpay processes payment
                                └─→ Returns payment response:
                                    {
                                      razorpay_order_id,
                                      razorpay_payment_id,
                                      razorpay_signature
                                    }
                                    │
                                    └─→ Call: POST /api/subscription/verify-payment


┌─────────────────────────────────────────────────────────────────┐
│               PAYMENT VERIFICATION (Both Options)               │
└─────────────────────────────────────────────────────────────────┘

7. VERIFY PAYMENT
   └─→ Subscription Service receives payment data
       │
       ├─→ IF DUMMY PAYMENT (starts with "dummy_" or "order_dummy_")
       │   └─→ Skip Razorpay verification
       │
       └─→ IF REAL PAYMENT
           └─→ Verify HMAC signature
               └─→ Call Razorpay API: verify_payment_signature()
                   │
                   └─→ IF VALID ⬇️


8. UPDATE DATABASE
   └─→ MongoDB Operations (Parallel)
       │
       ├─→ UPDATE subscriptions collection
       │   {
       │     user_id: "USER_ID",
       │     plan: "pro",
       │     status: "active",
       │     start_date: NOW,
       │     end_date: NOW + 30 days,
       │     razorpay_order_id: "order_...",
       │     razorpay_payment_id: "pay_...",
       │     is_test_payment: true/false
       │   }
       │
       └─→ UPDATE users collection
           {
             _id: ObjectId("USER_ID"),
             premium: true,
             subscription_plan: "pro"
           }


9. RETURN SUCCESS
   └─→ Response to Frontend
       {
         status: "success",
         message: "Payment verified and subscription activated",
         plan: "pro",
         is_test: true/false
       }


10. FRONTEND UPDATES
    └─→ Close payment modal
        └─→ Refresh feature access
            └─→ ProtectedFeature re-checks subscription
                └─→ Call: GET /api/subscription/feature-access/{user_id}/projects
                    └─→ Returns: allowed: true
                        │
                        └─→ GRANT ACCESS TO PROJECTS PAGE


11. PROJECTS PAGE LOADS
    ┌──────────────────────────────────────┐
    │  🎯 Project Ideas                    │
    │                                      │
    │  [AI Recommendation Input]           │
    │                                      │
    │  Filters: [All] [Saved] [Phase...]  │
    │                                      │
    │  ┌────────┐ ┌────────┐ ┌────────┐   │
    │  │Project1│ │Project2│ │Project3│   │
    │  └────────┘ └────────┘ └────────┘   │
    │                                      │
    │  Full unlimited access! 🎉           │
    └──────────────────────────────────────┘


12. SIDEBAR UPDATES
    └─→ Crown badge 👑 removed from Projects link
        └─→ User now has premium access across all pages
```

## Database Schema Changes

### Before Payment (Free User)
```javascript
// subscriptions collection
{
  user_id: "USER_ID",
  plan: "free",
  status: "active",
  start_date: ISODate("2024-01-01"),
  end_date: null
}

// users collection
{
  _id: ObjectId("USER_ID"),
  email: "user@example.com",
  // no premium field
}
```

### After Payment (Premium User)
```javascript
// subscriptions collection
{
  user_id: "USER_ID",
  plan: "pro",
  status: "active",
  start_date: ISODate("2024-01-15T10:30:00"),
  end_date: ISODate("2024-02-15T10:30:00"),
  razorpay_order_id: "order_dummy_1705315800",
  razorpay_payment_id: "pay_dummy_1705315800",
  is_test_payment: true,
  trial_end: null
}

// users collection
{
  _id: ObjectId("USER_ID"),
  email: "user@example.com",
  premium: true,
  subscription_plan: "pro"
}
```

## API Call Sequence

```
Frontend                 Subscription Service           MongoDB
   │                              │                        │
   ├─1. Check Access─────────────→│                        │
   │                              ├─Query Subscription────→│
   │                              │←─Return Status─────────┤
   │←─2. Access Denied────────────┤                        │
   │                              │                        │
   ├─3. Create Order──────────────→│                        │
   │                              ├─Create Razorpay Order  │
   │←─4. Order Details────────────┤                        │
   │                              │                        │
   ├─5. Process Payment           │                        │
   │   (Razorpay Checkout)        │                        │
   │                              │                        │
   ├─6. Verify Payment────────────→│                        │
   │                              ├─Verify Signature       │
   │                              ├─Update Subscription───→│
   │                              ├─Update User───────────→│
   │←─7. Success───────────────────┤                        │
   │                              │                        │
   ├─8. Re-check Access───────────→│                        │
   │                              ├─Query Subscription────→│
   │                              │←─Return Premium Status─┤
   │←─9. Access Granted────────────┤                        │
   │                              │                        │
```

## Component Architecture

```
App.jsx
 └─→ Routes
      └─→ /projects
           └─→ ProtectedRoute (Auth Check)
                └─→ Layout
                     └─→ Sidebar (Shows Crown Badge)
                     └─→ Projects Component
                          └─→ ProtectedFeature (Subscription Check)
                               ├─→ IF FREE
                               │    └─→ Premium Gate
                               │         └─→ PremiumModal
                               │              ├─→ Plan Selection
                               │              ├─→ Dummy Payment Button
                               │              └─→ Razorpay Payment Button
                               │
                               └─→ IF PREMIUM
                                    └─→ ProjectsContent (Full Access)
```

## State Management Flow

```
User State
 ├─→ localStorage: { token, user }
 │
Subscription State (Real-time Check)
 ├─→ API Call: GET /feature-access/{user_id}/projects
 ├─→ Returns: { allowed: boolean, plan: string, usage: {...} }
 │
Payment State
 ├─→ Loading: Show spinner
 ├─→ Processing: Show Razorpay modal or dummy payment
 ├─→ Success: Close modal, refresh access
 ├─→ Error: Show error message
 │
UI State
 ├─→ Show Premium Gate (free user)
 ├─→ Show Payment Modal (on upgrade click)
 ├─→ Show Projects Content (premium user)
 └─→ Update Sidebar Badge (remove crown after upgrade)
```

## Security Flow

```
Payment Request
 │
 ├─→ 1. User Authentication (JWT)
 │    └─→ Verify token
 │         └─→ Extract user_id
 │
 ├─→ 2. Create Order (Backend)
 │    └─→ Razorpay API with secret key
 │         └─→ Generate order_id
 │
 ├─→ 3. Process Payment (Razorpay)
 │    └─→ Secure payment gateway
 │         └─→ Generate payment_id + signature
 │
 ├─→ 4. Verify Signature (Backend)
 │    └─→ HMAC SHA256 verification
 │         ├─→ Expected: HMAC(order_id|payment_id, secret)
 │         └─→ Compare with received signature
 │
 └─→ 5. Update Database (Only if verified)
      └─→ Atomic transaction
           └─→ Update subscription + user
```

---

**End of Flow Diagram**

This diagram shows the complete journey from a free user clicking on Projects to successfully upgrading and accessing premium features.

