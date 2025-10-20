"""
Test the smart roadmap detection feature
"""

import requests
import json
import time

def test_smart_roadmap_detection():
    """Test that roadmap requests are automatically detected"""
    print("🧪 Testing Smart Roadmap Detection")
    print("=" * 50)
    
    base_url = "http://localhost:8004"
    user_id = "test_smart_detection"
    
    # Test messages that should trigger roadmap detection
    roadmap_messages = [
        "How do I learn Python programming step by step?",
        "Can you create a learning path for React development?",
        "What's the roadmap to become a data scientist?",
        "I want to learn web development from scratch",
        "Show me a study plan for machine learning"
    ]
    
    # Test messages that should NOT trigger roadmap detection
    non_roadmap_messages = [
        "Hello, how are you?",
        "What's the weather like?",
        "Explain this code to me",
        "Help me debug this error"
    ]
    
    print("📝 Testing Roadmap Detection Messages:")
    print("-" * 40)
    
    for i, message in enumerate(roadmap_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        try:
            # Create a new chat for each test
            chat_response = requests.post(
                f"{base_url}/chats/new",
                json={
                    "user_id": user_id,
                    "title": f"Test {i}"
                }
            )
            
            if chat_response.status_code == 200:
                chat_id = chat_response.json()['chat_id']
                
                # Send the message
                response = requests.post(
                    f"{base_url}/chat",
                    json={
                        "message": message,
                        "user_id": user_id,
                        "chat_id": chat_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if roadmap metadata is present
                    if 'roadmap_metadata' in data and data['roadmap_metadata']:
                        print("   ✅ Roadmap detected!")
                        print(f"   📋 Title: {data['roadmap_metadata']['suggested_title']}")
                        print(f"   🏷️  Domain: {data['roadmap_metadata']['suggested_domain']}")
                        print(f"   🎯 Goal: {data['roadmap_metadata']['suggested_goal']}")
                    else:
                        print("   ❌ Roadmap NOT detected (should have been)")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            else:
                print(f"   ❌ Failed to create chat: {chat_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("📝 Testing Non-Roadmap Messages:")
    print("-" * 40)
    
    for i, message in enumerate(non_roadmap_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        try:
            # Create a new chat for each test
            chat_response = requests.post(
                f"{base_url}/chats/new",
                json={
                    "user_id": user_id,
                    "title": f"Non-Roadmap Test {i}"
                }
            )
            
            if chat_response.status_code == 200:
                chat_id = chat_response.json()['chat_id']
                
                # Send the message
                response = requests.post(
                    f"{base_url}/chat",
                    json={
                        "message": message,
                        "user_id": user_id,
                        "chat_id": chat_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if roadmap metadata is present
                    if 'roadmap_metadata' in data and data['roadmap_metadata']:
                        print("   ❌ Roadmap detected (should NOT have been)")
                    else:
                        print("   ✅ No roadmap detected (correct)")
                else:
                    print(f"   ❌ Failed: {response.status_code}")
            else:
                print(f"   ❌ Failed to create chat: {chat_response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("💡 Check the frontend to see the 'Add to Roadmap' buttons appear automatically!")

if __name__ == "__main__":
    test_smart_roadmap_detection()
