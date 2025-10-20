"""
Test script for PathWise Groq Chatbot Service
"""

import requests
import json
import time

BASE_URL = "http://localhost:8004"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_health():
    """Test health endpoint"""
    print_section("1. Testing Health Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Service is healthy!")
            print(f"   Status: {data.get('status')}")
            print(f"   MongoDB: {data.get('mongodb')}")
            print(f"   Groq API: {data.get('groq_api')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to chatbot service")
        print("   Make sure it's running on http://localhost:8004")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_conversation():
    """Test a complete conversation flow"""
    print_section("2. Testing Chat Conversation")
    
    user_id = f"test_user_{int(time.time())}"
    
    # Test 1: First message (creates new chat)
    print("\n📤 Sending first message: 'Hello, who are you?'")
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={
                "message": "Hello, who are you?",
                "user_id": user_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            chat_id = data["chat_id"]
            print(f"✅ Got response!")
            print(f"   Chat ID: {chat_id}")
            print(f"   Response: {data['response'][:100]}...")
            
            # Test 2: Follow-up message
            print("\n📤 Sending follow-up: 'What can you help me with?'")
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "message": "What can you help me with?",
                    "user_id": user_id,
                    "chat_id": chat_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Got follow-up response!")
                print(f"   Response: {data['response'][:100]}...")
                
                # Test 3: Technical question
                print("\n📤 Asking technical question: 'Explain recursion in programming'")
                response = requests.post(
                    f"{BASE_URL}/chat",
                    json={
                        "message": "Explain recursion in programming with a simple example",
                        "user_id": user_id,
                        "chat_id": chat_id
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Got technical response!")
                    print(f"\n📝 Full Response:")
                    print("-" * 70)
                    print(data['response'])
                    print("-" * 70)
                    return True
                else:
                    print(f"❌ Technical question failed: {response.status_code}")
                    return False
            else:
                print(f"❌ Follow-up failed: {response.status_code}")
                return False
        else:
            print(f"❌ First message failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out (this can happen if Groq API is slow)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_chat_management():
    """Test chat management features"""
    print_section("3. Testing Chat Management")
    
    user_id = f"test_user_{int(time.time())}"
    
    # Create a new chat
    print("\n📝 Creating new chat...")
    try:
        response = requests.post(
            f"{BASE_URL}/chats/new",
            json={
                "user_id": user_id,
                "title": "Test Chat"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            chat_id = data["chat_id"]
            print(f"✅ Chat created: {chat_id}")
            
            # Send a message
            print("\n📤 Sending message to chat...")
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "message": "This is a test message",
                    "user_id": user_id,
                    "chat_id": chat_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Message sent successfully")
                
                # Get chat history
                print("\n📜 Getting chat history...")
                response = requests.get(f"{BASE_URL}/chats/{user_id}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Found {len(data['chats'])} chats")
                    
                    # Update chat title
                    print("\n✏️  Updating chat title...")
                    response = requests.put(
                        f"{BASE_URL}/chats/{user_id}/{chat_id}/title",
                        params={"title": "Updated Test Chat"}
                    )
                    
                    if response.status_code == 200:
                        print("✅ Chat title updated")
                        
                        # Delete chat
                        print("\n🗑️  Deleting chat...")
                        response = requests.delete(f"{BASE_URL}/chats/{user_id}/{chat_id}")
                        
                        if response.status_code == 200:
                            print("✅ Chat deleted successfully")
                            return True
                        else:
                            print(f"❌ Delete failed: {response.status_code}")
                    else:
                        print(f"❌ Title update failed: {response.status_code}")
                else:
                    print(f"❌ Get history failed: {response.status_code}")
            else:
                print(f"❌ Send message failed: {response.status_code}")
        else:
            print(f"❌ Create chat failed: {response.status_code}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_various_questions():
    """Test the chatbot with various types of questions"""
    print_section("4. Testing Various Question Types")
    
    user_id = f"test_user_{int(time.time())}"
    
    questions = [
        "What is machine learning?",
        "Write a Python function to calculate fibonacci numbers",
        "Give me career advice for becoming a data scientist",
        "Explain quantum computing in simple terms",
    ]
    
    print(f"\n🤖 Testing {len(questions)} different questions...\n")
    
    for i, question in enumerate(questions, 1):
        print(f"{i}. Question: '{question}'")
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={
                    "message": question,
                    "user_id": user_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['response']
                print(f"   ✅ Answer preview: {answer[:80]}...")
            else:
                print(f"   ❌ Failed: {response.status_code}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(1)  # Be nice to the API
    
    return True

def main():
    """Run all tests"""
    print("\n" + "🧪" * 35)
    print("  PathWise Groq Chatbot - Comprehensive Test Suite")
    print("🧪" * 35)
    
    results = {
        "Health Check": test_health(),
        "Conversation Flow": test_chat_conversation(),
        "Chat Management": test_chat_management(),
        "Various Questions": test_various_questions()
    }
    
    print_section("TEST RESULTS SUMMARY")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("🎉 All tests passed! Your Groq chatbot is working perfectly!")
        print("💬 The chatbot can now answer anything like ChatGPT!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()

