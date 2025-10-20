"""
Test the complete AI + Database system
"""
import requests
import json
import time

API_BASE = 'http://localhost:5003'

def test_health():
    """Test health endpoint"""
    print("1. Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    data = response.json()
    print(f"   Status: {data['status']}")
    print(f"   AI Enabled: {data['ai_enabled']}")
    print()

def test_database_stats():
    """Test database statistics"""
    print("2. Testing database stats...")
    response = requests.get(f"{API_BASE}/api/projects/stats")
    data = response.json()
    if data['success']:
        stats = data['stats']
        print(f"   Total Projects: {stats['total_projects']}")
        print(f"   By Category: {stats['by_category']}")
        print(f"   By Difficulty: {stats['by_difficulty']}")
        print(f"   Recent Projects: {stats['recent_projects']}")
    print()

def test_ai_recommendation(aim):
    """Test AI recommendation"""
    print(f"3. Testing AI recommendation for: '{aim}'...")
    
    response = requests.post(f"{API_BASE}/api/recommend", 
                           json={"aim": aim, "limit": 3},
                           headers={"Content-Type": "application/json"})
    
    data = response.json()
    if data['success']:
        print(f"   Method: {data['method']}")
        print(f"   Projects Generated: {data['total']}")
        for i, proj in enumerate(data['recommendations'], 1):
            print(f"   {i}. {proj['title']} ({proj['difficulty']}) - ID: {proj['id']}")
    else:
        print(f"   Error: {data.get('error')}")
    print()

def test_database_search():
    """Test database search"""
    print("4. Testing database search...")
    
    # Test category filter
    response = requests.get(f"{API_BASE}/api/projects?category=web-dev")
    data = response.json()
    if data['success']:
        print(f"   Web Dev Projects: {data['total']}")
    
    # Test difficulty filter
    response = requests.get(f"{API_BASE}/api/projects?difficulty=beginner")
    data = response.json()
    if data['success']:
        print(f"   Beginner Projects: {data['total']}")
    
    # Test search
    response = requests.get(f"{API_BASE}/api/projects?search=html")
    data = response.json()
    if data['success']:
        print(f"   Projects with 'html': {data['total']}")
    print()

def main():
    print("=" * 60)
    print("AI + Database System Test")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Health
        test_health()
        
        # Test 2: Database stats (should be empty initially)
        test_database_stats()
        
        # Test 3: AI recommendation (this will populate database)
        test_ai_recommendation("I want to become a full-stack developer")
        
        # Wait a moment
        time.sleep(1)
        
        # Test 4: Database stats (should now have projects)
        test_database_stats()
        
        # Test 5: Database search
        test_database_search()
        
        # Test 6: Another AI recommendation
        test_ai_recommendation("I want to learn machine learning")
        
        # Test 7: Final stats
        test_database_stats()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        print()
        print("Check the ai_projects.json file to see saved projects!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service!")
        print("Make sure to start the service first:")
        print("   start_project_recommendation_service.bat")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
