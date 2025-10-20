#!/usr/bin/env python3
"""
Quick API test - checks if service is accessible
"""
import requests
import json
import sys

def test_service():
    base_url = "http://localhost:8005"
    
    print("="*60)
    print("Testing LinkedIn Mentor Scraping Service")
    print("="*60)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/api/mentors/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to service!")
        print("\nService is not running. Start it with:")
        print("   cd linkedin_mentor_service")
        print("   python start_simple.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Root endpoint
    print("\n2. Testing root endpoint...")
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Root endpoint working!")
            print(f"   Response: {response.json()}")
        else:
            print(f"⚠️  Root endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"⚠️  Root endpoint error: {e}")
    
    print("\n" + "="*60)
    print("✅ Service is running and accessible!")
    print("="*60)
    print("\nAPI Endpoints:")
    print(f"  Health:  {base_url}/api/mentors/health")
    print(f"  Scrape:  POST {base_url}/api/mentors/scrape")
    print(f"  Cache:   DELETE {base_url}/api/mentors/cache/{{user_id}}")
    print(f"  Docs:    {base_url}/docs")
    
    print("\nTo test scraping (requires MongoDB with roadmap data):")
    print('  curl -X POST http://localhost:8005/api/mentors/scrape \\')
    print('       -H "Content-Type: application/json" \\')
    print('       -d \'{"user_id": "test_user", "limit": 5}\'')
    
    return True

if __name__ == "__main__":
    success = test_service()
    sys.exit(0 if success else 1)


