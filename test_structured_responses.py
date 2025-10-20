"""
Test structured responses from the chatbot
"""

import requests
import json

def test_structured_responses():
    """Test various questions to see structured responses"""
    print("🧪 Testing Structured Responses")
    print("=" * 60)
    
    base_url = "http://localhost:8004"
    user_id = "test_structured_user"
    
    questions = [
        "What is Docker and how does it work?",
        "Write a Python function to calculate fibonacci numbers with explanation",
        "Explain machine learning in simple terms with examples",
        "Create a table comparing different programming languages"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: '{question}'")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{base_url}/chat",
                json={
                    "message": question,
                    "user_id": user_id
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['response']
                print("✅ Response received!")
                print("\n📝 Structured Response:")
                print("=" * 60)
                print(answer)
                print("=" * 60)
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"Response: {response.text}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)
    
    print("\n🎉 Structured response test completed!")
    print("💡 Check the responses above for markdown formatting, headers, lists, and code blocks!")

if __name__ == "__main__":
    test_structured_responses()
