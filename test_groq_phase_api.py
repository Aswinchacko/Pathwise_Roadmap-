import requests
import json
import os
from dotenv import load_dotenv

# Load .env from the current directory
load_dotenv()

def test_groq_phase_api():
    """Test the Groq API directly for phase-based recommendations"""
    
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    
    if not GROQ_API_KEY:
        print("❌ No Groq API key found in .env file")
        return
    
    print(f"🔑 Using Groq API Key: {GROQ_API_KEY[:10]}...")
    
    # Test phase
    phase = "Design Fundamentals"
    limit = 3
    
    prompt = f"""Based on the completed phase "{phase}", recommend {limit} practical projects that would help reinforce and apply the skills learned in this phase.

The projects should be:
- Directly related to the completed phase
- Practical and hands-on
- Progressive in difficulty
- Include specific skills and technologies

Return ONLY a JSON array of project objects with this exact structure:
[
  {{
    "title": "Project Title",
    "description": "Detailed project description explaining what to build and why it's relevant to the phase",
    "difficulty": "beginner|intermediate|advanced",
    "skills": ["skill1", "skill2", "skill3"],
    "duration": "1-2 weeks|2-4 weeks|1-2 months",
    "category": "web-dev|ai-ml|data-science|mobile-dev|design|other"
  }}
]

Phase: {phase}"""

    print(f"\n🤖 Testing Groq API for phase: '{phase}'")
    print(f"📝 Prompt length: {len(prompt)} characters")
    
    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=20
        )
        
        print(f"📡 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            
            print(f"✅ Groq API Response Received!")
            print(f"📄 Response length: {len(content)} characters")
            print(f"\n📝 Raw Response:")
            print("-" * 50)
            print(content)
            print("-" * 50)
            
            # Try to parse JSON
            try:
                # Clean up the response
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                projects = json.loads(content)
                print(f"\n🎉 Successfully parsed {len(projects)} projects:")
                
                for i, project in enumerate(projects, 1):
                    print(f"\n{i}. {project.get('title', 'No title')}")
                    print(f"   Description: {project.get('description', 'No description')}")
                    print(f"   Difficulty: {project.get('difficulty', 'No difficulty')}")
                    print(f"   Skills: {', '.join(project.get('skills', []))}")
                    print(f"   Duration: {project.get('duration', 'No duration')}")
                    print(f"   Category: {project.get('category', 'No category')}")
                
                return True
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON Parse Error: {e}")
                print(f"Raw content: {content[:200]}...")
                return False
                
        elif response.status_code == 401:
            print("❌ Authentication failed - check your API key")
            return False
        elif response.status_code == 429:
            print("⚠️ Rate limit exceeded")
            return False
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("🔌 Connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_phase_recommendation_service():
    """Test the phase recommendation service endpoint"""
    print(f"\n{'='*60}")
    print("🧪 Testing Phase Recommendation Service")
    print(f"{'='*60}")
    
    try:
        response = requests.post(
            'http://localhost:5003/api/recommend/phase',
            json={
                'phase': 'Design Fundamentals',
                'limit': 3
            },
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📡 Service Response Status: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print(f"✅ Service Response:")
            print(f"   Method: {data.get('method')}")
            print(f"   Phase: {data.get('phase')}")
            print(f"   Total: {data.get('total')}")
            print(f"   Success: {data.get('success')}")
            
            if data.get('recommendations'):
                print(f"\n📋 Projects:")
                for i, proj in enumerate(data.get('recommendations', []), 1):
                    print(f"   {i}. {proj.get('title')} ({proj.get('difficulty')})")
            
            return True
        else:
            print(f"❌ Service Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service. Make sure it's running on port 5003")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testing Groq API for Phase-Based Recommendations")
    print("=" * 60)
    
    # Test 1: Direct Groq API
    groq_success = test_groq_phase_api()
    
    # Test 2: Service endpoint
    service_success = test_phase_recommendation_service()
    
    print(f"\n{'='*60}")
    print("📊 Test Results Summary")
    print(f"{'='*60}")
    print(f"Groq API Direct: {'✅ PASS' if groq_success else '❌ FAIL'}")
    print(f"Service Endpoint: {'✅ PASS' if service_success else '❌ FAIL'}")
    
    if groq_success and service_success:
        print(f"\n🎉 All tests passed! Groq API is working correctly.")
    else:
        print(f"\n⚠️ Some tests failed. Check the errors above.")
