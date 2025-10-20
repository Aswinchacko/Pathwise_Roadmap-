"""
Test the frontend fix by sending a message with markdown
"""

import requests
import json

def test_markdown_response():
    """Test that the chatbot returns markdown that should render properly"""
    print("🧪 Testing Markdown Response Fix")
    print("=" * 50)
    
    base_url = "http://localhost:8004"
    user_id = "test_markdown_fix"
    
    # Test with a message that should generate markdown
    test_message = "Write a Python function to calculate fibonacci numbers with proper formatting and explanation"
    
    print(f"📤 Sending message: '{test_message}'")
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json={
                "message": test_message,
                "user_id": user_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data['response']
            print("✅ Response received!")
            print("\n📝 Markdown Response Preview:")
            print("-" * 50)
            print(answer[:500] + "..." if len(answer) > 500 else answer)
            print("-" * 50)
            
            # Check if response contains markdown elements
            markdown_indicators = ['**', '##', '```', '- ', '1. ', '|']
            found_indicators = [indicator for indicator in markdown_indicators if indicator in answer]
            
            print(f"\n🔍 Markdown indicators found: {found_indicators}")
            
            if found_indicators:
                print("✅ Response contains markdown formatting!")
                print("💡 The frontend should now render this properly without errors.")
            else:
                print("⚠️  No markdown indicators found in response.")
            
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Test completed!")
    print("💡 Check the frontend at http://localhost:5173/chatbot")

if __name__ == "__main__":
    test_markdown_response()
