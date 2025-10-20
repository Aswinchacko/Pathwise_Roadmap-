"""
Test script for Job Agent Service
"""

import requests
import json
import time

BASE_URL = "http://localhost:5007"

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_job_search():
    """Test job search with user profile"""
    print("\n" + "="*60)
    print("Testing Job Search")
    print("="*60)
    
    try:
        payload = {
            "user_id": "test_user_123",
            "query": "React Developer",
            "location": "United States",
            "remote": True,
            "limit": 5,
            "use_ai_matching": True
        }
        
        print(f"\nSearching for: {payload['query']}")
        print("Please wait... (This may take 10-20 seconds)")
        
        response = requests.post(f"{BASE_URL}/api/jobs/search", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Found {data['total']} jobs!")
            print(f"Sources used: {', '.join(data['sources_used'])}")
            print(f"AI matching: {data['ai_matched']}")
            
            print("\n" + "-"*60)
            print("Top Job Listings:")
            print("-"*60)
            
            for i, job in enumerate(data['jobs'][:3], 1):
                print(f"\n{i}. {job['title']}")
                print(f"   Company: {job['company']}")
                print(f"   Location: {job['location']}")
                print(f"   Salary: {job.get('salary', 'Not specified')}")
                print(f"   Remote: {job.get('remote', False)}")
                print(f"   Source: {job.get('source', 'Unknown')}")
                if job.get('match_score'):
                    print(f"   Match Score: {job['match_score']}/100")
                if job.get('match_reason'):
                    print(f"   Reason: {job['match_reason']}")
                print(f"   URL: {job.get('url', 'N/A')[:60]}...")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_user_recommended_jobs():
    """Test getting recommended jobs based on user's roadmap"""
    print("\n" + "="*60)
    print("Testing User-Based Job Recommendations")
    print("="*60)
    
    try:
        user_id = "test_user_123"
        print(f"\nFetching jobs for user: {user_id}")
        print("(Based on their roadmap skills and goals)")
        
        response = requests.get(f"{BASE_URL}/api/jobs/user/{user_id}?limit=5", timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Found {data['total']} recommended jobs!")
            
            if data.get('user_profile'):
                profile = data['user_profile']
                print(f"\nUser Profile:")
                print(f"  Goal: {profile.get('goal')}")
                print(f"  Skills: {', '.join(profile.get('skills', [])[:5])}")
                print(f"  Experience: {profile.get('experience_level')}")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    print("\n" + "="*60)
    print("  PathWise Job Agent Service - Test Suite")
    print("="*60)
    print("\nMake sure the service is running: start_job_agent.bat")
    print("\nStarting tests in 3 seconds...")
    time.sleep(3)
    
    results = []
    
    # Test 1: Health Check
    results.append(("Health Check", test_health()))
    time.sleep(1)
    
    # Test 2: Job Search
    results.append(("Job Search", test_job_search()))
    time.sleep(1)
    
    # Test 3: User Recommendations
    results.append(("User Recommendations", test_user_recommended_jobs()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! Job Agent is working perfectly!")
    else:
        print("\n⚠️ Some tests failed. Check the logs above.")


if __name__ == "__main__":
    main()

