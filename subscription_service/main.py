"""
Subscription Service for PathWise
Handles subscription plans, payments, and feature access control
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
import json
import razorpay
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import uvicorn
from dotenv import load_dotenv
import secrets
import hashlib
import hmac

load_dotenv()

app = FastAPI(
    title="PathWise Subscription Service",
    description="Subscription management and payment processing",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Razorpay configuration
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_...")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "...")
razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# MongoDB connection
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.pathwise
subscriptions_collection = db.subscriptions
users_collection = db.users

# Subscription Plans
SUBSCRIPTION_PLANS = {
    "free": {
        "name": "Free Plan",
        "price": 0,
        "price_id": None,
        "features": {
            "roadmaps": 2,
            "projects": 3,
            "resources": 10,
            "opportunities": 0,
            "mentorship": False,
            "advanced_analytics": False,
            "priority_support": False,
            "custom_roadmaps": False
        },
        "description": "Basic access to PathWise features"
    },
    "pro": {
        "name": "Pro Plan",
        "price": 799,  # Price in paise (₹7.99)
        "price_display": "₹799/month",
        "features": {
            "roadmaps": -1,  # unlimited
            "projects": -1,  # unlimited
            "resources": -1,  # unlimited
            "opportunities": -1,  # unlimited
            "mentorship": True,
            "advanced_analytics": True,
            "priority_support": True,
            "custom_roadmaps": True
        },
        "description": "Full access to all PathWise features"
    },
    "enterprise": {
        "name": "Enterprise Plan",
        "price": 2999,  # Price in paise (₹29.99)
        "price_display": "₹2999/month",
        "features": {
            "roadmaps": -1,
            "projects": -1,
            "resources": -1,
            "opportunities": -1,
            "mentorship": True,
            "advanced_analytics": True,
            "priority_support": True,
            "custom_roadmaps": True,
            "team_collaboration": True,
            "api_access": True,
            "white_label": True
        },
        "description": "Advanced features for teams and organizations"
    }
}

# Pydantic Models
class SubscriptionPlan(BaseModel):
    plan_id: str
    name: str
    price: float
    features: Dict[str, Any]
    description: str

class UserSubscription(BaseModel):
    user_id: str
    plan: str
    status: str  # active, canceled, expired, trial
    start_date: datetime
    end_date: Optional[datetime]
    stripe_subscription_id: Optional[str]
    stripe_customer_id: Optional[str]
    trial_end: Optional[datetime]

class CreateOrderRequest(BaseModel):
    user_id: str
    plan: str

class FeatureAccess(BaseModel):
    feature: str
    allowed: bool
    current_usage: int
    limit: int
    plan: str

class UsageStats(BaseModel):
    roadmaps_created: int
    projects_accessed: int
    resources_viewed: int
    opportunities_applied: int

# Helper Functions
async def get_user_subscription(user_id: str) -> Optional[UserSubscription]:
    """Get user's current subscription"""
    subscription = await subscriptions_collection.find_one({"user_id": user_id})
    if subscription:
        subscription["_id"] = str(subscription["_id"])
        return UserSubscription(**subscription)
    return None

async def get_user_usage_stats(user_id: str) -> UsageStats:
    """Get user's current usage statistics"""
    # This would integrate with your existing services
    # For now, returning mock data - you'd implement actual counting
    return UsageStats(
        roadmaps_created=5,
        projects_accessed=12,
        resources_viewed=45,
        opportunities_applied=3
    )

async def check_feature_access(user_id: str, feature: str) -> FeatureAccess:
    """Check if user has access to a specific feature"""
    subscription = await get_user_subscription(user_id)
    usage_stats = await get_user_usage_stats(user_id)
    
    # Default to free plan if no subscription
    plan = subscription.plan if subscription else "free"
    plan_features = SUBSCRIPTION_PLANS[plan]["features"]
    
    # Get current usage based on feature
    usage_mapping = {
        "roadmaps": usage_stats.roadmaps_created,
        "projects": usage_stats.projects_accessed,
        "resources": usage_stats.resources_viewed,
        "opportunities": usage_stats.opportunities_applied
    }
    
    current_usage = usage_mapping.get(feature, 0)
    limit = plan_features.get(feature, 0)
    
    # Check access
    if limit == -1:  # unlimited
        allowed = True
    elif isinstance(limit, bool):  # boolean feature
        allowed = limit
    else:  # numeric limit
        allowed = current_usage < limit
    
    return FeatureAccess(
        feature=feature,
        allowed=allowed,
        current_usage=current_usage,
        limit=limit if limit != -1 else 999999,
        plan=plan
    )

# API Endpoints
@app.get("/")
async def root():
    return {"message": "PathWise Subscription Service", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/subscription/plans", response_model=List[SubscriptionPlan])
async def get_subscription_plans():
    """Get all available subscription plans"""
    plans = []
    for plan_id, plan_data in SUBSCRIPTION_PLANS.items():
        plans.append(SubscriptionPlan(
            plan_id=plan_id,
            name=plan_data["name"],
            price=plan_data["price"],
            features=plan_data["features"],
            description=plan_data["description"]
        ))
    return plans

@app.get("/api/subscription/user/{user_id}")
async def get_user_subscription_info(user_id: str):
    """Get user's subscription information"""
    subscription = await get_user_subscription(user_id)
    usage_stats = await get_user_usage_stats(user_id)
    
    if not subscription:
        # Create default free subscription
        free_sub = UserSubscription(
            user_id=user_id,
            plan="free",
            status="active",
            start_date=datetime.now(),
            end_date=None,
            stripe_subscription_id=None,
            stripe_customer_id=None,
            trial_end=None
        )
        await subscriptions_collection.insert_one(free_sub.model_dump())
        subscription = free_sub
    
    return {
        "subscription": subscription,
        "usage": usage_stats,
        "plan_details": SUBSCRIPTION_PLANS[subscription.plan]
    }

@app.get("/api/subscription/feature-access/{user_id}/{feature}")
async def check_user_feature_access(user_id: str, feature: str):
    """Check if user has access to a specific feature"""
    access = await check_feature_access(user_id, feature)
    return access

@app.post("/api/subscription/create-order")
async def create_razorpay_order(request: CreateOrderRequest):
    """Create a Razorpay order for subscription"""
    try:
        plan = SUBSCRIPTION_PLANS.get(request.plan)
        if not plan or request.plan == "free":
            raise HTTPException(status_code=400, detail="Invalid plan")
        
        # Get user details
        user = await users_collection.find_one({"_id": ObjectId(request.user_id)})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create Razorpay order
        order_data = {
            "amount": plan["price"],  # Amount in paise
            "currency": "INR",
            "receipt": f"order_{request.user_id}_{int(datetime.now().timestamp())}",
            "notes": {
                "user_id": request.user_id,
                "plan": request.plan,
                "email": user.get("email", ""),
                "name": user.get("full_name", f"{user.get('firstName', '')} {user.get('lastName', '')}").strip()
            }
        }
        
        order = razorpay_client.order.create(data=order_data)
        
        return {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": RAZORPAY_KEY_ID,
            "name": "PathWise Pro",
            "description": f"Upgrade to {plan['name']}",
            "prefill": {
                "name": user.get("full_name", f"{user.get('firstName', '')} {user.get('lastName', '')}").strip(),
                "email": user.get("email", ""),
                "contact": user.get("phone", "")
            },
            "theme": {
                "color": "#6366f1"
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@app.post("/api/subscription/verify-payment")
async def verify_payment(request: dict):
    """Verify Razorpay payment and activate subscription"""
    try:
        # Extract payment details
        razorpay_order_id = request.get("razorpay_order_id")
        razorpay_payment_id = request.get("razorpay_payment_id")
        razorpay_signature = request.get("razorpay_signature")
        user_id = request.get("user_id")
        plan = request.get("plan")
        
        if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, user_id, plan]):
            raise HTTPException(status_code=400, detail="Missing payment details")
        
        # Check if this is a dummy payment (for testing)
        is_dummy_payment = (
            razorpay_order_id.startswith("order_dummy_") or
            razorpay_payment_id.startswith("pay_dummy_")
        )
        
        if not is_dummy_payment:
            # Verify payment signature for real payments
            body = razorpay_order_id + "|" + razorpay_payment_id
            expected_signature = hmac.new(
                key=RAZORPAY_KEY_SECRET.encode(),
                msg=body.encode(),
                digestmod=hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(expected_signature, razorpay_signature):
                raise HTTPException(status_code=400, detail="Invalid payment signature")
            
            # Verify payment with Razorpay
            try:
                razorpay_client.utility.verify_payment_signature({
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': razorpay_payment_id,
                    'razorpay_signature': razorpay_signature
                })
            except:
                raise HTTPException(status_code=400, detail="Payment verification failed")
        
        # Update user subscription
        subscription_data = {
            "user_id": user_id,
            "plan": plan,
            "status": "active",
            "start_date": datetime.now(),
            "end_date": datetime.now() + timedelta(days=30),  # Monthly subscription
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": razorpay_payment_id,
            "trial_end": None,
            "is_test_payment": is_dummy_payment
        }
        
        await subscriptions_collection.update_one(
            {"user_id": user_id},
            {"$set": subscription_data},
            upsert=True
        )
        
        # Also update the user document to mark as premium
        await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"premium": True, "subscription_plan": plan}}
        )
        
        return {
            "status": "success",
            "message": "Payment verified and subscription activated",
            "plan": plan,
            "is_test": is_dummy_payment
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Payment verification error: {str(e)}")

@app.post("/api/subscription/cancel/{user_id}")
async def cancel_subscription(user_id: str):
    """Cancel user's subscription"""
    try:
        subscription = await get_user_subscription(user_id)
        if not subscription or subscription.status != "active":
            raise HTTPException(status_code=400, detail="No active subscription found")
        
        # Update local subscription (Razorpay doesn't have recurring subscriptions to cancel)
        await subscriptions_collection.update_one(
            {"user_id": user_id},
            {"$set": {"status": "canceled", "end_date": datetime.now()}}
        )
        
        return {"message": "Subscription canceled successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error canceling subscription: {str(e)}")

@app.get("/api/subscription/config")
async def get_razorpay_config():
    """Get Razorpay key ID for frontend"""
    return {"key_id": RAZORPAY_KEY_ID}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
