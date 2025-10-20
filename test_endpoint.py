"""
Test if the roadmap endpoint is registered
"""

import requests

def test_endpoints():
    """Test available endpoints"""
    print("🧪 Testing Available Endpoints")
    print("=" * 50)
    
    base_url = "http://localhost:8004"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health: {response.status_code}")
    except Exception as e:
        print(f"❌ Health: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root: {response.status_code}")
    except Exception as e:
        print(f"❌ Root: {e}")
    
    # Test roadmap endpoint
    try:
        response = requests.post(f"{base_url}/roadmap/create-from-chat", json={})
        print(f"✅ Roadmap: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Roadmap: {e}")
    
    # Test other endpoints
    try:
        response = requests.get(f"{base_url}/chats/test")
        print(f"✅ Chats: {response.status_code}")
    except Exception as e:
        print(f"❌ Chats: {e}")

if __name__ == "__main__":
    test_endpoints()
