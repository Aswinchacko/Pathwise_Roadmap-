"""
Test script to verify Groq API integration
"""
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv('project_recommendation_service/.env')

GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

print("=" * 60)
print("Groq API Integration Test")
print("=" * 60)
print()

# Check if API key exists
print(f"API Key present: {'✅ Yes' if GROQ_API_KEY else '❌ No'}")
if GROQ_API_KEY:
    print(f"API Key (first 10 chars): {GROQ_API_KEY[:10]}...")
else:
    print("⚠️  No API key found in .env file")
    print("   Add GROQ_API_KEY=your_key to project_recommendation_service/.env")
    print("   Get free key from: https://console.groq.com")
    exit(1)

print()
print("-" * 60)
print("Testing Groq API connection...")
print("-" * 60)
print()

# Simple test prompt
test_prompt = """List the numbers 1, 2, 3 as a JSON array. 
Response (JSON array only):"""

try:
    print(f"Endpoint: {GROQ_API_URL}")
    print(f"Model: llama-3.1-8b-instant")
    print(f"Test prompt: {test_prompt[:50]}...")
    print()
    
    response = requests.post(
        GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": test_prompt}],
            "temperature": 0.3,
            "max_tokens": 50
        },
        timeout=15
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ API Request Successful!")
        print()
        
        result = response.json()
        print("Response structure:")
        print(json.dumps(result, indent=2))
        print()
        
        if 'choices' in result and len(result['choices']) > 0:
            content = result['choices'][0]['message']['content']
            print("AI Response:")
            print(content)
            print()
            print("✅ Groq API is working correctly!")
            
    elif response.status_code == 401:
        print("❌ Authentication Error!")
        print("   Your API key is invalid or expired")
        print("   Get a new key from: https://console.groq.com")
        print()
        print("Response:", response.text)
        
    elif response.status_code == 429:
        print("⚠️  Rate Limit Exceeded!")
        print("   Too many requests. Wait a moment and try again.")
        
    else:
        print(f"❌ API Error! Status: {response.status_code}")
        print("Response:", response.text)
        
except requests.exceptions.Timeout:
    print("❌ Request Timeout!")
    print("   The API is taking too long to respond")
    print("   This might be temporary - try again")
    
except requests.exceptions.ConnectionError:
    print("❌ Connection Error!")
    print("   Cannot reach Groq API")
    print("   Check your internet connection")
    
except Exception as e:
    print(f"❌ Unexpected Error: {type(e).__name__}")
    print(f"   Message: {str(e)}")

print()
print("=" * 60)
print("Test complete!")
print("=" * 60)
print()

print("Next steps:")
print("1. If test passed: Your Groq API is working! ✅")
print("2. If test failed: Check error messages above")
print("3. Run: python test_project_recommendation.py")
print("4. Start service: start_project_recommendation_service.bat")

