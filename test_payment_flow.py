"""
Test script for payment and subscription flow
Tests the complete integration from feature check to payment verification
"""

import requests
import json
from datetime import datetime

# Configuration
SUBSCRIPTION_API = "http://localhost:8005/api/subscription"
TEST_USER_ID = "6756b1e37ef7c53a58c7f77f"  # Replace with actual user ID

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_get_plans():
    """Test getting subscription plans"""
    print_section("TEST 1: Get Subscription Plans")
    
    try:
        response = requests.get(f"{SUBSCRIPTION_API}/plans")
        response.raise_for_status()
        plans = response.json()
        
        print(f"✅ Successfully retrieved {len(plans)} plans")
        for plan in plans:
            print(f"\n  Plan: {plan['name']}")
            print(f"  Price: ₹{plan['price']/100}")
            print(f"  Features: {len(plan['features'])} features")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_user_subscription():
    """Test getting user subscription info"""
    print_section("TEST 2: Get User Subscription")
    
    try:
        response = requests.get(f"{SUBSCRIPTION_API}/user/{TEST_USER_ID}")
        response.raise_for_status()
        data = response.json()
        
        print(f"✅ Successfully retrieved subscription info")
        print(f"\n  Current Plan: {data['subscription']['plan']}")
        print(f"  Status: {data['subscription']['status']}")
        print(f"  Start Date: {data['subscription']['start_date']}")
        
        return data
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_check_feature_access():
    """Test checking feature access"""
    print_section("TEST 3: Check Feature Access")
    
    features = ['projects', 'roadmaps', 'resources', 'mentorship']
    
    for feature in features:
        try:
            response = requests.get(f"{SUBSCRIPTION_API}/feature-access/{TEST_USER_ID}/{feature}")
            response.raise_for_status()
            access = response.json()
            
            status = "✅ ALLOWED" if access['allowed'] else "❌ BLOCKED"
            print(f"\n  {feature.upper()}: {status}")
            print(f"    Current Usage: {access['current_usage']}")
            print(f"    Limit: {'Unlimited' if access['limit'] == 999999 else access['limit']}")
            print(f"    Plan: {access['plan']}")
            
        except Exception as e:
            print(f"  ❌ Error checking {feature}: {str(e)}")

def test_create_dummy_order():
    """Test creating a dummy order"""
    print_section("TEST 4: Create Dummy Order (Skipped)")
    print("  Note: This would create an actual Razorpay order")
    print("  Skipping to avoid unnecessary API calls")

def test_dummy_payment_verification():
    """Test dummy payment verification"""
    print_section("TEST 5: Dummy Payment Verification")
    
    try:
        # Simulate dummy payment data
        payment_data = {
            "razorpay_order_id": f"order_dummy_{int(datetime.now().timestamp())}",
            "razorpay_payment_id": f"pay_dummy_{int(datetime.now().timestamp())}",
            "razorpay_signature": f"dummy_signature_{int(datetime.now().timestamp())}",
            "user_id": TEST_USER_ID,
            "plan": "pro"
        }
        
        print(f"\n  Sending dummy payment data:")
        print(f"  Order ID: {payment_data['razorpay_order_id']}")
        print(f"  Payment ID: {payment_data['razorpay_payment_id']}")
        print(f"  Plan: {payment_data['plan']}")
        
        response = requests.post(
            f"{SUBSCRIPTION_API}/verify-payment",
            json=payment_data
        )
        response.raise_for_status()
        result = response.json()
        
        print(f"\n✅ Payment verification successful!")
        print(f"  Status: {result['status']}")
        print(f"  Message: {result['message']}")
        print(f"  Plan: {result['plan']}")
        print(f"  Test Payment: {result.get('is_test', False)}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if hasattr(e, 'response'):
            print(f"  Response: {e.response.text}")
        return False

def test_verify_subscription_update():
    """Verify subscription was updated after payment"""
    print_section("TEST 6: Verify Subscription Update")
    
    try:
        response = requests.get(f"{SUBSCRIPTION_API}/user/{TEST_USER_ID}")
        response.raise_for_status()
        data = response.json()
        
        subscription = data['subscription']
        
        print(f"✅ Subscription updated successfully!")
        print(f"\n  Current Plan: {subscription['plan']}")
        print(f"  Status: {subscription['status']}")
        print(f"  Start Date: {subscription['start_date']}")
        print(f"  End Date: {subscription.get('end_date', 'N/A')}")
        
        if subscription['plan'] == 'pro' and subscription['status'] == 'active':
            print(f"\n  🎉 User now has PREMIUM access!")
            return True
        else:
            print(f"\n  ⚠️  Subscription not active or not upgraded")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "🚀 "*30)
    print("  PATHWISE PAYMENT INTEGRATION TEST SUITE")
    print("🚀 "*30)
    
    print(f"\nTest Configuration:")
    print(f"  API Base URL: {SUBSCRIPTION_API}")
    print(f"  Test User ID: {TEST_USER_ID}")
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run tests
    results.append(("Get Plans", test_get_plans()))
    results.append(("Get User Subscription", test_get_user_subscription() is not None))
    test_check_feature_access()  # Just for display, not counted
    # results.append(("Create Order", test_create_dummy_order()))
    results.append(("Verify Dummy Payment", test_dummy_payment_verification()))
    results.append(("Verify Subscription Update", test_verify_subscription_update()))
    
    # Summary
    print_section("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n  Tests Passed: {passed}/{total}")
    print(f"  Success Rate: {(passed/total)*100:.1f}%")
    
    print("\n  Detailed Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"    {status} - {test_name}")
    
    if passed == total:
        print("\n  🎉 ALL TESTS PASSED! 🎉")
        print("  Payment integration is working correctly!")
    else:
        print("\n  ⚠️  SOME TESTS FAILED")
        print("  Please check the errors above")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    print("\n⚠️  IMPORTANT NOTES:")
    print("  1. Make sure subscription service is running on port 8005")
    print("  2. Replace TEST_USER_ID with a valid user ID from your database")
    print("  3. This will create a dummy payment and upgrade the user to premium")
    print("  4. Check MongoDB after running to verify database updates")
    
    input("\nPress ENTER to start tests (or Ctrl+C to cancel)...")
    
    run_all_tests()

