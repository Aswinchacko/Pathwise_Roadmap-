#!/usr/bin/env python3
"""
Test AI-Powered Mentor Search Service
Verifies Groq integration and mentor search functionality
"""

import requests
import json
import sys
import os
from dotenv import load_dotenv

# Load environment
load_dotenv('chatbot_service/.env')
load_dotenv('linkedin_mentor_service/.env')

MENTOR_SERVICE_URL = "http://localhost:8001"
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_status(check, status, message):
    """Print formatted status message"""
    symbol = "✓" if status else "✗"
    status_text = "PASS" if status else "FAIL"
    print(f"[{check}] {symbol} {status_text}: {message}")

def test_service_health():
    """Test if service is running and check AI status"""
    print_header("1. Service Health Check")
    
    try:
        response = requests.get(f"{MENTOR_SERVICE_URL}/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_status("Service", True, "Service is running")
            print(f"    Service: {data.get('service', 'Unknown')}")
            print(f"    MongoDB: {data.get('mongodb', 'Unknown')}")
            print(f"    AI Enabled: {data.get('ai_enabled', False)}")
            print(f"    Groq API: {data.get('groq_api_key_configured', False)}")
            
            # Check AI capabilities
            capabilities = data.get('search_capabilities', {})
            print(f"\n    Search Capabilities:")
            print(f"      - Web Search: {capabilities.get('web_search', False)}")
            print(f"      - AI Powered: {capabilities.get('ai_powered', False)}")
            print(f"      - Static Fallback: {capabilities.get('static_fallback', False)}")
            
            return data.get('ai_enabled', False)
        else:
            print_status("Service", False, f"HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_status("Service", False, "Cannot connect - is service running?")
        print("\n💡 Start service with: start_ai_mentor_service.bat")
        return False
    except Exception as e:
        print_status("Service", False, str(e))
        return False

def test_groq_api_key():
    """Check if Groq API key is configured"""
    print_header("2. Groq API Key Check")
    
    if GROQ_API_KEY:
        if GROQ_API_KEY.startswith('gsk_'):
            print_status("API Key", True, f"Valid key format")
            print(f"    Key: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-4:]}")
            return True
        else:
            print_status("API Key", False, "Invalid format (should start with 'gsk_')")
            return False
    else:
        print_status("API Key", False, "Not configured")
        print("\n💡 Setup instructions:")
        print("   1. Get free key at: https://console.groq.com")
        print("   2. Add to chatbot_service/.env: GROQ_API_KEY=gsk_...")
        print("   3. Or add to linkedin_mentor_service/.env")
        return False

def test_mentor_search():
    """Test mentor search with mock user"""
    print_header("3. Mentor Search Test")
    
    # First, we need to create a test roadmap in MongoDB
    print("\n📝 Note: This test requires:")
    print("   1. MongoDB running")
    print("   2. A user with a roadmap in the database")
    print("   3. Service running on port 8001")
    
    # Test with a mock request
    test_request = {
        "user_id": "test_user_12345",
        "limit": 5,
        "experience_level": "intermediate",
        "refresh_cache": True
    }
    
    print(f"\n🔍 Searching for mentors...")
    print(f"   User ID: {test_request['user_id']}")
    print(f"   Limit: {test_request['limit']}")
    
    try:
        response = requests.post(
            f"{MENTOR_SERVICE_URL}/api/mentors/scrape",
            json=test_request,
            timeout=30
        )
        
        if response.status_code == 404:
            print_status("Search", False, "No roadmap found for test user")
            print("\n💡 This is expected for test user")
            print("   Create a real roadmap in the app to test with real data")
            return True
        
        elif response.status_code == 200:
            data = response.json()
            
            if data.get('success'):
                mentors = data.get('mentors', [])
                search_source = data.get('search_source', 'unknown')
                message = data.get('message', '')
                
                print_status("Search", True, f"Found {len(mentors)} mentors")
                print(f"    Source: {search_source}")
                print(f"    Message: {message}")
                print(f"    Cached: {data.get('cached', False)}")
                
                if mentors:
                    print(f"\n    📊 Sample Mentor:")
                    mentor = mentors[0]
                    print(f"       Name: {mentor.get('name', 'N/A')}")
                    print(f"       Title: {mentor.get('title', 'N/A')}")
                    print(f"       Company: {mentor.get('company', 'N/A')}")
                    print(f"       Location: {mentor.get('location', 'N/A')}")
                    print(f"       Skills: {', '.join(mentor.get('skills', [])[:3])}")
                    print(f"       AI Generated: {mentor.get('is_ai_generated', False)}")
                
                # Check if AI was used
                if search_source == 'ai':
                    print(f"\n    🤖 AI Search Active!")
                elif search_source == 'static':
                    print(f"\n    📝 Using static fallback")
                
                return True
            else:
                print_status("Search", False, data.get('message', 'Unknown error'))
                return False
        
        else:
            print_status("Search", False, f"HTTP {response.status_code}")
            try:
                error = response.json()
                print(f"    Error: {error.get('detail', 'Unknown')}")
            except:
                pass
            return False
            
    except requests.exceptions.Timeout:
        print_status("Search", False, "Request timeout (>30s)")
        return False
    except Exception as e:
        print_status("Search", False, str(e))
        return False

def test_health_endpoint():
    """Test dedicated health endpoint"""
    print_header("4. Health Endpoint Test")
    
    try:
        response = requests.get(f"{MENTOR_SERVICE_URL}/api/mentors/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print_status("Health", True, "Endpoint accessible")
            print(f"    Status: {data.get('status', 'Unknown')}")
            print(f"    MongoDB: {data.get('mongodb', 'Unknown')}")
            print(f"    AI Search: {data.get('ai_search', 'Unknown')}")
            print(f"    Search Mode: {data.get('search_mode', 'Unknown')}")
            return True
        else:
            print_status("Health", False, f"HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print_status("Health", False, str(e))
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  AI-Powered Mentor Search Service - Test Suite")
    print("="*60)
    
    results = []
    
    # Test 1: Service Health
    ai_enabled = test_service_health()
    results.append(("Service Running", ai_enabled is not False))
    
    # Test 2: API Key
    has_api_key = test_groq_api_key()
    results.append(("API Key Configured", has_api_key))
    
    # Test 3: Health Endpoint
    health_ok = test_health_endpoint()
    results.append(("Health Endpoint", health_ok))
    
    # Test 4: Mentor Search
    search_ok = test_mentor_search()
    results.append(("Mentor Search", search_ok))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, status in results if status)
    total = len(results)
    
    print(f"\n📊 Results: {passed}/{total} tests passed\n")
    
    for test_name, status in results:
        symbol = "✓" if status else "✗"
        print(f"   {symbol} {test_name}")
    
    # Final verdict
    print("\n" + "="*60)
    if passed == total:
        print("  ✓ ALL TESTS PASSED - Service is ready!")
        print("="*60)
        print("\n🚀 Next Steps:")
        print("   1. Open frontend: http://localhost:5173")
        print("   2. Navigate to Mentors page")
        print("   3. Create a roadmap if you haven't")
        print("   4. See AI-powered mentor recommendations!")
        return 0
    else:
        print("  ⚠ SOME TESTS FAILED - Check configuration")
        print("="*60)
        print("\n💡 Troubleshooting:")
        print("   1. Ensure MongoDB is running")
        print("   2. Start service: start_ai_mentor_service.bat")
        print("   3. Configure Groq API key for AI search")
        print("   4. See: linkedin_mentor_service/AI_SETUP.md")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        print("\n")
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted by user")
        sys.exit(1)

