"""
Middleware to integrate subscription checking with existing services
"""

import asyncio
from functools import wraps
from typing import Optional, Dict, Any
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

SUBSCRIPTION_SERVICE_URL = os.getenv("SUBSCRIPTION_SERVICE_URL", "http://localhost:8004")

class SubscriptionMiddleware:
    """Middleware to check subscription access for API endpoints"""
    
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def check_feature_access(self, user_id: str, feature: str) -> Dict[str, Any]:
        """Check if user has access to a specific feature"""
        try:
            session = await self.get_session()
            async with session.get(
                f"{SUBSCRIPTION_SERVICE_URL}/api/subscription/feature-access/{user_id}/{feature}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "allowed": data.get("allowed", False),
                        "current_usage": data.get("current_usage", 0),
                        "limit": data.get("limit", 0),
                        "plan": data.get("plan", "free")
                    }
                else:
                    # If subscription service is down, allow access
                    return {"allowed": True, "current_usage": 0, "limit": -1, "plan": "free"}
        except Exception as e:
            print(f"Subscription check failed: {e}")
            # If subscription service is down, allow access
            return {"allowed": True, "current_usage": 0, "limit": -1, "plan": "free"}
    
    async def increment_usage(self, user_id: str, feature: str) -> bool:
        """Increment usage count for a feature (would be implemented in subscription service)"""
        try:
            # This would be implemented as an API call to subscription service
            # For now, we'll just return True
            return True
        except Exception as e:
            print(f"Usage increment failed: {e}")
            return True

# Global middleware instance
subscription_middleware = SubscriptionMiddleware()

def require_subscription(feature: str):
    """Decorator to require subscription for an endpoint"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user_id from request
            user_id = None
            
            # Try to get user_id from different sources
            if 'user_id' in kwargs:
                user_id = kwargs['user_id']
            elif len(args) > 0 and hasattr(args[0], 'user_id'):
                user_id = args[0].user_id
            elif len(args) > 0 and hasattr(args[0], 'get'):
                # For request objects
                user_id = args[0].get('user_id')
            
            if not user_id:
                # If no user_id, allow access (for backwards compatibility)
                return await func(*args, **kwargs)
            
            # Check subscription access
            access = await subscription_middleware.check_feature_access(user_id, feature)
            
            if not access["allowed"]:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=402,  # Payment Required
                    detail={
                        "error": "Subscription required",
                        "feature": feature,
                        "current_usage": access["current_usage"],
                        "limit": access["limit"],
                        "plan": access["plan"],
                        "message": f"You've reached your {feature} limit on the {access['plan']} plan. Upgrade to continue."
                    }
                )
            
            # Increment usage count
            await subscription_middleware.increment_usage(user_id, feature)
            
            # Call the original function
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator

def check_subscription_sync(user_id: str, feature: str) -> Dict[str, Any]:
    """Synchronous version for non-async functions"""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            subscription_middleware.check_feature_access(user_id, feature)
        )
    except Exception as e:
        print(f"Sync subscription check failed: {e}")
        return {"allowed": True, "current_usage": 0, "limit": -1, "plan": "free"}

# Express.js middleware equivalent (for Node.js services)
def create_express_middleware():
    """Create Express.js middleware for Node.js services"""
    return """
const axios = require('axios');

const SUBSCRIPTION_SERVICE_URL = process.env.SUBSCRIPTION_SERVICE_URL || 'http://localhost:8004';

const checkSubscription = (feature) => {
  return async (req, res, next) => {
    try {
      const userId = req.user?.id || req.body?.user_id || req.params?.user_id;
      
      if (!userId) {
        return next(); // Allow access if no user_id (backwards compatibility)
      }
      
      const response = await axios.get(
        `${SUBSCRIPTION_SERVICE_URL}/api/subscription/feature-access/${userId}/${feature}`
      );
      
      if (!response.data.allowed) {
        return res.status(402).json({
          error: 'Subscription required',
          feature: feature,
          current_usage: response.data.current_usage,
          limit: response.data.limit,
          plan: response.data.plan,
          message: `You've reached your ${feature} limit on the ${response.data.plan} plan. Upgrade to continue.`
        });
      }
      
      // Add subscription info to request
      req.subscription = response.data;
      next();
    } catch (error) {
      console.error('Subscription check failed:', error.message);
      // Allow access if subscription service is down
      next();
    }
  };
};

module.exports = { checkSubscription };
"""


