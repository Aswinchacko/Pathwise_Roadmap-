"""
Test the roadmap creation from chat functionality
"""

import requests
import json
import time

def test_roadmap_creation():
    """Test creating a roadmap from a chat conversation"""
    print("🧪 Testing Roadmap Creation from Chat")
    print("=" * 50)
    
    base_url = "http://localhost:8004"
    user_id = "test_roadmap_user"
    
    # Step 1: Create a new chat
    print("📝 Step 1: Creating new chat...")
    try:
        chat_response = requests.post(
            f"{base_url}/chats/new",
            json={
                "user_id": user_id,
                "title": "Learn Python Programming"
            }
        )
        
        if chat_response.status_code == 200:
            chat_data = chat_response.json()
            chat_id = chat_data['chat_id']
            print(f"✅ Chat created: {chat_id}")
        else:
            print(f"❌ Failed to create chat: {chat_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error creating chat: {e}")
        return
    
    # Step 2: Send some messages to build a conversation
    print("\n💬 Step 2: Building conversation...")
    messages = [
        "I want to learn Python programming from scratch",
        "What are the best resources for beginners?",
        "Can you create a step-by-step learning plan?",
        "What projects should I build to practice?"
    ]
    
    for i, message in enumerate(messages, 1):
        print(f"   Sending message {i}: {message}")
        try:
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
                print(f"   ✅ Response received")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Small delay between messages
    
    # Step 3: Create roadmap from chat
    print("\n🗺️ Step 3: Creating roadmap from chat...")
    try:
        roadmap_response = requests.post(
            f"{base_url}/roadmap/create-from-chat",
            json={
                "user_id": user_id,
                "chat_id": chat_id,
                "title": "Python Programming Learning Path",
                "goal": "Learn Python programming from beginner to intermediate level",
                "domain": "Programming"
            }
        )
        
        if roadmap_response.status_code == 200:
            roadmap_data = roadmap_response.json()
            print("✅ Roadmap created successfully!")
            print(f"   Roadmap ID: {roadmap_data['roadmap_id']}")
            print(f"   Message: {roadmap_data['message']}")
        else:
            print(f"❌ Failed to create roadmap: {roadmap_response.status_code}")
            print(f"   Response: {roadmap_response.text}")
    except Exception as e:
        print(f"❌ Error creating roadmap: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("💡 Check the frontend to see the 'Create Roadmap' button in the chat header")

if __name__ == "__main__":
    test_roadmap_creation()
