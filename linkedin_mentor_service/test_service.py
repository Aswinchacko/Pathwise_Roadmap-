#!/usr/bin/env python3
"""
Test script for LinkedIn Mentor Scraping Service
"""
import requests
import json

BASE_URL = "http://localhost:8005"

def test_health_check():
    """Test service health endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/mentors/health")
        print(f"✅ Health check: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_scrape_mentors():
    """Test mentor scraping"""
    print("\n🔍 Testing mentor scraping...")
    try:
        payload = {
            "user_id": "test_user_123",
            "limit": 5,
            "experience_level": "intermediate",
            "refresh_cache": False
        }
        
        print(f"📤 Sending request: {json.dumps(payload, indent=2)}")
        
        response = requests.post(
            f"{BASE_URL}/api/mentors/scrape",
            json=payload,
            timeout=120  # Scraping can take time
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success!")
            print(f"   - Total mentors: {data.get('total_found', 0)}")
            print(f"   - Search query: {data.get('search_query', 'N/A')}")
            print(f"   - Cached: {data.get('cached', False)}")
            print(f"   - Message: {data.get('message', 'N/A')}")
            
            if data.get('mentors'):
                print(f"\n📋 Sample mentor:")
                mentor = data['mentors'][0]
                print(f"   - Name: {mentor.get('name')}")
                print(f"   - Title: {mentor.get('title')}")
                print(f"   - Company: {mentor.get('company', 'N/A')}")
                print(f"   - Location: {mentor.get('location', 'N/A')}")
                print(f"   - Skills: {', '.join(mentor.get('skills', [])[:5])}")
                print(f"   - Profile: {mentor.get('profile_url')}")
            
            return True
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Scraping test failed: {e}")
        return False

def test_clear_cache():
    """Test cache clearing"""
    print("\n🔍 Testing cache clearing...")
    try:
        response = requests.delete(f"{BASE_URL}/api/mentors/cache/test_user_123")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cache cleared: {data.get('deleted_count', 0)} entries deleted")
            return True
        else:
            print(f"❌ Cache clear failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cache clear test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("LinkedIn Mentor Scraping Service - Test Suite")
    print("=" * 60)
    
    # Test 1: Health Check
    health_ok = test_health_check()
    
    if not health_ok:
        print("\n⚠️  Service is not running. Start it with: python main.py")
        return
    
    # Test 2: Scrape Mentors (this may take a while)
    print("\n⚠️  This test will scrape LinkedIn (may take 30-60 seconds)...")
    input("Press Enter to continue...")
    
    scrape_ok = test_scrape_mentors()
    
    # Test 3: Clear Cache
    if scrape_ok:
        test_clear_cache()
    
    print("\n" + "=" * 60)
    print("Tests Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()


