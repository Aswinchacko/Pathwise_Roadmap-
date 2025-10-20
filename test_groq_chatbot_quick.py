"""
Quick test for Groq Chatbot Service
"""

import requests
import sys

def test_quick():
    """Quick test to verify service is working"""
    print("🧪 Quick Test: Groq Chatbot Service")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Checking service health...")
    try:
        response = requests.get("http://localhost:8004/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service is healthy")
            print(f"   MongoDB: {data.get('mongodb')}")
            print(f"   Groq API: {data.get('groq_api')}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to service on port 8004")
        print("   Make sure to run: start_groq_chatbot.bat")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Send a simple message
    print("\n2. Testing AI conversation...")
    print("   Asking: 'Hello, what is 2+2?'")
    try:
        response = requests.post(
            "http://localhost:8004/chat",
            json={
                "message": "Hello, what is 2+2?",
                "user_id": "test_user"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            print(f"   ✅ Got response!")
            print(f"   AI: {answer[:100]}...")
            print(f"\n   Chat ID: {data.get('chat_id')}")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ⏱️  Request timed out")
        print("   This can happen if Groq API is slow")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n")
    success = test_quick()
    print("\n" + "=" * 50)
    
    if success:
        print("🎉 SUCCESS! Chatbot is working!")
        print("\n💡 Next steps:")
        print("   1. Run: start_frontend.bat")
        print("   2. Open: http://localhost:5173")
        print("   3. Go to Chatbot page and start chatting!")
        print("\n   Or run full test suite:")
        print("   test_groq_chatbot.bat")
    else:
        print("❌ FAILED! Please check errors above")
        print("\n💡 Troubleshooting:")
        print("   1. Make sure chatbot service is running")
        print("   2. Check .env file has GROQ_API_KEY")
        print("   3. Check internet connection")
    
    print("=" * 50 + "\n")
    sys.exit(0 if success else 1)

